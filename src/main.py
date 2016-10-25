'''
Created on Sep 6, 2016

@author: Jacob Brunsting
'''

import crossword_tools
import constants
import crossword_gui
import solver
import time

def main():
    width = read_int(constants.PUZZLE_WIDTH_STR, 2)
    height = read_int(constants.PUZZLE_HEIGHT_STR, 2)
    print(constants.DRAW_PUZZLE_STR)
    crossword_gui.display_crossword_generation_window(width, height, 
                                                      on_puzzle_retrieval)

def on_puzzle_retrieval(puzzle):
    """
    Gets a word bank from the user, uses it to solve the provided puzzle,
    and displays the results to the user. Should be called once the user
    has finished generating the puzzle using the puzzle creation window
    
    args:
        puzzle: A crossword_tools.Puzzle object representing the puzzle the
                user created
    """
    
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
        if user_input == 'q':
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
        
    print(constants.SOLVE_TIME_STR.format(seconds, seconds_ending, mills, 
                                          mills_ending))
    
    if solutions:
        print(constants.DISPLAYING_SOLUTIONS_STR)
        crossword_gui.display_puzzle_solutions(puzzle, solutions, lambda: main())
    else:
        user_input = input(constants.NO_SOLUTIONS_STR)
        if user_input == 'y':
            main()

def read_int(message, min_val):
    """
    Reads an integer from the user, prompting the user with the provided 
    message. Continually gives an error message and prompts the user with the
    provided message until they provide valid input, if they do not provide an 
    integer input initially.
    
    args:
        message: The message shown to the user to prompt them to input an
                 integer.
    """
    
    while True:
        try:
            int_input = int(input(message))
            
            if int_input >= min_val:
                return int_input
            else:
                print(constants.TOO_LOW_INPUT_STR.format(min_val))
        except ValueError:
            print(constants.IMPROPER_INPUT_STR)

main();