import numpy as np
import sys
"""We start by assuming we know the letters in our hand and the letters on the board. The letters on the board are in a 100x100 (arbitrary size) grid.
We save the letters on the grid and their position, and then iterate through the possible plays. 
Using Scrabble 2022 dictionary
Assumptions:
Only look for solutions with one intersection to the current board state (no double word creation)
No blank tiles (can change later)
Grid position (0, 0) is at the top left
"""

def prettyprint(grid):
    for i in range(len(grid)):
        pretty_row = []
        for j in range(len(grid)):
            pretty_row.append(grid[i, j].decode())
        print(pretty_row)


def free_space(counter):
    # checks how many horizonal and vertical spaces around tile are free
    row, col = grid_positions[counter]
    #print(str(row) + " " + str(col))
    free_left = 0
    free_right = 0
    free_up = 0
    free_down = 0

    for j in reversed(range(col)):
        if row != 0 and row != grid_size - 1:
            if grid_state[row, j] == b'0' and grid_state[row + 1, j] == b'0' and grid_state[row - 1, j] == b'0':
                free_left += 1
            else:
                break
        elif row != 0:
            if grid_state[row, j] == b'0' and grid_state[row - 1, j] == b'0':
                free_left += 1
            else:
                break
        else:
            if grid_state[row, j] == b'0' and grid_state[row + 1, j] == b'0':
                free_left += 1
            else:
                break
    for j in range(1, grid_size - col):
        if row != 0 and row != grid_size - 1:
            if grid_state[row, col + j] == b'0' and grid_state[row + 1, col + j] == b'0' and grid_state[row - 1, col + j] == b'0':
                free_right += 1
            else:
                break
        elif row != 0:
            if grid_state[row, col + j] == b'0' and grid_state[row + 1, col + j] == b'0':
                free_right += 1
            else:
                break
        else:
            if grid_state[row, col + j] == b'0' and grid_state[row - 1, col + j] == b'0':
                free_right += 1
            else:
                break
    for j in reversed(range(row)):
        if col != 0 and col != grid_size - 1:
            if grid_state[j, col] == b'0' and grid_state[j, col + 1] == b'0' and grid_state[j, col - 1] == b'0':
                free_up += 1
            else:
                break
        elif col != 0:
            if grid_state[j, col] == b'0' and grid_state[j, col - 1] == b'0':
                free_up += 1
            else:
                break
        else: 
            if grid_state[j, col] == b'0' and grid_state[j, col + 1] == b'0':
                free_up += 1
            else:
                break
    for j in range(1, grid_size - row):
        if col != 0 and col != grid_size - 1:
            if grid_state[row + j, col] == b'0' and grid_state[row + j, col + 1] == b'0' and grid_state[row + j, col - 1] == b'0':
                free_down += 1
            else:
                break
        elif col != 0:
            if grid_state[row + j, col] == b'0' and grid_state[row + j, col - 1] == b'0':
                free_down += 1
            else:
                break
        else:
            if grid_state[row + j, col] == b'0' and grid_state[row + j, col + 1] == b'0':
                free_down += 1
            else:
                break
    return free_left, free_right, free_up, free_down

data = iter(open("dictionary.txt", "r"))

grid_size = 11
letter_value = {'A':1 , 'B':3, 'C':3, 'D':2, 'E':1, 'F':4, 
                'G':2, 'H':4, 'I':1, 'J':8, 'K':5, 'L':1, 
                'M':3, 'N':1, 'O':1, 'P':3, 'Q':10, 'R':1, 
                'S':1, 'T':1, 'U':1, 'V':8, 'W':4, 'X':8, 'Y':4, 'Z':10}
grid_state = np.chararray((grid_size, grid_size))
grid_state[:] = b'0'

player_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
grid_state[5, 6] = 'C'
grid_state[5, 7] = 'H'
grid_state[5, 8] = 'A'
grid_state[5, 9] = 'N'
grid_state[5, 10] = 'T'
grid_state[4, 7] = 'A'
prettyprint(grid_state)

def findBestMove(first_move=False):
    words = []
    for element in data:
        stripped = element.strip("\n")
        words.append(stripped.split(" "))

    grid_letters = []
    grid_positions = []
    for i in range(grid_size):
        for j in range(grid_size):
            if grid_state[i, j] != b'0':
                grid_letters.append(grid_state[i, j])
                grid_positions.append([i, j])

    #print(grid_positions)
    #print(grid_letters)

    plays = []
    for i in range(len(grid_letters)):
        # check how many horizonal and vertical spaces around tile are free
        free_left, free_right, free_up, free_down = free_space(i)
        letter = grid_letters[i].decode()
        #print(letter)
        row, col = grid_positions[i]

        axes = np.array([free_left, free_right, free_up, free_down])
        #print("free spaces: " + str(axes))
        free_grid = np.array([free_left + free_right, free_up + free_down])
        free_spaces = max(free_grid)

        #find whether free space is horizontal or vertical
        free_axis = np.argmax(free_grid)
        negative_direction = axes[free_axis*2]
        positive_direction = axes[free_axis*2 + 1]

        #check to make sure we're not at a corner or an intersection
        if free_spaces > 0 and negative_direction > 0 and positive_direction > 0:
            #iterate through list of words to find possible combinations with tiles in player hand (left/right and up/down)

            #check whether words in dictionary are shorter than the number of free spaces
            #check whether words only use letters in the player's hand
            possible_plays = []
            for line in words:
                word = line[0]
                player_letters_temp = player_letters.copy()
                player_letters_temp.append(letter)
                if len(word) < free_spaces:
                    for l in range(len(word)):
                        if player_letters_temp.count(word[l]) > 0:
                            player_letters_temp.remove(word[l])
                        else:
                            break
                        if l == len(word) - 1:
                            possible_plays.append(word)
                            break
            #print(possible_plays)

            #check whether tile location in the word will not interfere with freespace amount
            for word in possible_plays:
                tile_locations = []
                for l in range(len(word)):
                    if word[l] == letter:
                        tile_locations.append(l)
                for location in tile_locations:
                    if negative_direction - (location + 1) > 0 and positive_direction - (len(word) - (location + 1)) > 0:
                        plays.append([word, row, col, location, free_axis])

    #print(plays)
    scores = []
    #calculate number of points for each possible play
    for possible_play in plays:
        word = possible_play[0]
        points = 0
        for l in range(len(word)):
            points += letter_value[word[l]]
        scores.append(points)

    #find highest-scoring play
    best_play = plays[np.argmax(scores)]
    word = best_play[0]
    tile_position = [best_play[1], best_play[2]]

    print("best play: " + str(word))
    print("tile position: " + str(tile_position))
    print("points: " + str(scores[np.argmax(scores)]))

    tile_in_word = best_play[3]
    #print(tile_in_word)
    #0 - horizontal, 1 - vertical
    axis_orientation = best_play[4]
    #print("axis orientation: " + str(axis_orientation))
    for i in range(len(word)):
        if i != tile_in_word:
            if i < tile_in_word:
                grid_state[tile_position[0] - (axis_orientation)*(tile_in_word - i), tile_position[1] - (1 - axis_orientation)*(tile_in_word - i)] = word[i]
            elif i > tile_in_word:
                grid_state[tile_position[0] + (axis_orientation)*(i - tile_in_word), tile_position[1] + (1 - axis_orientation)*(i - tile_in_word)] = word[i]
    prettyprint(grid_state)











    
