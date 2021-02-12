import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import time

import interpolation
import optimization
import flooding
import filtration
import evaporation


def calculate(data_in_y, data_in_x, t, v,
              check_evaporation, temperature, wind, moisture,
              check_filtartion, k, u, extended=None):

    def draw_line(a1, a2, color=None, linewidth=1):
        plt.plot(a1, a2, linewidth=linewidth, color=color)

    def draw_fill(xr1):
        y2 = np.empty(0)
        if xr1.size == 0:
            return
        for point in np.linspace(xr1[0], xr1[-1], 1000):
            y2 = np.append(y2, interpolation_function[0](xr1[0]))
        plt.fill_between(np.linspace(xr1[0], xr1[-1], 1000),
                         interpolation_function[0](np.linspace(xr1[0], xr1[-1], 1000)),
                         y2,
                         color=(0.0, 0.0, 1.0), alpha=0.6)

    def draw_filtration_data(xr, yr):
        color = (0.3, 0.0, 0.5, 0.8)
        xr1 = None
        i = 1
        while i < np.size(xr):
            if abs(xr[i] - xr[i - 1]) > abs(xr[1] - xr[0]) + 0.1:
                xr1 = xr[:i]
                xr2 = xr[i:]
                yr1 = yr[:i]
                yr2 = yr[i:]
                draw_filtration_data(xr2, yr2)
            i += 1
        if xr1 is None:
            xr1 = xr[:]
            yr1 = yr[:]
        draw_line(xr1, interpolation_function[0](xr1) + yr1, color=color)
        draw_fill(xr1)

    data_in_y = np.array(list(map(float, data_in_y.split())))
    data_in_x = np.array(list(map(float, data_in_x.split())))
    t = float(t)
    v = float(v) / 1000.0
    temperature = float(temperature)
    wind = float(wind)
    moisture = float(moisture)
    k = float(k)
    u = float(u)
    if extended:
        if len(extended[0]) >= 0:
            tau = float(extended[0])
        else:
            tau = 1.0 / 24.0
        if len(extended[1]) >= 0:
            intervals = int(extended[1])
        else:
            intervals = 100
        if len(extended[2]) >= 0:
            intervals_down = int(extended[2])
        else:
            intervals_down = 200
        if len(extended[3]) >= 0:
            hy = float(extended[3])
        else:
            hy = 1
    else:
        tau = 1.0 / 24.0
        intervals = 100
        intervals_down = 200
        hy = 1

    main_graphic = plt.figure('Graphic', figsize=(8, 5))
    ax = plt.subplot()
    main_graphic.subplots_adjust(left=0.07, right=0.96, top=0.95, bottom=0.05)
    ax.plot(data_in_x, data_in_y, '.', markerfacecolor='black', markeredgecolor='black', markersize=7)

    interpolation_function = interpolation.scipy_rbf(data_in_x, data_in_y)
    extreme = optimization.scipy_minimize(interpolation_function)

    draw_line(np.arange(data_in_x[0], data_in_x[-1], 0.01),
            interpolation_function[0](np.arange(data_in_x[0], data_in_x[-1], 0.01)))

    plt.plot(extreme[0], interpolation_function[0](extreme[0]), 'xg')
    plt.plot(extreme[1], interpolation_function[0](extreme[1]), 'xr')

    areas = flooding.step_by_step_flooding(extreme, interpolation_function, v)

    for area in areas:
        draw_line([area.x_filling_left, area.x_filling_right],
                  [interpolation_function[0](area.x_filling_left),
                   interpolation_function[0](area.x_filling_right)], color=(0.0, 0.0, 1.0, 0.4))

    if check_evaporation:
        for area in areas:
            evaporation_rate = evaporation.empiric_evaporation(t=t, Vb=wind, T=temperature, u=moisture)
            area.S_target -= ((area.x_filling_right - area.x_filling_left) * evaporation_rate) / (30.0 / tau)
            area.S_fill = 0.0
            area.x_filling_left = area.x_filling_right = area.min
        areas = flooding.step_by_step_flooding(extreme, interpolation_function, v, area=areas)
        for area in areas:
            draw_line([area.x_filling_left, area.x_filling_right],
                      [interpolation_function[0](area.x_filling_left),
                       interpolation_function[0](area.x_filling_right)], color=(0.0, 0.0, 1.0, 0.8))

    if check_filtartion:
        filtration_data = []
        for area in areas:
            filtration_data.append(filtration.spring_filtering(area, interpolation_function[0],
                                                               k=k, mu=u, tm=t, tau=tau, hy=hy,
                                                               intervals=intervals,
                                                               intervals_down=intervals_down))
        for area in filtration_data:
            xr = area[0][-1][:]
            yr = area[1][-1][:]
            draw_filtration_data(xr, yr)

    plt.ylim((np.array(plt.ylim())[0]-np.array(plt.xlim())[1]*0.05, np.array(plt.xlim())[1]))
    plt.show()


