'''
Created on Sep 6, 2016

@author: Jacob Brunsting
'''

import copy

DIR_DOWN = 0
DIR_RIGHT = 1
FILLER_CHAR = '#'


class Puzzle(object):
    """
    A description of a crossword puzzle composing of multiple lines with unique
    id's.
    
    Attributes:
        lines: A dictionary mapping integer line id's to CrosswordLine objects.
        LINE_DIR_DOWN: A constant representing a line pointing downwards.
        LINE_DIR_RIGHT: A constant representing a line pointing right.
    """
        
    def __init__(self):
        self.lines = {}
    
    def add_line(self, length, direction, intersection_points, line_id):
        """
        Adds a line to the puzzle based on the provide parameters.
        
        Args:
            length: The integer length of the line, in characters.
            direction: An integer denoting the direction the line points in,
                       where down is DIR_DOWN, and right is DIR_RIGHT.
            intersection_points: A list of intersection points describing every
                                 line the new line intersects, and where.
            line_id: The unique integer id of the line.
        """
        
        new_line = Puzzle.CrosswordLine(length, direction, intersection_points)
        self.lines[line_id] = new_line
        
    class CrosswordLine(object):    
        """
        A line in a crossword puzzle.
        
        Attributes:
            length: The integer length of the line, in characters.
            direction: An integer denoting the direction the line points in,
                       where down is DIR_DOWN, and right is DIR_RIGHT.
            intersection_points: A list of intersection points describing every
                                 line the line intersects, and where.
        """
        
        def __init__(self, length, direction, intersection_points):
            self.length = length
            self.direction = direction
            self.intersection_points = intersection_points
    
    class IntersectionPoint(object):
        """
        An intersection point between two CrosswordLine objects.
        
        Attributes:
            first_id: The id of the line where this intersection point is
                      stored.
            second_id: The line the line at first_id intersects with.
            first_intersect: The position in the first line the intersection
                             occurs, counting from the start of the line
                             starting at 0.
            second_intersect: The position in the second line the intersection
                              occurs
        """
        
        def __init__(self, first_id, second_id, first_intersect, second_intersect):
            self.first_id = first_id
            self.second_id = second_id
            self.first_intersect = first_intersect
            self.second_intersect = second_intersect
        
        def words_fit(self, first_word, second_word):
            """
            Determines if, when the provided words are inserted into the
            lines at this intersection point, there will be a conflict.
            
            Args:
                first_word: A string that will be inserted in the line with id
                        first_id
                second_word: A string that will be inserted in the line with id
                         second_id
            
            Returns:
                True if, at the point of intersection, the lines have the same
                character, and false if they do not.
            """
            
            return (first_word[self.first_intersect]
                 == second_word[self.second_intersect])

class CoordMap(object):
    """
    An enhanced dictionary of dictionaries, mapping x, y coordinates to values
    """
    
    def __init__(self):
        self._coord_map = {}
        self._x_shift = 0
        self._y_shift = 0
    
    def set_val(self, x, y, val):
        """
        Maps the provided coordinates to the provided value.
        
        Args:
            x: The x coordinate
            y: The y coordinate
            val: The value at x, y
        """
        
        x = x - self._x_shift
        y = y - self._y_shift
        if x in self._coord_map:
            self._coord_map[x][y] = val
        else:
            self._coord_map[x] = {y : val}
            
    def add_line(self, direction, x, y, values):
        """
        Maps the items in values to a line of coordinates starting at the 
        provided x and y value, and going in the provided direction.
        
        Args:
            direction: The direction the line is going in, where down is 
                       DIR_DOWN, and right is DIR_RIGHT.
            x: The x coordinate the line starts at.
            y: the y coordinate the line starts at.
            values: An array of the values that are going to be mapped to 
                    coordinates in the line.
        """
        
        x = x - self._x_shift
        y = y - self._y_shift
        
        for i in range(len(values)):
            if direction == DIR_RIGHT:
                self.set_val(x + i, y, values[i])
            elif direction == DIR_DOWN:
                self.set_val(x, y + i, values[i])
    
    def overlay_coordmap(self, coordmap, xoffset, yoffset):
        """
        Moves the mappings from the provided CoordMap to the current CoordMap,
        offsetting the values if required.
        
        Args:
            coordmap: The CoordMap the new values are being sourced from.
            xoffset: The integer amount the values of coordmap should be shifted 
                     in the x axis before they are added.
            yoffset: The integer amount the values of coordmap should be shifted 
                     in the y axis before they are added.
        """
        
        new_coords = coordmap.get_filled_coords()
        
        for coord in new_coords:
            self.set_val(coord.x + xoffset, coord.y + yoffset, coordmap.get_val(coord.x, coord.y))
    
    def get_val(self, x, y):
        """
        Gets the value at the provided coordinate.
        
        Args:
            x: The x coordinate.
            y: The y coordinate.
        
        Returns:
            The value at (x, y).
        """
        
        x = x - self._x_shift
        y = y - self._y_shift
        if x in self._coord_map and y in self._coord_map[x]:
            return self._coord_map[x][y]
        else:
            return None
    
    def get_filled_coords(self):
        """
        Gets the coordinates that are assigned to some value.
        
        Returns:
            A list of CoordMap.Coord objects representing the different
            coordinates that are mapped in this CoordMap.
        """
        
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
        """
        Gets the minimum x value a mapped coordinate has in this CoordMap.
        
        Returns:
            An integer representing the minimum assigned x value.
        """
        
        keys = self._coord_map.keys()
        if keys:
            return min(self._coord_map.keys()) + self._x_shift
        else:
            return None
    
    def get_min_y(self):
        """
        Gets the minimum y value a mapped coordinate has in this CoordMap.
        
        Returns:
            An integer representing the minimum assigned y value.
        """
        
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
        """
        Gets the maximum x value a mapped coordinate has in this CoordMap.
        
        Returns:
            An integer representing the maximum assigned x value.
        """
        
        keys = self._coord_map.keys()
        if keys:
            return max(self._coord_map.keys()) + self._x_shift
        else:
            return None
    
    def get_max_y(self):
        """
        Gets the maximum y value a mapped coordinate has in this CoordMap.
        
        Returns:
            An integer representing the maximum assigned y value.
        """
        
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
        """
        Shifts all mapped coordinates by the provided amount in the x axis.
        
        Args:
            shift: The integer amount that should be added to each x coordinate.
        """
        
        self._x_shift = self._x_shift + shift
    
    def shift_y(self, shift):
        """
        Shifts all mapped coordinates by the provided amount in the y axis.
        
        Args:
            shift: The integer amount that should be added to each y coordinate.
        """
        
        self._y_shift = self._y_shift + shift
        
    class Coord:
        def __init__(self, x, y):
            self.x = x
            self.y = y

def print_puzzle(puzzle):
    """
    Prints the provided puzzle into the console, representing the lines with
    a filler character, and using spaces to fill in the blank spaces.
    
    Args:
        puzzle: The Puzzle object that is describing what should be printed.
    """
    
    print_coord_map(get_empty_puzzle_coordmap(puzzle), 1)

def print_coord_map(coordmap, border):
    """
    Prints the points described in the provided CoordMap to the console
    
    Args:
        coordmap: The CoordMap that will be printed to the console
        border: The number of spaces to leave around the edge of the region
                where the CoordMap is being printed
    """
    
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
    """
    Generates a CoordMap describing the puzzle without a solution, filling in 
    the lines with filler characters.
    
    Args:
        puzzle: The Puzzle object that is the source for the CoordMap.
    
    Returns:
        A CoordMap object created from the provided puzzle, which maps
        coordinates to either a space character, or a filler character.
    """
    
    return get_puzzle_coordmaps(puzzle)[0]

def get_puzzle_coordmaps(puzzle, solution_set = None):
    """
    Generates a set of CoordMap's that can be used to display the solutions to
    the provided puzzle, or display the puzzle using filler characters if there
    are no solutions.
    
    Args:
        puzzle: The puzzle that we are displaying.
        solution_set: An optional parameter, consisting of a list of
                      dictionaries describing solutions to the provided puzzle,
                      where each dictionary maps the id of each of the lines in
                      the provided Puzzle to a word that goes in that line.
    """
    
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
        lines = add_line_and_decendents_to_coordmaps(line_and_decendant_maps, current_key, lines, solution_set)
        
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
    
def add_line_and_decendents_to_coordmaps(coordmaps, line_id, lines, line_solutions_by_coordmap):
    """
    Recursively adds the lines in the lines list to the CoordMap's in the 
    coordmaps list, using line_solutions_by_cooordmap to determine what 
    characters to put in each line. It may not end up adding all of the lines
    in the lines list, because it uses the intersection points of each line to
    determine what line to add next, so it only adds lines that are connected in
    some way to the line at line_id. It may seem confusing to use lists of
    CoordMap's and the line string information, but it is important so that we
    don't have to run this entire algorithm for every CoordMap.
    
    Args:
        coordmaps: A list of unfilled CoordMap's that will be filled from the
                   strings in line_solutions_by_coordmap.
        line_id: The id of the line that should be added in next
        lines: A list of CrosswordLine objects that still have to be used to
               populate the coordmaps list.
        line_solutions_by_coordmap: An array of dictionaries where the keys
                                    are the id's of different lines in the lines
                                    list, and the values are the strings that go
                                    in those lines. The i-th dictionary in the
                                    array will be used to populate the i-th 
                                    CoordMap in coordmaps, so it must have the 
                                    same length as coordmaps, or the spaces will
                                    be filled with a filler character.
    
    Returns:
        The lines array with all of the lines that have been added to the
        CoordMap's in the coordmaps list removed.
    """
    
    line = lines[line_id]
    
    for i, coordmap in enumerate(coordmaps):
        line_solutions = None
        if line_solutions_by_coordmap:
            line_solutions = line_solutions_by_coordmap[i]
            
        if line_solutions and line_id in line_solutions:
            line_string = line_solutions[line_id]
        else:
            line_string = [FILLER_CHAR for x in range(line.length)]
            
        coordmap.add_line(line.direction, 0, 0, line_string)
    
    line_intersection_points = line.intersection_points
    line_direction = line.direction
    del lines[line_id]
    for intersection in line_intersection_points:
        newline_x = 0
        newline_y = 0
        
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

def generate_puzzle_from_selected_tile_map(coordmap):
    """
    Takes a CoordMap object, where each assigned coordinate in the CoordMap is 
    mapped to a True or False value, and treats every True coordinate like an 
    unfilled place in a crossword puzzle, generating a Puzzle object.
    
    args:
        coordmap: A CoordMap object, mapping coordinates to boolean values, 
                  where a True value represents an empty spot in the crossword, 
                  and a false or non-existent value represents a spot that is 
                  not part of the crossword.
    """
    
    puzzle = Puzzle()
    rows = [] # list of tuples, each of the form (x, y, length, direction)
    
    width = coordmap.get_max_x() + 1
    height = coordmap.get_max_y() + 1

    # TODO: Kill this repetition
    # extract horizontal words
    for y in range(height):
        current_word_len = -1
        starting_x = -1
        starting_y = -1
        for x in range(width):
            if coordmap.get_val(x, y):
                if current_word_len == -1:
                    starting_x = x
                    starting_y = y
                    current_word_len = 1
                else:
                    current_word_len = current_word_len + 1
            elif current_word_len > 1:
                rows.append((starting_x, starting_y, current_word_len, DIR_RIGHT))
                current_word_len = -1
            else:
                current_word_len = -1
        else:
            if current_word_len > 1:
                rows.append((starting_x, starting_y, current_word_len, DIR_RIGHT))
                current_word_len = -1
            
    
    # extract vertical words
    for x in range(width):
        current_word_len = -1
        starting_x = -1
        starting_y = -1
        for y in range(height):
            if coordmap.get_val(x, y):
                if current_word_len == -1:
                    starting_x = x
                    starting_y = y
                    current_word_len = 1
                else:
                    current_word_len = current_word_len + 1
            elif current_word_len > 1:
                rows.append((starting_x, starting_y, current_word_len, DIR_DOWN))
                current_word_len = -1
            else:
                current_word_len = -1
        else:
            if current_word_len > 1:
                rows.append((starting_x, starting_y, current_word_len, DIR_DOWN))
                current_word_len = -1
    
    for i, row in enumerate(rows):
        line_id = i
        x = row[0]
        y = row[1]
        length = row[2]
        dir = row[3]
        intersections = []
        
        # calculate all intersection points
        for i2, row2 in enumerate(rows):
            if i2 == i or row2[3] == row[3]:
                continue
            
            x2 = row2[0]
            y2 = row2[1]
            length2 = row2[2]
            
            # this implies that row2 has direction right
            if dir == Puzzle.LINE_DIR_DOWN:
                # if they intersect
                if x2 <= x and x2 + length2 > x and y <= y2 and y + length > y2:
                    intersect = Puzzle.IntersectionPoint(i, i2, y2 - y, x - x2)
                    intersections.append(intersect)
            # this implies that row2 has direction down
            elif dir == Puzzle.LINE_DIR_RIGHT:
                # if they intersect
                if x <= x2 and x + length > x2 and y2 <= y and y2 + length2 > y:
                    intersect = Puzzle.IntersectionPoint(i, i2, x2 - x, y - y2)
                    intersections.append(intersect)
        
        puzzle.add_line(length, dir, intersections, i)
     
    return puzzle  
