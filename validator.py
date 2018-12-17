# Jason Zareski
#
# Greedy & Random Colorability Validator
# Facebook Data

import sys
import os
import random
import time

def run(file):
    def reset_file(graph):
        graph.seek(0)
        graph.readline()
    def printb(s):
        sys.stdout.write("\r" + s + "\r")
        sys.stdout.flush()
    def failedValidation():
        print("NOT A VALID COLORING.")
        exit(0)

    if not os.path.exists(file):
        print("Not a file!")
        exit(0)

    graph = open(file, 'r')
    colors = open(file + ".out", 'r')
    color_set = set()
    reset_file(graph)
    nodes = dict()
    for edge in graph.readlines():
        n,t = map(int, edge.split(","))
        if n not in nodes:
            nodes[n] = [set(), -1]
        if t not in nodes:
            nodes[t] = [set(), -1]
        nodes[n][0].add(t)
        nodes[t][0].add(n)
    for color in colors.readlines():
        n,c = map(int, color.split(","))
        nodes[n][1] = c
        color_set.add(c)
    # VALIDATE
    for n in nodes:
        neighbors,color = nodes[n]
        for i in neighbors:
            if n != i:
                c = nodes[i][1]
                if c == color:
                    #print("\nNodes %d shares an edge with %d, and has the same color %d" % (n, i, c))
                    failedValidation();

    #print("COLORING VALID.\n%d COLORS" % len(color_set))
    return len(color_set);
