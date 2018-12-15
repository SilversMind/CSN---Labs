#! /usr/bin/python
# -*- coding: utf-8 -*-
# Author: Samy Sidhoum
"""[Class Language for the CSN LabWork n°3]"""

import snap


class Language:
    def __init__(self, input_file):
        with open("datas/{}".format(input_file), "r") as file_content:
            self.content = file_content.read().split('\n')
        self.dictionary = dict()
        self.degree_sequence_ = snap.TIntV()

# --------------------- Graph properties--------------------- #

# Number of vertices of the language's dependency graph
    @property
    def N(self):
        return float(self.content[0].split()[0])

# Number of edges of the language's dependency graph
    @property
    def E(self):
        return float(self.content[0].split()[1])

    @property
    def mean_degree(self):
        return float(2*self.E/self.N)

    @property
    def edge_density(self):
        return float(2*self.E/(self.N * (self.N - 1)))

# ----------------------------------------------------------- #
    def characteristics(self):
        return int(self.N), int(self.E), self.mean_degree, self.edge_density

    # Dictionary containing the dependency of every word of the language dependency_dictionary return a dictionary which
    #  has, as key,  every word of the language, and as values, the set of word which has dependencies with the key
    @property
    def dependency_dictionary(self):
        for dependency in self.content[1:-1]:
            dependency_splitted = dependency.split()
            if dependency_splitted[0] != dependency_splitted[1]:
                if dependency_splitted[0] not in self.dictionary:
                    self.dictionary[dependency_splitted[0]] = set()
                self.dictionary[dependency_splitted[0]].add(dependency_splitted[1])

                if dependency_splitted[1] not in self.dictionary:
                    self.dictionary[dependency_splitted[1]] = set()
                self.dictionary[dependency_splitted[1]].add(dependency_splitted[0])

        return self.dictionary

# Returns the degree sequence of the language as a vector of integer from the snap library
    def degree_sequence(self):
        degree_sequence_list = sorted((len(x) for x in self.dependency_dictionary.values()), reverse=True)
        for item in degree_sequence_list:
            self.degree_sequence_.Add(item)
        return self.degree_sequence_

    def graph(self):
        graph = snap.TUNGraph.New()
        current_id = 1
        node_dictionnary = dict()
        for key, value in self.dependency_dictionary.items():
            if key not in node_dictionnary:
                node_dictionnary[key] = current_id
                graph.AddNode(current_id)
                current_id = current_id + 1
            for v in value:
                if v not in node_dictionnary:
                    node_dictionnary[v] = current_id
                    graph.AddNode(current_id)
                    current_id = current_id + 1
                graph.AddEdge(node_dictionnary[key], node_dictionnary[v])
        return graph


def main():
    pass


if __name__ == '__main__':
    main()