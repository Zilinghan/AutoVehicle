import picar_4wd as fc
import time
speed = 1

def turn_left():
    fc.turn_right(speed)
    time.sleep(1.09)
    fc.forward(0)

def turn_right():
    fc.turn_left(speed)
    time.sleep(1.16)
    fc.forward(0)

# turn_left()
turn_right()
# fc.forward(speed)
# time.sleep(0.62)
# fc.forward(0)