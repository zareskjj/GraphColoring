# Jason Zareski
#
# COLOR & VALIDATE
import sys
import os
import coloring
import validator

TEST_LENGTH = 1
csvs = list()
for f in os.listdir("tests"):
    if f.endswith(".csv"):
        csvs.append("tests/" + f)
bests = dict()
graphs = dict()
for file in csvs:
    if file not in graphs:
        graphs[file] = coloring.load_graph(file)
for file in csvs:
    for i in range(TEST_LENGTH):
        coloring.printb("%80s" % ("Test %d (%s) of %d" % (i, file, TEST_LENGTH)))
        for n in graphs[file]:
            graphs[file][n][1] = 0
        coloring.run(graphs[file], file)
        x = validator.run(file)
        if file not in bests:
            bests[file] = list()
        bests[file].append(x)

print("\n\nGraph\t\tBest (Avg) (Worst):\n%s" % ("="*40))
for l in sorted(bests):
    sum = 0
    for x in bests[l]:
        sum += x
    print("%20s\t\t%d (%.2f) (%d)" % (l[len("tests/"):len(l)-len("_edges.csv")], min(bests[l]), sum/TEST_LENGTH, max(bests[l]) ) )
