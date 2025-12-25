import json
import numpy as np

def create_mf(points):
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        def mf(val):
            if val <= x[0]:
                return y[0]
            elif val >= x[-1]:
                return y[-1]
            for i in range(len(x)-1):
                if x[i] <= val <= x[i+1]:
                    return y[i] + (y[i+1] - y[i]) * (val - x[i]) / (x[i+1] - x[i])
            return 0
        return mf

def main(temp_json, heat_json, rules_json, current_temp):
    temp_sets = json.loads(temp_json)
    heat_sets = json.loads(heat_json)
    rules = json.loads(rules_json)
    temp_mfs = {}
    for term in temp_sets["температура"]:
        temp_mfs[term["id"]] = create_mf(term["points"])
    heat_mfs = {}
    for term in heat_sets["уровень нагрева"]:
        heat_mfs[term["id"]] = create_mf(term["points"])
    temp_degrees = {}
    for term_id, mf in temp_mfs.items():
        temp_degrees[term_id] = max(0, min(1, mf(current_temp)))
    all_points = []
    for term in heat_sets["уровень нагрева"]:
        all_points.extend([p[0] for p in term["points"]])
    s_min = min(all_points)
    s_max = max(all_points)
    step = 1e-3
    s_vals = np.arange(s_min, s_max + step, step)
    aggr = np.zeros_like(s_vals)
    for rule in rules:
        temp_term, heat_term = rule
        activation = temp_degrees.get(temp_term, 0)
        if activation > 0:
            heat_mf = heat_mfs[heat_term]
            for i, s in enumerate(s_vals):
                val = min(activation, heat_mf(s))
                aggr[i] = max(aggr[i], val)
    max_val = np.max(aggr)
    if max_val == 0:
        return round((s_min + s_max) / 2, 2)
    for i, s in enumerate(s_vals):
        if aggr[i] >= max_val - 1e-6:
            if abs(s) <= 1e-3 + 1e-6:
                return 0.0
            return round(s, 2)
    return round((s_min + s_max) / 2, 2)

temp_json = """
{
    "температура": [
        {
        "id": "холодно",
        "points": [
            [0,1],
            [18,1],
            [22,0],
            [50,0]
        ]
        },
        {
        "id": "комфортно",
        "points": [
            [18,0],
            [22,1],
            [24,1],
            [26,0]
        ]
        },
        {
        "id": "жарко",
        "points": [
            [0,0],
            [24,0],
            [26,1],
            [50,1]
        ]
        }
    ]
}
"""

heat_json = """
{
    "уровень нагрева": [
        {
        "id": "слабый",
        "points": [
            [0,0],
            [0,1],
            [5,1],
            [8,0]
        ]
        },
        {
        "id": "умеренный",
        "points": [
            [5,0],
            [8,1],
            [13,1],
            [16,0]
        ]
        },
        {
        "id": "интенсивный",
        "points": [
            [13,0],
            [18,1],
            [23,1],
            [26,0]
        ]
        }
    ]
}
"""

rules_json = """
[
    ["холодно", "интенсивный"],
    ["комфортно", "умеренный"],
    ["жарко", "слабый"]
]
"""


for temp in range(0, 31, 2):
    opt = main(temp_json, heat_json, rules_json, temp)
    print(f"Температура: {temp}; Управление: {opt}")
