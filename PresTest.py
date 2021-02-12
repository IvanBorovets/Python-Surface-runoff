import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import time

import interpolation
import optimization
import flooding
import filtration
import evaporation

v = 350.0 / 1000.0

# data_in_y = np.array([1, 1, 0.7507688285032871, 0.9572689686335257, 0.6022617125298197, 0.32973987362833, 0.682238940178396, 1.0])
# data_in_y = np.array([1.1131974649984475, 0.36563599235956334, 0.5372441468814221, 0.7848641394729148, 0.4415514754443455, 0.5014639429399128, 0.9257576256430685, 0.8426941841492848, 0.8454577490569409, 0.969748624279577])
data_in_y = np.array([2.0, 1.3, 0.5507688285032871, 0.9572689686335257, 0.6022617125298197, 0.32973987362833, 0.682238940178396, 1.3, 2.1])
data_in_x = np.linspace(0, np.size(data_in_y), np.size(data_in_y))
data_in_x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
main_graphic = plt.figure('Graphic', figsize=(8, 5))
ax = plt.subplot()
main_graphic.subplots_adjust(left=0.07, right=0.96, top=0.95, bottom=0.05)
ax.plot(data_in_x, data_in_y, '.', markerfacecolor='black', markeredgecolor='black', markersize=7)

interpolation_function = interpolation.scipy_rbf(data_in_x, data_in_y)
extreme = optimization.scipy_minimize(interpolation_function)

ax.plot(np.arange(data_in_x[0], data_in_x[-1], 0.01),
            interpolation_function[0](np.arange(data_in_x[0], data_in_x[-1], 0.01)))

plt.plot(extreme[0], interpolation_function[0](extreme[0]), 'xg')
plt.plot(extreme[1], interpolation_function[0](extreme[1]), 'xr')

areas = flooding.step_by_step_flooding(extreme, interpolation_function, v)


for i in areas:
    plt.plot([i.x_filling_left, i.x_filling_right],
                [interpolation_function[0](i.x_filling_left),
                 interpolation_function[0](i.x_filling_right)], 'b', linewidth=1, color=(0.0, 0.0, 1.0), alpha=0.8)

    # y2 = np.empty(0)
    # for point in np.arange(i.x_filling_left, i.x_filling_right, 0.01):
    #     y2 = np.append(y2, interpolation_function[0](i.x_filling_left))
    # plt.fill_between(np.arange(i.x_filling_left, i.x_filling_right, 0.01),
    #                     interpolation_function[0](np.arange(i.x_filling_left, i.x_filling_right, 0.01)),
    #                     y2,
    #                     color=(0.0, 0.0, 1.0), alpha=0.5)

for area in areas:
    evaporation_rate = evaporation.empiric_evaporation(t = 24, Vb = 4.7, T = 18, u = 50)
    area.S_target -= ((area.x_filling_right - area.x_filling_left) * evaporation_rate) / 734.4
    area.S_fill = 0.0
    area.x_filling_left = area.x_filling_right = area.min
areas = flooding.step_by_step_flooding(extreme, interpolation_function, v, area=areas)

for i in areas:
    plt.plot([i.x_filling_left, i.x_filling_right],
                [interpolation_function[0](i.x_filling_left),
                 interpolation_function[0](i.x_filling_right)], 'g', linewidth=1)
    # y2 = np.empty(0)
    # for point in np.arange(i.x_filling_left, i.x_filling_right, 0.01):
    #     y2 = np.append(y2, interpolation_function[0](i.x_filling_left))
    # plt.fill_between(np.arange(i.x_filling_left, i.x_filling_right, 0.01),
    #                     interpolation_function[0](np.arange(i.x_filling_left, i.x_filling_right, 0.01)),
    #                     y2,
    #                     color=(0.0, 0.0, 1.0), alpha=0.5)

t = 24
filtration_data = []
for area in areas:
    filtration_data.append(filtration.spring_filtering(area, interpolation_function[0], k = 0.18, tm=t))

# def animate(i, filtration_data):
#     lines = []
#     for area in filtration_data:
#         lines.append(ax.plot(area[0][i].flat, interpolation_function[0](area[0][i].flat) + area[1][i].flat, linewidth=1,
#                              color=(1.0, 0.0, 0.0, 0.9))[0])
#     return lines
#
#
#
# anim = animation.FuncAnimation(main_graphic, animate, fargs=(filtration_data,), frames=t - 1, interval=500,
#                                    blit=True, repeat=False)

for area in filtration_data:
    i = 1
    while i < np.size(area):
        if abs(area[0][-1][i]-area[0][-1][i-1]) > abs(area[0][-1][1]-area[0][-1][0])+0.1:
            xr1 = np.copy(area[0][-1][:i])
            xr2 = np.copy(area[0][-1][i:])
            yr1 = np.copy(area[1][-1][:i])
            yr2 = np.copy(area[1][-1][i:])
        i += 1
    try:
        ax.plot(xr1, interpolation_function[0](xr1) + yr1, linewidth=1,
            color=(1.0, 0.0, 0.0, 0.9))
        y2 = np.empty(0)
        if xr1.size == 0:
            continue
        for point in np.linspace(xr1[0], xr1[-1], 1000):
            y2 = np.append(y2, interpolation_function[0](xr1[0]))
        plt.fill_between(np.linspace(xr1[0], xr1[-1], 1000),
                         interpolation_function[0](np.linspace(xr1[0], xr1[-1], 1000)),
                         y2,
                         color=(0.0, 0.0, 1.0), alpha=0.5)
        ax.plot(xr2, interpolation_function[0](xr2) + yr2, linewidth=1,
            color=(1.0, 0.0, 0.0, 0.9))
        y2 = np.empty(0)
        if xr2.size == 0:
            continue
        for point in np.linspace(xr2[0], xr2[-1], 1000):
            y2 = np.append(y2, interpolation_function[0](xr2[0]))
        plt.fill_between(np.linspace(xr2[0], xr2[-1], 1000),
                         interpolation_function[0](np.linspace(xr2[0], xr2[-1], 1000)),
                         y2,
                         color=(0.0, 0.0, 1.0), alpha=0.5)
    except:
        print('ERROR!')
        ax.plot(area[0][-1].flat, interpolation_function[0](area[0][-1].flat) + area[1][-1].flat,
            linewidth=1,
            color=(1.0, 0.0, 0.0, 0.9))
# for i in areas:
#     y2 = np.empty(0)
#     if i.final_x[-1].size == 0:
#         continue
#     for point in np.linspace(i.final_x[-1][0], i.final_x[-1][-1], 1000):
#         y2 = np.append(y2, interpolation_function[0](i.final_x[-1][0]))
#     plt.fill_between(np.linspace(i.final_x[-1][0], i.final_x[-1][-1], 1000),
#                         interpolation_function[0](np.linspace(i.final_x[-1][0], i.final_x[-1][-1], 1000)),
#                         y2,
#                         color=(0.0, 0.0, 1.0), alpha=0.5)

plt.ylim((np.array(plt.ylim())[0], np.array(plt.xlim())[1]))
plt.show()
