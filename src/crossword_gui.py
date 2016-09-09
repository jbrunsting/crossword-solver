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
        root.rowconfigure(r, minsize="30")
        for c in range(canvas_width):
            if r == 0:
                root.columnconfigure(c, minsize="30")
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
                    intersections.append(intersect)
            # this implies that row2 has direction down
            elif dir == crossword_tools.Puzzle.LINE_DIR_RIGHT:
                # if they intersect
                if x <= x2 and x + length > x2 and y2 <= y and y2 + length2 > y:
                    intersect = crossword_tools.Puzzle.IntersectionPoint(i, i2, x2 - x, y - y2)
                    intersections.append(intersect)
        
        puzzle.add_line(length, dir, intersections, i)
     
    return puzzle    

def display_coordmaps_on_pages(coordmaps, max_map_width, max_map_height, on_close):
    MIN_WIDTH = 6
    BORDER_WIDTH = 1
    
    grid_width = max(max_map_width + 2 * BORDER_WIDTH, MIN_WIDTH)
    grid_height = max_map_height + 2 * BORDER_WIDTH
    num_coordmaps = len(coordmaps)
    grid_tiles = []
    
    def display_coordmap(root, coordmap):        
        for x in range(len(grid_tiles)):
            for y in range(len(grid_tiles[x])):
                char_at_tile = coordmap.get_val(x - BORDER_WIDTH, y - BORDER_WIDTH)
                if char_at_tile:
                    grid_tiles[x][y].configure(text=char_at_tile)
                else:
                    grid_tiles[x][y].configure(text="")
    
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
    
    def new_puzzle():
        root.destroy()
        on_close()
    
    if not coordmaps:
        return
        
    root = tkinter.Tk()
    # not sure if this is a good way of passing the values into the click
    # functions, consider improving
    root.current_page = 0
    for x in range(grid_width):
        grid_tiles.append([])
        root.columnconfigure(x, minsize="30")
        for y in range(grid_height):
            if x == 0:
                root.rowconfigure(y, minsize="30")
            btn = tkinter.Label(root, borderwidth=1, font=("Helvetica", 15))
            grid_tiles[x].append(btn)
            btn.grid(row=y, column=x)

    if len(coordmaps) <= 1:
        next_btn_state = tkinter.DISABLED
    else:
        next_btn_state = tkinter.NORMAL
        
    next_btn = tkinter.Button(root, borderwidth=1, background="grey", text=">", state=next_btn_state)
    prev_btn = tkinter.Button(root, borderwidth=1, background="grey", text="<", state=tkinter.DISABLED)
    retry_btn = tkinter.Button(root, borderwidth=1, background="grey", text="new puzzle", command=new_puzzle)
    
    next_btn.configure(command=lambda: next_page(root, next_btn, prev_btn))
    prev_btn.configure(command=lambda: prev_page(root, next_btn, prev_btn))
    
    next_btn.grid(row=grid_height, column=grid_width - 2, columnspan=2)
    prev_btn.grid(row=grid_height, column=0, columnspan=2)
    retry_btn.grid(row=grid_height, column=int(grid_width / 2 - 1), columnspan = 2 + grid_width % 2)
    
    display_coordmap(root, coordmaps[0])
    root.mainloop()

# position with the corresponding ID
def display_puzzle_solutions(puzzle, solution_set, on_close):
    solution_coord_maps = crossword_tools.get_solution_coordmaps(puzzle, solution_set)
    display_coordmaps_on_pages(solution_coord_maps, solution_coord_maps[0].get_max_x() + 1, solution_coord_maps[0].get_max_y() + 1, on_close)
