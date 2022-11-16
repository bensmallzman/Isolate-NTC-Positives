import matplotlib.pyplot as plt
import pandas as pd
import re

months = []
y_values = []
newlist = []
pair = {}

f = open("yearly_statistics.txt", 'r')

for row in f:
    if (row.startswith("January")):
        months.append(row.rstrip())
    elif(row.startswith("February")):
        months.append(row.rstrip())
    elif(row.startswith("March")):
        months.append(row.rstrip())
    elif(row.startswith("April")):
        months.append(row.rstrip())
    elif(row.startswith("May")):
        months.append(row.rstrip())
    elif(row.startswith("June")):
        months.append(row.rstrip())
    elif(row.startswith("July")):
        months.append(row.rstrip())
    elif(row.startswith("August")):
        months.append(row.rstrip())
    elif(row.startswith("September")):
        months.append(row.rstrip())
    elif(row.startswith("October")):
        months.append(row.rstrip())
    elif(row.startswith("November")):
        months.append(row.rstrip())
    elif(row.startswith("December")):
        months.append(row.rstrip())

    # if last character in row is %
    if (row.endswith('%\n')):
        rate = re.findall(r'\d+', row)
        y_values.append(rate)
        
for each_list in y_values:
    for string in each_list:
        num = int(string)
        result = num/100
        newlist.append(result)

plt.bar(months, newlist, color = 'b')
plt.xlabel('Month', fontsize = 12)
plt.ylabel('Positive Runs per Total Runs', fontsize = 12)
plt.title("Monthly Rates of NTC Positives - 2022", fontsize = 20)
plt.show()
