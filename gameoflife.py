from PIL import Image
import os
import sys
import time
from colorama import Fore as f
from colorama import Back as b
from colorama import Style

def get_pixels(path: str) -> list:
    img = Image.open(path)
    if tuple(img.size) == (32, 32):
        pixels = []
        raw = img.getdata()
        for rgb in raw:
            if rgb[0] == 255:
                pixels.append(1)
            else:
                pixels.append(0)
        return pixels
    return False

def px(y: int, x: int) -> int:
    return y * 32 + x

def is_alive(pixels, y: int, x: int) -> bool:
    return True if pixels[px(y, x)] == 1 else False

def valid(coor):
    return True if coor >= 0 and coor <= 31 else False

def get_x_neigh(pixels, x: int, y: int) -> int:
    ng = 0
    # Left
    if x > 0 and valid(y):
        if is_alive(pixels, y, x-1):
            ng += 1
    # Right
    if x < 31 and valid(y):
        if is_alive(pixels, y, x+1):
            ng += 1
    return ng

def get_y_neigh(pixels, x: int, y: int) -> int:
    ng = 0
    # Above
    if y > 0 and valid(x):
        if is_alive(pixels, y-1, x):
            ng += 1
    # Below
    if y < 31 and valid(x):
        if is_alive(pixels, y+1, x):
            ng += 1
    return ng

def get_neigh(pixels, x: int, y: int) -> int:
    ng = 0
    # Horizontal
    ng += get_x_neigh(pixels, x, y)
    # print("Horizontal:", get_x_neigh(pixels, x, y))
    # Vertical
    ng += get_y_neigh(pixels, x, y)
    # print("Vertical:", get_y_neigh(pixels, x, y))
    # Diagonal - Top
    ng += get_x_neigh(pixels, x, y-1)
    # print("Diagonal - Top:", get_x_neigh(pixels, x, y-1))
    # Diagonal - Bottom
    ng += get_x_neigh(pixels, x, y+1)
    # print("Diagonal - Bottom:", get_x_neigh(pixels, x, y+1))
    return ng

def calc_pixel(pixels, y: int, x: int) -> bool:
    # Returns a boolean saying if the pixel will be alive (True)
    # or dead (False) next update
    alive = is_alive(pixels, y, x)
    ng = get_neigh(pixels, x, y)
    if alive:
        if ng < 2:
            return False
        elif ng == 2 or ng == 3:
            return True
    else:
        if ng == 3:
            return True
    return False

def set_pixel(pixels, y: int, x: int, new: int) -> None:
    pixels[px(y, x)] = new

def conways_game_of_life():
    pixels = get_pixels('con2.png')
    try:
        while True:
            x = 0
            y = 0
            # new_pixels is used to append each pixel after it has been updated. Used
            # so you can update each pixel "at the same time", as per Conway's Game of Life
            # rules.
            new_pixels = []
            # Calculate each cell's next state and add changes to the new_pixels list 
            for y in range(32):
                for x in range(32):
                    next_state = calc_pixel(pixels, y, x)
                    new_pixels.append(next_state)
            # Update pixels
            pixels = new_pixels[:]
            # Print pixels
            screen = ""
            for y in range(32):
                for x in range(32):
                    if is_alive(pixels, y, x):
                        screen += f"  "
                    else:
                        # If the pixel is dead, print two light-blue background spaces (blocks)
                        screen += f"{b.LIGHTBLUE_EX}  "
                    # Reset colors every cell
                    screen += Style.RESET_ALL
                screen += "\n"
            os.system('clear')
            # Print screen, used in favor of printing each cell individually, which causes stuttering as
            # the lower cells take longer to be printed
            print(screen)
            time.sleep(0.4)
    except KeyboardInterrupt:
        # If CTRL+C is pressed, exit gracefully, instead of throwing an exception
        os.system('clear')
        sys.exit(0)

# curses.wrapper(conways_game_of_life)
conways_game_of_life()

