import sys
import csv
import numpy as np

SNAKE_SIZE = 7

def generate_random_grid():
    """Generate a random grid if none if passed in the command line"""
    size = np.random.randint(10, 100)
    grid = np.zeros((size,size), np.int32)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            grid[i,j] = np.random.randint(1, 257)
    np.savetxt('random.csv', grid, fmt='%d',  delimiter=';')
    return grid

def load_grid():
    """Load the grid from the file passed in the command line"""
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if len(sys.argv) > 2:
            delimiter = sys.argv[2]
        else:
            delimiter = ';'
        with open(input_file, 'r') as f:
            reader = csv.reader(f, delimiter=delimiter)
            l = list(reader)
        return np.array(l).astype("int")
    else:
        return generate_random_grid()

def get_shapes(shape, shapes, n):
    """Generate all possible snake shape respecting the problem specification"""
    if len(shape)==7:
        #apply an offset if there is any negative coordinate
        minx = min(shape, key=lambda x: x[0])[0]
        if minx<0:
            shape = [(x-minx, y) for x, y in shape]
        miny = min(shape, key=lambda x: x[1])[1]
        if miny<0:
            shape = [(x, y-miny) for x, y in shape]

        #sort the coords so the same shape found through different paths will be ignored
        shape.sort()
        if shape not in shapes:
            shapes.append(shape)
    else:
        x, y = shape[-1]
        if     (x+1, y)   not in shape \
           and (x+2, y)   not in shape \
           and (x+1, y+1) not in shape \
           and (x+1, y-1) not in shape:
            new_shape = shape + [(x+1, y)]
            shapes = get_shapes(new_shape, shapes, n)
        if     (x,   y+1) not in shape \
           and (x,   y+2) not in shape \
           and (x+1, y+1) not in shape \
           and (x-1, y+1) not in shape:
            new_shape = shape + [(x, y+1)]
            shapes = get_shapes(new_shape, shapes, n)
        if     (x-1, y)   not in shape \
           and (x-2, y)   not in shape \
           and (x-1, y+1) not in shape \
           and (x-1, y-1) not in shape:
            new_shape = shape + [(x-1, y)]
            shapes = get_shapes(new_shape, shapes, n)
        if     (x,   y-1) not in shape \
           and (x,   y-2) not in shape \
           and (x+1, y-1) not in shape \
           and (x-1, y-1) not in shape:
            new_shape = shape + [(x, y-1)]
            shapes = get_shapes(new_shape, shapes, n)
    return shapes

def share_cells(a, b):
    "Check whether two snakes share any cell"""
    for cell in a:
        if cell in b:
            return True
    return False

def get_matching_snake(snakes, new_snake, value):
    """Given one snake, find one with the same sum of cell's values"""
    if value not in snakes.keys():
        snakes[value] = [new_snake]
        return None
    else:
        for snake in snakes[value]:
            if not share_cells(snake, new_snake):
                return snake
        snakes[value].append(new_snake)
    return None

def search_snakes(grid):
    """Search through the grid for two snakes with the same sum of the cell's values
       using the pre-generated shapes
    """
    snakes = dict()
    shapes = get_shapes([(0, 0)], [], SNAKE_SIZE)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            for shape in shapes:
                value = 0
                snake = [(x+i, y+j) for x, y, in shape]
                for x, y in snake:
                    if x<grid.shape[0] and  y<grid.shape[1]:
                        value += grid[x, y]
                    else:
                        value = 0
                        break
                if value > 0:
                    match = get_matching_snake(snakes, snake, value)
                    if match != None:
                        return [match, snake]
    return []

def adjust_indices(snake):
    """Adjust the indices to start from 1 instead of 0"""
    return [(x+1, y+1) for x, y in snake]

grid = load_grid()
result = search_snakes(grid)
with open('output.txt', 'w') as f:
    if len(result) == 0:
        f.write('Fail')
    else:
        f.write(str(adjust_indices(result[0])))
        f.write('\n')
        f.write(str(adjust_indices(result[1])))





