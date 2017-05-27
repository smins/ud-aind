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
                stripped = values[peer].replace(digit,'')
                assign_value(values, peer, stripped)
                
    return values

def only_choice(values):
    """
    Loop through all units - for every unit with a box that is the only 
    possible space for a digit, assign that digit to that box
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
                assign_value(values, contains_digit[0], digit)
                
    return values

def reduce_puzzle(values):
    """
    While changes are still be applied (e.g. not stalled), iteratively 
    run the elimination then only_choice strategies. 
    
    If a puzzle stalls, return false. Otherwise, return the solved puzzle
    """
    
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
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return reduce_puzzle(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
