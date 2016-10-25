import crossword_tools
import constants
import tkinter

# callback must take a puzzle as an argument
def display_crossword_generation_window(canvas_width, canvas_height, callback):
    """
    Displays a grid to the user which they can click to select different grid
    tiles, forming a crossword puzzle. Calls the callback function with the 
    puzzle formed by the tiles the user clicked.
    
    Args:
        canvas_width: The width, in tiles, the crossword creation grid should 
                      be.
        canvas_height: The height, in tiles, the crossword creation grid should
                       be.
        callback: A function that takes a crossword_tools.Puzzle object as its
                  only argument. This function will be called after the user
                  designs their crossword puzzle, and will be created from the
                  user input.
    """
    
    selected_tile_map = crossword_tools.CoordMap()

    def on_button_click(btn, r, c):
        """
        Generates a lambda function that should be called when the button at
        row r and column c is clicked.
        
        Args:
            btn: The button that is having the lambda function set as its
                 click action.
            r: The row at which btn is placed in the grid.
            c: The column at which btn is placed in the grid.
        """
        
        # We have this inner function in here, instead of just making a
        # lambda function where we set the button click action, because it
        # makes the btn, r, and c values equal to their values at when the
        # on_button_click function was called, instead of their current values,
        # which would cause them to have the same value for all buttons.
        def fn():
            if btn.selected:
                btn.selected = False
                selected_tile_map.set_val(c, r, False)
                btn.configure(background=constants.GUI_DESELECTED_TILE_COLOR, 
                              activebackground=constants.GUI_DESELECTED_TILE_COLOR)
            else:
                btn.selected = True
                selected_tile_map.set_val(c, r, True)
                btn.configure(background=constants.GUI_SELECTED_TILE_COLOR, 
                              activebackground=constants.GUI_SELECTED_TILE_COLOR)
        return lambda: fn()

    def on_enter_click(root):
        root.destroy()
        callback(crossword_tools.generate_puzzle_from_selected_tile_map(selected_tile_map))
        
    root = tkinter.Tk()
    
    for r in range(canvas_height):
        for c in range(canvas_width):
            btn = tkinter.Button(root, borderwidth=1, height="2", width="2",
                                 background=constants.GUI_DESELECTED_TILE_COLOR, 
                                 activebackground=constants.GUI_DESELECTED_TILE_COLOR)
            btn.selected = False
            selected_tile_map.set_val(c, r, False)
            btn.configure(command=on_button_click(btn, r, c))
            btn.grid(row=r,column=c)
            
    enter = tkinter.Button(root, borderwidth=1, 
                           background=constants.GUI_DESELECTED_TILE_COLOR, 
                           text=constants.ENTER_BTN_TEXT,
                           command=lambda: on_enter_click(root))
    enter.grid(row=(r + 1), column=0, columnspan=canvas_width)
    
    root.mainloop()  

def display_puzzle_solutions(puzzle, solution_set, new_puzzle):
    """
    Displays the solutions to the puzzle in a new window. Calls new_puzzle if
    the user chooses to create a new puzzle.
    
    Args:
        puzzle: A crossword_tools.Puzzle object representing the puzzle that
                was solved.
        solution_set: A list of solutions to the puzzle, where each solution
                      is a dictionary mapping every line id in the puzzle to
                      a string that goes at that line.
        new_puzzle: A function that takes no arguments, and restarts the puzzle
                    creation process
    """

    def on_restart_button():
        """
        Hides the current window and restarts the crossword generation process
        """
        
        new_puzzle()
    
    solution_coord_maps = crossword_tools.get_puzzle_coordmaps(puzzle, solution_set)
    display_coordmaps_on_pages(solution_coord_maps, 
                               solution_coord_maps[0].get_max_x() + 1, 
                               solution_coord_maps[0].get_max_y() + 1, 
                               True, constants.NEW_PUZZLE_BTN_TEXT, 
                               on_restart_button, True)

def display_coordmaps_on_pages(coordmaps, grid_width, grid_height,
                               show_middle_btn=False, middle_btn_text=None,
                               middle_button_action=None, 
                               close_on_middle_btn=False):
    """
    Displays the values of each of the provided coordmaps on a page, where the
    user can navigate through the pages using navigation buttons.
    
    Args:
        coordmaps: A list of crossword_tools.CoordMap objects that are going to
                   be displayed to the user
        grid_width: The width, in tiles, the portion of the grid displaying
                    the coordmaps must be in order to show all of them properly
        grid_height: The height, in tiles, the portion of the grid displaying
                     the coordmaps must be in order to show all of them properly
        show_middle_btn: True if the button centered below the grid should be
                         shown
        middle_btn_text: The text of the button at the bottom of the grid if it
                         is visible
        middle_button_action: The action preformed when the middle button is
                              is clicked
        close_on_middle_btn: True if the window generated by this function
                             should close when the middle button is clicked
        
    """
    
    MIN_WIDTH = 6
    BORDER_WIDTH = 1
    
    grid_width = max(grid_width + 2 * BORDER_WIDTH, MIN_WIDTH)
    grid_height = grid_height + 2 * BORDER_WIDTH
    num_coordmaps = len(coordmaps)
    grid_tiles = []
    current_page = 0
    
    def display_coordmap(coordmap):
        """
        Modifies the tkinter elements stored in grid_tiles to display the
        information stored in the provided coordmap.
        
        Args:
            coordmap: A crossword_tools.CoordMap object that will be displayed
                      to the user.
        """

        for x in range(len(grid_tiles)):
            for y in range(len(grid_tiles[x])):
                char_at_tile = coordmap.get_val(x - BORDER_WIDTH, y - BORDER_WIDTH)
                if char_at_tile:
                    grid_tiles[x][y].configure(text=char_at_tile, 
                                               background=constants.GUI_SELECTED_TILE_COLOR, 
                                               activebackground=constants.GUI_SELECTED_TILE_COLOR)
                else:
                    grid_tiles[x][y].configure(text=" ", 
                                               background=constants.GUI_DESELECTED_TILE_COLOR, 
                                               activebackground=constants.GUI_DESELECTED_TILE_COLOR)
    
    def next_page(next_page_btn, prev_page_btn):
        """
        Displays the CoordMap following the currently visible CoordMap in the
        coordmaps list to the user.
        
        Args:
            next_page_btn: The tkinter button for the next page button
            prev_page_btn: The tkinter button for the previous page button
        """
        
        nonlocal current_page
        if current_page + 1 >= num_coordmaps:
            return
        
        current_page = current_page + 1
        if current_page + 1 >= num_coordmaps:
            next_page_btn.configure(state=tkinter.DISABLED)
        
        prev_page_btn.configure(state=tkinter.NORMAL)
        
        display_coordmap(coordmaps[current_page])
        
    def prev_page(next_page_btn, prev_page_btn):
        """
        Displays the CoordMap preceding the currently visible CoordMap in the
        coordmaps list to the user.
        
        Args:
            next_page_btn: The tkinter button for the next page button
            prev_page_btn: The tkinter button for the previous page button
        """
        
        nonlocal current_page
        if current_page <= 0:
            return
        
        current_page = current_page - 1
        if current_page <= 0:
            prev_page_btn.configure(state=tkinter.DISABLED)

        next_page_btn.configure(state=tkinter.NORMAL)
            
        display_coordmap(coordmaps[current_page])
    
    def on_middle_btn_click(root):
        """
        The action run when the button at the bottom of the window is clicked,
        closes the window if required and runs the middle_button_action if 
        required
        
        Args:
            root: The root element of the window created by the parent function
        """
        
        if close_on_middle_btn:
            root.destroy()
        
        if middle_button_action:
            middle_button_action()
    
    if not coordmaps:
        return
        
    root = tkinter.Tk()
    
    for x in range(grid_width):
        grid_tiles.append([])
        for y in range(grid_height):
            # Using a button here because tkinter is bad at formatting labels.
            # Not super happy about it though.
            tile = tkinter.Button(root, borderwidth=1, height="2", width="2", 
                                  background=constants.GUI_DESELECTED_TILE_COLOR, 
                                  activebackground=constants.GUI_DESELECTED_TILE_COLOR, 
                                  disabledforeground="black",
                                  state=tkinter.DISABLED, font=("Monospace", 12))
            grid_tiles[x].append(tile)
            tile.grid(row=y, column=x)

    if len(coordmaps) <= 1:
        next_btn_state = tkinter.DISABLED
    else:
        next_btn_state = tkinter.NORMAL
        
    next_btn = tkinter.Button(borderwidth=1, 
                              background=constants.GUI_DESELECTED_TILE_COLOR, 
                              text=constants.RIGHT_BTN_TEXT, 
                              state=next_btn_state)
    prev_btn = tkinter.Button(borderwidth=1, 
                              background=constants.GUI_DESELECTED_TILE_COLOR, 
                              text=constants.LEFT_BTN_TEXT, 
                              state=tkinter.DISABLED)
    middle_btn = tkinter.Button(borderwidth=1, 
                               background=constants.GUI_DESELECTED_TILE_COLOR, 
                               text=middle_btn_text, 
                               command=lambda: on_middle_btn_click(root))
    
    next_btn.configure(command=lambda: next_page(next_btn, prev_btn))
    prev_btn.configure(command=lambda: prev_page(next_btn, prev_btn))
    
    next_btn.grid(row=grid_height, column=grid_width - 2, columnspan=2)
    prev_btn.grid(row=grid_height, column=0, columnspan=2)
    middle_btn.grid(row=grid_height, column=int(grid_width / 2 - 1), 
                   columnspan = 2 + grid_width % 2)
    
    display_coordmap(coordmaps[0])
    
    root.mainloop()
