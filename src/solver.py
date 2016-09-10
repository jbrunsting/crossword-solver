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
    
    # First, we make a dictionary mapping a length to a list of words from the
    # word bank with that length
    for word in word_bank:
        length = len(word)
        if length not in word_by_length:
            word_by_length[length] = []
        word_by_length[length].append(word)
    
    # Next, we find the length of each line and take the list of words that can
    # fit there from the word_by_length dictionary
    for line_id, line in puzzle.lines.items():
        if line.length not in word_by_length:
            return None
        fitting_words[line_id] = copy.copy(word_by_length[line.length])
        if fitting_words[line_id] == None:
            return None
    
    keylist = list(puzzle.lines.keys())
    if not keylist:
        return None
    
    # Finally, we pass in the information we have generated to the 
    # find_solutions function, which will modify solution_set to contain all of
    # the solutions to the puzzle, so it can be returned to the user.
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
    # We copy new_fitting_words so that we can remove words from it without
    # modifying the fitting_words list in other solution branches.
    new_fitting_words = copy.deepcopy(fitting_words)
    
    # Remove all words from the new_fitting_words list that don't fit with the
    # new guess.
    for intersect in guessed_line.intersection_points:
        # If the spot is filled, don't bother doing any calculations
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
    
    # If there are no more id's to guess, meaning all of the lines have been
    # filled in, we have found a solution, so we add it to the current_solutions
    # list.
    if not possible_ids:
        solution_set.append(copy.copy(current_solution))
        del current_solution[line_id]
        return
    
    target_id = get_optimal_guess_line(possible_ids, new_fitting_words)
    
    for possible_word in new_fitting_words[target_id]:
        if possible_word not in current_solution.values():
            guess_word(puzzle, target_id, possible_word, new_fitting_words, current_solution, solution_set)
    
    # It is important to remove the guess from the current_solutions list after
    # we are done with it so that it is not still there when we are attempting
    # to start a new search branch.
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
    