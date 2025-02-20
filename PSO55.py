import numpy as np
import random
import time

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


class Particle:
    def __init__(self):
        self.position = np.zeros((18, 18), dtype=int)
        self.velocity = np.zeros((18, 18))
        self.best_position = np.zeros((18, 18), dtype=int)
        self.best_score = float('-inf')

        # 随机初始化1个3x3区域
        while True:
            i, j = random.randint(0, 15), random.randint(0, 15)
            if np.sum(self.position[max(0, i - 2):min(18, i + 3), max(0, j - 2):min(18, j + 3)]) == 0:
                self.position[i:i + 3, j:j + 3] = 1
                self.expand_selection(i, j)
                break

    def expand_selection(self, i, j):
        center_sum = np.sum(A[i:i + 3, j:j + 3])
        threshold = (center_sum / 9) * 0.8
        for x in range(max(0, i - 1), min(18, i + 4)):
            for y in range(max(0, j - 1), min(18, j + 4)):
                if A[x, y] >= threshold:
                    self.position[x, y] = 1


def objective_function(position):
    score = 0
    for i in range(16):
        for j in range(16):
            if np.sum(position[i:i + 3, j:j + 3]) == 9:  # 如果找到一个完整的3x3区域
                center_sum = np.sum(A[i:i + 3, j:j + 3])
                score += center_sum
                # 计算周围区域
                for x in range(max(0, i - 1), min(18, i + 4)):
                    for y in range(max(0, j - 1), min(18, j + 4)):
                        if position[x, y] == 1:
                            score += A[x, y]
    return score


def pso(n_particles, n_iterations):
    particles = [Particle() for _ in range(n_particles)]
    global_best_position = None
    global_best_score = float('-inf')

    for _ in range(n_iterations):
        for particle in particles:
            score = objective_function(particle.position)

            if score > particle.best_score:
                particle.best_score = score
                particle.best_position = particle.position.copy()

            if score > global_best_score:
                global_best_score = score
                global_best_position = particle.position.copy()

        for particle in particles:
            w = 0.5  # 惯性权重
            c1 = 1  # 认知参数
            c2 = 2  # 社会参数

            r1, r2 = random.random(), random.random()

            particle.velocity = (w * particle.velocity +
                                 c1 * r1 * (particle.best_position - particle.position) +
                                 c2 * r2 * (global_best_position - particle.position))

            new_position = particle.position + particle.velocity.round().astype(int)

            # 确保新位置是有效的
            valid_new_position = np.zeros((18, 18), dtype=int)
            for i in range(16):
                for j in range(16):
                    if np.sum(new_position[i:i + 3, j:j + 3]) >= 7:  # 如果3x3区域中至少有7个点被选中
                        valid_new_position[i:i + 3, j:j + 3] = 1
                        particle.expand_selection(i, j)
                        break
                if np.sum(valid_new_position) > 0:
                    break

            if np.sum(valid_new_position) == 0:  # 如果没有找到有效位置，随机初始化
                i, j = random.randint(0, 15), random.randint(0, 15)
                valid_new_position[i:i + 3, j:j + 3] = 1
                particle.expand_selection(i, j)

            particle.position = valid_new_position

    return global_best_position, global_best_score


# 运行PSO并计时
start_time = time.time()

best_position, best_score = pso(n_particles=500, n_iterations=400)

end_time = time.time()
run_time = end_time - start_time

print(f"Best score: {best_score}")
print("Best position:")
for i in range(18):
    for j in range(18):
        if best_position[i, j] == 1:
            print(f'x{i},{j}')

print(f"\nRunning time: {run_time:.2f} seconds")
