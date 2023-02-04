from heapq import heappop, heappush
import matplotlib.pyplot as plt

'''
Reference: https://codereview.stackexchange.com/questions/208311/python-a-star-with-fewest-turns-and-shortest-path-variations
'''

class AStar(object):

    def __init__(self, start_pos: tuple, end_pos: tuple, grid: list):
        """Instantiate AStar object.

        start_pos and end_pos are tuples of coordinates.
        (0, 2), (0, 4)

        grid is a np.array where 1 indicates a barrier.

        :param start_pos: Coordinates of start position.
        :param end_pos: Coordinates of end position.
        :param grid: List containing square grid of strings with 'x' denoting barriers.
        """
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.grid = grid

class MinTurns(AStar):

    """A star algorithm for navigating a map in the fewest turns.

    Given start and end points for a grid style maze, outputs a tuple containing; a list of coordinates of the turning points.

    """

    def find_neighbors(self, curr_pos: tuple, prev_pos: tuple) -> list:
        """Finds neighbors of curr_pos.

        Adds coordinates of neighbors to list along with boolean(is_turn) representing whether a turn occurs to reach
        the neighbor given path from prev_pos to curr_pos.

        :param curr_pos: curr_pos of self.search().
        :param prev_pos: position prior to curr_pos.
        :return: list of tuples [((pos of neighbor), is_turn)].
        """
        limit = len(self.grid) - 1
        neighbors = []
        # Check each position adjacent to curr_pos.
        for y, x in zip([0, -1, 0, 1], [1, 0, -1, 0]):
            # If adjacent position is outside of grid, skip it.
            if (curr_pos[0] + y) > limit or (curr_pos[0] + y) < 0 or (curr_pos[1] + x) > limit or (curr_pos[1] + x) < 0:
                continue
            # If adjacent position is a barrier, skip it.
            if self.grid[curr_pos[0] + y][curr_pos[1] + x] == 1:
                continue
            else:
                # Ensure we do not count a first step as a turn.
                if curr_pos == self.start_pos:
                    is_turn = False
                else:
                    # Determine direction from prev_pos to curr_pos.
                    if curr_pos != prev_pos[1] and curr_pos[0] == prev_pos[1][0]:
                        direction = 'horizontal'
                    else:
                        direction = 'vertical'

                    # Determine movement from curr_pos to new position.
                    if y != 0:
                        movement = 'vertical'
                    else:
                        movement = 'horizontal'

                    # If we're not still moving in the same direction, we have turned.
                    is_turn = not (movement == direction)
                neighbors.append(((curr_pos[0] + y, curr_pos[1] + x), is_turn))
        return neighbors

    def make_path(self, curr_pos: tuple, route: dict) -> tuple:
        """Creates list of coordinates representing turns in path.

        :param curr_pos: end point of path.
        :param route: dict of coordinates leading to curr_pos
        :return: tuple containing list of coordinates of turns, len(list of coordinates)
        """
        turn_coords = []
        x, path_length = 0, 1
        prev_pos = curr_pos

        if route.get(self.end_pos) is None:
            return None

        while route[curr_pos] is not None:
            curr_pos = route[curr_pos][1]

            if curr_pos[x] != prev_pos[x]:
                if x == 0:
                    x = 1
                else:
                    x = 0

                if prev_pos is not self.end_pos:
                    turn_coords.append(prev_pos)

            prev_pos = curr_pos
            path_length += 1

        turn_coords.append(self.start_pos)
        turn_coords.reverse()
        turn_coords.append(self.end_pos)
        return turn_coords

    def search(self):
        """Finds path through self.grid in fewest number of turns.

        Uses a priority queue to sort nodes by least number of turns required to reach it.
        Continually updates number of turns needed to reach any given position if a better path is found.

        :return: self.make_path().
        """
        # Keep track of where we've been.
        visited = set()

        # We'll keep track of the route and the number of turns to reach the curr_pos with a dict.
        # {(position): (turns_count, (previous-position))}
        route = {self.start_pos: None}

        # turn_count is used to promote routes with fewer turns.
        turn_count = {self.start_pos: 0}

        open_pos = []
        heappush(open_pos, (0, self.start_pos))

        while open_pos:
            # Routes with fewest turns_so_far are up first in the priority queue.
            turns_so_far, curr_pos = heappop(open_pos)

            if curr_pos in visited:
                continue

            prev = route[curr_pos]  # Always remember where you came from so we know if we've turned.
            visited.add(curr_pos)  # But keep moving forward. Never go back!

            neighbors_list = self.find_neighbors(curr_pos, prev)
            for pos, did_turn in neighbors_list:
                if pos in visited:
                    continue

                if turn_count.get(pos):  # Have we been here before?
                    # If so, lets update our turn_count with the route containing the fewest turns.
                    turn_count[pos] = min(turn_count[pos], turns_so_far + int(did_turn))
                else:
                    turn_count[pos] = turns_so_far + int(did_turn)

                # In any case add this place to the list of places to explore.
                heappush(open_pos, (turn_count[pos], pos))

                old_route = route.get(pos)  # Do we know of another way to get here?
                # If so, does the old_route take more turns than the current route to get to pos?
                if old_route and turn_count[pos] < old_route[0]:
                    # If pos can be reached in fewer turns by the current route, we overwrite the old route.
                    route[pos] = (turn_count[pos], curr_pos)
                if not old_route:
                    route[pos] = (turn_count[pos], curr_pos)

        # Wait until open_pos is exhausted to ensure a shorter path doesn't end our search prematurely.
        return self.make_path(self.end_pos, route)

class Navigator:
    def __init__(self, map, source, direction) -> None:
        '''
        :param map: a numpy array
        :param direction: a length-2 tuple (front, left): the distance to go front, and the distance
                        to go left. Negative values represent go back and right respectively.
        '''
        self.map = map
        self.mapsize = self.map.shape[0]
        self.direction = direction
        self.source = source
        self.destination = self.__getDestination(source, direction)
        self.path = None

    def __getDestination(self, source, direction):
        x, y = source
        up, left = direction
        if up < 0:
            self.destination = None
            return
        y = min(up+y, self.mapsize-1)
        x = min(max(x - left, 0), self.mapsize-1)
        return (x, y)

    def getRoute(self):
        if self.destination is None:
            if self.direction[1] >= 0:
                return [('L', 0)]
            else:
                return [('R', 0)]
        self.path = MinTurns(self.source, self.destination, self.map).search()
        if self.path is None:
            return None
        route = []
        for i in range(0, len(self.path) - 1):
            curr_point = self.path[i]
            next_point = self.path[i+1]
            if curr_point[0] == next_point[0]:
                if curr_point[1] < next_point[1]:
                    route.append(('U', next_point[1]-curr_point[1]))
                else:
                    route.append(('D', curr_point[1]-next_point[1]))
            elif curr_point[1] == next_point[1]:
                if curr_point[0] < next_point[0]:
                    route.append(('R', next_point[0]-curr_point[0]))
                else:
                    route.append(('L', curr_point[0]-next_point[0]))
        return route

    def plotRoute(self):
        print(self.path)
        if self.path is None:
            return None
        for i in range(len(self.path)-1):
            curr_point = self.path[i]
            next_point = self.path[i+1]
            if curr_point[0] == next_point[0]:
                for j in range(min(curr_point[1], next_point[1]), max(curr_point[1], next_point[1])+1):
                    self.map[curr_point[0]][j] = 2
            else:
                for j in range(min(curr_point[0], next_point[0]), max(curr_point[0], next_point[0])+1):
                    self.map[j][curr_point[1]] = 2        
        plt.imshow(self.map)
        plt.show()

