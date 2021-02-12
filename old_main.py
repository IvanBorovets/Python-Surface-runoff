import sys

from scipy.optimize import minimize
from scipy.interpolate import Rbf, CubicSpline
from scipy import integrate
from matplotlib import pyplot as plt
import numpy as np


#data_in_Y = np.random.rand(30)*9
#data_in_Y = np.array([1.14, 2.57, 1.80, 0.02, 0.28, 0.24, 1.23, 0.91, 0.58, 1.41])
#data_in_Y = np.array([0.17, 2.1, 2.62, 0.43, 0.72, 2.25, 1.02, 2.72, 1.53, 2.97])
#data_in_Y = np.array([2, 1.8, 1.6, 1.4, 1.2, 1, 1, 1.3, 1.6, 2])
#data_in_Y = np.array([2.79494186, 2.52382158, 1.20701306, 2.39743015, 2.62776144, 2.45370954, 0.50185104, 2.69531928, 1.80515071, 1.00869593])
#data_in_Y = np.array([2.91372804, 1.80949204, 2.10589421, 2.60137063, 2.10389632, 0.76131113, 2.48825884, 1.30512281, 1.36386196, 0.13620369])
#data_in_Y = np.array([0.7964446431657703, 2.942815161298308, 1.20720975440465, 0.8349077869745598, 2.1323699538616867, 0.15267346387598468, 0.8008679445171716, 0.939749819225956, 1.9424069566097735, 2.968112752511759])
#data_in_Y = np.array([0.31717398, 0.66958189, 2.15029997, 0.65312464, 2.76833298, 1.32328608, 2.42244306, 1.41823956, 2.37208415, 1.38580909])
#data_in_Y = np.array([0.3368089,  0.14018586, 1.65930419, 1.2076528,  0.69870003, 2.81409677, 1.82576447, 0.66278039, 2.09698761, 1.37506893])
#data_in_Y = np.array([2.4663246708028828, 6.027260880727679, 6.501422081039556, 6.0882998344628065, 2.4428776831528514, 2.3497372091387216, 2.750464543389156, 0.7824059390733309, 4.414132585872393, 5.74967591509414, 3.9573452094861157, 5.381455512244044, 7.1575408033461, 4.61804477483289, 5.764879693929554, 1.037774799191794, 8.562963573961374, 6.781781919133156, 0.19310524756232372, 8.209719357107883, 7.143584097767553, 1.7776918020008319, 8.323476870613312, 6.700501598622095, 5.6169559650572705, 3.672974501603105, 4.899618442864512, 0.49416439409179136, 8.373317307934807, 6.0744511374327])
data_in_Y = np.array([0.18015079690515057, 0.33162539692726023, 0.1950973171752114, 0.7766202343269035, 0.4409400355890204, 0.6858285847083454, 0.40079429236352626, 0.7411878229883639, 0.12381337347846955, 0.8004619356545113, 0.8004619356545113])

N = np.size(data_in_Y)
data_in_X = np.arange(0, np.size(data_in_Y)*3, 1*3)

print('data_in_Y = np.array([', end='')
for i in data_in_Y:
    print(f'{i}, ', end='')
print('])')

spline = Rbf(data_in_X, data_in_Y)
spline_reverse = Rbf(data_in_X, -data_in_Y)

plt.figure('Main')
dx = np.arange(data_in_X[0], data_in_X[np.size(data_in_X) - 1] + 0.1, 0.01)
plt.plot(data_in_X, data_in_Y, '.', markerfacecolor='black', markeredgecolor='black', markersize=7)
plt.plot(dx, spline(dx))

local_min = np.array([])
local_max = np.array([])

for i in data_in_X:
    temp = minimize(spline, i, method='L-BFGS-B',
                    bounds=((np.min(data_in_X), np.max(data_in_X)),), options={'gtol': 1e-8})
    local_min = np.append(local_min, temp.x)

    temp = minimize(spline_reverse, i, method='L-BFGS-B',
                    bounds=((np.min(data_in_X), np.max(data_in_X)),), options={'gtol': 1e-8})
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
    if local_min[np.size(local_min)-1] > local_max[np.size(local_max)-1]:
        local_min = np.delete(local_min, np.size(local_min)-1)
        continue
    if local_min[0] < local_max[0]:
        local_min = np.delete(local_min, 0)
        if np.size(local_min) == 0:
            print("Minimum not found")
            plt.plot()
            sys.exit()
        continue
    if np.size(local_min) >= np.size(local_max):
        i = 0
        while i < np.size(local_min):
            if local_max[i] > local_min[i]:
                local_min = np.delete(local_min, i)
                i = 0
            if local_min[i] > local_max[i+1]:
                local_min = np.delete()
                i = 0
            i += 1
    break
print(f'max = {local_max}')
print(f'min = {local_min}')

plt.plot(local_min, spline(local_min), 'xg')
plt.plot(local_max, spline(local_max), 'xr')

#=====
class Area:
    filled = False
    x_filling_left = float
    x_filling_right = float
    x_left_max = float
    x_right_max = float
    min = float
    S_fill = 0.0
    S_target = float

    def __init__(self, minimum, x_left_max, x_right_max, S):
        self.min = self.x_filling_left = self.x_filling_right = minimum
        self.x_left_max = x_left_max
        self.x_right_max = x_right_max
        self.S_target = S


def check(iterable):
    for element in iterable:
        if abs(element.S_target - element.S_fill) > precision_S:
            element.filled = False
        if not element.filled:
            return False
    return True

def square(x_left, x_right, spline):
    if abs(x_right - x_left) < 0.05:
        return (abs(area[i].x_filling_right - area[i].x_filling_left) + abs(x_right - x_left))*j*dh*0.5
    else:
        area[i].S_fill
        a = (spline(x_left) - spline(x_right)) / (x_left - x_right)
        #a = 0
        b = spline(x_right) - a * x_right
        def linear(x, a, b):
            return a * x + b
        return integrate.quad(linear, a=x_left, b=x_right, args=(a,b))[0] - integrate.quad(spline, a=x_left, b=x_right)[0]

def balance(area):
    while abs(spline(area.x_filling_right) - spline(area.x_filling_left)) > abs(epsilon):
        if spline(area.x_filling_right) > spline(area.x_filling_left):
            area.x_filling_right -= epsilon/4
        else:
            area.x_filling_right += epsilon/4

plt.show(block=False)
v = 1
dx_max = np.empty(0)
for i in range(0, np.size(local_max)-1, 1):
    dx_max = np.append(dx_max, local_max[i+1] - local_max[i])
S_target = dx_max * v
epsilon = 0.02
precision_S = 0.02
area = np.array([Area(local_min[i], local_max[i], local_max[i+1], S_target[i]) for i in range(np.size(local_min))])
i = 0
while not check(area):
    if i >= np.size(area): i = 0
    dh = (np.minimum(spline(local_max[i]),spline(local_max[i+1])) - spline(local_min[i]))/50
    h = spline(area[i].x_filling_left)
    j = 1
    while True:
        h += dh

        x = x_left = area[i].x_filling_left
        x = x_right = area[i].x_filling_right
        if x <= area[i].x_left_max:
            area[i].filled = True
            area[i].S_target -= (area[i].S_target - area[i].S_fill)
        while x >= area[i].x_left_max and not area[i].filled:
            if abs(spline(x) - h) <= abs(epsilon):
                x_left = x
                break
            else:
                x -= epsilon/4
            if x <= area[i].x_left_max:
                area[i].filled = True
                area[i].x_filling_left = x_left = area[i].x_left_max
                area[i].S_fill = square(x_left, x_right, spline)

                """while abs(spline(area[i].x_filling_right) - spline(area[i].x_filling_left)) > abs(epsilon):
                    if spline(area[i].x_filling_right) > spline(area[i].x_filling_left):
                        area[i].x_filling_right -= epsilon/2
                    else:
                        area[i].x_filling_right += epsilon/2"""

                if i == 0:
                    area[i].S_target -= (area[i].S_target - area[i].S_fill)
                    print('Void on the left')
                    continue
                area[i-1].filled = False
                area[i-1].S_target += (area[i].S_target - area[i].S_fill)
                area[i].S_target -= (area[i].S_target - area[i].S_fill)
                print('Overflow to the left')

        x = x_right = area[i].x_filling_right
        if x >= area[i].x_right_max:
            area[i].filled = True
            area[i].S_target -= (area[i].S_target - area[i].S_fill)
        while x <= area[i].x_right_max and not area[i].filled:
            if abs(spline(x) - h) <= abs(epsilon):
                x_right = x
                break
            else:
                x += epsilon/4
                if abs(x - x_left) > dh:
                    x -= epsilon/4
                    x += epsilon/8
            if x >= area[i].x_right_max:
                area[i].filled = True
                area[i].x_filling_right = x_right = area[i].x_right_max
                area[i].S_fill = square(x_left, x_right, spline)

                #print(f'{spline.solve(spline(area[i].x_right_max))}')
                """while abs(spline(area[i].x_filling_right) - spline(area[i].x_filling_left)) > abs(epsilon):
                    if spline(area[i].x_filling_left) > spline(area[i].x_filling_right):
                        area[i].x_filling_left += epsilon/2
                    else:
                        area[i].x_filling_left -= epsilon/2"""

                if i == np.size(area)-1:
                    area[i].S_target -= (area[i].S_target - area[i].S_fill)
                    print('Void on the right')
                    continue
                area[i+1].filled = False
                area[i+1].S_target += (area[i].S_target - area[i].S_fill)
                area[i].S_target -= (area[i].S_target - area[i].S_fill)
                print('Overflow to the right')

        #balance(area[i])

        area[i].S_fill = square(x_left, x_right, spline)
        if abs(area[i].S_fill - area[i].S_target) < precision_S or area[i].filled:
            area[i].x_filling_right = x_right
            area[i].x_filling_left = x_left
            area[i].filled = True
            plt.plot([area[i].x_filling_left, area[i].x_filling_right],[spline(area[i].x_filling_left),spline(area[i].x_filling_right)], 'b--')
            plt.draw()
            i += 1
            break
        elif abs(area[i].S_fill - area[i].S_target) > precision_S and area[i].S_fill > area[i].S_target:
            h -= dh
            dh /= 2
            j += 1
            continue
        elif abs(area[i].S_fill - area[i].S_target) >= precision_S and area[i].S_fill < area[i].S_target:
            area[i].x_filling_right = x_right
            area[i].x_filling_left = x_left
            plt.plot([area[i].x_filling_left, area[i].x_filling_right],[spline(area[i].x_filling_left),spline(area[i].x_filling_right)], 'b--')
            plt.draw()
            j += 1
            continue
    k = 0
    while k < np.size(area)-1:
        if area[k].x_filling_right == area[k+1].x_filling_left:
            area[k].x_filling_right = area[k+1].x_filling_right
            area[k].x_right_max = area[k+1].x_right_max
            area[k].S_target += area[k+1].S_target
            area = np.delete(area, k+1)
            print(f'{k+1} joining with {k}')
        k += 1


#=====
plt.show()
print('end?')

