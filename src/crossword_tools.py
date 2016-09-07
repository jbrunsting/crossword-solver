'''
Created on Sep 6, 2016

@author: Jacob Brunsting
'''

import copy

DIR_DOWN = 0
DIR_RIGHT = 1

# external

class Puzzle(object):   
    LINE_DIR_DOWN = DIR_DOWN
    LINE_DIR_RIGHT = DIR_RIGHT
    
    def __init__(self):
        self.lines = {}
    
    # length and id are integers, direction is either LINE_DIR_DOWN or 
    # LINE_DIR_RIGHT, intersection_points is a list of IntersectionPoint objects
    def add_line(self, length, direction, intersection_points, line_id):
        new_line = CrosswordLine(length, direction, intersection_points)
        self.lines[line_id] = new_line
        
    def words_fit(self, first_id, first_word, second_id, second_word):
        if first_id not in self.lines:
            return True
        
        for intersection in self.lines[first_id].intersection_points:
            if (intersection.second_id == second_id and
                not intersection.words_fit(first_word, second_word)):
                return False
            
        return True
    
    class IntersectionPoint(object):
    
        # first_id, second_id, first_intersect, and second_intersect must all be
        # integers
        def __init__(self, first_id, second_id, first_intersect, second_intersect):
            self.first_id = first_id
            self.second_id = second_id
            self.first_intersect = first_intersect
            self.second_intersect = second_intersect
        
        # first_word and second_word must both be strings
        # returns true if first_word and second_word have identical values at
        # their intersection points
        def words_fit(self, first_word, second_word):
            return (first_word[self.first_intersect]
                 == first_word[self.second_intersect])

# TODO: Allow for a solutions field, that takes each word and puts it in the 
# position with the corresponding ID
def print_puzzle(puzzle):
    FILLED = '#'
    
    standalone_lines = []
    
    lines = copy.deepcopy(puzzle.lines)
    if not lines:
        return
    
    while lines.keys():
        print_values_map = CoordMap()
        current_key = list(lines.keys())[0]
        current_val = lines[current_key]
        lines = add_line_to_coordmap(print_values_map, 0, 0, current_val, current_key, lines)
        print_coord_map(print_values_map, 1, ' ')

# internal

def print_coord_map(coordmap, border, empty_char):
    minx = coordmap.get_min_x()
    miny = coordmap.get_min_y()
    maxx = coordmap.get_max_x()
    maxy = coordmap.get_max_y()
    
    if minx == None or maxx == None:
        minx = 0
        maxx = 0
    if miny == None or maxy == None:
        miny = 0
        maxy = 0
    
    coordmap.shift_x(-minx)
    coordmap.shift_y(-miny)
    map_width = maxx + 1
    map_height = maxy + 1
    for y in range(map_height + 2 * border):
        for x in range(map_width + 2 * border):
            if (x < border or y < border or 
                x >= map_width + border or y >= map_height + border):
                print(empty_char, end="")
            else:
                val = coordmap.get_val(x - border, y - border)
                if val == None:
                    print(empty_char, end="")
                else:
                    print(val, end="")
        print("")

# returns the list of lines with the lines that were added removed
def add_line_to_coordmap(coordmap, x, y, line, line_id, lines):
    FILLED = '#'
    
    print_line = [FILLED for i in range(line.length)]
    coordmap.add_line(line.direction, x, y, print_line)
    
    line_intersection_points = line.intersection_points
    line_direction = line.direction
    for intersection in line_intersection_points:
        newline_x = x
        newline_y = y
        
        if line_direction == Puzzle.LINE_DIR_DOWN:
            newline_y = newline_y + intersection.first_intersect
        else:
            newline_x = newline_x + intersection.first_intersect
        
        intersected_id = intersection.second_id
        if intersected_id not in lines:
            continue
        
        intersected_line = lines[intersected_id]
        
        if intersected_line == None:
            continue
        
        if intersected_line.direction == Puzzle.LINE_DIR_DOWN:
            newline_y = newline_y - intersection.second_intersect
        else:
            newline_x = newline_x - intersection.first_intersect
        
        lines = add_line_to_coordmap(coordmap, newline_x, newline_y, intersected_line, intersected_id, lines)
    
    del lines[line_id]
    return lines

class CrosswordLine(object):    
    # length, direction, and id must all be integers. intersection_points
    # must be a list of IntersectionPoint objects
    def __init__(self, length, direction, intersection_points):
        self.length = length
        self.direction = direction
        self.intersection_points = intersection_points
        
class CoordMap(object):
    
    def __init__(self):
        self._coord_map = {}
        self._x_shift = 0
        self._y_shift = 0
    
    def set_val(self, x, y, val):
        x = x - self._x_shift
        y = y - self._y_shift
        if x in self._coord_map:
            self._coord_map[x][y] = val
        else:
            self._coord_map[x] = {y : val}
            
    def add_line(self, direction, x, y, values):
        x = x - self._x_shift
        y = y - self._y_shift
        
        for i in range(len(values)):
            if direction == DIR_RIGHT:
                self.set_val(x + i, y, values[i])
            elif direction == DIR_DOWN:
                self.set_val(x, y + i, values[i])
    
    def get_val(self, x, y):
        x = x - self._x_shift
        y = y - self._y_shift
        if x in self._coord_map and y in self._coord_map[x]:
            return self._coord_map[x][y]
        else:
            return None
    
    def get_min_x(self):
        keys = self._coord_map.keys()
        if keys:
            return min(self._coord_map.keys()) + self._x_shift
        else:
            return None
    
    def get_min_y(self):
        min_val = None
        for row in self._coord_map.values():
            row_min = min(row.keys())
            if min_val == None or min_val > row_min:
                min_val = row_min
        
        if min_val == None:
            return None
        else:
            return min_val + self._y_shift
    
    def get_max_x(self):
        keys = self._coord_map.keys()
        if keys:
            return max(self._coord_map.keys()) + self._x_shift
        else:
            return None
    
    def get_max_y(self):
        max_val = None
        for row in self._coord_map.values():
            row_max = max(row.keys())
            if max_val == None or max_val < row_max:
                max_val = row_max
        
        if max_val == None:
            return None
        else:
            return max_val + self._y_shift
    
    def shift_x(self, shift):
        self._x_shift = self._x_shift + shift
    
    def shift_y(self, shift):
        self._y_shift = self._y_shift + shift














        