import cv2
import time
import argparse
import picar_4wd as fc
from map.map import CarMap
from detection.detect import detect
from detection.utils import detection2names
from navigation.astar import Navigator
from picar import (scan_distance, turn_left, turn_right, forward)
from utils.timer import Timer
from utils.dest import Destination_tracker

def main(args):
    cap = cv2.VideoCapture(args.cameraId)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.frameWidth)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.frameHeight)
    cur_dest = Destination_tracker(args.front_dist, args.left_dist)
    first = True
    stop_sign_checked = False
    while True:
        # Obtain the scanned list of distances to obstacles
        scan_list = scan_distance()
        if not scan_list:
            continue
        if first:
            first = False
            continue
        for i in range(len(scan_list)):
            scan_list[i] = scan_list[i] if scan_list[i] != -2 else 1000

        # Generate the map from the scanned list
        carmap = CarMap()
        carmap.constructMap(scan_list)
        carmap.extendMap(width=5)
        # carmap.printMap()

        # Obtain the route to the destination in the current iteration
        navigator = Navigator(carmap.getMap(), carmap.getSource(), cur_dest.get_destination())
        route = navigator.getRoute()
        cur_dest.reset_face()   # reset face after routing
        # print("route is", route)
        # navigator.plotRoute()
        
        # Open camera to see things
        while cap.isOpened():
            # capture an image
            success, image = cap.read()
            if not success:
                sys.exit(
                    'ERROR: Unable to read from webcam. Please verify your webcam settings.'
                )
            # detect the image
            detection_result = detect(image)
            detection_classes = list(detection2names(detection_result))
            # check persons and stop sign
            if 'person' in detection_classes:
                print("Person detected, wait!")
                continue
            elif 'stop sign' in detection_classes and (not stop_sign_checked):
                print("Stop sign detected, stop!")
                time.sleep(5)
                stop_sign_checked = True
                continue
            else:
                break
        if route is None:
            if cur_dest.get_destination()[1] > 0:
                go('L', 0, 0, cur_dest)
            else:
                go('R', 0, 0, cur_dest)
            continue

        # follow the route by at most 20 cm
        left_dist = 20
        for r in route:
            if left_dist == 0:
                break
            left_dist = go(r[0], r[1], left_dist, cur_dest)

        if cur_dest.reached():
            break

        
def go(dir, dist, left_dist, dest):
    dist_togo = min(left_dist, dist)
    left_dist = left_dist - dist_togo

    if dir == 'U':
        dest.go_front(dist_togo)

    elif dir == 'L':
        dest.go_left(dist_togo)
        
    elif dir == 'R':
        dest.go_right(dist_togo)

    return left_dist
        


########### Input Arguments ############        
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '--cameraId', 
    help='Id of camera.', 
    required=False, 
    type=int, 
    default=0)
parser.add_argument(
    '--frameWidth',
    help='Width of frame to capture from camera.',
    required=False,
    type=int,
    default=640)
parser.add_argument(
    '--frameHeight',
    help='Height of frame to capture from camera.',
    required=False,
    type=int,
    default=480)
parser.add_argument(
    '--left_dist',
    help='Distance to the destination to the left in cm',
    type=int,
    required=False,
    default=100
)
parser.add_argument(
    '--front_dist',
    help='Distance to the destination in the front in cm',
    type=int,
    required=False,
    default=100
)

args = parser.parse_args()

if __name__ == "__main__":
    try: 
        main(args)
    finally: 
        fc.stop()

