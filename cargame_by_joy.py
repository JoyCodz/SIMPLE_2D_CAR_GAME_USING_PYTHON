import pygame
from pygame.locals import *
import random

# Set game parameters
size = width, height = (800, 800)
road_w = int(width / 1.6)
roadmark_w = int(width / 80)
right_lane = width / 2 + road_w / 4
left_lane = width / 2 - road_w / 4
speed = 1
max_speed = 10
car_move_speed = 5

# Road line parameters
road_line_height = 70
road_line_space = 25

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode(size)
pygame.display.set_caption("JOY's CAR GAME!")
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)

# Load assets
car = pygame.image.load("car.png")
car2 = pygame.image.load("otherCar.png")
game_over_img = pygame.image.load("gameover.png")

# Initialize mixer for audio
pygame.mixer.init()

# Load background music and sound effects
pygame.mixer.music.load("background.mp3")
game_over_sound = pygame.mixer.Sound("game_over.wav")

# Function to draw text on screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Main game loop
def game_loop(highest_score):
    pygame.mixer.music.play(-1)  # Play background music
    running = True
    speed = 1
    score = 0
    counter = 0

    car_loc = car.get_rect()
    car_loc.center = right_lane, height * 0.8

    car2_loc = car2.get_rect()
    car2_loc.center = left_lane, height * 0.2

    # Initialize road lines
    road_lines = [i for i in range(0, height, road_line_height + road_line_space)]

    target_lane = car_loc.center[0]

    while running:
        counter += 1
        if counter % 100 == 0:
            score += 1  # Increment score

        # Increase difficulty over time
        if counter == 3500:
            speed += 0.07
            counter = 0

        # Move enemy vehicle down the screen
        car2_loc[1] += speed
        road_line_speed = 1.05
        if car2_loc[1] > height:
            # Randomly assign lane to enemy car
            car2_loc.center = (right_lane, -200) if random.randint(0, 1) == 0 else (left_lane, -200)

        # Check for collision and trigger game over
        if (car_loc[0] < car2_loc[0] + car2.get_width() and
            car_loc[0] + car.get_width() > car2_loc[0] and
            car_loc[1] < car2_loc[1] + car2.get_height() and
            car_loc[1] + car.get_height() > car2_loc[1]):
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(game_over_sound)
            screen.blit(game_over_img, (0, 130))
            pygame.display.update()
            pygame.time.wait(1200)
            return score, highest_score

        # Handle user inputs for car movement
        keys = pygame.key.get_pressed()

        if keys[K_UP] or keys[K_w]:
            if speed < max_speed:
                speed += 0.005

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key in [K_a, K_LEFT] and target_lane > left_lane:
                    target_lane = left_lane
                elif event.key in [K_d, K_RIGHT] and target_lane < right_lane:
                    target_lane = right_lane
                elif event.key == K_ESCAPE:
                    running = False

        # Smooth car movement
        if car_loc.center[0] < target_lane:
            car_loc = car_loc.move([car_move_speed, 0])
        elif car_loc.center[0] > target_lane:
            car_loc = car_loc.move([-car_move_speed, 0])

        screen.fill((0, 0, 0))

        # Move the road lines to create the moving road effect
        for i in range(len(road_lines)):
            road_lines[i] += road_line_speed
            if road_lines[i] > height:
                road_lines[i] = -road_line_height

        # Draw the road and road markings
        pygame.draw.rect(screen, (50, 50, 50), (width / 2 - road_w / 2, 0, road_w, height))
        pygame.draw.rect(screen, (0, 0, 0), (width / 2 - roadmark_w / 2, 0, roadmark_w, height))
        pygame.draw.rect(screen, (255, 255, 255), (width / 2 - road_w / 2 + roadmark_w * 2, 0, roadmark_w, height))
        pygame.draw.rect(screen, (255, 255, 255), (width / 2 + road_w / 2 - roadmark_w * 3, 0, roadmark_w, height))

        # Draw the animated road lines
        for line_y in road_lines:
            pygame.draw.rect(screen, (255, 255, 255), (width / 2 - roadmark_w / 2, line_y, roadmark_w, road_line_height))

        # Render the cars
        screen.blit(car, car_loc)
        screen.blit(car2, car2_loc)

        # Draw the current score and highest score
        draw_text(f"Score: {score}", small_font, (255, 255, 255), screen, 70, 30)
        draw_text(f"High Score: {highest_score}", small_font, (255, 255, 255), screen, width - 150, 30)

        pygame.display.update()

    return None

def show_play_again_screen(score, highest_score):
    screen.fill((0, 0, 0))
    draw_text("GAME OVER!", font, (255, 0, 0), screen, width // 2, height // 3)
    draw_text(f"Your Score: {score}", small_font, (255, 255, 255), screen, width // 2, height // 2 - 50)
    draw_text(f"Highest Score: {highest_score}", small_font, (255, 255, 255), screen, width // 2, height // 2)
    draw_text("Press SPACE to Play Again or ESC to Quit", small_font, (255, 255, 255), screen, width // 2, height // 2 + 50)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return False

# Main game loop with score tracking
highest_score = 0

while True:
    result = game_loop(highest_score)
    if result is None:
        break
    
    score, highest_score = result

    if score > highest_score:
        highest_score = score

    if not show_play_again_screen(score, highest_score):
        break

pygame.quit()
