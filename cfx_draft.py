# calculates statistics of positive runs / total runs in the cwd.
# cd to the folder of the target month
# python3 month.py << name of target month >>

import csv
import sys
import os
import tabulate
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from glob import glob
from pathlib import Path

x_values = []
y_values = []

# function to run per month
def per_csv(argv1):

    frequency = {}
    lst = []
    all_run_files = []
    run_informations = []
    all_positive_runs = []
    all_positive_testnames = []
    checker = []
    positive_cfxs = []
    names = []
    stat_list = []

    # calculate the number of total monthly runs
    paths = Path(os.getcwd()).glob('**/*.txt')
    for path in paths:
        if ("Quantification Cq Results" in str(path)):
            all_run_files.append(path)
        elif ("Run Information" in str(path)):
            run_informations.append(path)
    
    # isolate positive runs
    for run in all_run_files:
        with open(run,'r') as csvfile:
            file = csv.reader(csvfile, delimiter = ',')
            for row in file:
                try:
                    if ("NTC" in row[4]):
                        if (row[7].isnumeric()) or (float(row[7])):
                            if (float(row[7]) > 0):
                                # we've determined the current file to have at least 1 positive, so break and move to the next txt file
                                all_positive_runs.append(run)
                                break
                except:
                    pass

    # print(all_positive_runs) # check file paths before split()

    total_positives = len(all_positive_runs)

    for positive in all_positive_runs:
        testname = str(positive)
        words = testname.split('/')                 # on my computer
        # try:
        test = words[7].partition("_")[0]           # on my computer
        test2 = words[7].partition(" ")
        all_positive_testnames.append(test)
        checker.append(test2[0])

    # checker holds the identifier of each positive run
    for id in checker:
        for run in run_informations:
            if (id in str(run)):
                try:
                    # get each run's corresponding information file
                    with open(run, 'r') as csvfile:
                        f = csv.reader(csvfile, delimiter = ',')
                        first_line = next(f)
                        name = first_line[1].partition('_')[0]
                        names.append(name)
                        for line in f:
                            base = str(line[0])
                            cfx = str(line[1])
                            if (base.startswith("Base Serial Number")):
                                positive_cfxs.append(cfx)
                except:
                    pass

    # get number of total runs per cfx
    for run in run_informations:
        try:
            with open(run, 'r') as csvfile:
                f = csv.reader(csvfile, delimiter = ',')
                for line in f:
                    base = str(line[0])
                    serial = str(line[1])
                    if (base.startswith("Base Serial Number")):
                        lst.append(serial)
        except:
            pass

    # lst holds the source of every run this month
    # lst.count(source) = number of total runs on that cfx

    total_runs = Counter(lst)
    # total_runs{} holds    serial : its total runs

    # y_values is a list of the cfx rates in the same order as positive_cfxs

    for test in all_positive_testnames:
        frequency.update({test: all_positive_testnames.count(test)})

    statistic = "{:.0%}".format(total_positives / (len(all_run_files)))     # for year

    # pair serial numbers with their statistics
    for positive in positive_cfxs:
        num_of_robots_positive_runs = positive_cfxs.count(positive)
        # can now access output file and check if string is there
        stats = {positive: (num_of_robots_positive_runs, total_runs[positive], (num_of_robots_positive_runs) / (total_runs[positive]))}
        stat_list.append(stats)

    # stat_list holds each positive robot tied to its num_of_positives, total, and percentage
    # same length as number of monthly positives
    
    # remove duplicates
    res = []
    [res.append(x) for x in stat_list if x not in res]

    # list of cfx_names to write
    cfx_list = [x for x in res]
    # list of values to pair 
    stats_list = [x.values() for x in res]
    
    for dict_item in cfx_list:
        d = str(dict_item)
        temp = d.partition("'")[2]
        ct_serial = temp.partition("'")[0]
        k = str(ct_serial)
        current_folder = Path(os.getcwd())
        file_to_open = current_folder / "output.txt"
        f = open(file_to_open, 'a+')
        read_file = f.readlines()
        if (ct_serial not in read_file):
            f.write(ct_serial + ": ")
            for values in stats_list:
                for tup in values:
                    positives = tup[0]
                    total = tup[1]
                    percent = tup[2] * 100
                    f.write(str(positives) + " positives out of " + str(total) + " total runs, percentage of " + str(percent) + "%\n")
                    break

# graph template
def plot_graph(month):

    plt.bar(x_values, y_values)
    plt.xlabel('CFX Serial Number', fontsize = 12)
    plt.ylabel('Positives / Total Runs', fontsize = 12)
    plt.title(month + " 2022: Positive Runs per CFX", fontsize = 20)
    plt.show()


# MAIN #
per_csv("November")
#plot_graph(sys.argv[1])
