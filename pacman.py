import numpy
import pygame
import sys

# Initialize pygame
pygame.init()

clock = pygame.time.Clock()

# Constants for grid dimensions and cell size
GRID_WIDTH = 30
GRID_HEIGHT = 15
CELL_SIZE = 20

# Colors
LIGHT_GREY = (211, 211, 211)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Create a window
window = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
pygame.display.set_caption('Algorithm Testing GUI')

# Agent and goal
agent_img = pygame.image.load('agent.png')
goal_img = pygame.image.load('goal.png')
agent_img = pygame.transform.scale(agent_img, (CELL_SIZE, CELL_SIZE))
goal_img = pygame.transform.scale(goal_img, (CELL_SIZE, CELL_SIZE))

# Initial positions of the agent and goal
agent_pos = [0, 0]  # (x, y)
goal_pos = [GRID_WIDTH-1, GRID_HEIGHT-1]  # (x, y)

# Flags to indicate if the agent or goal is being dragged
dragging_agent = False
dragging_goal = False

# Define the buttons
start_button = pygame.Rect(10, GRID_HEIGHT * CELL_SIZE + 10, 80, 30)
pause_button = pygame.Rect(100, GRID_HEIGHT * CELL_SIZE + 10, 80, 30)

# Define a font object to render text
font = pygame.font.Font(None, 36)  # You can also specify a font file instead of using the default font

# Inside your main loop
for event in pygame.event.get():
    # ... existing event handling code ...
    if event.type == pygame.MOUSEBUTTONDOWN:
        if start_button.collidepoint(event.pos):
            # Start the BFS algorithm
            print('Start BFS')
        elif pause_button.collidepoint(event.pos):
            # Pause the BFS algorithm
            print('Pause BFS')

# Drawing the buttons
pygame.draw.rect(window, (0, 255, 0), start_button)  # Green for start
pygame.draw.rect(window, (255, 0, 0), pause_button)  # Red for pause

# Grid

# Create a grid initialized with all cells as empty
grid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = WHITE if grid[y][x] else LIGHT_GREY
            pygame.draw.rect(window, color, pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(window, (200, 200, 200), pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)  # Grid lines
    # Draw agent and goal
    window.blit(agent_img, (agent_pos[0]*CELL_SIZE, agent_pos[1]*CELL_SIZE))
    window.blit(goal_img, (goal_pos[0]*CELL_SIZE, goal_pos[1]*CELL_SIZE))

def handle_click(pos, erase=False):
    global dragging_agent, dragging_goal  # Make sure to use the global variables
    x, y = pos
    grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
    print(f'Click at: {grid_x}, {grid_y}')  # Debug print
    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
        # Check if the agent or goal is clicked
        if (grid_x, grid_y) == agent_pos:
            print('Agent clicked')  # Debug print
            dragging_agent = True
            return  # Return early to skip the wall addition/erasure code
        elif (grid_x, grid_y) == goal_pos:
            print('Goal clicked')  # Debug print
            dragging_goal = True
            return  # Return early to skip the wall addition/erasure code
        else:
            grid[grid_y][grid_x] = 0 if erase else 1  # Set cell state based on erase flag

def handle_mouse_motion(pos):
    global dragging_agent, dragging_goal, agent_pos, goal_pos  # Ensure you're updating the global variable
    x, y = pos
    grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
        if dragging_agent:
            agent_pos[0], agent_pos[1] = grid_x, grid_y
        elif dragging_goal:
            goal_pos[0], goal_pos[1] = grid_x, grid_y

def is_over_sprite(pos, sprite_pos):
    x, y = pos
    grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
    return (grid_x, grid_y) == sprite_pos


drawing = False
erasing = False
last_move_time = 0


# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                drawing = True
                handle_click(event.pos)
            elif event.button == 3:  # Right mouse button
                erasing = True
                handle_click(event.pos, erase=True)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                drawing = False
            elif event.button == 3:  # Right mouse button
                erasing = False
        elif event.type == pygame.MOUSEMOTION:
            handle_mouse_motion(event.pos)
            if drawing:
                handle_click(event.pos)
            elif erasing:
                handle_click(event.pos, erase=True)

    current_time = pygame.time.get_ticks()

    # if event.type == pygame.KEYDOWN:
    keys = pygame.key.get_pressed()
    if current_time - last_move_time >= 1000:  # Check if at least 0.5 seconds have passed

        if keys[pygame.K_w] and agent_pos[1] > 0:
            agent_pos[1] -= 1
            print(f'UP Action at: {agent_pos[0]}, {agent_pos[1]}')  # Debug print
        elif keys[pygame.K_a] and agent_pos[0] > 0:
            agent_pos[0] -= 1
            print(f'LEFT Action at: {agent_pos[0]}, {agent_pos[1]}')
        elif keys[pygame.K_s] and agent_pos[1] < GRID_HEIGHT - 1:
            agent_pos[1] += 1
            print(f'DOWN Action at: {agent_pos[0]}, {agent_pos[1]}')
        elif keys[pygame.K_d] and agent_pos[0] < GRID_WIDTH - 1:
            agent_pos[0] += 1
            print(f'RIGHT Action at: {agent_pos[0]}, {agent_pos[1]}')

    # Drawing the buttons
    pygame.draw.rect(window, (0, 255, 0), start_button)  # Green for start
    pygame.draw.rect(window, (255, 0, 0), pause_button)  # Red for pause

    # Drawing the text
    start_text = font.render('Start', True, (0, 0, 0))  # Black text
    pause_text = font.render('Pause', True, (0, 0, 0))  # Black text
    window.blit(start_text, (start_button.x + 10, start_button.y + 5))
    window.blit(pause_text, (pause_button.x + 10, pause_button.y + 5))

    mouse_pos = pygame.mouse.get_pos()
    if is_over_sprite(mouse_pos, agent_pos) or is_over_sprite(mouse_pos, goal_pos):
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)  # Change to hand cursor (or another cursor of your choice)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)  # Change back to default arrow cursor
    
    draw_grid()
    pygame.display.flip()
    clock.tick(10)