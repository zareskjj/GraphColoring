# Jason Zareski
#
# Greedy & Random Colorability
# Facebook Data

import sys
import os
import random

def printb(s):
    sys.stdout.write("\r" + s + "\r\r")
    sys.stdout.flush()
def reset_file(graph_file):
    graph_file.seek(0)
    graph_file.readline()
def checkNeighbors(neighbors: set, color: int, nodes: dict):
    for x in neighbors:
        if nodes[x][1] == color:
            return False
    return True;

def load_graph(file):
    if not os.path.exists(file):
        print("COLORING: Not a file!")
        exit(0)
    graph = open(file, 'r')
    nodes = dict()
    reset_file(graph)
    for edge in graph.readlines():
        n1, n2 = map(int, edge.split(","))
        if n1 not in nodes:
            nodes[n1] = [set(), 0] # NEIGHBORS, COLOR
        if n2 not in nodes:
            nodes[n2] = [set(), 0] # NEIGHBORS, COLOR
        nodes[n1][0].add(n2)
        nodes[n2][0].add(n1)
    graph.close()
    return nodes

def run(nodes_from_file, file):
    nodes = dict(nodes_from_file)

    for n in nodes:  # REMOVING CIRCULAR EDGES
        while n in nodes[n][0]:
            nodes[n][0].remove(n)

    entry = random.randrange(0, len(nodes)) # List starting point, randomized for best result
    color_limit = 2 # Starting coloring limit, will increase if coloring at this limit is not possible
    nodeList = list(nodes) # List of keys (all the nodes), to access the set of neighbors in "nodes"
    l = len(nodes)
    i = 0
    while i < l:
        j = (i + entry) % l
        neighbors = nodes[nodeList[j]][0]
        color = nodes[nodeList[j]][1]
        starting_color = color
        while not checkNeighbors(neighbors, color, nodes):
            color = (color + 1) % color_limit
            if color == starting_color:
                color_limit += 1
        nodes[nodeList[j]][1] = color
        #printb("Coloring Limit: %d\tWorking on node %d of %d" % (color_limit, i if entry > i else i-entry,l))
        i += 1
    graph = open(file, 'r')
    #print("\n\nDone coloring. Outputting coloring...")
    reset_file(graph)
    output = open(file + ".out", "w+")
    allNodes = set()
    for edge in graph.readlines():
        x,y = map(int, edge.split(","))
        allNodes.add(x)
        allNodes.add(y)

    reset_file(graph)
    for edge in graph.readlines():
        x,_ = map(int, edge.split(","))
        if x in allNodes:
            output.write(str(x) + "," +str(nodes[x][1]) + "\n")
            allNodes.remove(x)
