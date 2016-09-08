import crossword_tools
import tkinter
import copy

# callback must take a puzzle as an argument
def get_user_generated_crossword(canvas_width, canvas_height, callback):
    selected_tile_map = crossword_tools.CoordMap()

    def on_button_click(btn, r, c):
        def fn():
            if btn.selected:
                btn.selected = False
                selected_tile_map.set_val(c, r, False)
                btn.configure(background="grey")
            else:
                btn.selected = True
                selected_tile_map.set_val(c, r, True)
                btn.configure(background="blue")
        return lambda: fn()

    def on_enter_click():
        callback(get_puzzle_from_selected_tile_map(selected_tile_map))
        
    root = tkinter.Tk()
    for r in range(canvas_height):
        for c in range(canvas_width):
            btn = tkinter.Button(root, borderwidth=1, background="grey")
            btn.selected = False
            selected_tile_map.set_val(c, r, False)
            btn.configure(command=on_button_click(btn, r, c))
            btn.grid(row=r,column=c)
    enter = tkinter.Button(root, borderwidth=1, background="grey", text="enter",
                         command=on_enter_click)
    enter.grid(row=(r + 1), column=0, columnspan=canvas_width)
    root.mainloop()
    
def get_puzzle_from_selected_tile_map(coordmap):
    puzzle = crossword_tools.Puzzle()
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
                rows.append((starting_x, starting_y, current_word_len, crossword_tools.Puzzle.LINE_DIR_RIGHT))
                current_word_len = -1
            else:
                current_word_len = -1
        else:
            if current_word_len > 1:
                rows.append((starting_x, starting_y, current_word_len, crossword_tools.Puzzle.LINE_DIR_RIGHT))
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
                rows.append((starting_x, starting_y, current_word_len, crossword_tools.Puzzle.LINE_DIR_DOWN))
                current_word_len = -1
            else:
                current_word_len = -1
        else:
            if current_word_len > 1:
                rows.append((starting_x, starting_y, current_word_len, crossword_tools.Puzzle.LINE_DIR_DOWN))
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
            if dir == crossword_tools.Puzzle.LINE_DIR_DOWN:
                # if they intersect
                if x2 <= x and x2 + length2 > x and y <= y2 and y + length > y2:
                    intersect = crossword_tools.Puzzle.IntersectionPoint(i, i2, y2 - y, x - x2)
                    print("adding intersection at " + str(y2 - y) + " and " +  str(x - x2))
                    intersections.append(intersect)
            # this implies that row2 has direction down
            elif dir == crossword_tools.Puzzle.LINE_DIR_RIGHT:
                # if they intersect
                if x <= x2 and x + length > x2 and y2 <= y and y2 + length2 > y:
                    print("adding intersection at " + str(x2 - x) + " and " +  str(y - y2))
                    intersect = crossword_tools.Puzzle.IntersectionPoint(i, i2, x2 - x, y - y2)
                    intersections.append(intersect)
        
        print("adding word with length " + str(length) + " and id " + str(i))
        puzzle.add_line(length, dir, intersections, i)
     
    return puzzle       

# position with the corresponding ID
def print_puzzle(puzzle, solution_set):   
    for i in range(len(solution_set)): 
        lines = copy.deepcopy(puzzle.lines)
        if not lines:
            return
        
        print("Solution " + str(i) + " is:")
        while lines.keys():
            print_values_map = crossword_tools.CoordMap()
            current_key = list(lines.keys())[0]
            lines = crossword_tools.add_line_and_decendents_to_coordmap(print_values_map, 0, 0, current_key, lines, solution_set[i])
            print_coord_map(print_values_map, 1, ' ')


def print_coord_map(coordmap, border, empty_char):
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
    
    print("maxx and maxy are " + str(maxx) + ", " + str(maxy))
    for y in range(maxy + 1 + 2 * border):
        for x in range(maxx + 1 + 2 * border):
            if (x < border or y < border or 
                x > maxx + border or y > maxy + border):
                print(empty_char, end="")
            else:
                val = coordmap.get_val(x - border, y - border)
                if val == None:
                    print(empty_char, end="")
                else:
                    print(val, end="")
        print("")