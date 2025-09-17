import csv
import numpy as np

path = "/task2.csv"
node = []
with open(path, 'r') as taskfile:
    iter = csv.reader(taskfile)
    for i in iter:
        node.append((int(i[0]),int(i[1])))
#def main(path):
