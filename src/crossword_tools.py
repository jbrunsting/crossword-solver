'''
Created on Sep 6, 2016

@author: Jacob Brunsting
'''

import copy

DIR_DOWN = 0
DIR_RIGHT = 1


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
                 == second_word[self.second_intersect])

def print_puzzle(puzzle):    
    print_coord_map(get_empty_puzzle_coordmap(puzzle), 1)

def print_coord_map(coordmap, border):
    minx = coordmap.get_min_x()
    miny = coordmap.get_min_y()
    maxx = coordmap.get_max_x()
    maxy = coordmap.get_max_y()
    
    if minx == None or maxx == None or miny == None or maxy == None:
        return;
    
    coordmap.shift_x(-minx)
    coordmap.shift_y(-miny)
    
    maxx = maxx - minx
    maxy = maxy - miny
    
    for y in range(maxy + 1 + 2 * border):
        for x in range(maxx + 1 + 2 * border):
            if (x < border or y < border or 
                x > maxx + border or y > maxy + border):
                print(' ', end="")
            else:
                val = coordmap.get_val(x - border, y - border)
                if val == None:
                    print(' ', end="")
                else:
                    print(val, end="")
        print("")

def get_empty_puzzle_coordmap(puzzle):
    return get_solution_coordmaps(puzzle)[0]

def get_solution_coordmaps(puzzle, solution_set = None, show_loading = False):
    if solution_set:
        num_solution_coord_maps = len(solution_set)
    else:
        num_solution_coord_maps = 1
    
    solution_coord_maps = [CoordMap() for i in range(num_solution_coord_maps)]
    lines = copy.deepcopy(puzzle.lines)
    if not lines:
        return
    
    overlay_x_shift = 0
    while lines.keys():
        line_and_decendant_maps = [CoordMap() for i in range(num_solution_coord_maps)]
        current_key = list(lines.keys())[0]
        lines = add_line_and_decendents_to_coordmaps(line_and_decendant_maps, 0, 0, current_key, lines, solution_set)
        
        for i, solution_coord_map in enumerate(solution_coord_maps):
            overlay_map = line_and_decendant_maps[i]
            overlay_map.shift_x(-overlay_map.get_min_x())
            overlay_map.shift_y(-overlay_map.get_min_y())
            solution_coord_map.overlay_coordmap(overlay_map, overlay_x_shift, 0)
            
        overlay_x_shift = solution_coord_map.get_max_x() + 2
        
    for coord_map in solution_coord_maps:
        coord_map.shift_x(-coord_map.get_min_x())
        coord_map.shift_y(-coord_map.get_min_y())
    
    return solution_coord_maps
    
# returns the list of lines with the lines that were added removed
# coordmaps is a list of CoordMaps with the same length as line_solutions_by_coordmap
# line_solutions_by_coordmap is an array of dictionaries where the keys are the
# id's of different lines in the coordmap, and the values are the word that goes
# at that line
def add_line_and_decendents_to_coordmaps(coordmaps, x, y, line_id, lines, line_solutions_by_coordmap):
    FILLER_CHAR = '#'
    
    line = lines[line_id]
    
    for i, coordmap in enumerate(coordmaps):
        line_solutions = None
        if line_solutions_by_coordmap:
            line_solutions = line_solutions_by_coordmap[i]
            
        if line_solutions and line_id in line_solutions:
            line_string = line_solutions[line_id]
        else:
            line_string = [FILLER_CHAR for x in range(line.length)]
            
        coordmap.add_line(line.direction, x, y, line_string)
    
    line_intersection_points = line.intersection_points
    line_direction = line.direction
    del lines[line_id]
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
            newline_x = newline_x - intersection.second_intersect
        
        lines = add_line_and_decendents_to_coordmaps(coordmaps, newline_x, newline_y, intersected_id, lines, line_solutions_by_coordmap)
    
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
    
    def overlay_coordmap(self, coordmap, xoffset, yoffset):
        new_coords = coordmap.get_filled_coords()
        
        for coord in new_coords:
            self.set_val(coord.x + xoffset, coord.y + yoffset, coordmap.get_val(coord.x, coord.y))
    
    def get_val(self, x, y):
        x = x - self._x_shift
        y = y - self._y_shift
        if x in self._coord_map and y in self._coord_map[x]:
            return self._coord_map[x][y]
        else:
            return None
    
    def get_filled_coords(self):
        xcoords = list(self._coord_map.keys())
        coords = []
        for xindex in range(len(xcoords)):
            x = xcoords[xindex]
            ycoords = list(self._coord_map[x].keys())
            for yindex in range(len(ycoords)):
                y = ycoords[yindex]
                coords.append(CoordMap.Coord(x + self._x_shift, y + self._y_shift))
        return coords
    
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
        
    class Coord:
        def __init__(self, x, y):
            self.x = x
            self.y = y