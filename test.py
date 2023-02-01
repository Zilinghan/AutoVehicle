import picar_4wd as fc
from map.map import CarMap
from navigation.astar import Navigator
ANGLE_RANGE = 180
STEP = 18
us_step = STEP
angle_distance = [0,0]
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
scan_list = []

def scan_distance():
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
            # print("reverse")
            scan_list.reverse()
        # print(scan_list)
        tmp = scan_list.copy()
        scan_list = []
        return tmp
    else:
        return False


def main():
    first = True
    while True:
        scan_list = scan_distance()
        if not scan_list:
            continue
        if first:
            first = False
            continue
        for i in range(len(scan_list)):
            scan_list[i] = scan_list[i] if scan_list[i] != -2 else 1000
        carmap = CarMap()
        carmap.constructMap(scan_list)
        carmap.printMap()

        

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()

