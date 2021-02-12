import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import time

import interpolation
import optimization
import flooding
import filtration
import evaporation

start_time = int(round(time.time() * 1000))

coef = 1
v = 150.0 / 1000.0
data_in_y = np.random.rand(10*coef)*coef
# data_in_y = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.45, 0.37, 0.3, 0.2, 0.1])
# data_in_y = np.array([1.1269689862619268, 1.5431244584800168, 0.8370225833975262, 0.5173791781536476, 1.1110267069859034, 1.0987147224051177, 0.07785358093265105, 0.38396909784135635, 1.8503065187093963, 1.4974254812592123])
# data_in_y = np.array([12, 10, 9, 7, 5, 3, 5, 7, 8, 8, 7, 5, 4, 3, 2, 1, 5, 7, 9, 12])
# data_in_y = np.array([1.4043782231702724, 1.876229958468473, 1.7953668264167575, 1.8237145453712675, 1.3839047211675757, 1.2561772354593446, 0.25311861228619015, 0.5662674787064741, 0.6997181450116798, 1.9180196257898818])
# data_in_y = np.array([1.5106808893128956, 0.8568454221184931, 0.1607688285032871, 1.5572689686335257, 0.7622617125298197, 1.262973987362833, 0.8892238940178396, 0.1372770473913436, 0.9164959058329247, 0.17419591945096125])
data_in_x = np.linspace(0, np.size(data_in_y), np.size(data_in_y))

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
ax = plt.subplot()
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
                 interpolation_function[0](i.x_filling_right)], 'b', linewidth=1, color=(0.0, 0.0, 1.0), alpha=0.8)

    # y2 = np.empty(0)
    # for point in np.arange(i.x_filling_left, i.x_filling_right, 0.01):
    #     y2 = np.append(y2, interpolation_function[0](i.x_filling_left))
    # plt.fill_between(np.arange(i.x_filling_left, i.x_filling_right, 0.01),
    #                     interpolation_function[0](np.arange(i.x_filling_left, i.x_filling_right, 0.01)),
    #                     y2,
    #                     color=(0.0, 0.0, 1.0), alpha=0.5)

plt.ylim(plt.xlim())
print(f'Your code like shit did the task in: {(int(round(time.time() * 1000)) - start_time)/1000:.2f} seconds')
t = 24

for area in areas:
    evaporation_rate = evaporation.empiric_evaporation(t = t, Vb = 4.7, T = 18, u = 50)
    area.S_target -= ((area.x_filling_right - area.x_filling_left) * evaporation_rate) / 734.4
    area.S_fill = 0.0
    area.x_filling_left = area.x_filling_right = area.min
areas = flooding.step_by_step_flooding(extreme, interpolation_function, v, area=areas)

for i in areas:
    plt.plot([i.x_filling_left, i.x_filling_right],
                [interpolation_function[0](i.x_filling_left),
                 interpolation_function[0](i.x_filling_right)], 'g', linewidth=1)
#
#     y2 = np.empty(0)
#     for point in np.arange(i.x_filling_left, i.x_filling_right, 0.01):
#         y2 = np.append(y2, interpolation_function[0](i.x_filling_left))
#     plt.fill_between(np.arange(i.x_filling_left, i.x_filling_right, 0.01),
#                         interpolation_function[0](np.arange(i.x_filling_left, i.x_filling_right, 0.01)),
#                         y2,
#                         color=(0.0, 1.0, 0.0), alpha=0.4)

filtration_data = []
for area in areas:
    filtration_data.append(filtration.spring_filtering(area, interpolation_function[0], tm=t))


# def animate(i, filtration_data):
#     lines = []
#     for area in filtration_data:
#         lines.append(ax.plot(area[0][i].flat, interpolation_function[0](area[0][i].flat) + area[1][i].flat, linewidth=1,
#                              color=(1.0, 0.0, 0.0, 0.9))[0])
#     return lines
#
# anim = animation.FuncAnimation(main_graphic, animate, fargs=(filtration_data,), frames=t - 1, interval=500,
#                                    blit=True, repeat=False)

for area in filtration_data:
    ax.plot(area[0][-1].flat, interpolation_function[0](area[0][-1].flat) + area[1][-1].flat, linewidth=1,
            color=(1.0, 0.0, 0.0, 0.9))
for i in areas:
    y2 = np.empty(0)
    if i.final_x[-1].size == 0:
        continue
    for point in np.linspace(i.final_x[-1][0], i.final_x[-1][-1], 1000):
        y2 = np.append(y2, interpolation_function[0](i.final_x[-1][0]))
    plt.fill_between(np.linspace(i.final_x[-1][0], i.final_x[-1][-1], 1000),
                        interpolation_function[0](np.linspace(i.final_x[-1][0], i.final_x[-1][-1], 1000)),
                        y2,
                        color=(0.0, 0.0, 1.0), alpha=0.5)

print(f'Your code like shit did the second task in: {(int(round(time.time() * 1000)) - start_time)/1000:.2f} seconds')
plt.show()
print(f'End.')
