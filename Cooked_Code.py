from tkinter import *
from PIL import Image, ImageTk, ImageFilter, ImageGrab
import random
from collections import deque

class MazeGame:
    def __init__(self, width=20, height=20, cell_size=40):
        self.root = Tk()
        self.root.title('Maze Navigator')

        self.cell_size = cell_size
        self.canvas = Canvas(self.root, width=width * cell_size, height=height * cell_size, bg='black')
        self.canvas.pack()
        self.width = width
        self.height = height
        self.start = (1, 1)
        self.finish = (height - 2, width - 2)
        self.maze = self.generate_maze(width, height)  # Generate the maze
        self.current_position = self.start
        self.game_active = True  # Flag to track the game state
        self.move_count = 0  # Initialize move counter
        self.overlay = None  # Initialize overlay attribute

        self.load_images()  # Load images for the game
        self.draw_maze()  # Draw the maze on the canvas
        self.draw_player()  # Draw the player on the canvas

        self.root.bind("<KeyPress>", self.move)  # Bind keypress events to the move function
        self.root.focus_set()

        self.shortest_path_length = self.find_shortest_path_length()  # Calculate the shortest path length
        self.display_shortest_path_length()  # Display the shortest path length
        self.move_count_text = self.canvas.create_text(self.width * self.cell_size / 2, 40, text=f"Moves: {self.move_count}", font=('Helvetica', 16, 'bold'), fill='white')

        self.create_difficulty_selector()  # Create difficulty selector buttons

    def create_difficulty_selector(self):
        """Create radio buttons for selecting difficulty level."""
        self.difficulty_var = StringVar(value="Medium")
        difficulties = ["Easy", "Medium", "Hard"]
        for difficulty in difficulties:
            Radiobutton(self.root, text=difficulty, variable=self.difficulty_var, value=difficulty, command=self.set_difficulty).pack(side=LEFT)

    def set_difficulty(self):
        """Adjust the maze complexity based on the selected difficulty level."""
        difficulty = self.difficulty_var.get()
        if difficulty == "Easy":
            self.width, self.height = 10, 10
        elif difficulty == "Medium":
            self.width, self.height = 20, 20
        elif difficulty == "Hard":
            self.width, self.height = 30, 30

        # Adjust the maze complexity without resizing the window
        self.maze = self.generate_maze(self.width, self.height)
        self.current_position = self.start
        self.move_count = 0
        self.game_active = True
        self.canvas.delete("all")
        self.draw_maze()
        self.draw_player()
        self.shortest_path_length = self.find_shortest_path_length()
        self.display_shortest_path_length()
        self.move_count_text = self.canvas.create_text(self.width * self.cell_size / 2, 40, text=f"Moves: {self.move_count}", font=('Helvetica', 16, 'bold'), fill='white')

    def load_images(self):
        """Load images for the maze, walls, player, and goal."""
        base_path = "/Users/vishanamarnath/Library/CloudStorage/OneDrive-HagleyCommunityCollege/Maze 2024/"
        self.floor_image = ImageTk.PhotoImage(Image.open(base_path + "floor.png").resize((self.cell_size, self.cell_size)))
        self.wall_image = ImageTk.PhotoImage(Image.open(base_path + "wall.png").resize((self.cell_size, self.cell_size)))
        self.player_image = ImageTk.PhotoImage(Image.open(base_path + "player.png").resize((self.cell_size, self.cell_size)))
        self.goal_image = ImageTk.PhotoImage(Image.open(base_path + "goal.png").resize((self.cell_size, self.cell_size)))

    def draw_maze(self):
        """Draw the maze on the canvas."""
        for row in range(self.height):
            for col in range(self.width):
                x, y = col * self.cell_size, row * self.cell_size
                if self.maze[row][col] == 1:
                    self.canvas.create_image(x, y, image=self.wall_image, anchor=NW)
                else:
                    self.canvas.create_image(x, y, image=self.floor_image, anchor=NW)
        self.canvas.create_image(self.finish[1] * self.cell_size, self.finish[0] * self.cell_size, image=self.goal_image, anchor=NW)

    def draw_player(self):
        """Draw the player on the canvas."""
        x, y = self.start[1] * self.cell_size, self.start[0] * self.cell_size
        self.player = self.canvas.create_image(x, y, image=self.player_image, anchor=NW)

    def move(self, event):
        """Handle player movement based on keypress events."""
        if not self.game_active:
            return  # Prevent movement if the game is over or won

        key = event.keysym
        if key not in ["Up", "Down", "Left", "Right"]:
            return  # Ignore non-movement keys

        dx, dy = 0, 0
        if event.keysym == 'Up':
            dy = -1
        elif event.keysym == 'Down':
            dy = 1
        elif event.keysym == 'Left':
            dx = -1
        elif event.keysym == 'Right':
            dx = 1

        new_x = self.current_position[1] + dx
        new_y = self.current_position[0] + dy
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            if (new_y, new_x) == self.finish:
                self.move_count += 1  # Increment move counter for the final move
                self.update_move_count_display()  # Update the display
                self.canvas.move(self.player, dx * self.cell_size, dy * self.cell_size)
                self.current_position = (new_y, new_x)
                self.game_won()
            elif self.maze[new_y][new_x] == 1:
                self.game_over()
            else:
                self.canvas.move(self.player, dx * self.cell_size, dy * self.cell_size)
                self.current_position = (new_y, new_x)
                self.move_count += 1  # Increment move counter
                self.update_move_count_display()  # Update the display

    def update_move_count_display(self):
        """Update the move counter display."""
        self.canvas.itemconfig(self.move_count_text, text=f"Moves: {self.move_count}")

    def game_over(self):
        """Handle game over state."""
        self.game_active = False  # Set the flag to False to stop movement
        self.show_end_screen("Game Over!", "darkred")

    def game_won(self):
        """Handle game won state."""
        self.game_active = False  # Set the flag to False to stop movement
        self.show_end_screen("You Won!", "darkgreen")

    def show_end_screen(self, message, color):
        """Display the end screen with a message and a 'Try Again' button."""
        # Create a semi-transparent overlay with the specified background color
        self.overlay = Canvas(self.root, width=self.width * self.cell_size, height=self.height * self.cell_size, bg=color, highlightthickness=0)
        self.overlay.place(x=0, y=0)
        self.overlay.create_rectangle(0, 0, self.width * self.cell_size, self.height * self.cell_size, fill=color, stipple='gray50')

        # Display the end message and game summary
        self.overlay.create_text(self.width * self.cell_size / 2, self.height * self.cell_size / 2 - 40, text=message, font=('Helvetica', 24, 'bold'), fill='white')
        self.overlay.create_text(self.width * self.cell_size / 2, self.height * self.cell_size / 2, text=f"Total Moves: {self.move_count}", font=('Helvetica', 16, 'bold'), fill='white')
        self.overlay.create_text(self.width * self.cell_size / 2, self.height * self.cell_size / 2 + 40, text=f"Minimum Moves: {self.shortest_path_length}", font=('Helvetica', 16, 'bold'), fill='white')

        # Add a "Try Again" button
        try_again_button = Button(self.root, text="Try Again", command=self.restart_game, font=('Helvetica', 16, 'bold'))
        self.overlay.create_window(self.width * self.cell_size / 2, self.height * self.cell_size / 2 + 80, window=try_again_button)

    def restart_game(self):
        """Restart the game by resetting the maze and player position."""
        if self.overlay:
            self.overlay.destroy()  # Remove the overlay
            self.overlay = None

        self.canvas.delete("all")
        self.maze = self.generate_maze(self.width, self.height)
        self.current_position = self.start
        self.move_count = 0
        self.game_active = True
        self.draw_maze()
        self.draw_player()
        self.shortest_path_length = self.find_shortest_path_length()
        self.display_shortest_path_length()
        self.move_count_text = self.canvas.create_text(self.width * self.cell_size / 2, 40, text=f"Moves: {self.move_count}", font=('Helvetica', 16, 'bold'), fill='white')

    def generate_maze(self, width, height):
        """Generate a random maze using depth-first search algorithm."""
        # Create a grid of 'walls', represented by 1s
        maze = [[1] * width for _ in range(height)]
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        x, y = 1, 1
        stack = [(x, y)]
        maze[y][x] = 0

        while stack:
            x, y = stack[-1]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                    if maze[ny - dy // 2][nx - dx // 2] == 1:
                        maze[ny][nx] = 0
                        maze[ny - dy // 2][nx - dx // 2] = 0
                        stack.append((nx, ny))
                        break
            else:
                stack.pop()

        # Ensure start and finish are open
        maze[self.start[0]][self.start[1]] = 0
        maze[self.finish[0]][self.finish[1]] = 0

        self.print_maze(maze)  # Print the maze for debugging
        return maze

    def print_maze(self, maze):
        """Print the maze to the console for debugging."""
        for row in maze:
            print(' '.join(str(cell) for cell in row))
        print()

    def find_shortest_path_length(self):
        """Find the shortest path length from start to finish using BFS."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        queue = deque([(self.start, 0)])
        visited = set()
        visited.add(self.start)

        while queue:
            (x, y), dist = queue.popleft()
            if (x, y) == self.finish:
                return dist

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.height and 0 <= ny < self.width and self.maze[nx][ny] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), dist + 1))

        return -1  # If no path is found

    def display_shortest_path_length(self):
        """Display the shortest path length on the canvas."""
        if self.shortest_path_length != -1:
            self.canvas.create_text(self.width * self.cell_size / 2, 20, text=f"Shortest Path: {self.shortest_path_length} moves", font=('Helvetica', 16, 'bold'), fill='white')
        else:
            self.canvas.create_text(self.width * self.cell_size / 2, 20, text="No path found", font=('Helvetica', 16, 'bold'), fill='red')

if __name__ == "__main__":
    game = MazeGame()
    game.root.mainloop()