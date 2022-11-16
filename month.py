# calculates statistics of positive runs / total runs in the cwd.
# cd to the folder of the target month
# python3 month.py << name of target month >>

import csv
import sys
import os
from glob import glob
from pathlib import Path

# function to run per month
def per_csv(argv1):

    frequency = {}
    all_run_files = []
    all_positive_runs = []
    all_positive_testnames = []

    # isolate the month's run files and calculate the number of total monthly runs
    paths = Path(os.getcwd()).glob('**/*.txt',)
    for path in paths:
        if ("Quantification Cq Results" in str(path)):
            all_run_files.append(path)

    # isolate positive runs   
    for run in all_run_files:
        with open(run,'r') as csvfile:
            file = csv.reader(csvfile, delimiter = ',')
            for row in file:
                # we've isolated every row in the current file
                try:
                    if ("NTC" in row[4]):
                        if (row[7].isnumeric()) or (float(row[7])):
                            if (float(row[7]) > 0):
                                # we've determined the current file to have at least 1 positive, so we can break and move to the next txt file
                                all_positive_runs.append(run)
                                break
                except:
                    pass

    # check file paths before split()

    total_positives = len(all_positive_runs)
    
    for positive in all_positive_runs:
        testname = str(positive)
        words = testname.split('/')                 # on my computer
        try:
            test = words[7].partition("_")[0]       # on my computer
            all_positive_testnames.append(test)
        except:
            pass
    
    for test in all_positive_testnames:
        frequency.update({test: all_positive_testnames.count(test)})

    statistic = "{:.0%}".format(total_positives / (len(all_run_files)))

    try:
        f = open("monthly_statistics.txt", 'x')
    except:
        f = open("monthly_statistics.txt", 'a')
    f.write(argv1 + "\n")
    f.write(str(len(all_run_files)) + " total runs\n")
    f.write(str(total_positives) + " positives\n")
    f.write("Positive rate of approx: " + statistic + "\n")
    f.write("Positive Tests:\n")
    for test, count in frequency.items():
        statistic2 = "{:.0%}".format(count/total_positives)
        f.write(test + " - " + str(count) + " runs contained positives: makes up " + statistic2 + " of this month's positives\n")

# MAIN #
per_csv(sys.argv[1])
