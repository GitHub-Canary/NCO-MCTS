import numpy as np

# Assuming 'matrix' is your 20x20 numpy array with the values
matrix = np.array([
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
])


# Objective function to minimize (negative sum of the 3x3 submatrix)
def objective_function(positions, matrix):
    total = 0
    positions = positions.reshape((10, 2))
    for pos in positions:
        row, col = pos
        total -= matrix[row:row + 3, col:col + 3].sum()
    return total


# Check if the submatrices overlap
def check_constraints(positions):
    positions = positions.reshape((10, 2))
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            if abs(positions[i][0] - positions[j][0]) < 3 and abs(positions[i][1] - positions[j][1]) < 3:
                return False
    return True


# Particle class representing a potential solution
class Particle:
    def __init__(self, bounds):
        self.position = np.array([np.random.randint(b[0], b[1]) for b in bounds])
        self.velocity = np.zeros_like(self.position)
        self.best_position = np.copy(self.position)
        self.best_value = float('inf')

        # Evaluate the current position
        self.value = objective_function(self.position, matrix)

        # Update the best position/value if the current position is better
        if self.value < self.best_value:
            self.best_value = self.value
            self.best_position = np.copy(self.position)

    def update_velocity(self, global_best_position):
        w = 0.5  # Inertia weight
        c1 = c2 = 1.49  # Cognitive and social coefficients

        # Update velocity according to the PSO velocity update formula
        self.velocity = (w * self.velocity +
                         c1 * np.random.rand(*self.position.shape) * (self.best_position - self.position) +
                         c2 * np.random.rand(*self.position.shape) * (global_best_position - self.position))

    def update_position(self, bounds):
        # Update position according to the velocity
        self.position += self.velocity.astype(int)

        # Apply the constraints to ensure the particle stays within bounds
        for i in range(len(self.position)):
            self.position[i] = np.clip(self.position[i], bounds[i][0], bounds[i][1] - 1)

        # Check and resolve overlaps
        if not check_constraints(self.position):
            self.position = np.array([np.random.randint(b[0], b[1]) for b in bounds])


# Initialize the swarm
num_particles = 500
bounds = [(0, 17)] * 20  # Bounds for the top-left corner of each 3x3 submatrix
particles = [Particle(bounds) for _ in range(num_particles)]
global_best_value = float('inf')
global_best_position = None

# Run the PSO algorithm
num_iterations = 400
for _ in range(num_iterations):
    for particle in particles:
        # Update the velocity of each particle
        particle.update_velocity(global_best_position if global_best_position is not None else particle.position)

        # Update the position of each particle
        particle.update_position(bounds)

        # Evaluate the new position
        particle.value = objective_function(particle.position, matrix)

        # Update the personal and global bests if necessary
        if particle.value < particle.best_value and check_constraints(particle.position):
            particle.best_value = particle.value
            particle.best_position = np.copy(particle.position)
            if particle.best_value < global_best_value:
                global_best_value = particle.best_value
                global_best_position = np.copy(particle.best_position)

# Print the results
max_sum = -global_best_value
submatrices_top_left = global_best_position.reshape((10, 2))
print("Max sum:", max_sum)
print("Submatrices top-left corners:", submatrices_top_left)
