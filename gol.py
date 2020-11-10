import os, time, random

w, h = 130, 65
board = [False for _ in range(w * h)]
def set_at(board, x, y, val):
    # Set value at position [x][y] to val
    board[x + y * w] = val

def cell_at(board, x, y):
    # if any of those are false, return False, else, return True
    return x >= 0 and y >= 0 and x < w and y < h and board[x + y * w]

def nb(board, x,  y) -> int:
    # get living neighbour count
    return len(list(filter(lambda e: e, [
        cell_at(board, x-1, y-1),
        cell_at(board, x,   y-1),
        cell_at(board, x+1, y-1),

        cell_at(board, x-1, y),
        cell_at(board, x+1, y),

        cell_at(board, x-1, y+1),
        cell_at(board, x,   y+1),
        cell_at(board, x+1, y+1),
    ])))

# Generate random board
for y in range(h):
    for x in range(w):
        set_at(board, x, y, random.randint(0, 1) == 1)

# Glider
# set_at(board, 3, 5, True)
# set_at(board, 4, 5, True)
# set_at(board, 5, 5, True)
# set_at(board, 5, 4, True)
# set_at(board, 4, 3, True)

line = " +"*(w+1)
while True:
    os.system('clear')
    old = board[:]
    print(line)
    for y in range(h):
        print("+ ", end="")
        for x in range(w):
            if cell_at(old, x, y):
                print("🮋🮋", end="")
            else:
                print("  ", end="")
            n = nb(old, x, y)
            set_at(board, x, y,
                   (cell_at(old, x, y) and n == 2) or n == 3
                   )
        print(" +")
    print(line)
    time.sleep(0.2)
