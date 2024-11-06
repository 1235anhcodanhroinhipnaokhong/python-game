import math
from typing import Tuple, Optional, List

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)



def liang_barsky(rect: Tuple[float, float, float, float], 
                 line_start: Tuple[float, float], 
                 line_end: Tuple[float, float]) -> Optional[List[Tuple[float, float]]]:
    x_min, y_min, x_max, y_max = rect
    x1, y1 = line_start
    x2, y2 = line_end

    dx = x2 - x1
    dy = y2 - y1

    p = [-dx, dx, -dy, dy]
    q = [x1 - x_min, x_max - x1, y1 - y_min, y_max - y1]

    u1, u2 = 0.0, 1.0 

    for i in range(4):
        if p[i] == 0: 
            if q[i] < 0:
                return None  
        else:
            u = q[i] / p[i]
            if p[i] < 0:
                u1 = max(u1, u)
            else:
                u2 = min(u2, u) 

    if u1 > u2:
        return None  
    clipped_points = (x1 + u1 * dx, y1 + u1 * dy)
    return clipped_points


class TimerCallback:
    def __init__(self, delay_time, call_back_func):
        self.delay_time = delay_time
        self.time_cnt = delay_time
        self.call_back_func = call_back_func
        self.done = False
        self.finished = True
    
    def count_down(self, amount):
        self.finished = False
        self.time_cnt -= amount
        if self.time_cnt <= 0:
            self.finished = True
            self.call_back_func()
            self.done = True
            self.time_cnt = self.delay_time
    
    def first_finished(self):
        if self.done:
            self.done = False
            return True
        return False        