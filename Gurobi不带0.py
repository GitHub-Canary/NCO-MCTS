import gurobipy as gp
from gurobipy import GRB
from gurobipy import *
import numpy as np
import matplotlib.pyplot as plt

A = np.matrix([
    [276, 39, 188, 293, 225, 92, 217, 318, 365, 101, 323, 246, 132, 211, 143, 17, 165, 274, 35, 233],
    [71, 317, 158, 249, 294, 224, 72, 232, 16, 239, 23, 259, 334, 265, 61, 391, 65, 245, 229, 368],
    [138, 32, 142, 280, 271, 195, 328, 290, 131, 51, 40, 110, 118, 349, 133, 302, 114, 139, 355, 205],
    [312, 191, 292, 38, 325, 364, 361, 107, 69, 146, 367, 24, 105, 194, 261, 170, 157, 382, 226, 199],
    [281, 269, 340, 152, 253, 341, 345, 221, 28, 356, 203, 164, 306, 113, 115, 33, 254, 384, 43, 37],
    [84, 277, 88, 268, 89, 94, 56, 200, 177, 18, 213, 50, 305, 378, 360, 49, 34, 250, 1, 222],
    [363, 169, 270, 41, 219, 230, 301, 3, 63, 6, 90, 366, 97, 55, 307, 160, 216, 329, 311, 124],
    [85, 171, 76, 67, 220, 283, 145, 264, 336, 218, 284, 25, 344, 14, 48, 78, 179, 163, 358, 354],
    [303, 212, 393, 237, 319, 7, 380, 181, 121, 73, 231, 381, 123, 12, 333, 202, 151, 31, 30, 166],
    [248, 68, 342, 315, 322, 187, 343, 372, 379, 243, 234, 75, 198, 266, 388, 190, 93, 260, 204, 60],
    [320, 148, 308, 109, 193, 127, 258, 29, 275, 279, 168, 66, 251, 257, 262, 140, 141, 313, 136, 36],
    [331, 111, 346, 375, 99, 22, 62, 228, 77, 197, 201, 135, 321, 370, 383, 353, 207, 137, 332, 183],
    [296, 70, 255, 172, 385, 389, 310, 374, 288, 98, 149, 27, 324, 242, 64, 10, 227, 173, 390, 95],
    [377, 273, 314, 338, 357, 167, 174, 122, 8, 289, 236, 399, 59, 215, 26, 153, 42, 398, 192, 396],
    [126, 112, 256, 282, 272, 252, 11, 46, 129, 155, 104, 278, 373, 86, 21, 350, 58, 330, 128, 81],
    [369, 209, 9, 223, 196, 387, 240, 392, 376, 130, 309, 326, 96, 185, 351, 214, 13, 286, 4, 176],
    [210, 316, 161, 106, 154, 150, 300, 45, 337, 5, 54, 235, 178, 295, 108, 327, 0, 144, 339, 386],
    [298, 74, 182, 117, 371, 102, 87, 352, 287, 91, 57, 19, 103, 263, 80, 120, 297, 359, 208, 189],
    [285, 2, 119, 147, 52, 134, 362, 79, 299, 53, 125, 159, 397, 116, 156, 394, 100, 180, 238, 247],
    [335, 83, 347, 291, 244, 304, 206, 175, 82, 241, 395, 15, 44, 162, 47, 184, 267, 20, 348, 186]
]
)


def value(x, y, A):
    ob = 0
    for i in range(row):
        for j in range(column):
            ob = ob + (x[i, j] + y[i, j]) * (
                    A[i, j] + A[i, j + 1] + A[i, j + 2] + A[i + 1, j] + A[i + 1, j + 1] + A[i + 1, j + 2] + A[
                i + 2, j] + A[i + 2, j + 1] + A[i + 2, j + 2])
    return ob


def solve_location_problem(n, m):
    Local = gp.Model("TenPoint")
    x = Local.addVars(18, 18, vtype=GRB.BINARY, name="x")
    y = Local.addVars(18, 18, vtype=GRB.BINARY, name="y")
    Local.setObjective(value(x, y, A), GRB.MAXIMIZE)

    for i in range(row - 2):
        for j in range(column - 2):
            Local.addConstr(
                x[i, j] + x[i, j + 1] + x[i, j + 2] + x[i + 1, j] + x[i + 1, j + 1] + x[i + 1, j + 2] + x[i + 2, j] + x[
                    i + 2, j + 1] + x[i + 2, j + 2] <= 1, "absconstr1")
            Local.addConstr(
                y[i, j] + y[i, j + 1] + y[i, j + 2] + y[i + 1, j] + y[i + 1, j + 1] + y[i + 1, j + 2] + y[i + 2, j] + y[
                    i + 2, j + 1] + y[i + 2, j + 2] <= 1, "absconstr2")

    Local.addConstr(gp.quicksum(x) == n, "absconstr3")
    Local.addConstr(gp.quicksum(y) == m, "absconstr4")
    Local.addConstr(gp.quicksum(x) + gp.quicksum(y) == 10, "absconstr5")

    for i in range(row):
        for j in range(column):
            for ii in range(i, row):
                for jj in range(column):
                    if ii != i or jj != j:
                        Local.addConstr(x[i, j] + x[ii, jj] <= 1 + (abs(ii - i) + abs(jj - j) >= 3),
                                        f"absconstr6_{i}_{j}_{ii}_{jj}")

    Local.optimize()

    for i in range(row):
        for j in range(column):
            if x[i, j].X == 1:
                print(f'x{i},{j}')
            if y[i, j].X == 1:
                print(f'y{i},{j}')

    print(Local.ObjVal)

    # 可视化结果
    grid = np.zeros((row, column))
    for i in range(row):
        for j in range(column):
            if x[i, j].X == 1:
                grid[i:i + 3, j:j + 3] = 1
            if y[i, j].X == 1:
                grid[i:i + 3, j:j + 3] = 1

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(grid, cmap='binary', origin='lower', alpha=0.2)

    for i in range(row):
        for j in range(column):
            if grid[i, j] == 1:
                ax.text(j, i, int(A[i, j]), ha='center', va='center', color='blue', fontsize=8)
            else:
                ax.text(j, i, int(A[i, j]), ha='center', va='center', color='black', fontsize=8)

    ax.set_xticks(np.arange(column))
    ax.set_yticks(np.arange(row))
    ax.set_xticklabels(np.arange(1, column + 1))
    ax.set_yticklabels(np.arange(1, row + 1))
    ax.grid(color='white', linewidth=1)

    plt.title(f'Selected Locations (n={n}, m={m})')
    plt.show()


# 示例用法
row = 18
column = 18
n = 6  # 先选择6个位置
m = 4  # 再从剩余区域选择4个位置
solve_location_problem(n, m)
