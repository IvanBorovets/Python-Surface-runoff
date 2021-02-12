import numpy as np
from scipy import integrate

from inside_class import Area

def step_by_step_flooding(extreme, interpolation_function, v = 1, area = None):
    spline = interpolation_function[0]
    local_min = extreme[0]
    local_max = extreme[1]

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
            b = spline(x_right) - a * x_right
            def linear(x, a, b):
                return a * x + b
            return integrate.quad(linear, a=x_left, b=x_right, args=(a, b), limit=500)[0] - integrate.quad(spline, a=x_left, b=x_right, limit=500)[0]

    dx_max = np.empty(0)
    for i in range(0, np.size(local_max)-1, 1):
        dx_max = np.append(dx_max, local_max[i+1] - local_max[i])
    S_target = dx_max * v
    epsilon = 0.01
    precision_S = abs(interpolation_function[0].xi[0][0] - interpolation_function[0].xi[0][-1])/1000
    if area is None:
        area = np.array([Area(local_min[i], local_max[i], local_max[i+1], S_target[i]) for i in range(np.size(local_min))])
    i = 0
    while not check(area):
        if i >= np.size(area): i = 0
        dh = (np.minimum(spline(area[i].x_left_max), spline(area[i].x_right_max)) - spline(area[i].min))/100
        epsilon = abs((np.minimum(area[i].x_left_max, area[i].x_right_max) - area[i].min)/500)
        h = spline(area[i].x_filling_left)
        j = 1
        while True:
            h += dh

            x = x_left = area[i].x_filling_left
            if x <= area[i].x_left_max:
                area[i].filled = True
                area[i].S_target -= (area[i].S_target - area[i].S_fill)
            while x >= area[i].x_left_max and not area[i].filled:
                if abs(spline(x) - h) <= abs(epsilon):
                    x_left = x
                    break
                else:
                    x -= epsilon/4.0
                if x <= area[i].x_left_max:
                    area[i].filled = True
                    area[i].x_filling_left = x_left = area[i].x_left_max
                    area[i].S_fill = square(x_left, x_right, spline)

                    if i == 0:
                        area[i].S_target -= (area[i].S_target - area[i].S_fill)
                        print('Void on the left')
                        continue
                    area[i-1].filled = False
                    area[i-1].S_target += (area[i].S_target - area[i].S_fill)
                    area[i].S_target -= (area[i].S_target - area[i].S_fill)
                    print(f'Overflow to the left from {i} area')

            x = x_right = area[i].x_filling_right
            if x >= area[i].x_right_max:
                area[i].filled = True
                area[i].S_target -= (area[i].S_target - area[i].S_fill)
            while x <= area[i].x_right_max and not area[i].filled:
                if abs(spline(x) - h) <= abs(epsilon):
                    x_right = x
                    break
                else:
                    x += epsilon/4.0
                if x >= area[i].x_right_max:
                    area[i].filled = True
                    area[i].x_filling_right = x_right = area[i].x_right_max
                    area[i].S_fill = square(x_left, x_right, spline)

                    if i == np.size(area)-1:
                        area[i].S_target -= (area[i].S_target - area[i].S_fill)
                        print('Void on the right')
                        continue
                    area[i+1].filled = False
                    area[i+1].S_target += (area[i].S_target - area[i].S_fill)
                    area[i].S_target -= (area[i].S_target - area[i].S_fill)
                    print(f'Overflow to the right from {i} area')

            area[i].S_fill = square(x_left, x_right, spline)
            if abs(area[i].S_fill - area[i].S_target) < precision_S or area[i].filled:
                area[i].x_filling_right = x_right
                area[i].x_filling_left = x_left
                area[i].filled = True
                # pyplot.plot([area[i].x_filling_left, area[i].x_filling_right],[spline(area[i].x_filling_left),spline(area[i].x_filling_right)], 'b', linewidth=1)
                # pyplot.draw()
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
                # pyplot.plot([area[i].x_filling_left, area[i].x_filling_right],[spline(area[i].x_filling_left),spline(area[i].x_filling_right)], 'b', linewidth=1, alpha=0.3)
                # pyplot.draw()
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

    return area