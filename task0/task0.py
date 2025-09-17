import csv
import numpy as np

path = "/task2.csv"
node = []
with open(path, 'r') as taskfile:
    iter = csv.reader(taskfile)
    for i in iter:
        node.append((int(i[0]),int(i[1])))
    size = max(max(node))
    matrix = np.zeros((size,size), dtype=np.int16)
    for a, b in node:
        matrix[a-1][b-1] = 1
        matrix[b-1][a-1] = 1
    print(matrix)
#def main(path):
