# Jason Zareski
#
# COLOR & VALIDATE
import sys

if sys.version_info[0] != 3:
    print("Requires python version >= 3")
    quit()

import os
import coloring
import validator
import time

TEST_LENGTH = 100
tests_dir = "tests/"
csvs = list()
google_file = ""
for f in os.listdir(tests_dir):
    if f.endswith(".csv"):
        csvs.append(tests_dir + f)
    if f.endswith(".txt"):
        google_file = tests_dir + f
bests = dict()
graphs = dict()

def run_test(iterations, file, graph_type):
    for i in range(iterations):
        coloring.printb("%80s" % ("Test %d (%s) of %d" % (i+1, file, iterations)))
        for n in graphs[file]:
            graphs[file][n][1] = 0
        start_color = time.time()
        coloring.run(graphs[file], file, graph_type)
        end_color = time.time()
        start_validation = time.time()
        x = validator.run(file,  graph_type)
        end_validation = time.time()
        validator.printb("Validated %s coloring. Coloring took %ds, validation took %ds." % (file, end_color-start_color, end_validation-start_validation))
        if file not in bests:
            bests[file] = list()
        bests[file].append(x)

coloring.printb("Preloading graphs... (Reset after each test iteration)")
# GOOGLE FILE
if google_file != "":
    coloring.printb("Loading %s" % (google_file))
    graphs[google_file] = coloring.load_graph(google_file, "google")
    coloring.printb("Loaded %s" % (google_file))

# FACEBOOK FILES
for file in csvs:
    if file not in graphs:
        coloring.printb("Loading %s" % (google_file))
        graphs[file] = coloring.load_graph(file, "facebook")
        coloring.printb("Loaded %s" % (file))

coloring.printb("")
interrupted = False
try:
    for file in csvs:
        run_test(TEST_LENGTH, file, "facebook")

    if google_file in graphs:
        run_test(TEST_LENGTH, google_file, "google")
except KeyboardInterrupt:
    interrupted = True
    print("\nPROCESS INTERRUPTED.\n\nPrinting results as is, and exiting.")

print("\n\nGraph\t\tBest (Avg) (Worst):\n%s" % ("="*40))
for file_name in sorted(bests):
    sum = 0
    for x in bests[file_name]:
        sum += x
    display_name = file_name[len(tests_dir):len(file_name)-len("_edges.csv")] if file_name.endswith(".csv") else file_name[len(tests_dir):len(file_name) - len(".txt")]
    if not interrupted:
        print("%20s\t\t%d (%.2f) (%d)" % (display_name, min(bests[file_name]), sum/TEST_LENGTH, max(bests[file_name])))
    else:
        print("%20s\t\t%d (N/A) (%d)" % (display_name, min(bests[file_name]), max(bests[file_name])))
