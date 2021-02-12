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