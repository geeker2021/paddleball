import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
sidebar_width = 200  # Width of the sidebar
screen = pygame.display.set_mode((width + sidebar_width, height))
pygame.display.set_caption("Ball Game with Opponent AI")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
sidebar_color = (50, 50, 50)  # Sidebar color

# Ball properties
ball_radius = 20
ball_x = width // 2
ball_y = height // 2
ball_speed_x = 5 * random.choice([-1, 1])
ball_speed_y = 7
ball_color = WHITE  # Initial ball color

# Paddle properties
paddle_width = 150
paddle_height = 20
player_paddle_x = (width - paddle_width) // 2
player_paddle_y = height - paddle_height - 10
opponent_paddle_x = (width - paddle_width) // 2
opponent_paddle_y = 10
paddle_speed = 8

start_ticks = pygame.time.get_ticks()  # Get start time in milliseconds

font = pygame.font.Font(None, 36)  # Font for the timer
small_font = pygame.font.Font(None, 24)  # Font for hit count

clock = pygame.time.Clock()

# Function to display "Game Over" message and hit count
def display_game_over(hit_count):
    game_over_text = font.render("Game Over", True, WHITE)
    text_rect = game_over_text.get_rect(center=(width // 2, height // 2))
    screen.blit(game_over_text, text_rect)

# Function to display pause text
def display_pause():
    pause_text = font.render("Paused", True, WHITE)
    text_rect = pause_text.get_rect(center=(width // 2, height // 2))
    screen.blit(pause_text, text_rect)

# Function to display sidebar (hit score and game options)
def draw_sidebar(hit_count):
    pygame.draw.rect(screen, sidebar_color, (width, 0, sidebar_width, height))  # Sidebar background

    hit_count_text = small_font.render("Hits: " + str(hit_count), True, WHITE)
    screen.blit(hit_count_text, (width + 20, 50))  # Display hit count in the sidebar

    if game_over:
        restart_text = small_font.render("Press R to Restart", True, WHITE)
        screen.blit(restart_text, (width + 20, 100))  # Display restart instructions in the sidebar

# Game variables
game_started = False  # Flag to control game start
game_over = False  # Flag to control game over condition
hit_count = 0  # Counter for hits on player paddle
elapsed_time = 0

# Main game loop
paused = False  # Flag to control pause state
running = True
while running:
    screen.fill(BLACK)  # Set background color to black

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Reset the game when 'R' is pressed and game is over
                ball_x = width // 2
                ball_y = height // 2
                ball_speed_x = 5 * random.choice([-1, 1])
                ball_speed_y = 7
                game_over = False
                start_ticks = pygame.time.get_ticks()
                hit_count = 0
            if event.key == pygame.K_p:
                # Pause/resume the game when 'P' is pressed
                paused = not paused
                if paused:
                    # Update start_ticks to maintain elapsed time when pausing
                    start_ticks = pygame.time.get_ticks() - elapsed_time * 1000
            if event.key == pygame.K_q:
                # Quit the game when 'Q' is pressed
                running = False
            if event.key == pygame.K_s and not game_started:
                # Start the game when 'S' is pressed and the game hasn't started yet
                game_started = True

    if game_started:
        # Player controls (only active if the game is not paused)
        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_paddle_x > 0:
                player_paddle_x -= paddle_speed
            if keys[pygame.K_RIGHT] and player_paddle_x < width - paddle_width:
                player_paddle_x += paddle_speed

        # Update ball position if the game is not over and not paused
        if not game_over and not paused:
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Check for collisions with the walls and top/bottom boundaries
            if ball_x + ball_radius > width or ball_x - ball_radius < 0:
                ball_speed_x = -ball_speed_x
            if ball_y - ball_radius < 0:
                game_over = True  # Ball went out of the top boundary
            elif ball_y + ball_radius > height:  # Ball went completely out of the bottom boundary
                game_over = True

            # Check for collisions with the player paddle
            if ball_y + ball_radius >= player_paddle_y and ball_x + ball_radius >= player_paddle_x and ball_x - ball_radius <= player_paddle_x + paddle_width:
                ball_speed_y = -ball_speed_y
                ball_color = WHITE  # Change ball color back to white on collision with player paddle
                hit_count += 1
                # Increase ball speed gradually based on hit_count
                ball_speed_x *= 1.01
                ball_speed_y *= 1.01

            # Update opponent paddle's position based on the ball's position
            if ball_y < height / 2:  # Opponent reacts only if the ball is in the upper half of the screen
                target_pos_opponent = ball_x - paddle_width / 2
                error_opponent = target_pos_opponent - opponent_paddle_x
                opponent_paddle_x += error_opponent * 0.12

            # Check for collisions with the opponent paddle
            if ball_y - ball_radius <= opponent_paddle_y + paddle_height and ball_x + ball_radius >= opponent_paddle_x and ball_x - ball_radius <= opponent_paddle_x + paddle_width:
                ball_speed_y = -ball_speed_y
                ball_color = RED  # Change ball color to red on collision with opponent paddle

            # Draw ball with updated color
            pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

        # Draw elements (paddles, sidebar, etc.)
        pygame.draw.rect(screen, WHITE, (player_paddle_x, player_paddle_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, WHITE, (opponent_paddle_x, opponent_paddle_y, paddle_width, paddle_height))

        # Display sidebar with hit count and game options
        pygame.draw.rect(screen, sidebar_color, (width, 0, sidebar_width, height))  # Sidebar background
        hit_count_text = small_font.render("Score : " + str(hit_count), True, WHITE)
        screen.blit(hit_count_text, (width + 20, 50))  # Display hit count in the sidebar
        if game_over:
            restart_text = small_font.render("Press R to Restart", True, WHITE)
            screen.blit(restart_text, (width + 20, 100))  # Display restart instructions in the sidebar

        if paused:
            pause_text = small_font.render("Paused", True, WHITE)
            screen.blit(pause_text, (width + 20, 150))  # Display paused message in the sidebar
        else:
            pause_instruction = small_font.render("Press P to Pause", True, WHITE)
            screen.blit(pause_instruction, (width + 20, 150))  # Display pause instruction in the sidebar

    else:
        # Display "Press S to Start" message until the game starts
        start_text = font.render("Press S to Start", True, WHITE)
        text_rect = start_text.get_rect(center=(width // 2, height // 2))
        screen.blit(start_text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
