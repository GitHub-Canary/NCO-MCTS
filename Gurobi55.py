import gurobipy as gp
from gurobipy import GRB
from gurobipy import *
import numpy as np

A = np.matrix([
    [204, 248, 28, 328, 0, 37, 43, 30, 144, 0, 125, 247, 209, 321, 72, 315, 347, 132, 95, 216],
    [169, 0, 75, 324, 281, 0, 322, 312, 64, 177, 52, 184, 25, 200, 0, 285, 44, 0, 257, 298],
    [161, 133, 329, 11, 59, 332, 241, 10, 154, 325, 82, 22, 234, 89, 55, 42, 265, 235, 309, 4],
    [307, 53, 174, 202, 87, 155, 344, 0, 0, 246, 91, 119, 333, 186, 0, 199, 123, 0, 31, 134],
    [314, 102, 137, 0, 359, 16, 126, 208, 54, 269, 295, 111, 251, 173, 284, 271, 0, 143, 357, 96],
    [214, 149, 0, 32, 259, 26, 219, 0, 103, 0, 38, 76, 98, 34, 0, 92, 172, 279, 223, 354],
    [299, 243, 194, 289, 12, 266, 41, 29, 212, 68, 182, 88, 35, 61, 128, 176, 13, 190, 19, 105],
    [267, 323, 108, 264, 18, 0, 274, 167, 104, 100, 117, 80, 0, 3, 282, 206, 254, 249, 193, 51],
    [233, 317, 0, 110, 69, 338, 272, 15, 70, 73, 201, 326, 145, 197, 240, 148, 0, 316, 9, 170],
    [358, 222, 262, 131, 335, 327, 0, 0, 20, 356, 273, 278, 213, 79, 7, 0, 296, 27, 304, 115],
    [158, 138, 130, 0, 129, 320, 239, 165, 355, 135, 236, 292, 258, 47, 33, 225, 78, 185, 179, 237],
    [340, 0, 63, 168, 8, 302, 109, 139, 99, 287, 263, 120, 313, 81, 339, 77, 331, 231, 350, 180],
    [218, 205, 230, 245, 253, 242, 0, 189, 303, 107, 280, 275, 0, 162, 66, 1, 0, 160, 0, 136],
    [45, 24, 224, 152, 293, 164, 0, 112, 0, 290, 147, 351, 127, 283, 297, 166, 58, 342, 0, 0],
    [175, 268, 221, 113, 94, 122, 151, 0, 220, 198, 40, 50, 157, 0, 277, 210, 150, 349, 345, 5],
    [85, 232, 0, 288, 106, 260, 183, 49, 229, 187, 60, 215, 228, 310, 121, 14, 90, 291, 118, 163],
    [181, 353, 65, 97, 308, 141, 227, 57, 83, 153, 178, 23, 196, 39, 341, 116, 46, 334, 244, 337],
    [261, 336, 146, 17, 156, 74, 252, 238, 318, 124, 62, 343, 188, 101, 311, 211, 226, 255, 114, 0],
    [86, 203, 319, 352, 2, 305, 84, 142, 191, 250, 93, 140, 217, 0, 286, 192, 330, 67, 301, 306],
    [171, 270, 256, 71, 348, 21, 48, 159, 294, 56, 6, 207, 0, 195, 0, 276, 36, 346, 0, 300]
]
)

row = 18
column = 18
validdot_list = [[[] for _ in range(20)] for _ in range(20)]


def value(x, A):
    ob = 0
    for i in range(row):
        for j in range(column):
            ob = ob + x[i, j] * (
                        A[i, j] + A[i, j + 1] + A[i, j + 2] + A[i + 1, j] + A[i + 1, j + 1] + A[i + 1, j + 2] + A[
                    i + 2, j] + A[i + 2, j + 1] + A[i + 2, j + 2])
    for i in range(20):
        for j in range(20):
            ob = ob + r[i, j] * A[i, j]
    return ob


average = np.matrix([[0 for _ in range(18)] for _ in range(18)])
for i in range(row):
    for j in range(column):
        average[i, j] = (A[i, j] + A[i, j + 1] + A[i, j + 2] + A[i + 1, j] + A[i + 1, j + 1] + A[i + 1, j + 2] + A[
            i + 2, j] + A[i + 2, j + 1] + A[i + 2, j + 2]) / 9

for i in range(20):
    for j in range(20):
        dotlist = [[i - 3, j - 3], [i - 2, j - 3], [i - 1, j - 3], [i, j - 3], [i + 1, j - 3], [i + 1, j - 2],
                   [i + 1, j - 1], [i + 1, j], [i + 1, j + 1], [i, j + 1], [i - 1, j + 1], [i - 2, j + 1],
                   [i - 3, j + 1], [i - 3, j], [i - 3, j - 1], [i - 3, j - 2]]
        num_dot = 0
        for dot in dotlist:
            a, b = dot
            if 0 <= a <= 17 and 0 <= b <= 17:
                validdot_list[i][j].append(dot)
                num_dot += 1

Local = gp.Model("TenPoint")
x = Local.addVars(18, 18, vtype=GRB.BINARY, name="x")
r = Local.addVars(20, 20, vtype=GRB.BINARY, name="r")

# 修改此处，z变量不再使用i,j作为参数
z = Local.addVars(20, 20, len(validdot_list), vtype=GRB.BINARY, name="z")

# 添加约束以确保z变量与validdot_list对应
for i in range(20):
    for j in range(20):
        Local.addConstr(r[i, j] <= gp.quicksum(z[i, j, k] for k in range(len(validdot_list[i][j]))))
        Local.addConstr(r[i, j] >= gp.quicksum(z[i, j, k] for k in range(len(validdot_list[i][j]))) / 3)
        for k, (a, b) in enumerate(validdot_list[i][j]):
            Local.addConstr(z[i, j, k] <= x[a, b] * (A[i, j] / average[a, b]))

Local.setObjective(value(x, A), GRB.MAXIMIZE)
for i in range(row - 2):
    for j in range(column - 2):
        Local.addConstr(
            x[i, j] + x[i, j + 1] + x[i, j + 2] + x[i + 1, j] + x[i + 1, j + 1] + x[i + 1, j + 2] + x[i + 2, j] + x[
                i + 2, j + 1] + x[i + 2, j + 2] <= 1, "absconstr1")
Local.addConstr(gp.quicksum(x) == 10, "absconstr1")

for i in range(row):
    for j in range(column):
        Local.addConstr(r[i, j] <= 1 - x[i, j])
        Local.addConstr(r[i + 1, j] <= 1 - x[i, j])
        Local.addConstr(r[i + 2, j] <= 1 - x[i, j])
        Local.addConstr(r[i, j + 1] <= 1 - x[i, j])
        Local.addConstr(r[i + 1, j + 1] <= 1 - x[i, j])
        Local.addConstr(r[i + 2, j + 1] <= 1 - x[i, j])
        Local.addConstr(r[i, j + 2] <= 1 - x[i, j])
        Local.addConstr(r[i + 1, j + 2] <= 1 - x[i, j])
        Local.addConstr(r[i + 2, j + 2] <= 1 - x[i, j])

Local.addConstr(x[8, 15] == 0, "absconstr1")

Local.optimize()

for i in range(row):
    for j in range(column):
        if x[i, j].X == 1:
            print(f'x{i},{j}')

print(Local.ObjVal)
for i in range(20):
    for j in range(20):
        if r[i, j].X == 1:
            print(f'r{i},{j}')
