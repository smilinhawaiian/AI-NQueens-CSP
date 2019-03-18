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
        self.state = state# -1 if queen, 0, 1, ... N otherwise
        self.x = x
        self.y = y

    def update_square(self, new_state):
        if(self.state != -1):#it's not a queen - update
            self.state += new_state
        elif(new_state == 0):# remove the queen
            self.state = 0

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
            #a_row = []
            a_row = np.empty((self.n,0), int)
            for col in range(self.n):
                #a_row.append(self.board_squares[row,col].get_state())
                #a_row = np.append(a_row, str(self.board_squares[row,col].get_state()))
                a_row = np.append(a_row, str(self.board_squares[row,col].get_state()))
            print((*a_row), sep='  ')
        print('--------------------------------------------------------')

    def update_board(self, a_queen, flag):
        q_position = a_queen.get_position()
        row = q_position[0]
        col = q_position[1]
        up = 1
        q_up = -1
        if(flag != 1):#remove the queen
            up = -1
            q_up = 0
            #self.board_squares[row,col].update_square(0)
            #print(self.board_squares[row,col].get_state())
        #else:
            # update the queen space
            #self.board_squares[row, col].update_square(-1)
            #print(self.board_squares[row,col].get_state())
        # update rows and cols
        self.board_squares[row,col].update_square(q_up)
        for i in range(self.n):
            self.board_squares[i, col].update_square(up)
            self.board_squares[row, i].update_square(up)
            #print(self.board_squares[row,col].get_state())
        self.board_squares[row,col].update_square(q_up)
        # update diagonals
        x_dn = row
        y_up = col
        while(((x_dn-1) >= 0) and ((y_up+1) < self.n)):
            x_dn -= 1
            y_up += 1
            self.board_squares[x_dn, y_up].update_square(up)
        x_dn = row
        y_dn = col
        while(((x_dn-1) >= 0) and ((y_dn-1) >= 0)):
            x_dn -= 1
            y_dn -= 1
            self.board_squares[x_dn, y_dn].update_square(up)
        x_up = row
        y_up = col
        while(((x_up+1) < self.n) and ((y_up+1) < self.n)):
            x_up += 1
            y_up += 1
            self.board_squares[x_up, y_up].update_square(up)
        x_up = row
        y_dn = col
        while(((x_up+1) < self.n) and ((y_dn-1) >= 0)):
            x_up += 1
            y_dn -= 1
            self.board_squares[x_up, y_dn].update_square(up)
        #print(self.board_squares[row,col].get_state())

    # build a recursive instead of iterative function for this later
    def solve(self, num_queens, board):
        # set current state space
        state_space_list = np.empty((num_queens,0),Board)
        # set queens list (concurrent to state space list) -- can zip later
        queens_list = []
        state_space_list = np.append(state_space_list, (board))
        first_board = board # for testing
        current_board = board
        working_board = board
        # for printing
        #for i in state_space_list:
        #    i.print_board()
        for a_queen in range(num_queens):
            free_space = []
            # find possible free locations
            free_space = current_board.get_free_spaces()
            if not free_space:
                print("COLLISION! - Rollback")#placeholder
                # remove a queen
                bad_queen = queens_list.pop()
                # remove the board
                working_board = state_space_list[-1]
                state_space_list = np.delete(state_space_list, -1)
                # re-set to re-place the queen
                working_board.update_board(bad_queen, -1)
                bad_queen.update_position(-1, -1)# queen has no position -- must be placed again
                # choose a new spot
                #print(a_queen+1)
            else:
                # update working board
                working_board = current_board
                #choose a random free space for the queen -- later use mrv/lcv? constraints
                free_space_coord = random.choice(free_space)
                space_coord = free_space_coord.get_coord()
                # add queen to random available square
                curr_queen = Queen(a_queen)
                curr_queen.update_position(space_coord[0], space_coord[1])
                # add queen to list
                queens_list.append(curr_queen)
                # update the board spaces
                working_board.update_board(curr_queen, 1)
                print(f'----------------Queen number: {a_queen+1}-------------------------')
                working_board.print_board()
                state_space_list = np.append(state_space_list, working_board)
            #update board
            current_board = working_board
        return state_space_list

    # returns squares with constraint value == 0
    def get_free_spaces(self):
        available_spaces = []
        for row in range(self.n):
            for col in range(self.n):
                if((self.board_squares[row,col].get_state()) == 0):
                    available_spaces.append(self.board_squares[row,col])
        return available_spaces


class Queen:
    def __init__(self, my_number):
        self.my_number = my_number# which queen am I - do I need this?
        self.my_row = -1
        self.my_col = -1
        self.position = (self.my_row, self.my_col)
        self.seen_positions = []

    def update_position(self, row, col):
        if(self.my_row != -1):# add current to seen positions
            self.seen_positions.append(self.position)
        # update position
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

    solution_set = board.solve(n, board)
    solution = solution_set[-1]
    print("Solution:\n")
    solution.print_board()




