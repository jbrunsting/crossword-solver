'''
Created on Sep 6, 2016

@author: Jacob Brunsting
'''

import crossword_tools
import constants

# Yea, your gonna have to improve these alot

puzzle = crossword_tools.Puzzle()

# TODO: account for incorrect input, and allow re-starting and stuff
# TODO: follow the actual crossword format, with the same number having across
# and down values
def configure_puzzle():
    remaining_lines = read_int(constants.LINE_COUNT_STR)
    current_line = 0
    
    while current_line < remaining_lines:
        length_message = (constants.LINE_LENGTH_STR).format(str(current_line + 1))
        line_length = read_int(length_message)
        dir_message = (constants.LINE_DIR_STR).format(
            crossword_tools.Puzzle.LINE_DIR_DOWN, 
            crossword_tools.Puzzle.LINE_DIR_RIGHT)
        line_dir = read_int(dir_message)
        line_id = current_line
        intersections = []
        
        intersects_to_read = read_int(constants.INTERSECT_COUNT_STR)
        while intersects_to_read > 0:
            # subtract one because users are 1-based and we are 0-based
            intersected_line_id = read_int(constants.INTERSECTED_LINE_ID_STR) - 1;
            
            if intersected_line_id < line_id:
                print(constants.INTERSECTION_RECORDED)
                intersects_to_read = intersects_to_read - 1;
                continue
            
            first_line_intersection = read_int(constants.FIRST_LINE_INTERSECT_POS) - 1
            second_line_intersection = read_int(constants.SECOND_LINE_INTERSECT_POS) - 1
            intersection = crossword_tools.Puzzle.IntersectionPoint(
                               line_id, intersected_line_id, 
                               first_line_intersection, 
                               second_line_intersection)
            intersections.append(intersection)
            intersects_to_read = intersects_to_read - 1;
        
        puzzle.add_line(line_length, line_dir, intersections, line_id)
        
        current_line = current_line + 1
    
    print(constants.PRINTING_PUZZLE)
    crossword_tools.print_puzzle(puzzle)
        



def read_int(message):
    return int(input(message))

def main():
    configure_puzzle()

main();