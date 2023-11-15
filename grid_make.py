import numpy as np
import tkinter as tk
import time



def initialize_grid(grid):

    print(grid)

    rows = grid.strip().split('\n')
    cleaned_rows = []
    for row in rows:
        cleaned_row = row.strip().split(' ')
        cleaned_rows.append(cleaned_row)

    # Convert spaces to 0 and split each row into columns
    rows = [row.split(' ') for row in rows]

    matrix = np.array(cleaned_rows)
    matrix = np.flip(matrix, axis=0)

    print(matrix)

    return matrix



def parse_grid(matrix):

    reward_positions, cost_positions, obstacle_positions = [], [], []

    for i in range (matrix.shape[0]):
        for j in range (matrix.shape[1]):
            # print(i+1, j+1)
            cell = matrix[i, j]
            pos = (i+1, j+1)
            if cell == '*':
                print("Reward: ", pos)
                REWARD_STATE = (pos) # *
                reward_positions.append(pos)
            elif cell == '!':
                print("Cost: ", pos)
                COST_STATES = [pos] # !
                cost_positions.append(pos)
            elif cell == 'X':
                print("Obstacle: ", pos)
                OBSTACLES = [pos] # X
                obstacle_positions.append(pos)
            
    print("Reward Positions: ", reward_positions)
    print("Cost Positions: ", cost_positions)
    print("Obstacle Positions: ", obstacle_positions)

    return reward_positions, cost_positions, obstacle_positions



def initialize_gui(frame, GRID_HEIGHT, GRID_WIDTH, reward_positions, cost_positions, obstacle_positions):

    # Add row numbers
    for i in range(1, GRID_HEIGHT + 1):
        label = tk.Label(frame, text=str(i), width=5, height=2)
        label.grid(row=GRID_HEIGHT - i, column=0)

    # Add column numbers (x-axis)
    for j in range(1, GRID_WIDTH + 1):
        label = tk.Label(frame, text=str(j), width=10, height=2)
        label.grid(row=GRID_HEIGHT, column=j)

    # Add grid buttons
    buttons = {}
    for i in range(1, GRID_HEIGHT + 1):
        for j in range(1, GRID_WIDTH + 1):
            state = (i, j)
            text = "0"  # Default is an open cell
            bg_color = "white"
            fg_color = "black"

            if state in reward_positions:
                text = "*"
                bg_color = "green"

            elif state in cost_positions:
                text = "!"
                bg_color = "orange"

            elif state in obstacle_positions:
                text = "X"
                bg_color = "black"
                fg_color = "white"

            
            button = tk.Button(frame, text=text, width=10, height=2, bg=bg_color, fg=fg_color)
            button.grid(row=GRID_HEIGHT - i, column=j)  # Adjusted row and column positioning
            buttons[state] = button



if __name__ == '__main__':

    grid = """
    ! 0 0 * 0 0 !
    * ! * X * ! *
    0 ! X 0 X ! 0
    0 ! 0 X 0 ! 0
    """

    # Initialize Tkinter GUI
    root = tk.Tk()
    root.title("Grid World")
    frame = tk.Frame(root)
    frame.pack()

    matrix = initialize_grid(grid)
    num_rows, num_cols = matrix.shape
    print("axis 1: ", matrix.shape[0])
    print("axis 2: ", matrix.shape[1])

    reward_positions, cost_positions, obstacle_positions = parse_grid(matrix)

    # Grid dimensions
    GRID_WIDTH = num_cols
    GRID_HEIGHT = num_rows

    initialize_gui(frame, GRID_HEIGHT, GRID_WIDTH, reward_positions, cost_positions, obstacle_positions)

    root.mainloop()
