import random
import re

class Board():
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board()
        self.assign_values_to_board()

        self.dug = set() # will contain tuples of (row,col) to track which locations we have already dug in

    

    def make_new_board(self):
        board = [[0 for _ in range(self.dim_size)] for _ in range(self.dim_size)] # this generates a grid/array of None values with the dimensions in dim_size
        bombs_planted = 0
        while bombs_planted < self.num_bombs: # check how many bombs we have already planted until we reach the desired number
            loc = random.randint(0, self.dim_size**2 -1) # assign a random location on the board
            row = loc // self.dim_size # find the row to plant the bomb by using floor divide (how many times does the dimension size go into the location)
            col = loc % self.dim_size # find the column by using the remainder (how far into the row we have to go)

            if board[row][col] == "*":
                continue # continue if a bomb already exists in this location

            board[row][col] = "*" # plant a bomb
            bombs_planted += 1 # increase the number of bombs planted

        return board

    def assign_values_to_board(self): # assign values from 0 to 8 to all empty spaces to represent how many neighbouring bombs there are
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*": # if this place is a bomb, don't calculate anything
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r, c) # assign the number of surrounding bombs

    def get_num_neighbouring_bombs(self, row, col):
        # iterate through all neighbouring positions and sum the number of bombs
        num_neighbouring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):  # make sure not to go out of bounds
                if r == row and c == col:
                    continue # skip the oroginal location
                if self.board[r][c] == "*":
                    num_neighbouring_bombs += 1
        return num_neighbouring_bombs
    
    def dig(self, row, col):
        self.dug.add((row,col)) # keep track of dug locations

        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True
        
         # when self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r,c) in self.dug:
                    continue # don't dig visited places
                self.dig(r, c)
        return True
    
    def __str__(self): # return a string that shows the board to the player
        visible_board = [[0 for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " "

        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def play_the_game(dim_size=10, num_bombs=10):
    # 1. create the board
    board = Board(dim_size, num_bombs)

    # 2. show the board and ask for where to dig
    # 3. show a game over screen or continue digging
    # 4. continue untill there are no more places to dig
    safe = True

    while len(board.dug) < board.dim_size**2 - num_bombs:
        print(board)
        user_input = re.split(",(\\s)*", input("Where would you like to dig? Input row,col: ")) # split the input at the comma, while ignoring any spaces after the comma
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location - out of bounds. Try again.")
            continue

        safe = board.dig(row, col)
        if not safe:
            break # game over, we don't allow the player to dig anymore

    if safe:
        print("You win! Congratulations!")
    else:
        print("Game over! Sorry!")
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == "__main__":
    play_the_game()
