import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen_width = 640
screen_height = 480

# Set the colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Set the border dimensions
border_size = 10

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Set the clock to control the game's frame rate
clock = pygame.time.Clock()

# Define the Snake class
class Snake:
    def __init__(self):
        self.size = 1
        self.segments = [(screen_width // 2, screen_height // 2)]
        self.direction = "right"
        self.speed = 10

    def move(self):
        if self.direction == "up":
            self.segments.insert(0, (self.segments[0][0], self.segments[0][1] - self.speed))
        elif self.direction == "down":
            self.segments.insert(0, (self.segments[0][0], self.segments[0][1] + self.speed))
        elif self.direction == "left":
            self.segments.insert(0, (self.segments[0][0] - self.speed, self.segments[0][1]))
        elif self.direction == "right":
            self.segments.insert(0, (self.segments[0][0] + self.speed, self.segments[0][1]))

        if len(self.segments) > self.size:
            self.segments.pop()

    def draw(self):
        for segment in self.segments:
            pygame.draw.rect(screen, white, (segment[0], segment[1], 10, 10))

# Define the Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = red
        self.spawn()

    def spawn(self):
        x = random.randint(0, (screen_width - 10) // 10) * 10
        y = random.randint(0, (screen_height - 10) // 10) * 10
        self.position = (x, y)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], 10, 10))

# Define the BonusFood class
class BonusFood:
    def __init__(self):
        self.position = (0, 0)
        self.color = green
        self.active = False
        self.spawn_time = 0
        self.duration = 5
        self.points = 10

    def activate(self):
        self.active = True
        self.spawn_time = time.time()
        self.spawn()

    def deactivate(self):
        self.active = False

    def spawn(self):
        x = random.randint(0, (screen_width - 10) // 10) * 10
        y = random.randint(0, (screen_height - 10) // 10) * 10
        self.position = (x, y)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], 10, 10))

    def is_expired(self):
        return self.active and time.time() - self.spawn_time > self.duration

# Define the Scoreboard class
class Scoreboard:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.high_score = 0

    def update(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
        if self.score % 5 == 0:
            bonus_food.activate()

    def draw(self):
        score_text = self.font.render("Score: " + str(self.score), True, white)
        high_score_text = self.font.render("High Score: " + str(self.high_score), True, white)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))

# Create instances of the Snake, Food, BonusFood, and Scoreboard classes
snake = Snake()
food = Food()
bonus_food = BonusFood()
scoreboard = Scoreboard()

# Game states
GAME_STATE_HOMEPAGE = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAMEOVER = 2

game_state = GAME_STATE_HOMEPAGE

# Game loop
running = True
player_score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == GAME_STATE_HOMEPAGE:
                if event.key == pygame.K_RETURN:
                    snake = Snake()
                    food.spawn()
                    bonus_food.deactivate()
                    scoreboard.score = 0
                    game_state = GAME_STATE_PLAYING
            elif game_state == GAME_STATE_PLAYING:
                if event.key == pygame.K_UP and snake.direction != "down":
                    snake.direction = "up"
                elif event.key == pygame.K_DOWN and snake.direction != "up":
                    snake.direction = "down"
                elif event.key == pygame.K_LEFT and snake.direction != "right":
                    snake.direction = "left"
                elif event.key == pygame.K_RIGHT and snake.direction != "left":
                    snake.direction = "right"
            elif game_state == GAME_STATE_GAMEOVER:
                if event.key == pygame.K_r:
                    snake = Snake()
                    food.spawn()
                    bonus_food.deactivate()
                    scoreboard.score = 0
                    game_state = GAME_STATE_PLAYING
                elif event.key == pygame.K_q:
                    running = False

    if game_state == GAME_STATE_PLAYING:
        # Move the snake
        snake.move()

        # Check for collision with the food
        if snake.segments[0] == food.position:
            snake.size += 1
            food.spawn()
            scoreboard.update(1)
            player_score = scoreboard.score

        # Check for collision with the bonus food
        if (
            bonus_food.active
            and snake.segments[0] == bonus_food.position
            and not bonus_food.is_expired()
        ):
            snake.size += 1
            scoreboard.update(bonus_food.points)
            bonus_food.deactivate()
            player_score = scoreboard.score

        # Check for collision with the walls
        if (
            snake.segments[0][0] < border_size
            or snake.segments[0][0] >= screen_width - border_size
            or snake.segments[0][1] < border_size
            or snake.segments[0][1] >= screen_height - border_size
        ):
            game_state = GAME_STATE_GAMEOVER

        # Check for collision with the snake's body
        for segment in snake.segments[1:]:
            if snake.segments[0] == segment:
                game_state = GAME_STATE_GAMEOVER

        # Deactivate expired bonus food
        if bonus_food.is_expired():
            bonus_food.deactivate()

    # Clear the screen
    screen.fill(black)

    # Draw the borders
    pygame.draw.rect(screen, white, (0, 0, screen_width, border_size))  # Top border
    pygame.draw.rect(screen, white, (0, screen_height - border_size, screen_width, border_size))  # Bottom border
    pygame.draw.rect(screen, white, (0, 0, border_size, screen_height))  # Left border
    pygame.draw.rect(screen, white, (screen_width - border_size, 0, border_size, screen_height))  # Right border

    if game_state == GAME_STATE_HOMEPAGE:
        # Draw the homepage text
        font = pygame.font.Font(None, 36)
        title_text = font.render("Snake Game", True, white)
        start_text = font.render("Press ENTER to start", True, white)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - 50))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2))

    elif game_state == GAME_STATE_PLAYING:
        # Draw the snake, food, bonus food, and score
        snake.draw()
        food.draw()
        if bonus_food.active:
            bonus_food.draw()
        scoreboard.draw()

    elif game_state == GAME_STATE_GAMEOVER:
        # Draw the game over text and final score
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over", True, white)
        score_text = font.render("Score: " + str(player_score), True, white)
        restart_text = font.render("Press 'R' to restart", True, white)
        quit_text = font.render("Press 'Q' to quit", True, white)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 50))
        screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 + 100))

    # Update the display
    pygame.display.flip()

    # Control the game's frame rate
    clock.tick(15)

# Quit the game
pygame.quit()
