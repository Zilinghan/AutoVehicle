import sys
sys.path.append('..')
from picar import (turn_left, turn_right, forward)
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
BASE = 4

class Destination_tracker:
    ''' dist must be > 0
    '''
    def __init__(self, front, left):
        self.front = front
        self.left = left
        self.face = UP

    def turn_left(self):
        temp = self.front
        self.front = self.left
        self.left = -temp
        self.face = (self.face + 1) % BASE
        turn_left()

    def turn_right(self):
        temp = self.front
        self.front = -self.left
        self.left = temp
        self.face = (self.face - 1) % BASE
        turn_right()

    def go_front(self, dist):
        if dist < 0:
            print("dist must be > 0")
        else: 
            if self.face == RIGHT:
                self.turn_left()
            elif self.face == LEFT:
                self.turn_right()
            self.front = self.front - dist
            forward(dist)

    def go_left(self, dist):
        if dist < 0:
            print("dist must be > 0")
        else:
            if self.face == UP:
                self.turn_left()
            elif self.face == DOWN:
                self.turn_right()
            self.front = self.front - dist
            forward(dist)
            
    def go_right(self, dist):
        if dist < 0:
            print("dist must be > 0")
        else:
            if self.face == DOWN:
                self.turn_left()
            elif self.face == UP:
                self.turn_right()
            self.front = self.front - dist
            forward(dist)

    def get_destination(self):
        return (self.front, self.left)

    def reached(self):
        if self.front == 0 and self.left == 0:
            return True
        return False

    def reset_face(self):
        self.face = UP

# dest = Destination_tracker(60, 45)
# print(dest.get_destination())
# print(dest.go_front(20))
# print(dest.go_left(10))
# print(dest.go_right(20))
