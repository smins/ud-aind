###
# Udacity AI Nanodegree
# Sudoku Solver
# Stu Minshull 5.4.2017
###

### Functions

# Returns all combinations of the contents of lists a & b
def cross(a, b):
    return [s+t for s in a for t in b]

# Returns a dictionary representation of the sudoku puzzle
def grid_values(grid):
    rows = 'ABCDEFGHI'
    cols = '123456789'

    grid_dict = dict()
    boxes = cross(rows, cols)

    for index, boxval in enumerate(grid):
        # Convert empty boxes from . to all possible vals
        if boxval == '.':
            boxval = '123456789'
        grid_dict[boxes[index]] = boxval

    return grid_dict

# If a box contains a single value, remove that value from all peers
def eliminate(values):

    rows = 'ABCDEFGHI'
    cols = '123456789'

    # Generate all the needed lists
    boxes = cross(rows, cols)
    # Unit lists
    row_units = [cross(row, cols) for row in rows]
    col_units = [cross(rows, col) for col in cols]
    square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
    # Combine the units into a master list
    unitlist = row_units + col_units + square_units
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    # Create a dict containing lists of peers for each box, keyed by box label
    peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)

    # Get the list of all boxes with only 1 possible values
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        # Grab the digit of each box
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')

    return values

def only_choice(values):
    rows = 'ABCDEFGHI'
    cols = '123456789'

    # Generate all the needed lists
    boxes = cross(rows, cols)
    # Unit lists
    row_units = [cross(row, cols) for row in rows]
    col_units = [cross(rows, col) for col in cols]
    square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
    # Combine the units into a master list
    unitlist = row_units + col_units + square_units

    # Loop through all units
    for unit in unitlist:
        # Loop through each digit, generating a list of boxes containing it
        for digit in '123456789':
            digit_boxes = [box for box in unit if digit in values[box]]
            if len(digit_boxes) == 1:
                # Only 1 box contains this digit, so assign it that value
                values[digit_boxes[0]] = digit

    return values
    
### Script Below ###
rows = 'ABCDEFGHI'
cols = '123456789'

# All boxes on the board
boxes = cross(rows, cols)

print(grid_values('..0..2.1.2.2..234..21.23.2'))
