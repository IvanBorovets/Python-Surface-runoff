import numpy as np
from matplotlib import pyplot as plt
import time

import interpolation
import optimization
import flooding
import filtration

start_time = int(round(time.time() * 1000))

coef = 1
v = 5
# data_in_y = np.random.rand(10*coef)*coef*2
#data_in_y = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.45, 0.37, 0.3, 0.2, 0.1])
#data_in_y = np.array([1.1269689862619268, 1.5431244584800168, 0.8370225833975262, 0.5173791781536476, 1.1110267069859034, 1.0987147224051177, 0.07785358093265105, 0.38396909784135635, 1.8503065187093963, 1.4974254812592123])
data_in_y = np.array([12, 10, 9, 7, 5, 3, 5, 7, 8, 8, 7, 5, 4, 3, 2, 1, 5, 7, 9, 12])

data_in_x = np.arange(0, np.size(data_in_y), 1)

print('data_in_y = np.array([', end='')
i = 0
while i < np.size(data_in_y)-1:
    print(f'{data_in_y[i]}, ', end='')
    i += 1
print(f'{data_in_y[i]}])')

interpolation_function = interpolation.scipy_rbf(data_in_x, data_in_y)
extreme = optimization.scipy_minimize(interpolation_function)

print(f'max = {extreme[1]}')
print(f'min = {extreme[0]}')

main_graphic = plt.figure('Graphic')
main_graphic.subplots_adjust(left=0.07, right=0.96, top=0.95, bottom=0.05)
plt.plot(data_in_x, data_in_y, '.', markerfacecolor='black', markeredgecolor='black', markersize=7)
plt.plot(np.arange(data_in_x[0], data_in_x[-1], 0.01),
            interpolation_function[0](np.arange(data_in_x[0], data_in_x[-1], 0.01)))
plt.plot(extreme[0], interpolation_function[0](extreme[0]), 'xg')
plt.plot(extreme[1], interpolation_function[0](extreme[1]), 'xr')

areas = flooding.step_by_step_flooding(extreme, interpolation_function, v)

for i in areas:
    plt.plot([i.x_filling_left, i.x_filling_right],
                [interpolation_function[0](i.x_filling_left),
                 interpolation_function[0](i.x_filling_right)], 'b', linewidth=1)

    y2 = np.empty(0)
    for point in np.arange(i.x_filling_left, i.x_filling_right, 0.01):
        y2 = np.append(y2, interpolation_function[0](i.x_filling_left))
    plt.fill_between(np.arange(i.x_filling_left, i.x_filling_right, 0.01),
                        interpolation_function[0](np.arange(i.x_filling_left, i.x_filling_right, 0.01)),
                        y2,
                        color=(0, 0, 1), alpha=0.4)
plt.ylim(plt.xlim())
print(f'Your code like shit did the task in: {(int(round(time.time() * 1000)) - start_time)/1000:.2f} seconds')
# %%
# def spring_filtering(area, spline):
area = areas[0]
spline = interpolation_function[0]
intervals = 1000
intervals_down = int(intervals / 100)
points_x = np.linspace(area.x_filling_left, area.x_filling_right, intervals)
h = np.zeros( (intervals_down, points_x.size ))

for i in np.arange(0, np.size(h[0])):
    h[0, i] = spline(area.x_filling_left) - spline(points_x[i])

a = np.linspace(0, spline(area.x_filling_left) - spline(area.min), intervals_down)
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

k = 0.09
mu = 0.0002
tau = 1.0/24.0
#hx = a[1]
hx = 0.5
a = b = k * tau
c = 2 * tau * k + mu * hx ** 2

alpha = np.array([0])
beta = np.zeros( (intervals_down, points_x.size ))

i = 1
while i < np.size(h, 0):
    alpha = np.append(alpha, b / (c - a * alpha[i-1]))
    i += 1

i = 0
while i < np.size(h, 1):
    beta[0, i] = h[0, i]
    j = 1
    while j < np.size(h, 0):
        beta[j, i] = (a * beta[j - 1, i] + mu * h[j, i] * hx ** 2) / (c - a * alpha[j - 1])
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
        q[i, j] = k * (h_n[i, j] - h[i, j]) / hx
        j += 1
    i += 1

i = 0
while i < np.size(h, 1):
    h_n[0, i] = h[0, i] - np.sum(q[:, i]) * tau
    i += 1
# input('Press <ENTER> to continue')
#%%
plt.plot(points_x, spline(points_x) + h_n[0, :], color=(1.0, 0.0, 0.0, 0.7))

plt.show()
print(f'End.')