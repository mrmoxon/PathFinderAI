import nashpy as nash
import numpy as np
# A = np.array([[1, -1], 
#               [-1, 1]])
# matching_pennies = nash.Game(A)
# print(matching_pennies)

# B1 = np.array([[3, 0], [5, 1]])
# B2 = np.array([[3, 5], [0, 1]])

# prisoners_dilemma = nash.Game(B1, B2)
# print(prisoners_dilemma)


A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
rps = nash.Game(A)
print(rps)
B = - A # This line represents the payoff matrix for the second player
# Here it is a zero sum game so utilities are inverted
rps2 = nash.Game(B)
print(rps2)

print('\n/// Rock v. Paper \n')
sigma_r = [0, 0, 1] # Rock
sigma_c = [0, 1, 0] # Paper
# Which wins? Rock or Paper? 
print(rps[sigma_r, sigma_c])

print('\n/// If Rock and Paper Play Mixed Strategy \n')
# Player 1 (column) sometimes plays Rock and sometimes Paper (never Scissors)
sigma_c = [1 / 2, 1 / 2, 0]
# Player 2 (row) sometimes plays Scissors and sometimes Paper (never Rock)
sigma_r = [0, 1 / 2, 1 / 2]

# When row plays Paper and column plays Paper, they draw.
# When row plays Paper and column plays Rock, row wins.
# When row plays Scissors and column plays Paper, row wins.
# When row plays Scissors and column plays Rock, column wins.

# This calculates expected utility over the course of the game,
# For row this is +0.25, as it wins 0.25% of the time, when it plays paper and column plays rock. There is no expected utlity when playing scissors as it loses as much as it wins.
# For column this is -0.25, as it loses 0.25% of the time, when it plays paper and row plays scissors.
print(rps[sigma_r, sigma_c])

print('\n/// Nash Equilibria \n')
eqs = rps.support_enumeration()
# We expect that the only Nash equilibrium is when both players play the mixed strategy
print(list(eqs))
# We get 0.3333 for each strategy, which is the expected utility for each move; they should be played with equal probability



print('\n/// NEXT... \n')
# Question a
# A = np.array([[3, 2], [1, 4]])
# B = np.array([[3, 4], [1, 2]])

# Question b
# A = np.array([[-1, 1], [2, -1]])
# B = np.array([[-1, 2], [1, -1]])

# Question c
A = np.array([[3, 1], [2, 4]])
B = np.array([[3, 1], [4, 2]])
game = nash.Game(A, B)
print(game)

# Dominant Strategy
def check_dominant_strategy(matrix):
    # Check each row for dominant strategy
    row_dominant = []
    for i in range(matrix.shape[0]):
        if all(matrix[i, j] >= matrix[k, j] for j in range(matrix.shape[1]) for k in range(matrix.shape[0]) if k != i):
            row_dominant.append(i)

    # Check each column for dominant strategy
    col_dominant = []
    for j in range(matrix.shape[1]):
        if all(matrix[i, j] >= matrix[i, k] for i in range(matrix.shape[0]) for k in range(matrix.shape[1]) if k != j):
            col_dominant.append(j)

    return row_dominant, col_dominant

# Check for dominant strategies in matrices A and B
dominant_A = check_dominant_strategy(A)
dominant_B = check_dominant_strategy(B)

print("\nDominant Strategy for P1:", dominant_A, "\nDominant Strategy for P1:", dominant_B)

# Nash Equilibrium
print("\nNash Equilibrium:\n")
equilibria = game.support_enumeration()
print(list(equilibria)) # If long list, group into chornological pairs


pareto_optimal = []
for i in range(2):
    for j in range(2):
        current_outcome = (A[i, j], B[i, j])
        better_exists = any(
            (A[k, l] >= current_outcome[0] and B[k, l] >= current_outcome[1] and 
             (A[k, l] > current_outcome[0] or B[k, l] > current_outcome[1]))
            for k in range(2) for l in range(2)
        )
        if not better_exists:
            pareto_optimal.append((i, j))

print("\nPareto Optimal Outcomes:", pareto_optimal)

max_welfare = -np.inf
max_welfare_outcome = None

for i in range(2):
    for j in range(2):
        total_welfare = A[i, j] + B[i, j]
        if total_welfare > max_welfare:
            max_welfare = total_welfare
            max_welfare_outcome = (i, j)

print("\nOutcome that Maximizes Social Welfare:", max_welfare_outcome)


