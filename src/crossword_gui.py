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

    def on_enter_click(root):
        root.destroy()
        callback(generate_puzzle_from_selected_tile_map(selected_tile_map))
        
    root = tkinter.Tk()
    for r in range(canvas_height):
        for c in range(canvas_width):
            btn = tkinter.Button(root, borderwidth=1, background="grey")
            btn.selected = False
            selected_tile_map.set_val(c, r, False)
            btn.configure(command=on_button_click(btn, r, c))
            btn.grid(row=r,column=c)
    enter = tkinter.Button(root, borderwidth=1, background="grey", text="enter",
                         command=lambda: on_enter_click(root))
    enter.grid(row=(r + 1), column=0, columnspan=canvas_width)
    root.mainloop()
    
def generate_puzzle_from_selected_tile_map(coordmap):
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

def display_coordmaps_on_pages(coordmaps, max_map_width, max_map_height):
    MIN_WIDTH = 6
    BORDER_WIDTH = 1
    
    grid_width = max(max_map_width, MIN_WIDTH) + 2 * BORDER_WIDTH
    grid_height = max_map_height + 2 * BORDER_WIDTH
    num_coordmaps = len(coordmaps)
    
    def display_coordmap(root, coordmap):        
        for x in range(len(root.grid_tiles)):
            for y in range(len(root.grid_tiles[x])):
                char_at_tile = coordmap.get_val(x - BORDER_WIDTH, y - BORDER_WIDTH)
                if char_at_tile:
                    root.grid_tiles[x][y].configure(text=char_at_tile)
                else:
                    root.grid_tiles[x][y].configure(text="")
    
    def next_page(root, next_page_btn, prev_page_btn):
        if root.current_page + 1 >= num_coordmaps:
            return
        
        root.current_page = root.current_page + 1
        if root.current_page + 1 >= num_coordmaps:
            next_page_btn.configure(state=tkinter.DISABLED)
        
        prev_page_btn.configure(state=tkinter.NORMAL)
        
        display_coordmap(root, coordmaps[root.current_page])
        
    def prev_page(root, next_page_btn, prev_page_btn):
        if root.current_page <= 0:
            return
        
        root.current_page = root.current_page - 1
        if root.current_page <= 0:
            prev_page_btn.configure(state=tkinter.DISABLED)

        next_page_btn.configure(state=tkinter.NORMAL)
            
        display_coordmap(root, coordmaps[root.current_page])
    
    if not coordmaps:
        return
        
    root = tkinter.Tk()
    # not sure if this is a good way of passing the values into the click
    # functions, consider improving
    root.current_page = 0
    root.coordmaps = coordmaps
    root.grid_tiles = []
    for x in range(grid_height):
        root.grid_tiles.append([])
        for y in range(grid_width):
            btn = tkinter.Button(root, borderwidth=1, background="grey")
            root.grid_tiles[x].append(btn)
            btn.grid(row=y,column=x)

    if len(coordmaps) == 0:
        next_btn_state = tkinter.DISABLED
    else:
        next_btn_state = tkinter.NORMAL
        
    next_btn = tkinter.Button(root, borderwidth=1, background="grey", text=">", state=next_btn_state)
    prev_btn = tkinter.Button(root, borderwidth=1, background="grey", text="<", state=tkinter.DISABLED)
    
    next_btn.configure(command = lambda: next_page(root, next_btn, prev_btn))
    prev_btn.configure(command = lambda: prev_page(root, next_btn, prev_btn))
    
    next_btn.grid(row=(grid_height), column=0, columnspan=2)
    prev_btn.grid(row=(grid_width), column=grid_width - 3, columnspan=2)
    
    display_coordmap(root, coordmaps[0])
    root.mainloop()

# position with the corresponding ID
def print_puzzle(puzzle, solution_set):
    solution_coord_maps = [crossword_tools.CoordMap() for i in range(len(solution_set))]
    lines = copy.deepcopy(puzzle.lines)
    if not lines:
        return
    
    coordmap_y = 0
    while lines.keys():
        line_and_decendant_maps = [crossword_tools.CoordMap() for i in range(len(solution_set))]
        current_key = list(lines.keys())[0]
        lines = add_line_and_decendents_to_coordmap(line_and_decendant_maps, 0, 0, current_key, lines, solution_set)
        
        for i, solution_coord_map in enumerate(solution_coord_maps):
            solution_coord_map.overlay_coordmap(line_and_decendant_maps[i], coordmap_y, 0)
            
        coordmap_y = line_and_decendant_maps[0].get_max_y() + 2
    display_coordmaps_on_pages(solution_coord_maps, solution_coord_maps[0].get_max_x() + 1, solution_coord_maps[0].get_max_y() + 1)
    

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

# returns the list of lines with the lines that were added removed
# coordmaps is a list of CoordMaps with the same length as line_solutions_by_coordmap
# line_solutions_by_coordmap is an array of dictionaries where the keys are the
# id's of different lines in the coordmap, and the values are the word that goes
# at that line
def add_line_and_decendents_to_coordmap(coordmaps, x, y, line_id, lines, line_solutions_by_coordmap = None):    
    line = lines[line_id]
    
    for i, coordmap in enumerate(coordmaps):
        line_solutions = line_solutions_by_coordmap[i]
        if line_solutions and line_id in line_solutions:
            line_string = line_solutions[line_id]
        else:
            line_string = ['#' for x in range(line.length)]
        coordmap.add_line(line.direction, x, y, line_string)
    
    line_intersection_points = line.intersection_points
    line_direction = line.direction
    del lines[line_id]
    for intersection in line_intersection_points:
        newline_x = x
        newline_y = y
        
        if line_direction == crossword_tools.Puzzle.LINE_DIR_DOWN:
            newline_y = newline_y + intersection.first_intersect
        else:
            newline_x = newline_x + intersection.first_intersect
        
        intersected_id = intersection.second_id
        if intersected_id not in lines:
            continue
        
        intersected_line = lines[intersected_id]
        
        if intersected_line == None:
            continue
        
        if intersected_line.direction == crossword_tools.Puzzle.LINE_DIR_DOWN:
            newline_y = newline_y - intersection.second_intersect
        else:
            newline_x = newline_x - intersection.second_intersect
        
        lines = add_line_and_decendents_to_coordmap(coordmaps, newline_x, newline_y, intersected_id, lines, line_solutions_by_coordmap)
    
    return lines