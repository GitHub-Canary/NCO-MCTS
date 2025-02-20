import numpy as np

# 定义矩阵
matrix = np.array([
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
])


# 定义粒子类
class Particle:
    def __init__(self, bounds):
        self.position = np.array([np.random.randint(b[0], b[1]) for b in bounds])
        self.velocity = np.zeros_like(self.position)
        self.best_position = np.copy(self.position)
        self.best_value = float('inf')
        self.value = self.evaluate(self.position)

        if self.value < self.best_value:
            self.best_value = self.value
            self.best_position = np.copy(self.position)

    def evaluate(self, position):
        return objective_function_with_new_constraint(position, matrix)

    def update_velocity(self, global_best_position, iteration, max_iterations):
        w = 0.9 - iteration * (0.5 / max_iterations)  # 动态调整惯性权重
        c1 = 1.5  # 认知系数
        c2 = 1.5  # 社会系数
        self.velocity = (w * self.velocity +
                         c1 * np.random.rand(*self.position.shape) * (self.best_position - self.position) +
                         c2 * np.random.rand(*self.position.shape) * (global_best_position - self.position))

    def update_position(self, bounds):
        self.position += self.velocity.astype(int)
        for i in range(len(self.position)):
            self.position[i] = np.clip(self.position[i], bounds[i][0], bounds[i][1] - 1)

    def update_velocity(self, global_best_position, iteration, max_iterations):
        w = 0.9 - iteration * (0.5 / max_iterations)  # 动态调整惯性权重
        c1 = 1.5  # 认知系数
        c2 = 1.5  # 社会系数

        if global_best_position is None:
            global_best_position = self.position  # 使用当前位置作为初始全局最佳位置

        self.velocity = (w * self.velocity +
                         c1 * np.random.rand(*self.position.shape) * (self.best_position - self.position) +
                         c2 * np.random.rand(*self.position.shape) * (global_best_position - self.position))


# 检查子矩阵是否被零分割的函数
def is_split_by_zeros(submatrix):
    rows, cols = submatrix.shape
    visited = set()

    def dfs(r, c):
        if (r, c) in visited:
            return
        visited.add((r, c))
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and submatrix[nr, nc] != 0:
                dfs(nr, nc)

    # 找到第一个非零元素并开始DFS
    start_found = False
    for i in range(rows):
        for j in range(cols):
            if submatrix[i, j] != 0:
                dfs(i, j)
                start_found = True
                break
        if start_found:
            break

    # 检查是否所有非零元素都已访问
    for i in range(rows):
        for j in range(cols):
            if submatrix[i, j] != 0 and (i, j) not in visited:
                return True  # 发现未访问的非零元素，说明被零分割

    return False  # 所有非零元素都被访问，未被零分割


# 目标函数，考虑了新的约束
def objective_function_with_new_constraint(positions, matrix):
    positions = positions.reshape((10, 2))
    total = 0
    for i in range(10):
        for j in range(i + 1, 10):
            if np.any(positions[i] == positions[j]):
                return float('inf')  # 重复的子矩阵

        row, col = positions[i]
        submatrix = matrix[row:row + 3, col:col + 3]
        if is_split_by_zeros(submatrix):
            return float('inf')  # 被零分割的子矩阵
        total -= submatrix.sum()

    return total


# 初始化粒子群
num_particles = 500
bounds = [(0, 17)] * 20
particles = [Particle(bounds) for _ in range(num_particles)]
global_best_value = float('inf')
global_best_position = None

# 执行PSO算法
num_iterations = 400
for iteration in range(num_iterations):
    for particle in particles:
        particle.update_velocity(global_best_position, iteration, num_iterations)
        particle.update_position(bounds)
        particle.value = particle.evaluate(particle.position)

        if particle.value < particle.best_value:
            particle.best_value = particle.value
            particle.best_position = np.copy(particle.position)

        if particle.best_value < global_best_value:
            global_best_value = particle.best_value
            global_best_position = np.copy(particle.best_position)

# 输出结果
if global_best_position is not None:
    max_sum = -global_best_value
    submatrices_top_left = global_best_position.reshape((10, 2))
    print("Max sum:", max_sum)
    print("Submatrices top-left corners:", submatrices_top_left)
else:
    print("No valid solution found.")
