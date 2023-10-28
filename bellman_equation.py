import numpy as np
import tkinter as tk
import time

# Initialize Tkinter GUI
root = tk.Tk()
root.title("Grid World")
frame = tk.Frame(root)
frame.pack()

# Constants for grid dimensions and cell size

# Grid dimensions
GRID_WIDTH = 4
GRID_HEIGHT = 4

# Reward
REWARD_STATE = (4, 1) # *
COST_STATES = [(4, 4), (1, 1)] # !
OBSTACLES = [(2, 3), (3, 2)] # X

# Possible actions: up, down, left, right
ACTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
# 0.8 CHANCE OF MOVING IN CHOSEN DIRECTION
# 0.1 CHANCE OF MOVING EITHER LEFT OR RIGHT

#                      U(s) = R(s) + Y * max(a belongs to A(s)) sum(s') P(s' | s, a) * U(s')

initial_utility = 0
reward_all_cells = -0.04
gamma = 0.99
reward_state_value = 10  # Reward for the reward state
cost_state_value = -5  # Cost for the cost states

epsilon = 1e-6


global U

# Initialize utility grid
U = np.zeros((GRID_HEIGHT, GRID_WIDTH))

# Initialize special state values
U[GRID_HEIGHT - REWARD_STATE[0], REWARD_STATE[1] - 1] = reward_state_value
for cost_state in COST_STATES:
    U[GRID_HEIGHT - cost_state[0], cost_state[1] - 1] = cost_state_value

# Value Iteration
def value_iteration_step(epsilon=1e-6, gamma=0.99):
    global U
    U_new = U.copy()
    delta = 0
    
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            state = (GRID_HEIGHT - i, j + 1)
            if state in [REWARD_STATE] + COST_STATES + OBSTACLES:
                continue
            
            # Calculate new utility for the state
            max_utility = -float('inf')
            for action in ACTIONS:
                next_i, next_j = i + action[0], j + action[1]
                if 0 <= next_i < GRID_HEIGHT and 0 <= next_j < GRID_WIDTH:
                    utility = U[next_i, next_j]
                    max_utility = max(max_utility, utility)
            
            U_new[i, j] = reward_all_cells + gamma * max_utility
            delta = max(delta, abs(U_new[i, j] - U[i, j]))
    
    # Update utility grid
    U = U_new

    converged = delta < epsilon

    print(U)

    return U, converged

def on_space_press(event):
    # global U
    _, converged = value_iteration_step(U)
    
    # Update the Tkinter grid here based on new U values
    for i in range(1, GRID_HEIGHT + 1):
        for j in range(1, GRID_WIDTH + 1):
            state = (GRID_HEIGHT - i + 1, j)  # Reversed i coordinate
            button = buttons[state]
            
            if state in [REWARD_STATE] + COST_STATES + OBSTACLES:
                continue
            
            # Update button text to new utility value, rounded for readability
            button.config(text=str(round(U[GRID_HEIGHT - i, j - 1], 2)))

# Bind spacebar to on_space_press function
root.bind('<space>', on_space_press)

# Add row numbers
for i in range(1, GRID_HEIGHT + 1):
    label = tk.Label(frame, text=str(i), width=5, height=2)
    label.grid(row=GRID_HEIGHT - i, column=0)

# Add column numbers (x-axis)
for j in range(1, GRID_WIDTH + 1):
    label = tk.Label(frame, text=str(j), width=10, height=2)
    label.grid(row=GRID_HEIGHT, column=j)

buttons = {}
# Add grid buttons
for i in range(1, GRID_HEIGHT + 1):
    for j in range(1, GRID_WIDTH + 1):
        state = (GRID_WIDTH - i + 1, GRID_HEIGHT - j + 1)
        text = "0"  # Default to open cell
        bg_color = "white"
        fg_color = "black"

        if state == REWARD_STATE:
            text = "*"
            bg_color = "green"

        elif state in COST_STATES:
            text = "!"
            bg_color = "orange"

        elif state in OBSTACLES:
            text = "X"
            bg_color = "black"
            fg_color = "white"

        
        button = tk.Button(frame, text=text, width=10, height=2, bg=bg_color, fg=fg_color)
        button.grid(row=GRID_HEIGHT - i, column=j)  # Adjusted row and column positioning
        buttons[state] = button

root.mainloop()
