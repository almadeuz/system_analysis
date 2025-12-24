import numpy as np
import sys

def parse(txt, root):
    edg = []
    ver = set()
    for lin in txt.strip().split('\n'):
        if lin:
            par, chd = lin.split(',')
            edg.append((par.strip(), chd.strip()))
            ver.add(par.strip())
            ver.add(chd.strip())
    ver.add(root)
    vls = sorted(ver, key=lambda x: int(x) if x.isdigit() else x)
    vtoi = {v: i for i, v in enumerate(vls)}
    n = len(vls)
    adj = np.zeros((n, n), dtype=bool)
    for par, chd in edg:
        i = vtoi[par]
        j = vtoi[chd]
        adj[i][j] = True
    
    return adj, vls

def r1(adj):
    return adj.copy()

def r2(adj):
    return adj.T.copy()

def r3(adj):
    n = adj.shape[0]
    rch = adj.copy().astype(bool)
    for k in range(n):
        for i in range(n):
            if rch[i, k]:
                rch[i] = rch[i] | rch[k]
    
    res = rch & ~adj
    np.fill_diagonal(res, False)
    return res

def r4(adj):
    return r3(adj).T

def r5(adj):
    n = adj.shape[0]
    res = np.zeros((n, n), dtype=bool)
    for par in range(n):
        chl = np.where(adj[par])[0]
        if len(chl) >= 2:
            for i in range(len(chl)):
                for j in range(i + 1, len(chl)):
                    a = chl[i]
                    b = chl[j]
                    res[a, b] = True
                    res[b, a] = True
    return res

def main(s, e):
    adj, _ = parse(s, e)
    
    return (
        r1(adj).tolist(),
        r2(adj).tolist(),
        r3(adj).tolist(),
        r4(adj).tolist(),
        r5(adj).tolist()
    )

data = "1,2\n1,3\n3,4\n3,5\n5,6\n6,7"
root = "1"

if len(sys.argv) > 2:
    inp = sys.argv[1]
    root = sys.argv[2]
    
    if inp.endswith('.csv'):
        try:
            with open(inp, 'r') as f:
                data = f.read().strip()
        except:
            pass

matrices = main(data, root)
adj, vertices = parse(data, root)

names = ["r1", "r2", "r3", "r4", "r5"]

for name, matrix in zip(names, matrices):
    print(f"\n{name}:")
    print("  " + " ".join(f"{v}" for v in vertices))
    for i, row in enumerate(matrix):
        print(f"{vertices[i]} " + " ".join(f"{int(cell)}" for cell in row))
