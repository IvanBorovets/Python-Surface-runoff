from scipy.interpolate import Rbf


def scipy_rbf(data_in_x, data_in_y):
    spline = Rbf(data_in_x, data_in_y, function='thin-plate')
    spline_reverse = Rbf(data_in_x, -data_in_y, function='thin-plate')
    return spline, spline_reverse

