import copy

def solve(puzzle, word_bank):
    """
    Solves the provided crossword puzzle using words from the word bank.
    
    Args:
        puzzle: A crossword_tools.Puzzle object.
        word_bank: A list of strings.
    
    Returns:
        A list of dictionaries, where each dictionary is a solution to the
        puzzle, mapping every line id in the puzzle to a word from the word 
        bank. None is returned if a solution could not be found.
        found.
    """
    
    fitting_words = {}
    word_by_length = {}
    solution_set = []
    
    for word in word_bank:
        length = len(word)
        if length not in word_by_length:
            word_by_length[length] = []
        word_by_length[length].append(word)
    
    
    for line_id, line in puzzle.lines.items():
        if line.length not in word_by_length:
            return None
        fitting_words[line_id] = copy.copy(word_by_length[line.length])
        if fitting_words[line_id] == None:
            return None
    
    keylist = list(puzzle.lines.keys())
    if not keylist:
        return None
    
    find_solutions(puzzle, fitting_words, solution_set)
    
    return solution_set

def find_solutions(puzzle, fitting_words, solution_set):
    """
    Fills solution_set with all of the possible solutions to the puzzle, based
    on the words from fitting_words, where each solution is a dictionary mapping
    a key from puzzle to a word from fitting_words.
    
    Args:
        puzzle: The puzzle being solved.
        fitting_words: A dictionary mapping every line id in puzzle to a list of
                       words that are the right size to fit in that line.
        solution_set: An empty list that will be modified to contain multiple
                      dictionaries, where each dictionary is a solution to the
                      puzzle, mapping every line id to a word from 
                      fitting_words.
    """
    
    initial_id = get_optimal_guess_line(list(puzzle.lines.keys()), fitting_words)
        
    current_solution = {}
    for possible_word in fitting_words[initial_id]:
        guess_word(puzzle, initial_id, possible_word, fitting_words, current_solution, solution_set)

def guess_word(puzzle, line_id, guess, fitting_words, current_solution, solution_set):
    """
    Recursively attempts to fill in the lines not yet assigned in
    current_solution with all possible words, as described by fitting_words, 
    starting by attempting to fill the line with ID line_id with the word stored 
    at guess. When current_solution is filled, meaning a solution has been 
    found, the solution is added to solution_set.
    
    Args:
        puzzle: The puzzle being solved.
        line_id: The id (as stored in puzzle) of the line we are trying to fit
                 a word into.
        guess: The word we are trying to insert at line_id
        fitting_words: a dictionary of arrays, where the dictionary has a key
                       for every line id in puzzle, and the key maps to a list
                       of all the words that could fit at that line, given the
                       words that have already been filled in current_solution
        current_solution: A dictionary of strings, where the dictionary has a 
                          key for every line id in puzzle, and the key maps to
                          the word that we are putting at that line in an
                          attempt to find a solution
        solution_set: A list containing all of the solutions that have been
                      found so far, where each solution is a dictionary mapping
                      every line id in puzzle to a word that goes in that line
    """
    
    current_solution[line_id] = guess
    guessed_line = puzzle.lines[line_id]
    # we copy this so that we don't have to reset the lists at the end of the 
    # function like we do with current_solution. Its not ideal, but its
    # better than recording all the changes we do to it and then reappplying
    # them.
    new_fitting_words = copy.deepcopy(fitting_words)
    
    # adjust the possible words for each blank to match the guess
    for intersect in guessed_line.intersection_points:
        # if the spot is filled, don't bother eliminating possibilities
        if intersect.second_id in current_solution:
            continue
        
        second_id_fitting_words = copy.copy(new_fitting_words[intersect.second_id])
        for word in second_id_fitting_words:
            if not intersect.words_fit(guess, word):
                new_fitting_words[intersect.second_id].remove(word)
                
        if not new_fitting_words[intersect.second_id]:
            del current_solution[line_id]
            return
    
    solved_ids = current_solution.keys()
    all_ids = puzzle.lines.keys()
    possible_ids = [x for x in all_ids if x not in solved_ids]
    
    # if there are no more id's to check, meaning everything has been filled
    if not possible_ids:
        solution_set.append(copy.copy(current_solution))
        del current_solution[line_id]
        return
    
    target_id = get_optimal_guess_line(possible_ids, new_fitting_words)
    
    for possible_word in new_fitting_words[target_id]:
        if possible_word not in current_solution.values():
            guess_word(puzzle, target_id, possible_word, new_fitting_words, current_solution, solution_set)
    
    # it is important to reset this value, so that after we have guessed, we are
    # able to guess different values without the parent functions getting all
    # mad and stuff cause they think the spot is already filled
    del current_solution[line_id]

def get_optimal_guess_line(id_list, fitting_words):
    """
    Finds the id from id_list that maps to the smallest list of words in
    fitting_words.
    
    Args:
        id_list: A list of id's which are keys in fitting_words.
        fitting_words: A dictionary with integer keys that map to lists of
                       strings
    
    Returns:
        The id in id_list that, of all the ids in the list, maps to the smallest
        list in fitting_words
    """
    
    if not id_list:
        return None
    
    target_id = id_list[0]
    lowest_possibility_count = len(fitting_words[target_id])
    for line_id in id_list:
        num_fitting_words = len(fitting_words[line_id])
        if num_fitting_words < lowest_possibility_count:
            lowest_possibility_count = num_fitting_words
            target_id = line_id
    
    return target_id
    