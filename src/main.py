'''
Created on Sep 6, 2016

@author: Jacob Brunsting
'''

import crossword_tools
import constants
import crossword_gui
import solver
import time

# Yea, your gonna have to improve these alot

puzzle = crossword_tools.Puzzle()

# TODO: account for incorrect input, and allow re-starting and stuff
# TODO: follow the actual crossword format, with the same number having across
# and down values
def main():
    def on_puzzle_retrieval(puzzle):
        if not puzzle:
            user_input = input(constants.NO_SOLUTIONS_STR)
            if user_input == 'y':
                main()
            
        print(constants.PRINTING_PUZZLE_STR)
        crossword_tools.print_puzzle(puzzle)
        word_bank = []
        word_count = 0
        print(constants.WORD_BANK_ENTRY_STR)
        while True:
            word_count += 1
            user_input = input(constants.WORD_BANK_WORD_ENTRY_STR.format(word_count))
            if user_input == "q":
                break
            word_bank.append(user_input)
        
        print(constants.SOLVING_STR)
        start_time = time.clock()
        solutions = solver.solve(puzzle, word_bank)
        end_time = time.clock()
        diff = end_time - start_time
        seconds = round(diff)
        mills = round((diff - seconds) * 1000)
        
        if seconds == 1:
            seconds_ending = ''
        else:
            seconds_ending = 's'
            
        if mills == 1:
            mills_ending = ''
        else:
            mills_ending = 's'
            
        print(constants.SOLVE_TIME_STR.format(seconds, seconds_ending, 
                                              mills, mills_ending))
        
        if solutions:
            print(constants.DISPLAYING_SOLUTIONS_STR)
            crossword_gui.display_puzzle_solutions(puzzle, solutions, lambda: main())
        else:
            user_input = input(constants.NO_SOLUTIONS_STR)
            if user_input == 'y':
                main()
    
    width = read_int(constants.PUZZLE_WIDTH_STR)
    height = read_int(constants.PUZZLE_HEIGHT_STR)
    print(constants.DRAW_PUZZLE_STR)
    crossword_gui.get_user_generated_crossword(width, height, on_puzzle_retrieval)

def read_int(message):
    return int(input(message))

main();