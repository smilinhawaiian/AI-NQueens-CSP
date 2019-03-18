# Final Group Project
# AI-NQueens-CSP
# March 17, 2019
# Sharice Mayer
# Tyler Race
# Daniel Song
# Ching-Wei Lin

import numpy as np
import random
import time

# replace this code with something prompting for user to enter number of queens desired
n = 4

class Square:
    def __init__(self, state, x, y):
        self.state = state
        self.x = x
        self.y = y

    def update_square(self, new_state):
        if(self.state != -1):#it's not a queen
            self.state += new_state

    def get_state(self):
        if(self.state == -1):
            return "Q"
        else:
            return self.state

    def get_coord(self):
        coord = (self.x, self.y)
        return coord


class Board:
    def __init__(self, n):
        self.n = n
        self.board_size = n*n
        # board square space
        self.board_squares = np.empty((n,n), Square)
        #initialize squares
        for row in range(n):
            for col in range(n):
                self.board_squares[row,col] = Square(0, row, col)

    def print_board(self):
        print('--------------------------------------------------------')
        for row in range(self.n):
            a_row = []
            for col in range(self.n):
                a_row.append(self.board_squares[row,col].get_state())
            print(a_row)
        print('--------------------------------------------------------')

    def solve(self, num_queens, board):
        # set current state space
        state_space_list = np.empty((num_queens,0),Board)
        # set queens concurrent to state space list
        queens_list = []
        state_space_list = np.append(state_space_list, (board))
        current_board = board
        # for printing
        #for i in state_space_list:
        #    i.print_board()
        for a_queen in range(num_queens):
            free_space = []
            # find possible locations
            free_space = current_board.get_free_spaces()
            if not free_space:
                # remove a queen
                # spool everything back
                print("List is empty")#placeholder
            else:
                #choose a random free space for the queen -- later use constraints
                free_space_coord = random.choice(free_space)
                space_coord = free_space_coord.get_coord()
                # add queen to random available square
                curr_queen = Queen(a_queen)
                curr_queen.update_position(space_coord[0], space_coord[1])
                #print(curr_queen.get_position())
                # add queen to list
                queens_list.append(curr_queen)

    def get_free_spaces(self):
        available_spaces = []
        coordinates = np.empty((self.n,self.n),int)
        for row in range(self.n):
            for col in range(self.n):
                if((self.board_squares[row,col].get_state()) == 0):
                    available_spaces.append(self.board_squares[row,col])
        return available_spaces


class Queen:
    def __init__(self, my_number):
        self.my_number = my_number# which queen am I
        self.my_row = -1
        self.my_col = -1
        self.position = (self.my_row, self.my_col)

    def update_position(self, row, col):
        self.my_row = row
        self.my_col = col
        self.position = (self.my_row, self.my_col)

    def get_position(self):
        return self.position




if __name__ == "__main__":
    #create a new board
    board = Board(n)
    print('----------------Starting board--------------------------')
    board.print_board()
    print('--------------------------------------------------------')
    board.solve(n, board)




