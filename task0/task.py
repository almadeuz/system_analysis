import csv
import numpy as np

def main(csvfile):
    node = []
    iter = csv.reader(csvfile.splitlines())
    for i in iter:
        print(i)
        node.append((int(i[0]),int(i[1])))
    size = max(max(node))
    matrix = np.zeros((size,size), dtype=np.int16)
    for a, b in node:
        matrix[a-1][b-1] = 1
        matrix[b-1][a-1] = 1
    return matrix
