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
def grid_values(puzzle_str):
    puzzle_dict = dict()
    boxes = cross(g_rows, g_cols)
    # Puzzle_str must be the same size as boxes
    for index, boxval in enumerate(puzzle_str):
        puzzle_dict[boxes[index]] = boxval

    return puzzle_dict

# Global vars - labels for the board
g_rows = 'ABCDEFGHI'
g_cols = '123456789'

### Script Below ###
# All boxes on the board
boxes = cross(g_rows, g_cols)
print(boxes)

# Unit sets as lists
row_units = [cross(row, g_cols) for row in g_rows]
col_units = [cross(col, g_rows) for col in g_cols]

# Hardcode the square units
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# Concat all the unit sets into a master set
unitlist = row_units + col_units + square_units
print(unitlist)

print(grid_values('..0..2.1.2.2..234..21.23.2'))
