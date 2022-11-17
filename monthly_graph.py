import matplotlib.pyplot as plt
import pandas as pd
import sys
import re

def plot_graph(month):

    dict = {}

    f = open("monthly_statistics.txt", 'r')
    f = f.readlines()

    for line in f[5::]:
        try:
            line = line.split(" ")
            temp = line[8].partition("%")[0]
            temp = (int(temp))/100
            dict.update({line[0]: temp})
        except:
            pass

    x = list(dict.keys())
    y = list(dict.values())

    plt.bar(x, y)
    plt.xlabel('Test Name', fontsize = 12)
    plt.ylabel('Percentage of Total Positives', fontsize = 12)
    plt.title(month + " 2022: NTC Positives by Test", fontsize = 20)
    plt.show()

# MAIN #
plot_graph(sys.argv[1])
