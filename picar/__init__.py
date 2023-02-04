import picar_4wd as fc
import time
ANGLE_RANGE = 180
STEP = 5
us_step = STEP
angle_distance = [0,0]
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
scan_list = []
SPEED = 1
DIST_TO_TIME = {
    0 : 0,
    1 : 0.06,
    2 : 0.1,
    3 : 0.15,
    4 : 0.17,
    5 : 0.2,
    6 : 0.24,
    7 : 0.29,
    8 : 0.34,
    9 : 0.38,
   10 : 0.42,
   11 : 0.46,
   12 : 0.5,
   13 : 0.54,
   14 : 0.58,
   15 : 0.62,
   16 : 0.66,
   17 : 0.7,
   18 : 0.74,
   19 : 0.78,
   20 : 0.82
}

############# Ultrasonic Sensor #############
def scan_distance():
    '''
    scan_distance:
        obtain a list of distances to obstacles around the car (from left to right)
    '''
    global scan_list, current_angle, us_step
    current_angle += us_step
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    status = fc.get_distance_at(current_angle)#ref1
    scan_list.append(status)
    if current_angle == min_angle or current_angle == max_angle:
        if us_step < 0:
            scan_list.reverse()
        tmp = scan_list.copy()
        scan_list = []
        return tmp
    else:
        return False

################# Motor ###################
def turn_left():
    fc.turn_right(SPEED)
    time.sleep(1.09)
    fc.forward(0)

def turn_right():
    fc.turn_left(SPEED)
    time.sleep(1.16)
    fc.forward(0)

def forward(dist):
    fc.forward(SPEED)
    time.sleep(DIST_TO_TIME[int(dist)])
    fc.forward(0)