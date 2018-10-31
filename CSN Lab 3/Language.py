#! /usr/bin/python
# -*- coding: utf-8 -*-
# Author: Samy Sidhoum
"""[Class Language for the CSN LabWork n°3]"""


class Language:
    def __init__(self, input_file):
        with open("datas/{}".format(input_file), "r") as file_content:
            self.content = file_content.read().split('\n')
        self.dictionary = dict()
        self.degree_sequence_list = list()

# --------------------- Graph properties--------------------- #

# Number of vertices of the language's dependency graph
    @property
    def N(self):
        return float(self.content[0].split()[0])

# Number of vertices of the language's dependency graph
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

# Dictionary containing the dependency of every word of the language
# depency_dictionary return a dictionary which has, as key,  every word of the language, and as values, the set of word
#  which has dependencies with the key
    @property
    def dependency_dictionary(self):
        for dependency in self.content[1:-1]:
            dependency_splitted = dependency.split()
            if dependency_splitted[0] not in self.dictionary:
                self.dictionary[dependency_splitted[0]] = set()
            self.dictionary[dependency_splitted[0]].add(dependency_splitted[1])
        return self.dictionary

# Returns the degree sequence of the language
    @property
    def degree_sequence(self):
        for value in self.dependency_dictionary.values():
            self.degree_sequence_list.append(len(value))
        return self.degree_sequence_list


def main():
    x = Language("Basque_syntactic_dependency_network.txt")
    print(x.degree_sequence)


if __name__ == '__main__':
    main()