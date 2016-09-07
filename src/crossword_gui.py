import crossword_tools
import tkinter

# callback must take a puzzle as an argument
def get_user_generated_crossword(canvas_width, canvas_height, callback):
    selected_tile_map = crossword_tools.CoordMap()

    def on_button_click(btn, r, c):
        def fn():
            print("button at " + str(r) + ", " + str(c) + " clicked")
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
    
    width = coordmap.get_max_x()
    height = coordmap.get_max_y()

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
            
            x2 = row[0]
            y2 = row[1]
            length2 = row[2]
            
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
    
    
    
    
    
    
    
    
    
    
    
    
    
