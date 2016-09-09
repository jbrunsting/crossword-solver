'''
Created on Sep 6, 2016

@author: Jacob Brunsting
'''

import crossword_tools
import constants
import crossword_gui
import solver

# Yea, your gonna have to improve these alot

puzzle = crossword_tools.Puzzle()

# TODO: account for incorrect input, and allow re-starting and stuff
# TODO: follow the actual crossword format, with the same number having across
# and down values
def main():
    def on_puzzle_retrieval(puzzle):
        print(constants.PRINTING_PUZZLE)
        crossword_tools.print_puzzle(puzzle)
        word_bank = []
        while True:
            user_input = input(constants.WORD_BANK_ENTRY_STR)
            if user_input == "q":
                break
            word_bank.append(user_input)
        
        solutions = solver.solve(puzzle, word_bank)
        
        if solutions:
            crossword_gui.display_puzzle_solutions(puzzle, solutions, lambda: main())
        else:
            print("No solutions found")
    
    width = read_int(constants.PUZZLE_WIDTH_STR)
    height = read_int(constants.PUZZLE_HEIGHT_STR)
    crossword_gui.get_user_generated_crossword(width, height, on_puzzle_retrieval)

def read_int(message):
    return int(input(message))

main();