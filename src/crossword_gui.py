import crossword_tools
import tkinter
import copy

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
        def fn():
            if btn.selected:
                btn.selected = False
                selected_tile_map.set_val(c, r, False)
                btn.configure(background="grey", activebackground="grey")
            else:
                btn.selected = True
                selected_tile_map.set_val(c, r, True)
                btn.configure(background="white", activebackground="white")
        return lambda: fn()

    def on_enter_click(root):
        root.destroy()
        callback(crossword_tools.generate_puzzle_from_selected_tile_map(selected_tile_map))
        
    root = tkinter.Tk()
    for r in range(canvas_height):
        for c in range(canvas_width):
            btn = tkinter.Button(root, borderwidth=1, height="2", width="2",
                                 background="grey", activebackground="grey")
            btn.selected = False
            selected_tile_map.set_val(c, r, False)
            btn.configure(command=on_button_click(btn, r, c))
            btn.grid(row=r,column=c)
    enter = tkinter.Button(root, borderwidth=1, background="grey", text="enter",
                         command=lambda: on_enter_click(root))
    enter.grid(row=(r + 1), column=0, columnspan=canvas_width)
    root.mainloop()  

# position with the corresponding ID
def display_puzzle_solutions(puzzle, solution_set, new_puzzle):
    """
    Displays the solutions to the puzzle in a new window. Calls new_puzzle if
    the user choses to create a new puzzle.
    
    Args:
        puzzle: A crossword_tools.Puzzle object representing the puzzle that
                was solved.
        solution_set: A list of solutions to the puzzle, where each solution
                      is a dictionary mapping every line id in the puzzle to
                      a string that goes at that line.
        new_puzzle: A function that takes no arguments, and restarts the puzzle
                    creation process
    """
    
    solution_coord_maps = crossword_tools.get_puzzle_coordmaps(puzzle, solution_set)
    display_coordmaps_on_pages(solution_coord_maps, solution_coord_maps[0].get_max_x() + 1, solution_coord_maps[0].get_max_y() + 1, new_puzzle)

def display_coordmaps_on_pages(coordmaps, grid_width, grid_height, new_puzzle):
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
                    grid_tiles[x][y].configure(text=char_at_tile, background="white", activebackground="white")
                else:
                    grid_tiles[x][y].configure(text=" ", background="grey", activebackground="grey")
    
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
    
    def new_puzzle():
        """
        Hides the current window and restarts the crossword generation process
        """
        
        root.destroy()
        new_puzzle()
    
    if not coordmaps:
        return
        
    root = tkinter.Tk()
    for x in range(grid_width):
        grid_tiles.append([])
        for y in range(grid_height):
            # using a button here because tkinter is bad at formatting labels
            tile = tkinter.Button(root, borderwidth=1, height="2", width="2", 
                                  background="grey", activebackground="grey", 
                                  disabledforeground="black",
                                  state=tkinter.DISABLED, font=("Monospace", 12))
            grid_tiles[x].append(tile)
            tile.grid(row=y, column=x)

    if len(coordmaps) <= 1:
        next_btn_state = tkinter.DISABLED
    else:
        next_btn_state = tkinter.NORMAL
        
    next_btn = tkinter.Button(borderwidth=1, background="grey", text=">", state=next_btn_state)
    prev_btn = tkinter.Button(borderwidth=1, background="grey", text="<", state=tkinter.DISABLED)
    retry_btn = tkinter.Button(borderwidth=1, background="grey", text="new puzzle", command=new_puzzle)
    
    next_btn.configure(command=lambda: next_page(next_btn, prev_btn))
    prev_btn.configure(command=lambda: prev_page(next_btn, prev_btn))
    
    next_btn.grid(row=grid_height, column=grid_width - 2, columnspan=2)
    prev_btn.grid(row=grid_height, column=0, columnspan=2)
    retry_btn.grid(row=grid_height, column=int(grid_width / 2 - 1), columnspan = 2 + grid_width % 2)
    
    display_coordmap(coordmaps[0])
    root.mainloop()
