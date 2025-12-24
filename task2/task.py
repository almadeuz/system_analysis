import numpy as np
import math
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

def task(s, e):
    adj, vls = parse(s, e)
    mat = [
        r1(adj),
        r2(adj),
        r3(adj),
        r4(adj),
        r5(adj)
    ]
    n = len(vls)
    ent = 0.0
    if n == 1:
        H = 0.0
        H_ref = 0.5307 * n * 5
        h = 0.0
        return (round(H, 1), round(h, 1))
    for i in range(5):
        for j in range(n):
            lij = np.sum(mat[i][j])
            if lij > 0:
                p = lij / (n - 1)
                ent += -p * math.log2(p)
    H = ent
    H_ref = 0.5307 * n * 5
    h = H / H_ref
    return (round(H, 1), round(h, 1))

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

H, h = task(data, root)
