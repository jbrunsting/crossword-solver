import crossword_tools
import copy

# word_bank is a list of strings
# returns a list of dictionaries, where the keys of the dictionary are the line
# id's, and the values are the different words that fill in the crossword
def solve(puzzle, word_bank):
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
    
    initial_id = get_optimal_guess_line(list(puzzle.lines.keys()), fitting_words)
        
    current_solution = {}
    for possible_word in fitting_words[initial_id]:
        guess_word(puzzle, initial_id, possible_word, fitting_words, current_solution, solution_set)
    
    return solution_set

# populates solution_set with all the possibilities that can be found without
# removing anything from current_solution
def guess_word(puzzle, line_id, guess, fitting_words, current_solution, solution_set):
    current_solution[line_id] = guess
    guessed_line = puzzle.lines[line_id]
    # we copy this so that we don't have to reset the lists at the end of the 
    # function like we do with current_solution. It is just a shallow copy, so
    # it shouldn't be too terrible on memory or processing, although it is 
    # not ideal
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
    