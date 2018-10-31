#! /usr/bin/python
# -*- coding: utf-8 -*-
# Author: Samy Sidhoum
"""[Source code in Python of the CSN laboratory work n°3]"""
import os
import snap
from Language import Language


def table1():
    print("   N   |   E   |     <k>     |        delta       ")
    for input_file in os.listdir("datas"):
        current_language = Language(input_file)
        print(current_language.characteristics())


def main():
    current_language = Language("Basque_syntactic_dependency_network.txt")
    G2 = snap.GenRndGnm(snap.PUNGraph, int(current_language.N), int(current_language.E))
    for NI in G2.Nodes():
        print "node: %d, degree %d" % (NI.GetId(), NI.GetDeg())


if __name__ == '__main__': main()