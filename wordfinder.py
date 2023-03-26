import numpy as np
"""We start by assuming we know the letters in our hand and the letters on the board. The letters on the board are in a 100x100 (arbitrary size) grid.
We save the letters on the grid and their position, and then iterate through the possible plays. 
Using Scrabble 2022 dictionary
Assumptions:
Only look for solutions with one intersection to the current board state (no double word creation)
No blank tiles (can change later)
Grid position (0, 0) is at the bottom left
"""

data = iter(open("dictionary.txt", "r"))
words = []
for element in data:
    stripped = element.strip("\n")
    words.append(stripped.split(" "))

player_letters = []
grid_letters = []
grid_positions = []
grid_state = []

def free_space(i):
    # checks how many horizonal and vertical spaces around tile are free, returns 4x1 vector 
    x, y = grid_positions[i]
    free_left = 0
    free_right = 0
    free_up = 0
    free_down = 0
    for j in range(100 - y):
        if grid_state[x, j + y] == None:
            free_up += 1
        else:
            break
    for j in reversed(range(y)):
        if grid_state[x, j] == None:
            free_down += 1
        else:
            break
    for j in range(100 - x):
        if grid_state[x + j, y] == None:
            free_right += 1
        else:
            break
    for j in reversed(range(x)):
        if grid_state[j, y] == None:
            free_left += 1
        else:
            break
    return [free_left, free_right, free_up, free_down]

for i in range(len(grid_letters)):
    # check how many horizonal and vertical spaces around tile are free
    free_left, free_right, free_up, free_down = free_space(i)
    letter = grid_letters[i]

    #iterate through list of words to find possible combinations with tiles in player hand (left/right and up/down)
    short_list = []
    for word in words:
        for l in range(word):
            if word[l] == letter:
                short_list.append(word)
