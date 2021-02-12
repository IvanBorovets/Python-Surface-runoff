import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import time

import interpolation
import optimization
import flooding
import filtration
import evaporation

def graph(data_in_y, data_in_x):
    data_in_y = np.array(list(map(float, data_in_y.split())))
    data_in_x = np.array(list(map(float, data_in_x.split())))

    main_graphic = plt.figure('Test Graphic', figsize=(8, 5))
    ax = plt.subplot()
    main_graphic.subplots_adjust(left=0.07, right=0.96, top=0.95, bottom=0.05)
    ax.plot(data_in_x, data_in_y, '.', markerfacecolor='black', markeredgecolor='black', markersize=7)

    interpolation_function = interpolation.scipy_rbf(data_in_x, data_in_y)
    extreme = optimization.scipy_minimize(interpolation_function)

    ax.plot(np.arange(data_in_x[0], data_in_x[-1], 0.01),
            interpolation_function[0](np.arange(data_in_x[0], data_in_x[-1], 0.01)))

    plt.plot(extreme[0], interpolation_function[0](extreme[0]), 'xg')
    plt.plot(extreme[1], interpolation_function[0](extreme[1]), 'xr')

    plt.ylim((np.array(plt.ylim())[0]-np.array(plt.xlim())[1]*0.05, np.array(plt.xlim())[1]))
    plt.show()
