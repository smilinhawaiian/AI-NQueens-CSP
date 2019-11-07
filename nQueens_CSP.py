# Final Project
# AI-NQueens-CSP
# March 17, 2019
# Sharice Mayer

import numpy as np
from matplotlib import pyplot as plt
import random
import time
from timeit import default_timer as timer


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
        self.board_queens = Queens(n)
        # board square space
        self.board_squares = np.empty((n,n), Square)
        #initialize squares
        for row in range(n):
            for col in range(n):
                self.board_squares[row,col] = Square(0, row, col)

    def print_board(self):
        print('--------------------------------------------------------')
        for row in range(self.n):
            a_row = np.empty((self.n,0), int)
            for col in range(self.n):
                a_row = np.append(a_row, str(self.board_squares[row,col].get_state()))
            print((*a_row), sep='  ')
        print('--------------------------------------------------------')


    def print_final_board(self):
        #print('----------------Final Solution--------------------------')
        for row in range(self.n):
            a_row = np.empty((self.n,0), int)
            for col in range(self.n):
                if(str(self.board_squares[row,col].get_state()) == 'Q'):
                    a_row = np.append(a_row, str(self.board_squares[row,col].get_state()))
                else:
                    a_row = np.append(a_row, str('-'))
            print((*a_row), sep='')
        #print('--------------------------------------------------------')

    def update_board(self, a_queen, flag):
        q_position = a_queen.get_position()
        row = q_position[0]
        col = q_position[1]
        up = 1
        q_up = -1
        if(flag != 1):#remove the queen
            up = -1
            q_up = 0
        # update rows and cols
        self.board_squares[row,col].update_square(q_up)
        for i in range(self.n):
            self.board_squares[i, col].update_square(up)
            self.board_squares[row, i].update_square(up)
        # update the queen space
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

    # build a recursive instead of iterative function for this later
    def solve(self, num_queens, board):
        # set current state space
        state_space_list = np.empty((self.n,0),Board)
        # set queens list (concurrent to state space list) -- can zip later
        queens_list = self.board_queens
        state_space_list = np.append(state_space_list, (board))
        current_board = board
        working_board = board
        # for printing
        #for i in state_space_list:
        #    i.print_board()
        for a_queen in range(num_queens, self.n+1):
            free_space = []
            #print(f"value of a_queen: {a_queen}")
            #print(f"value of num_queen: {num_queens}")
            curr_queen = queens_list.get_queen(a_queen-1)# index is -1 queen number
            # find possible free locations
            free_space = current_board.get_free_spaces(curr_queen)
            if not free_space:
                #print("COLLISION! - Rollback")
                # remove a queen
                bad_queen = curr_queen
                # remove the board
                working_board = state_space_list[-1]
                state_space_list = np.delete(state_space_list, -1)
                # re-set to re-place the queen
                working_board.update_board(bad_queen, -1)
                bad_queen.update_position(-1, -1)# queen has no position -- must be placed again
                # make sure that spaces we've used before are not valid in get_free_space
                # choose a new spot   #RECURSIVE
                queen_to_replace = a_queen - 1
                queens_left = self.n - queen_to_replace - 1
                #print(f"queens left: {queens_left}")
            else:
                # update working board
                working_board = current_board
                #choose a random free space for the queen -- later use mrv/lcv? constraints
                free_space_coord = random.choice(free_space)
                space_coord = free_space_coord.get_coord()
                # add queen to random available square
                curr_queen.update_position(space_coord[0], space_coord[1])
                # add queen to list
                queens_list.update_queen(curr_queen, a_queen)
                # update the board spaces
                working_board.update_board(curr_queen, 1)
                #print(f'----------------Queen number: {a_queen}-------------------------')
                #working_board.print_board()
                state_space_list = np.append(state_space_list, working_board)
            #update board
            current_board = working_board
            print(f"Length of queens list:{a_queen}")
        return state_space_list

    # returns squares with constraint value == 0
    def get_free_spaces(self, current_queen):
        available_spaces = []
        seen_list = current_queen.get_seen_positions()
        for row in range(self.n):
            for col in range(self.n):
                if((self.board_squares[row,col].get_state()) == 0):
                    available_spaces.append(self.board_squares[row,col])
        return available_spaces


class Queen:
    def __init__(self):
        self.my_row = -1
        self.my_col = -1
        x = self.my_row
        y = self.my_col
        self.position = (x,y)
        initial_loc = self.position
        self.seen_positions = np.array([(x,y)])

    def update_position(self, row, col):
        x = self.my_row
        y = self.my_col
        pair = np.array([x, y]).astype(int)####
        pair.shape = (1,2)
        #print(f"up seen_positions = {self.seen_positions}")
        #print(f"\t type:{type(self.seen_positions)} and dims:{(self.seen_positions).shape}")
        if((x < 0) or (y < 0)):
            self.seen_positions[:,0] = row
            self.seen_positions[:,1] = col
        else:
            self.seen_positions = np.append((self.seen_positions), pair, axis=0)
            #print(f"update seen_positions = {self.seen_positions}")
            #print(f"\t type:{type(self.seen_positions)} and dims:{(self.seen_positions).shape}")
        self.my_row = row
        self.my_col = col
        self.position = np.array([row, col])

    def get_position(self):
        #print(f"get position {(self.position)}")
        #print(f"get position type:{type(self.position)} and dims:{np.ndim(self.position)}")
        return self.position

    def get_seen_positions(self):
        #print(f"get seen_positions {(self.seen_positions)}")
        #print(f"get seen_positions type:{type(self.seen_positions)} and dims:{(self.seen_positions).shape}")
        return self.seen_positions

class Queens:
    def __init__(self, num_queens):
        self.num_queens = (num_queens+1)
        self.queens_list = [Queen() for index in range(num_queens+1)]

    def get_queen(self, index):
        queen = self.queens_list[index]
        return queen

    def add_queen(self, index):
        self.num_queens += 1
        self.queens_list.append(Queen(index))

    def update_queen(self, queen, index):
        position = queen.get_position()
        (self.queens_list[index]).update_position(position[0], position[1])


if __name__ == "__main__":

    min_val = 4
    max_val = 100
    times = []
    single_run_max = 250
    #create a new board
    for n in range(min_val,  max_val):
        start_time = timer()
        board = Board(n)
        #print('----------------Starting board--------------------------')
        #board.print_board()
        #print('--------------------------------------------------------')
        solution_set = board.solve(1, board)
        solution = solution_set[-1]

        end_time = timer()
        time_taken = end_time - start_time
        times.append(time_taken)

    single_board = Board(single_run_max)
    single_solution_set = single_board.solve(1,single_board)
    single_solution = single_solution_set[-1]
    print(f"Solution for {single_run_max} Queens:\n")
    solution.print_final_board()


    #time vs numberofqueens puzzle solved

    #plotting
    plt.figure(figsize=(100,100))
    x = range(min_val, max_val)#time intervals to test x queens each -- "eggs"
    plt.title('Testing 4-100 queens')
    plt.plot(x, times)
    plt.xlabel("Number of Queens")
    plt.ylabel("Time taken (Seconds)")
    plt.savefig('NPuzzle_With_Constraint_Propagation_Performance_Comparison.png', bbox_inches='tight')


    plt.show() # stops the program! Only do at the end


