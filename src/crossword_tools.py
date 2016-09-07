'''
Created on Sep 6, 2016

@author: Jacob Brunsting
'''

# external

class Puzzle(object):   
    LINE_DIR_DOWN = 0
    LINE_DIR_RIGHT = 1
    
    def __init__(self):
        self._lines = {}
    
    # length and id are integers, direction is either LINE_DIR_DOWN or 
    # LINE_DIR_RIGHT, intersection_points is a list of IntersectionPoint objects
    def add_line(self, length, direction, intersection_points, line_id):
        new_line = CrosswordLine(length, direction, intersection_points)
        self._lines[line_id] = new_line
    
    def words_fit(self, first_id, first_word, second_id, second_word):
        if first_id not in self._lines:
            return True
        
        for intersection in self._lines[first_id].intersection_points:
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

# internal

class CrosswordLine(object):    
    # length, direction, and id must all be integers. intersection_points
    # must be a list of IntersectionPoint objects
    def __init__(self, length, direction, intersection_points):
        self.length = length
        self.direction = direction
        self.intersection_points = intersection_points
        