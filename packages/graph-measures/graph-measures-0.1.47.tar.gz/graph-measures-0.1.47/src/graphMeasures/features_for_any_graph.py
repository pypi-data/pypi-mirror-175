import datetime
import networkx as nx
import numpy as np
import pickle
import logging

import pandas as pd

from .loggers import PrintLogger, FileLogger, multi_logger
import os
from .features_infra.graph_features import GraphFeatures


class FeatureCalculator:
    def __init__(self, graph, features, dir_path="", acc=True, directed=False, gpu=False, device=2, verbose=True,
                 params=None, should_zscore: bool = True):
        """
        A class used to calculate features for a given graph, input as a text-like file.

        :param graph: str|nx.Graph|nx.DiGraph
        Path to graph edges file (text-like file, e.g. txt or csv), from which the graph is built using networkx.
        The graph must be unweighted. If its vertices are not [0, 1, ..., n-1], they are mapped to become
        [0, 1, ..., n-1] and the mapping is saved.
        Every row in the edges file should include "source_id,distance_id", without a header row.
        :param features: list of strings
        List of the names of each feature. Could be any name from features_meta.py or "additional_features".
        :param dir_path: str
        Path to the directory in which the feature calculations will be (or already are) located.
        :param acc: bool
        Whether to run the accelerated features, assuming it is possible to do so.
        :param directed: bool
        Whether the built graph is directed.
        :param gpu: bool
        Whether to use GPUs, assuming it is possible to do so (i.e. the GPU exists and the CUDA matches).
        :param device: int
        If gpu is True, indicates on which GPU device to calculate. Will return error if the index doesn't match the
        available GPUs.
        :param verbose: bool
        Whether to print things indicating the phases of calculations.
        :param params: dict, or None
        For clique detection uses, this is a dictionary of the graph settings:
        size, directed, clique size, edge probability. The corresponding keys must have be:
        subgraph_size, directed, vertices, probability
        Ignored for any other use.
        """

        self._dir_path = dir_path
        self._features = features  # By their name as appears in accelerated_features_meta
        self._gpu = gpu
        self._device = device
        self._verbose = verbose
        self._logger = multi_logger([PrintLogger("Logger", level=logging.DEBUG),
                                     FileLogger("FLogger", path=dir_path, level=logging.INFO)], name=None) \
            if verbose else None
        self._params = params
        self._load_graph(graph, directed)
        self._get_feature_meta(features, acc)  # acc determines whether to use the accelerated features
        self.should_zscore = should_zscore

        self._adj_matrix = None
        self._raw_features = None
        self._other_features = None

    def _load_graph(self, graph, directed=False):
        if type(graph) is str:
            self._graph = nx.read_edgelist(graph, delimiter=',', create_using=nx.DiGraph() if directed else nx.Graph())
        elif type(graph) is nx.Graph or type(graph) is nx.DiGraph:
            if type(graph) is nx.Graph and directed:
                self._graph = nx.to_directed(graph.copy())
            elif type(graph) is nx.DiGraph and not directed:
                self._graph = nx.to_undirected(graph.copy())
            else:
                self._graph = graph.copy()
        else:
            raise ValueError("Graph must be path to edgelist, nx.Graph or nx.DiGraph")

        # save the nodes before the convert to integers which mix their order
        self.nodes_order = list(self._graph.nodes)

        vertices = np.array(self._graph.nodes)
        should_be_vertices = np.arange(len(vertices))
        self._mapping = {i: v for i, v in enumerate(self._graph)}
        if not np.array_equal(vertices, should_be_vertices):
            if self._verbose:
                self._logger.debug("Relabeling vertices to [0, 1, ..., n-1]")
            pickle.dump(self._mapping, open(os.path.join(self._dir_path, "vertices_mapping.pkl"), "wb"))
            self._graph = nx.convert_node_labels_to_integers(self._graph)
        if self._verbose:
            self._logger.info(str(datetime.datetime.now()) + " , Loaded graph")
            self._logger.debug("Graph Size: %d Nodes, %d Edges" % (len(self._graph), len(self._graph.edges)))

    def _get_feature_meta(self, features, acc):
        if acc:
            from .features_meta.accelerated_features_meta import FeaturesMeta
            features_meta_kwargs = dict(gpu=self._gpu, device=self._device)
        else:
            from .features_meta.features_meta import FeaturesMeta
            features_meta_kwargs = dict()

        all_node_features = FeaturesMeta(**features_meta_kwargs).NODE_LEVEL
        self._features = {}
        self._special_features = []
        for key in features:
            if key in ['degree', 'in_degree', 'out_degree', 'additional_features']:
                self._special_features.append(key)
            elif key not in all_node_features:
                if self._verbose:
                    self._logger.debug("Feature %s unknown, ignoring this feature" % key)
                features.remove(key)
                continue
            else:
                self._features[key] = all_node_features[key]

    def calculate_features(self, should_dump=True, dumping_specs=None):
        """
        :param should_dump: A boolean flag. If True the feature will be dumped and saved.
                            Otherwise, the features will not be saved.
        :param dumping_specs: A dictionary of specifications how to dump the non-special features.
                              The default is saving the class only (as a pickle file).
                              'object': What to save - either 'class' (save the calculator with the features inside),
                                        'feature' (the feature itself only, saved as name + '_ftr') or 'both'.
                                        Note that if only the feature is saved, when one calls the calculator again,
                                        the class will not load the feature and instead calculate it again.
                              'file_type': If the feature itself is saved, one can choose between two formats:
                                           either 'pkl' (save the feature as a pickle file, as is) or 'csv' (save a
                                           csv file of the feature values).
                              'vertex_names': If the features are saved as a csv file, there is an option of saving
                                              the name of each vertex in each row, before the feature values.
                                              The value here is a boolean indicating whether to put the original names
                                              the vertices in the beginning of each row.
        """
        if not len(self._features) + len(self._special_features) and self._verbose:
            print("No features were chosen!")
        else:
            self._adj_matrix = nx.adjacency_matrix(self._graph)
            # self._adj_matrix = self._adj_matrix.toarray()
            self._raw_features = GraphFeatures(gnx=self._graph, features=self._features, dir_path=self._dir_path,
                                               logger=self._logger)
            if dumping_specs is not None:
                if 'vertex_names' in dumping_specs:
                    if dumping_specs['vertex_names']:
                        dumping_specs['vertex_names'] = self._mapping
                    else:
                        del dumping_specs['vertex_names']
            self._raw_features.build(should_dump=should_dump, dumping_specs=dumping_specs)
            self._other_features = OtherFeatures(self._graph, self._special_features, self._dir_path, self._params,
                                                 self._logger)
            self._other_features.build(should_dump=should_dump)
            self._logger.info(str(datetime.datetime.now()) + " , Calculated features")

    @property
    def feature_matrix(self):
        return np.hstack((self._raw_features.to_matrix(mtype=np.array, should_zscore=self.should_zscore),
                          self._other_features.feature_matrix))

    def feature_matrix_with_names(self):
        # return the feature matrix and the order of the features in the matrix
        raw_features, raw_order = self._raw_features.to_matrix(mtype=np.array, should_zscore=self.should_zscore,
                                                               get_features_order=True)
        other_features = self._other_features.feature_matrix
        other_order = self._other_features.features
        return np.hstack((raw_features, other_features)), self.build_names_list(raw_order + other_order)

    def get_pandas_df(self):
        feature_matrix, names = self.feature_matrix_with_names()
        features_df = pd.DataFrame(feature_matrix)
        features_df.columns = names
        features_df.index = self.nodes_order
        features_df.sort_index(inplace=True)
        return features_df

    @property
    def adjacency_matrix(self):
        return self._adj_matrix

    def build_names_list(self, names):
        """
        This function get a features list, and return a new list
        with each feature time it's output size.
        For example - feature which it's output is two columns will appear twice.
        """
        features_output_size = {}
        new_list = []
        if self._graph.is_directed:
            features_output_size = {
                "average_neighbor_degree": 1,
                "betweenness_centrality": 1,
                "bfs_moments": 2,
                "closeness_centrality": 1,
                "eccentricity": 1,
                "fiedler_vector": 0,
                "k_core": 1,
                "load_centrality": 1,
                "motif3": 13,
                "motifs_node_3": 13,
                "motif4": 199,
                "motifs_node_4": 199,
                "degree": 1,
                "eigenvector_centrality": 1,
                "clustering_coefficient": 1,
                "square_clustering_coefficient": 1,
                "generalized_degree": 0,
                "all_pairs_shortest_path_length": len(self._graph.nodes),
                "attractor_basin": 1,
                "flow": 1,
                "general": 2,
                "page_rank": 1
            }
        else:
            features_output_size = {
                "average_neighbor_degree": 1,
                "betweenness_centrality": 1,
                "bfs_moments": 2,
                "closeness_centrality": 1,
                "eccentricity": 1,
                "fiedler_vector": 1,
                "k_core": 1,
                "load_centrality": 1,
                "motif3": 2,
                "motifs_node_3": 2,
                "motif4": 6,
                "motifs_node_4": 6,
                "degree": 1,
                "eigenvector_centrality": 1,
                "clustering_coefficient": 1,
                "square_clustering_coefficient": 1,
                "generalized_degree": 16,
                "all_pairs_shortest_path_length": len(self._graph.nodes),
                "attractor_basin": 0,
                "flow": 0,
                "general": 1,
                "page_rank": 1
            }

        for name in names:
            num = features_output_size[name]
            if num == 1:
                new_list.append(name)
            if num > 1:
                for i in range(num):
                    new_list.append(f'{name}_{i+1}')

        return new_list


class OtherFeatures:
    def __init__(self, graph, features, dir_path, params=None, logger=None):
        self._graph = graph
        self._features = features
        self._dir_path = dir_path
        self._logger = logger
        self._params = params
        self._feat_string_to_function = {
            'degree': self._calc_degree,
            'in_degree': self._calc_in_degree,
            'out_degree': self._calc_out_degree,
            'additional_features': self._calc_additional_features
        }

        self._feature_matrix = None

    def _calc_degree(self):
        degrees = list(self._graph.degree)
        # return {n: d for n, d in degrees}
        return np.array([d[1] for d in degrees]).reshape(-1, 1)

    def _calc_in_degree(self):
        degrees = list(self._graph.in_degree)
        return np.array([d[1] for d in degrees]).reshape(-1, 1)

    def _calc_out_degree(self):
        degrees = list(self._graph.out_degree)
        return np.array([d[1] for d in degrees]).reshape(-1, 1)

    def _calc_additional_features(self):
        from .additional_features import AdditionalFeatures
        if self._params is None:
            raise ValueError("params is None")
        if not os.path.exists(os.path.join(self._dir_path, "motif3.pkl")):
            raise FileNotFoundError("Motif 3 must be calculated")
        if not os.path.exists(os.path.join(self._dir_path, "motif4.pkl")):
            raise FileNotFoundError("Motif 4 must be calculated")

        motif_matrix = np.hstack((pickle.load(open(os.path.join(self._dir_path, "motif3.pkl"), "rb")),
                                  pickle.load(open(os.path.join(self._dir_path, "motif4.pkl"), "rb"))))
        add_ftrs = AdditionalFeatures(self._params, self._graph, self._dir_path, motif_matrix)
        return add_ftrs.calculate_extra_ftrs()

    def build(self, should_dump=False):
        self._feature_matrix = np.empty((len(self._graph), 0))
        for feat_str in self._features:
            if self._logger:
                start_time = datetime.datetime.now()
                self._logger.info("Start %s" % feat_str)
            if os.path.exists(
                    os.path.join(self._dir_path, feat_str + '.pkl')) and feat_str != "additional_features":
                feat = pickle.load(open(os.path.join(self._dir_path, feat_str + ".pkl"), "rb"))
                self._feature_matrix = np.hstack((self._feature_matrix, feat))
                if self._logger:
                    cur_time = datetime.datetime.now()
                    self._logger.info("Finish %s at %s" % (feat_str, cur_time - start_time))
            else:
                feat = self._feat_string_to_function[feat_str]()
                if should_dump:
                    pickle.dump(feat, open(os.path.join(self._dir_path, feat_str + ".pkl"), "wb"))
                self._feature_matrix = np.hstack((self._feature_matrix, feat))
                if self._logger:
                    cur_time = datetime.datetime.now()
                    self._logger.info("Finish %s at %s" % (feat_str, cur_time - start_time))

    @property
    def feature_matrix(self):
        return self._feature_matrix

    @property
    def features(self):
        return self._features


if __name__ == "__main__":
    # head = 'path/to/dir_path'
    # path = 'path/to/edges_file'
    # all possible features:
    #           ["average_neighbor_degree", "betweenness_centrality", "bfs_moments",
    #              "closeness_centrality", "eccentricity", "fiedler_vector", "k_core",
    #              "load_centrality", "louvain", "motif3", "motif4", "degree",
    #              "eigenvector_centrality", "clustering_coefficient", "page_rank",
    #              "square_clustering_coefficient", "generalized_degree", "general",
    #              "attractor_basin", "flow"]
    feats = ["louvain", "eigenvector_centrality", "clustering_coefficient"]

    ftr_calc = FeatureCalculator("edges.txt", features=feats,
                                 dir_path=os.path.join("try"), acc=False,
                                 directed=False, gpu=False, verbose=True)

    ftr_calc.calculate_features()
    print(ftr_calc.feature_matrix)

    with open("./try/gnx.pkl", 'rb') as f:
        graph = pickle.load(f)
    with open("./try/eigenvector_centrality.pkl", 'rb') as f:
        eigenvector_centrality = pickle.load(f)
    with open("./try/louvain.pkl", 'rb') as f:
        louvain = pickle.load(f)
    with open("./try/clustering_coefficient.pkl", 'rb') as f:
        clustering_coefficient = pickle.load(f)
    b = 3
