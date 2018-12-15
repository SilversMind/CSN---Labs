#! /usr/bin/python
# -*- coding: utf-8 -*-
# Author: Samy Sidhoum
"""[Source code in Python of the CSN laboratory work n°3]"""
import os
import snap
from Language import Language
import random
import math


def table1():
    print("   N   |   E   |     <k>     |        delta       ")
    for input_file in os.listdir("datas"):
        current_language = Language(input_file)
        print(current_language.characteristics())


def monte_carlo_centrality(original_graph, sample, random_graph_type='erdos', loops=100, order=None, result_file=None):
    cpt = 0
    list_cc = set()
    real_network_centrality = 0
    for x in range(loops):
        print '\n Step {}'.format(x)
        if random_graph_type == 'erdos':
            # Create a erdos-renyi graph of size (N,E) from the original graph
            random_graph = snap.GenRndGnm(snap.PUNGraph, original_graph.GetNodes(), original_graph.GetEdges())
        elif random_graph_type == 'switching':
            # Randomize the graph by rewiring the original graph log(E) * E times
            E = original_graph.GetEdges()
            random_graph = snap.GenRewire(original_graph, (int(math.log10(E)*E/100)))

        else:
            raise TypeError

        real_network_centrality = closeness_centrality_total(original_graph, sample)
        cc_random = closeness_centrality_total(random_graph, sample,
                                               real_network_centrality=real_network_centrality,
                                               order=order)
        list_cc.add(cc_random)

        if cc_random > real_network_centrality:
            cpt = cpt + 1
    print '\n'
    print 'Closeness centrality for original graph {}'.format(real_network_centrality)
    print "Value of closeness centrality for random graph {}".format(sum(list_cc)/len(list_cc))
    print "\n Probability cc_random > cc_original = {}%".format(float(cpt*100)/loops)
    random_centrality = sum(list_cc)/len(list_cc)
    p_value = float(cpt*100)/loops
    if result_file:
        result_file.write('{0} {1} {2}\n'.format(real_network_centrality, random_centrality, p_value))
        result_file.flush()


def closeness_centrality_total(graph, sample, real_network_centrality=None, order=None):
    sample = random.sample(xrange(graph.GetNodes()), sample)
    len_sample = len(sample)
    list_cc = set()
    deg_sequence = [(x, graph.GetNI(x).GetDeg()) for x in sample]
    # Multiple of sorts for the degree distribution of the sample of studied nodes
    # Randomization
    if order == 'random':
        degree_sequence_opt = random.shuffle(deg_sequence)
    # Increasing order
    elif order == 'increase':
        degree_sequence_opt = sorted(deg_sequence, key=lambda tuple: tuple[1])
    # Decreasing order
    elif order == 'decrease':
        degree_sequence_opt = sorted(deg_sequence, key=lambda tuple: tuple[1], reverse=True)
    # Original
    else:
        degree_sequence_opt = deg_sequence

    for x in degree_sequence_opt:
        list_cc.add(closeness_centrality_node(graph, x[0], sample))
        if not real_network_centrality and (sum(list_cc) + (len_sample - len(list_cc)))/len_sample < real_network_centrality:
            break # Break if go beyond upper bound
        elif real_network_centrality and (sum(list_cc)/len_sample) > real_network_centrality:
            break  # Break if go above lower bound
    return sum(list_cc)/len(list_cc)


def closeness_centrality_node(graph, node, sample=None):
    if not sample:
        list_nodes = {x for x in range(graph.GetNodes())}
    else:
        list_nodes = random.sample(xrange(graph.GetNodes()), len(sample))
    N = len(list_nodes)
    list_of_sp = (snap.GetShortPath(graph, node, x) for x in list_nodes)  # Better to use list comprehension than
    #  map for clarity and speed reasons
    return sum((1.0/x for x in list_of_sp if x > 0))/N


def main():
    with open('datas/ZCloseness_centralities_results.txt', 'a') as result_file:
        result_file.write('Language | original cc | random cc | p_value \n')
        result_file.flush()
        for language_file in os.listdir('datas')[:5]:

            result_file.write(' {}'.format(language_file.split('_')[0]))
            result_file.flush()
            current_language = Language(language_file)

            original_graph = current_language.graph()

            #run the centrality calculation
            monte_carlo_centrality(original_graph, 150, 'switching', 20, 'decrease', result_file=result_file)

if __name__ == '__main__': main()