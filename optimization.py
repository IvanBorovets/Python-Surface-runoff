import numpy as np
import sys
from scipy.optimize import minimize


def scipy_minimize(interpolation_function):
    local_min = np.array([])
    local_max = np.array([])

    for i in interpolation_function[0].xi[0]:
        temp = minimize(interpolation_function[0], i, method='L-BFGS-B',
                        bounds=((interpolation_function[0].xi[0][0], interpolation_function[0].xi[0][-1]),), options={'gtol': 1e-8})
        local_min = np.append(local_min, temp.x)

        temp = minimize(interpolation_function[1], i, method='L-BFGS-B',
                        bounds=( (interpolation_function[1].xi[0][0], interpolation_function[1].xi[0][-1]),), options={'gtol': 1e-8})
        local_max = np.append(local_max, temp.x)

    local_min = np.sort(local_min)
    local_max = np.sort(local_max)
    for i in range(np.size(local_min) - 2, -1, -1):
        if abs(local_min[i] - local_min[i + 1]) < 0.1:
            local_min = np.delete(local_min, i)

    for i in range(np.size(local_max) - 2, -1, -1):
        if abs(local_max[i] - local_max[i + 1]) < 0.1:
            local_max = np.delete(local_max, i)

    while True:
        if local_min[np.size(local_min) - 1] > local_max[np.size(local_max) - 1]:
            local_min = np.delete(local_min, np.size(local_min) - 1)
            continue
        if local_min[0] < local_max[0]:
            local_min = np.delete(local_min, 0)
            if np.size(local_min) == 0:

                print("Minimum not found")
                sys.exit()
            continue
        if np.size(local_min) >= np.size(local_max):
            i = 0
            while i < np.size(local_min):
                if local_max[i] > local_min[i]:
                    local_min = np.delete(local_min, i)
                    i = 0
                if local_min[i] > local_max[i + 1]:
                    local_min = np.delete()
                    i = 0
                i += 1
        break
    return local_min, local_max
