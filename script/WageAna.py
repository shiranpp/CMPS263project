# coding: utf-8

# In[27]:

'''
    Job Salary analysis
    Author: Zhuo Wang,Ziqiang Wang
    For CMPS263 project
    Analysis the Salary data to show total saving.
'''
import matplotlib.pyplot as plt
import numpy as np
import unicodecsv as csv
import sys
import re
import os
import json

default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.setdefaultencoding("utf-8")
sys.stdout = default_stdout
sys.stderr = default_stderr

if __name__ == "__main__":
    CS = []
    with open("wage.csv", "rb") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (re.search(u"计算机", row["area"]) or re.search(u"销售", row["area"])):
                CS.append(row)

    # In[28]:

    # aquire and catalog salary data
    sale = []
    pmanager = []
    dev = []
    for row in CS:
        wage = []
        if (row["exp_3"] == ''):
            continue
        if ((row["exp_5"] != '')):
            wage += [int(row["exp_0"]) * 12]
            wage += [int(row["exp_1"]) * 12] * 2
            wage += [int(row["exp_2"]) * 12] * 3
            wage += [int(row["exp_3"]) * 12] * 2
            wage += [int(row["exp_4"]) * 12] * 3
            wage += [int(row["exp_5"]) * 12] * 19
        else:
            if (row["exp_4"] != ''):
                wage += [int(row["exp_0"]) * 12]
                wage += [int(row["exp_1"]) * 12] * 2
                wage += [int(row["exp_2"]) * 12] * 3
                wage += [int(row["exp_3"]) * 12] * 2
                wage += [int(row["exp_4"]) * 12] * 22
            else:
                wage += [int(row["exp_0"]) * 12] * 3
                wage += [int(row["exp_1"]) * 12] * 3
                wage += [int(row["exp_2"]) * 12] * 2
                wage += [int(row["exp_3"]) * 12] * 22
        if (re.search(u"工程师", row["title"])):
            dev.append(wage)
        if (re.search(u"销售", row["title"])):
            sale.append(wage)
        if (re.search(u"产品经理", row["title"])):
            pmanager.append(wage)
    sale = np.average(np.array(sale), axis=0)
    dev = np.average(np.array(dev), axis=0)
    pmanager = np.average(np.array(pmanager), axis=0)

    sale = [sum(sale[0:i]) for i in range(1, 31)]
    dev = [sum(dev[0:i]) for i in range(1, 31)]
    pmanager = [sum(pmanager[0:i]) for i in range(1, 31)]

    # curve fitting and sample visualization
    twages = [dev, sale, pmanager]
    names = ["Developer", "SaleMan", "ProductManager"]
    factor = []
    for i in range(0, len(twages)):
        x = np.arange(1, 31, 1)
        y = np.array(twages[i])
        z1 = np.polyfit(x, y, 3)
        factor.append(z1)
        plt.plot(range(1, 31), twages[i], label=names[i])

    data = []
    for i in range(0, len(twages)):
        data.append({"title": names[i], "factor": factor[i].tolist()})

    # write in to samplewage.js
    if (os.path.exists('samplewage.js')):
        os.remove('samplewage.js')
    x = "var jobs = " + json.dumps(data) + ";"
    with open('samplewage.js', 'w') as outfile:
        outfile.write(x)
    plt.show()
