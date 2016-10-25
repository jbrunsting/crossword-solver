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
        
        def __init__(self, first_id, second_id, first_intersect, 
                     second_intersect):
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
            self.set_val(coord.x + xoffset, coord.y + yoffset, 
                         coordmap.get_val(coord.x, coord.y))
    
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
                coords.append(CoordMap.Coord(x + self._x_shift, 
                                             y + self._y_shift))
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
    
    if not coordmap:
        return
    
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
    
    coordmaps = get_puzzle_coordmaps(puzzle)
    if coordmaps:
        return coordmaps[0]
    else:
        return None

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
    Returns:
        A list of CoordMap's containing the mappings required to display the
        provided solutions to the puzzle.
    """
    
    if solution_set:
        num_solution_coord_maps = len(solution_set)
    else:
        num_solution_coord_maps = 1
    
    # This list contains the CoordMap's that will eventually be returned to the
    # caller.
    solution_coord_maps = [CoordMap() for i in range(num_solution_coord_maps)]
    
    lines = copy.deepcopy(puzzle.lines)
    if not lines:
        return
    
    overlay_x_shift = 0
    
    # Continually take a key from the lines list, and add it, and its
    # descendants, to the CoordMap's, until all of the lines have been added.
    while lines.keys():
        # First, we get a list of blank CoordMap's, and pick a random line to
        # insert into them, along with its descendants (lines that are
        # connected to it through intersection points).
        line_and_descendant_maps = [CoordMap() for i in range(num_solution_coord_maps)]
        current_key = list(lines.keys())[0]
        lines = add_line_and_descendants_to_coordmaps(line_and_descendant_maps, 
                                                      0, 0, current_key, lines, 
                                                      solution_set)
        
        # Next, we take every CoordMap that was generated, shift it so that all
        # of its elements are at coordinates greater than (0, 0), and then 
        # combine them with the master CoordMap, ensuring they do not overlap
        # by shifting the overlay right by overlay_x_shift
        for i, solution_coord_map in enumerate(solution_coord_maps):
            overlay_map = line_and_descendant_maps[i]
            overlay_map.shift_x(-overlay_map.get_min_x())
            overlay_map.shift_y(-overlay_map.get_min_y())
            solution_coord_map.overlay_coordmap(overlay_map, overlay_x_shift, 0)
            
        overlay_x_shift = solution_coord_map.get_max_x() + 2
    
    # Before returning the CoordMaps to the user, we shift them so that they 
    # have all their coordinates greater than (0, 0)
    for coord_map in solution_coord_maps:
        coord_map.shift_x(-coord_map.get_min_x())
        coord_map.shift_y(-coord_map.get_min_y())
    
    return solution_coord_maps
    
def add_line_and_descendants_to_coordmaps(coordmaps, x, y, line_id, lines, 
                                          line_solutions_by_coordmap):
    """
    Recursively adds the lines in the lines list to the CoordMaps in the 
    coordmaps list, using line_solutions_by_cooordmap to determine what 
    characters to put in each line. It may not end up adding all of the lines
    in the lines list, because it uses the intersection points of each line to
    determine what line to add next, so it only adds lines that are connected in
    some way to the line at line_id. It may seem confusing to use lists of
    CoordMap's and the line string information, but it is important so that we
    don't have to run this entire algorithm for every CoordMap.
    
    Args:
        coordmaps: A list of unfilled CoordMaps that will be filled from the
                   strings in line_solutions_by_coordmap.
        x: The x coordinate the line with in line_id should start at
        y: The y coordinate the line with id line_id should start at
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
        CoordMaps in the coordmaps list removed.
    """
    
    line = lines[line_id]
    
    # Add the line specified by line_id to the CoordMaps. The ith CoordMap is
    # filled with the string in the ith dictionary in line_solutions_by_
    # coordmap, if it exists, or with filler characters, if it does not.
    for i, coordmap in enumerate(coordmaps):
        line_solutions = None
        if line_solutions_by_coordmap:
            line_solutions = line_solutions_by_coordmap[i]
            
        if line_solutions and line_id in line_solutions:
            line_string = line_solutions[line_id]
        else:
            line_string = [FILLER_CHAR for i in range(line.length)]
            
        coordmap.add_line(line.direction, x, y, line_string)
    
    # Since we have added the line to the CoordMaps, we no longer want it in the
    # lines list, because we don't want to add it twice and cause infinite
    # loops.
    line_intersection_points = line.intersection_points
    line_direction = line.direction
    del lines[line_id]
    
    # For every intersection point, try to add the intersected line to the 
    # CoordMaps, if it has not already been added.
    for intersection in line_intersection_points:
        newline_x = x
        newline_y = y
        
        if line_direction == DIR_DOWN:
            newline_y = newline_y + intersection.first_intersect
        else:
            newline_x = newline_x + intersection.first_intersect
        
        intersected_id = intersection.second_id
        if intersected_id not in lines:
            continue
        
        intersected_line = lines[intersected_id]
        
        if intersected_line == None:
            continue
        
        if intersected_line.direction == DIR_DOWN:
            newline_y = newline_y - intersection.second_intersect
        else:
            newline_x = newline_x - intersection.second_intersect
        
        lines = add_line_and_descendants_to_coordmaps(coordmaps, newline_x, newline_y, intersected_id, lines, line_solutions_by_coordmap)
    
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
    
    rows = [] # list of tuples, each of the form (x, y, length, direction)
    X_FIELD =  0;
    Y_FIELD = 1;
    LEN_FIELD = 2;
    DIR_FIELD = 3;
    
    def find_lines(direction):
        """
        Finds the lines in the provided direction in the CoordMap provided by 
        the parent function, and adds the row information to the rows array.
        
        Args:
            direction: The direction of the lines being searched for, must be
                       DIR_DOWN for up/down rows, and DIR_RIGHT for left/right
                       ones.
        """
        
        width = coordmap.get_max_x() + 1
        height = coordmap.get_max_y() + 1
        
        # If we are searching for up/down lines, we want our primary range to 
        # be the range of the x axis, because we want to take every coordinate
        # column in the x, and look at all of the y subvalues to see if they
        # form a line. It is the inverse for right/left lines.
        if direction == DIR_DOWN:
            primary_range = range(width)
            sub_range = range(height)
        else:
            primary_range = range(height)
            sub_range = range(width)
        
        for p in primary_range:
            current_word_len = -1
            starting_x = -1
            starting_y = -1
            for s in sub_range:
                if direction == DIR_DOWN:
                    x = p
                    y = s
                else:
                    x = s
                    y = p
                
                if coordmap.get_val(x, y):
                    if current_word_len == -1:
                        starting_x = x
                        starting_y = y
                        current_word_len = 1
                    else:
                        current_word_len = current_word_len + 1
                elif current_word_len > 1:
                    rows.append((starting_x, starting_y, current_word_len, direction))
                    current_word_len = -1
                else:
                    current_word_len = -1
            else:
                if current_word_len > 1:
                    rows.append((starting_x, starting_y, current_word_len, direction))
                    current_word_len = -1
        
    find_lines(DIR_DOWN)
    find_lines(DIR_RIGHT)
    
    puzzle = Puzzle()
    
    # Calculate the intersection points of each row, and combine these points,
    # and the row information, by adding it to the puzzle.
    for i, row in enumerate(rows):
        line_id = i
        x = row[X_FIELD]
        y = row[Y_FIELD]
        length = row[LEN_FIELD]
        dir = row[DIR_FIELD]
        intersections = []
        
        print("at row " + str(line_id) + " with x, y, len, dir " + str(x) + ", " + str(y) + ", " + str(length) + ", " + str(dir));
        
        # Check all other lines to see if they intersect with this one.
        for i2, row2 in enumerate(rows):
            c_line_id = i2;
            c_x = row2[X_FIELD]
            c_y = row2[Y_FIELD]
            c_length = row2[LEN_FIELD]
            c_dir = row2[DIR_FIELD];
            # ensure that we are not trying to compare a row with itself, and
            # don't bother finding the intersection of parallel lines
            if line_id == c_line_id or dir == c_dir:
                continue
            
            
            if dir == DIR_DOWN: # Implying row2 has direction right
                # If they intersect
                if c_x <= x and c_x + c_length > x and y <= c_y and y + length > c_y:
                    intersect = Puzzle.IntersectionPoint(line_id, c_line_id, c_y - y, x - c_x)
                    intersections.append(intersect)
            elif dir == DIR_RIGHT: # Implying row2 has direction down
                # If they intersect
                if x <= c_x and x + length > c_x and c_y <= y and c_y + c_length > y:
                    intersect = Puzzle.IntersectionPoint(line_id, c_line_id, c_x - x, y - c_y)
                    intersections.append(intersect)
        
        puzzle.add_line(length, dir, intersections, line_id)
     
    return puzzle  
