from tkinter import *
import random
import time


class SnakeGame:
    """
    SnakeGame - Core game logic and GUI for the Snake game.
    Implements game rules, board management, collision detection, and Tkinter GUI.
    Supports two types of food, keyboard controls, and restart functionality.
    """

    # Configuration constants
    CANVAS_WIDTH = 600
    CANVAS_HEIGHT = 400
    CELL_SIZE = 20
    MAX_SNAKE_LENGTH = 8
    GAME_SPEED = 200  # milliseconds

    # Colors
    COLOR_BG = "black"
    COLOR_SNAKE_HEAD = "lime"
    COLOR_SNAKE_BODY = "green"
    COLOR_FOOD_TYPE_1 = "red"
    COLOR_FOOD_TYPE_2 = "orange"
    COLOR_TEXT = "white"
    COLOR_TEXT_YELLOW = "yellow"
    COLOR_TEXT_LIGHTBLUE = "lightblue"

    # Game states
    STATE_PLAYING = "playing"
    STATE_GAME_OVER = "game_over"

    def __init__(self, root):
        """
        Constructor for SnakeGame.
        Initializes the game window, canvas, and game state.

        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Snake Game")

        # Create canvas
        self.canvas = Canvas(root, bg=self.COLOR_BG,
                             width=self.CANVAS_WIDTH,
                             height=self.CANVAS_HEIGHT)
        self.canvas.pack()

        # Initialize game state
        self.reset_game()

        # Bind keyboard events
        self.root.bind('<KeyPress>', self.key_press)

        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start game loop
        self.game_loop()

    def reset_game(self):
        """Resets the game to initial state."""
        # Initialize snake (start from center)
        start_x = self.CANVAS_WIDTH // 2
        start_y = self.CANVAS_HEIGHT // 2
        self.snake = [
            (start_x, start_y),
            (start_x - self.CELL_SIZE, start_y)
        ]

        # Initial direction: right
        self.direction = 'Right'
        self.next_direction = 'Right'

        # Quick lookup sets (optimization) - MUST be initialized before generate_food
        self.snake_set = set(self.snake)
        self.food_positions = set()

        # Initialize food
        self.foods = []
        self.generate_food()
        self.generate_food()

        # Game state variables
        self.game_state = self.STATE_PLAYING
        self.start_time = time.time()
        self.pending_growth = 0  # Tracks pending growth from food consumption
        self.end_reason = None  # Track win or lose
        self.score = 0  # Initialize score

        # Update food positions set after generating food
        self.food_positions = {(f[0], f[1]) for f in self.foods}

        # Unbind restart click if it exists
        try:
            self.canvas.unbind('<Button-1>')
        except Exception:
            pass

    def generate_food(self):
        """
        Generates food at random position not occupied by snake or other food.

        Food types:
        - Type 1 (red): Increases snake length by 1 unit
        - Type 2 (orange): Increases snake length by 2 units
        """
        max_attempts = 1000

        for attempt in range(max_attempts):
            # Calculate grid dimensions
            grid_width = (self.CANVAS_WIDTH - self.CELL_SIZE) // self.CELL_SIZE
            grid_height = (self.CANVAS_HEIGHT - self.CELL_SIZE) // self.CELL_SIZE

            # Random grid position
            x = random.randint(0, grid_width) * self.CELL_SIZE
            y = random.randint(0, grid_height) * self.CELL_SIZE

            # Check if position is free
            if (x, y) not in self.snake_set and (x, y) not in self.food_positions:
                # Random food type (1 or 2)
                food_type = random.choice([1, 2])
                self.foods.append((x, y, food_type))
                self.food_positions.add((x, y))
                return

        # If we get here, couldn't find free space
        # In a real game, you might want to handle this differently
        print("Warning: Could not find free space for food")

    def key_press(self, event):
        """
        Handles keyboard input for snake direction control and game restart.

        Args:
            event: Tkinter key press event
        """
        if self.game_state != self.STATE_PLAYING:
            return

        # Handle direction keys
        if event.keysym == 'Left' and self.direction != 'Right':
            self.next_direction = 'Left'
        elif event.keysym == 'Right' and self.direction != 'Left':
            self.next_direction = 'Right'
        elif event.keysym == 'Up' and self.direction != 'Down':
            self.next_direction = 'Up'
        elif event.keysym == 'Down' and self.direction != 'Up':
            self.next_direction = 'Down'
        # Handle restart key
        elif event.keysym.lower() == 'r' and self.game_state == self.STATE_GAME_OVER:
            self.restart_game()

    def calculate_new_head(self):
        """
        Calculates new head position based on current direction.

        Returns:
            Tuple (x, y) representing the new head position
        """
        head_x, head_y = self.snake[0]

        if self.direction == 'Right':
            return (head_x + self.CELL_SIZE, head_y)
        elif self.direction == 'Left':
            return (head_x - self.CELL_SIZE, head_y)
        elif self.direction == 'Up':
            return (head_x, head_y - self.CELL_SIZE)
        else:  # Down
            return (head_x, head_y + self.CELL_SIZE)

    def check_collision(self, position):
        """
        Checks if position collides with walls or snake.

        Args:
            position: Tuple (x, y) to check for collision

        Returns:
            True if collision detected, False otherwise
        """
        x, y = position

        # Wall collision
        if (x < 0 or x >= self.CANVAS_WIDTH or
                y < 0 or y >= self.CANVAS_HEIGHT):
            return True

        # Self collision (excluding tail which will move)
        if position in self.snake_set and position != self.snake[-1]:
            return True

        return False

    def update_snake(self):
        """Updates snake position and handles food consumption."""
        if self.game_state != self.STATE_PLAYING:
            return

        # Update direction
        self.direction = self.next_direction

        # Calculate new head position
        new_head = self.calculate_new_head()

        # Check for collisions
        if self.check_collision(new_head):
            self.end_game("lose")
            return

        # Check for food consumption
        eaten_food_index = None
        for i, (fx, fy, ftype) in enumerate(self.foods):
            if new_head == (fx, fy):
                eaten_food_index = i
                # Add growth based on food type (1 or 2 units)
                self.pending_growth += ftype
                break

        # Add new head
        self.snake.insert(0, new_head)
        self.snake_set.add(new_head)

        # Handle food consumption
        if eaten_food_index is not None:
            fx, fy, ftype = self.foods.pop(eaten_food_index)
            self.food_positions.discard((fx, fy))
            self.generate_food()
            # Increase score by 1 for each food eaten
            self.score += 1

        # Handle growth
        if self.pending_growth > 0:
            # Don't remove tail - snake is growing
            self.pending_growth -= 1
        else:
            # Remove tail to maintain length
            tail = self.snake.pop()
            self.snake_set.discard(tail)

        # Check max length
        if len(self.snake) >= self.MAX_SNAKE_LENGTH:
            self.end_game("win")
            return

    def draw(self):
        """Draws all game elements on canvas."""
        # Clear canvas
        self.canvas.delete('all')

        if self.game_state == self.STATE_PLAYING:
            # Draw snake
            for i, (x, y) in enumerate(self.snake):
                color = self.COLOR_SNAKE_HEAD if i == 0 else self.COLOR_SNAKE_BODY
                self.canvas.create_rectangle(
                    x, y,
                    x + self.CELL_SIZE, y + self.CELL_SIZE,
                    fill=color, outline='black'
                )

            # Draw food
            for fx, fy, ftype in self.foods:
                color = self.COLOR_FOOD_TYPE_1 if ftype == 1 else self.COLOR_FOOD_TYPE_2
                self.canvas.create_rectangle(
                    fx, fy,
                    fx + self.CELL_SIZE, fy + self.CELL_SIZE,
                    fill=color, outline='white'
                )

            # Draw length and time during gameplay
            elapsed_time = time.time() - self.start_time
            self.canvas.create_text(
                50, 20,
                text=f"Length: {len(self.snake)}/{self.MAX_SNAKE_LENGTH}",
                fill=self.COLOR_TEXT_YELLOW,
                font=('Arial', 12, 'bold')
            )
            self.canvas.create_text(
                180, 20,
                text=f"Score: {self.score}",
                fill=self.COLOR_TEXT_YELLOW,
                font=('Arial', 12, 'bold')
            )
            self.canvas.create_text(
                self.CANVAS_WIDTH - 50, 20,
                text=f"Time: {elapsed_time:.1f}s",
                fill=self.COLOR_TEXT_YELLOW,
                font=('Arial', 12, 'bold'),
                anchor='e'
            )

        elif self.game_state == self.STATE_GAME_OVER:
            elapsed_time = time.time() - self.start_time

            # Game over display
            self.canvas.create_text(
                self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 - 40,
                text="GAME OVER",
                fill=self.COLOR_TEXT,
                font=('Arial', 30, 'bold')
            )

            # Display Win/Lose message
            if self.end_reason == "win":
                self.canvas.create_text(
                    self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2,
                    text="YOU WIN!",
                    fill=self.COLOR_TEXT,
                    font=('Arial', 24, 'bold')
                )
            else:
                self.canvas.create_text(
                    self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2,
                    text="YOU LOSE!",
                    fill=self.COLOR_TEXT,
                    font=('Arial', 24, 'bold')
                )

            self.canvas.create_text(
                self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 + 40,
                text=f"Final Length: {len(self.snake)}",
                fill=self.COLOR_TEXT_YELLOW,
                font=('Arial', 16)
            )
            self.canvas.create_text(
                self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 + 70,
                text=f"Total Time: {elapsed_time:.1f} seconds",
                fill=self.COLOR_TEXT_YELLOW,
                font=('Arial', 16)
            )
            self.canvas.create_text(
                self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 + 100,
                text=f"Score: {self.score}",
                fill=self.COLOR_TEXT_YELLOW,
                font=('Arial', 16)
            )

            # Draw Restart Button
            btn_x, btn_y = self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 + 150
            btn_w, btn_h = 120, 40

            # Create button with specific tags for hover effect
            self.canvas.create_rectangle(
                btn_x - btn_w // 2, btn_y - btn_h // 2,
                btn_x + btn_w // 2, btn_y + btn_h // 2,
                fill=self.COLOR_TEXT_LIGHTBLUE,
                outline="white",
                width=2,
                tags=("restart_btn", "restart_bg")
            )
            self.canvas.create_text(
                btn_x, btn_y,
                text="Restart",
                fill="black",
                font=('Arial', 14, 'bold'),
                tags=("restart_btn", "restart_text")
            )

            # Bind events for hover and click
            self.canvas.tag_bind("restart_btn", "<Enter>", self.on_button_hover)
            self.canvas.tag_bind("restart_btn", "<Leave>", self.on_button_leave)
            self.canvas.tag_bind("restart_btn", "<Button-1>", self.on_click_restart)

    def on_button_hover(self, event):
        """Changes button color when mouse hovers over it."""
        self.canvas.itemconfig("restart_bg", fill="red")

    def on_button_leave(self, event):
        """Reverts button color when mouse leaves."""
        self.canvas.itemconfig("restart_bg", fill=self.COLOR_TEXT_LIGHTBLUE)

    def end_game(self, reason="lose"):
        """
        Ends the current game.

        Args:
            reason: "win" if player wins, "lose" if player loses
        """
        self.game_state = self.STATE_GAME_OVER
        self.end_reason = reason
        # Draw immediately to show game over screen
        self.draw()

    def on_click_restart(self, event):
        """Handles mouse click for restart button."""
        # No need to check bounds manually anymore as tag_bind handles the area
        self.restart_game()

    def restart_game(self):
        """Restarts the game."""
        # Reset game state
        self.reset_game()
        # Restart loop
        self.game_loop()

    def on_closing(self):
        """Handles window close event."""
        self.game_state = self.STATE_GAME_OVER
        self.root.destroy()

    def game_loop(self):
        """Main game loop."""
        if self.game_state == self.STATE_PLAYING:
            try:
                self.update_snake()
                self.draw()
                # Schedule next game loop iteration
                self.root.after(self.GAME_SPEED, self.game_loop)
            except Exception as e:
                print(f"Game error: {e}")
                self.end_game()
        else:
            # Game over, draw final state once
            self.draw()


# Main entry point
if __name__ == "__main__":
    root = Tk()
    game = SnakeGame(root)
    root.mainloop()