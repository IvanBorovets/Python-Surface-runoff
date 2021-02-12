import numpy as np


def spring_filtering(area, spline, tm = 5, k = 0.09, mu = 0.0002, hy = 1, tau =1.0 / 24.0, intervals = 100, intervals_down = 10):
    points_x = np.linspace(area.x_filling_left, area.x_filling_right, intervals)
    h = np.zeros((intervals_down, points_x.size))

    for i in np.arange(0, np.size(h[0])):
        h[0, i] = spline(area.x_filling_left) - spline(points_x[i])

    a = np.linspace(1, 10, intervals_down)
    i = 0
    while i < np.size(h[0]):
        if h[0, i] <= 0:
            h = np.delete(h, i, 1)
            points_x = np.delete(points_x, i)
            continue
        j = 1
        while j < np.size(a):
            h[j, i] = -a[j]
            j += 1
        i += 1


    a = b = k * tau
    c = 2 * tau * k + mu * hy ** 2

    alpha = np.array([0])
    beta = np.zeros((intervals_down, points_x.size))

    i = 1
    while i < np.size(h, 0):
        alpha = np.append(alpha, b / (c - a * alpha[i - 1]))
        i += 1

    area.final_h = []
    area.final_x = []
    t = 0
    while t < tm:
        i = 0
        while i < np.size(h[0]):
            if h[0, i] <= 0:
                h = np.delete(h, i, 1)
                points_x = np.delete(points_x, i)
                continue
            else:
                i += 1

        i = 0
        while i < np.size(h, 1):
            beta[0, i] = h[0, i]
            j = 1
            while j < np.size(h, 0):
                beta[j, i] = (a * beta[j - 1, i] + mu * h[j, i] * hy ** 2) / (c - a * alpha[j - 1])
                j += 1
            i += 1

        h_n = np.zeros((intervals_down, points_x.size))
        i = 0
        while i < np.size(h, 1):
            h_n[-1, i] = beta[-1, i] / (1 - alpha[-1])
            i += 1

        i = 0
        while i < np.size(h, 1):
            j = np.size(h, 0) - 2
            while j >= 0:
                h_n[j, i] = alpha[j] * h_n[j + 1, i] + beta[j, i]
                j -= 1
            i += 1

        q = np.zeros((intervals_down, points_x.size))
        i = 1
        while i < np.size(h, 0):
            j = 0
            while j < np.size(h, 1):
                q[i, j] = k * (h_n[i, j] - h[i, j]) / hy
                j += 1
            i += 1

        i = 0
        while i < np.size(h, 1):
            h_n[0, i] = h[0, i] - np.sum(q[:, i]) * tau
            i += 1
        h = np.copy(h_n)
        area.final_h.append(h_n[0, :])
        area.final_x.append(points_x)
        t += 1

    return [area.final_x, area.final_h]
