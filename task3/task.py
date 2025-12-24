import json
import numpy as np

def parse_rank(ranking):
    clstrs = []
    for item in ranking:
        if isinstance(item, list):
            clstrs.append(item)
        else:
            clstrs.append([item])
    return clstrs

def build_rel_mat(clstrs, objs):
    n = len(objs)
    mat = np.zeros((n, n), dtype=int)
    obj_to_clstr_idx = {}
    for idx, clstr in enumerate(clstrs):
        for obj in clstr:
            obj_to_clstr_idx[obj] = idx
    for i, obj_i in enumerate(objs):
        for j, obj_j in enumerate(objs):
            if obj_i in obj_to_clstr_idx and obj_j in obj_to_clstr_idx:
                clstr_i = obj_to_clstr_idx[obj_i]
                clstr_j = obj_to_clstr_idx[obj_j]
                if clstr_i <= clstr_j:
                    mat[i][j] = 1
    return mat

def find_contr_core(YA, YB, objs):
    n = len(objs)
    Y_AB = np.multiply(YA, YB)
    Y_ATBT = np.multiply(YA.T, YB.T)
    mat = np.logical_or(Y_AB, Y_ATBT).astype(int)
    contrs = []
    for i in range(n):
        for j in range(i+1, n):
            if mat[i][j] == 0:
                contrs.append([objs[i], objs[j]])
    return contrs

def build_agreed_mat(YA, YB, contrs, objs):
    mat = np.multiply(YA, YB).astype(int)
    obj_to_idx = {obj: idx for idx, obj in enumerate(objs)}
    for pair in contrs:
        i = obj_to_idx[pair[0]]
        j = obj_to_idx[pair[1]]
        mat[i][j] = 1
        mat[j][i] = 1
    return mat

def find_clstrs_from_mat(mat, objs):
    n = len(objs)
    E = np.logical_and(mat, mat.T).astype(int)
    E_w = E.copy()
    for i in range(n):
        for k in range(n):
            for j in range(n):
                if E_w[k][i] and E_w[i][j]:
                    E_w[k][j] = 1
    visited = [False] * n
    clstrs = []
    for i in range(n):
        if not visited[i]:
            clstr = []
            for j in range(n):
                if E_w[i][j]:
                    clstr.append(objs[j])
                    visited[j] = True
            clstrs.append(sorted(clstr))
    return clstrs

def order_clstrs(clstrs, mat, objs):
    n_clstrs = len(clstrs)
    obj_to_clstr = {}
    for idx, clstr in enumerate(clstrs):
        for obj in clstr:
            obj_to_clstr[obj] = idx
    clstr_order = np.zeros((n_clstrs, n_clstrs), dtype=int)
    obj_to_idx = {obj: idx for idx, obj in enumerate(objs)}
    for i in range(n_clstrs):
        for j in range(n_clstrs):
            if i != j:
                obj_i = clstrs[i][0]
                obj_j = clstrs[j][0]
                idx_i = obj_to_idx[obj_i]
                idx_j = obj_to_idx[obj_j]
                if mat[idx_i][idx_j] == 1 and mat[idx_j][idx_i] == 0:
                    clstr_order[i][j] = 1
    res_clstrs = []
    rem = list(range(n_clstrs))
    while rem:
        for i in rem:
            flag = False
            for j in rem:
                if clstr_order[j][i] == 1:
                    flag = True
                    break
            if not flag:
                res_clstrs.append(clstrs[i])
                rem.remove(i)
                break
    return res_clstrs

def main(json_str_a, json_str_b):
    ranking_a = json.loads(json_str_a)
    ranking_b = json.loads(json_str_b)
    clstrs_a = parse_rank(ranking_a)
    clstrs_b = parse_rank(ranking_b)
    all_objs = set()
    for clstr in clstrs_a:
        all_objs.update(clstr)
    for clstr in clstrs_b:
        all_objs.update(clstr)
    objs = sorted(all_objs)
    YA = build_rel_mat(clstrs_a, objs)
    YB = build_rel_mat(clstrs_b, objs)
    contrs = find_contr_core(YA, YB, objs)
    C = build_agreed_mat(YA, YB, contrs, objs)
    clstrs = find_clstrs_from_mat(C, objs)
    ordered_clstrs = order_clstrs(clstrs, C, objs)
    res = []
    for clstr in ordered_clstrs:
        if len(clstr) == 1: 
            res.append(clstr[0])
        else: 
            res.append(clstr)
    return json.dumps(res, ensure_ascii=False)
