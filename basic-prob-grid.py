import tkinter as tk
import random
import math

# This has toggle buttons that allow you to switch between modes.
# Can splash new positive/negative probabilities into the grid, or modify them pixel-by-pixel.

class DynamicGrid:
    def __init__(self, master, rows, cols):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()
        self.squares = {}  # To store square IDs and their attributes

        self.lines = []  # To store line IDs

        self.modify_mode = True  # The switch for turning on/off the increase/decrease functionality

        self.increase_mode = True

        self.create_grid()
        self.create_switch_button()
        self.create_reverse_button()

    def create_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                x1, y1 = i * 50, j * 50
                x2, y2 = x1 + 50, y1 + 50
                initial_value = round(random.uniform(0.01, 0.99), 2)
                color = "#{:02x}{:02x}{:02x}".format(0, int(initial_value * 255), 0)
                square_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                line_id = self.canvas.create_line((x1 + x2) / 2, y1, (x1 + x2) / 2, y2, fill="#CCCCCC")
                self.lines.append(line_id)

                label = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{initial_value:.2f}")
                # self.squares[square_id] = {'value': initial_value, 'label': label, 'x1': x1, 'x2': x2}

                self.squares[square_id] = {'value': initial_value, 'label': label, 'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2}

                self.canvas.tag_bind(square_id, '<Button-1>', self.handle_click)

    def create_switch_button(self):
        button = tk.Button(self.master, text="Toggle Modify Mode", command=self.toggle_modify_mode)
        button.pack()

    def toggle_modify_mode(self):
        self.modify_mode = not self.modify_mode

        for line_id in self.lines:
            new_state = 'hidden' if not self.modify_mode else 'normal'
            self.canvas.itemconfig(line_id, state=new_state)

    def handle_click(self, event):
        square_id = self.canvas.find_closest(event.x, event.y)[0]
        
        if self.modify_mode:
            self.modify_value(event, square_id)
        else:
            # Other behavior when modify_mode is off
            print(f"Clicked square {square_id} while in alternate mode.")

    def modify_value(self, event, square_id):
        x1, x2 = self.squares[square_id]['x1'], self.squares[square_id]['x2']
        midpoint = (x1 + x2) / 2

        if event.x > midpoint:
            self.squares[square_id]['value'] = min(self.squares[square_id]['value'] + 0.01, 1)
        else:
            self.squares[square_id]['value'] = max(self.squares[square_id]['value'] - 0.01, 0)

        self.update_square(square_id)

    def update_square(self, square_id):
        value = self.squares[square_id]['value']
        color = "#{:02x}{:02x}{:02x}".format(0, int(value * 255), 0)
        self.canvas.itemconfig(square_id, fill=color)
        self.canvas.itemconfig(self.squares[square_id]['label'], text=f"{value:.2f}")

    def create_reverse_button(self):
        button = tk.Button(self.master, text="Toggle Increase/Decrease", command=self.toggle_increase_mode)
        button.pack()

    def toggle_increase_mode(self):
        self.increase_mode = not self.increase_mode

    def propagate_values(self, clicked_square_id):
        clicked_x, clicked_y = self.get_square_center(clicked_square_id)

        for square_id, square_data in self.squares.items():
            x, y = self.get_square_center(square_id)
            distance = self.calculate_distance(clicked_x, clicked_y, x, y)
            
            # Incremental update based on distance
            increment = self.calculate_increment(distance)

            if self.increase_mode:
                new_value = min(square_data['value'] + increment, 1)
            else:
                new_value = max(square_data['value'] - increment, 0)
            
            # Update if the new value is greater than the current value
            # if new_value > square_data['value']:
            #     self.squares[square_id]['value'] = new_value
            #     self.update_square(square_id)

            if new_value != square_data['value']:
                self.squares[square_id]['value'] = new_value
                self.update_square(square_id)

    def get_square_center(self, square_id):
        x1, x2 = self.squares[square_id]['x1'], self.squares[square_id]['x2']
        y1, y2 = self.squares[square_id]['y1'], self.squares[square_id]['y2']
        return (x1 + x2) / 2, (y1 + y2) / 2

    def calculate_distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def calculate_increment(self, distance):
        sigma = 100  # Standard deviation, controls the "spread" of the curve
        increment = math.exp(-distance ** 2 / (2 * sigma ** 2))
        return increment

    # In your handle_click method:
    def handle_click(self, event):
        square_id = self.canvas.find_closest(event.x, event.y)[0]
        if self.modify_mode:
            self.modify_value(event, square_id)
        else:
            self.propagate_values(square_id)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dynamic Grid")
    grid = DynamicGrid(root, 10, 10)
    root.mainloop()
