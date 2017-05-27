# -*- coding: utf-8 -*-
"""
Created on Fri May 26 16:19:34 2017

@author: Stu
"""
# Stu Minshull
# Spring 2017
# Udacity AI Nanodegree
#########################
# A labeled Sudoku Board
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

# Globally define useful sets, under the cross function
# All boxes on the board
boxes = cross(rows, cols)

# The possible unit sets
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Diagonal Units
# A1 -> I9
ldiag_unit = [z[0]+z[1] for z in zip(rows, cols)] 
# A9 -> I1
rdiag_unit = [z[0]+z[1] for z in zip(rows, reversed(cols))]

# List of all units
unitlist = row_units + column_units + square_units # + topleftdiag_unit + trdiag_unit

# Dictionaries keyed by box tag: units containing a box & peers of a box
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


### TESTING ###
diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
norm_sudoku_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

# List to hold moves made on the board
assignments = []
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid_dict = dict()
    boxes = cross(rows, cols)

    # Assumes grid is encoded as rows starting from the top left corner A1
    for index, boxval in enumerate(grid):
        # Convert empty boxes from . to all possible vals
        if boxval == '.':
            boxval = '123456789'
        grid_dict[boxes[index]] = boxval

    return grid_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    # From project
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
        

def eliminate(values):
    """
    Loop through all boxes - if a box has a value assigned, remove that 
    value from all of its peers' possible values
    """
    for box in boxes:
        if len(values[box]) == 1:
            digit = values[box]
            # Box has a placed value, so remove it from it's peers values
            for peer in peers[box]:
                values[peer] = values[peer].replace(digit,'')

    return values

def only_choice(values):
    """
    Loop through all units - for every unit with a box that is the only 
    possible space for a digit, assign that digit to that box
    In: Sudoku in dict form
    Out: Altered sudoku in dict form
    """
    
    for unit in unitlist:
        # Create a list of all boxes containing the current digit
        for digit in '123456789':
            contains_digit = []
            for index, box in enumerate(unit):
                # If the current digit is possible
                if digit in values[box]:
                    contains_digit.append((box))
                    
            # Assign the current digit to its only possible space
            if len(contains_digit) == 1:
                #assign_value(values, contains_digit[0], digit)
                values[contains_digit[0]] = digit
                
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_before = 0
        for box in values:
            if len(values[box]) == 1:
                solved_before += 1
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_after = 0
        for box in values:
            if len(values[box]) == 1:
                solved_after += 1
        
        if solved_before == solved_after:
            stalled = True
            
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Implement a depth-first search approach to solve the board.
    Apply reduce puzzle, then select the board with the fewest possibilities.
    Follow this pattern recursively until a solved board is found, or no
    more boards exist
    """
    
    values = reduce_puzzle(values)
    
    # Puzzle has no solution
    if values is False:
        return False
    
    # puzzle is already solved
    if all(len(values[s]) == 1 for s in boxes): 
        return values
    
    # Begin solving the puzzle
    # OOB assignment
    fewest = -1
    for box in values:
        if (fewest == -1 or (len(values[box]) < len(fewest))):
            # Don't consider solved boxes
            if len(values[box]) == 1:
                pass
            else:
                fewest = box

    # We've selected a box with the min pos, solve recursively by placing
    # a value in the space & attempting to solve
    for value in values[fewest]:
        trial_board = values.copy()
        trial_board[fewest] = value
        
        # If we succeed, return the board!
        attempt = search(trial_board)
        if attempt:
            return attempt
        
        
        

### SOLVE ###
#norm_grid = grid_values(norm_sudoku_grid)
#
#display(norm_grid)
#print('*************************************************************')
#display(reduce_puzzle(norm_grid))

#diag_grid = grid_values(diag_sudoku_grid)
#
#display(diag_grid)
#print('*************************************************************')
#display(reduce_puzzle(diag_grid))

dfs = search(grid_values(norm_sudoku_grid))
print('*************************************************************')
display(dfs)