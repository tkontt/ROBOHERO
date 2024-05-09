import pygame
import math
import random

pygame.init()

# Screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ROBO HERO - Attack of the ghosts")

# Colors
GREY = (100, 100, 100)
DGREY = (51, 51, 51)
CONCRETE_GREY = (72, 72, 72)
LIGHT_GREY = (200, 200, 200)
MOON_GREY = (240, 240, 240)
BLACK = (0, 0 ,0)
BG_BLACK = (7, 7, 7)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
PURPLE = (172, 55, 238)
BLUE = (0, 0, 110)

# Fonts
default_font = pygame.font.Font(pygame.font.get_default_font(), 20)
logo_font = pygame.font.Font(pygame.font.get_default_font(), 110)
sub_logo_font = pygame.font.Font(pygame.font.get_default_font(), 40)
intro_font = pygame.font.Font(pygame.font.get_default_font(), 18)
stats_font = pygame.font.Font(pygame.font.get_default_font(), 20)
ingame_stats_font = pygame.font.Font(pygame.font.get_default_font(), 14)
leaderboard_font = pygame.font.Font(pygame.font.get_default_font(), 16)
gameover_font = pygame.font.Font(pygame.font.get_default_font(), 36)

# Load images
robot_image = pygame.image.load("robo.png")
monster_image = pygame.image.load("hirvio.png")
coin_image = pygame.image.load("kolikko.png")
laser_image = pygame.image.load("ovi.png")

# Resize the "ovi.png" image to laser style (** For future updates resize laser smaller/larger for different difficulties **)
laser_new_width = 5  # New width of the laser
laser_new_height = 20  # New height of the laser
laser_image_resized = pygame.transform.scale(laser_image, (laser_new_width, laser_new_height))


## CLASSES ##
class Robot:
    def __init__(self):
        self.image = robot_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 72)
        self.speed = 5
        self.jump_height = 10
        self.is_jumping = False
        self.jump_count = 10
        self.original_y = self.rect.y
        self.is_moving_left = False
        self.is_moving_right = False
        self.last_direction = "right"  # Initial direction

    def move_left(self):
        if self.rect.x - self.speed >= 0:  # Restrict movement to screen width
            self.rect.x -= self.speed
            self.last_direction = "left"

    def move_right(self):
        if self.rect.x + self.rect.width + self.speed <= screen_width:  # Restrict movement to screen width
            self.rect.x += self.speed
            self.last_direction = "right"

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_count = 10
            self.original_y = self.rect.y

    def update(self):
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.rect.y = self.original_y

        if self.is_moving_left:
            self.move_left()
        if self.is_moving_right:
            self.move_right()

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_angle):
        super().__init__()
        self.image = laser_image_resized
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction_x = math.cos(math.radians(direction_angle))  # Calculate x-component of direction vector
        self.direction_y = math.sin(math.radians(direction_angle))  # Calculate y-component of direction vector

    def update(self):
        self.rect.x += self.speed * self.direction_x
        self.rect.y -= self.speed * self.direction_y  # Negative because y-coordinate is top-down

class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = monster_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)  # Randomly spawn anywhere on the screen width
        self.rect.y = random.randint(-100, -50)  # Spawn above the screen
        self.speed = random.randint(1, 4)  # Randomize the falling speed (** For future updates eg. 1-2 Easy, 3-4 Normal, 5-6 Hard, 8+ Hardcore **)
        self.is_moving = False
        self.move_speed = 2  # Speed at which the ghost moves towards the player

    def update(self):
        if not self.is_moving:
            self.rect.y += self.speed
            if self.rect.y >= screen_height - 110:  # Check if ghost touches the ground
                self.is_moving = True
        else:
            if self.rect.x < robot.rect.x:  # Move towards the right if the player is to the right
                self.rect.x += self.move_speed
            elif self.rect.x > robot.rect.x:  # Move towards the left if the player is to the left
                self.rect.x -= self.move_speed

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 3  # Coin falls with constant speed
        # Check for collision with the robot
        if pygame.sprite.collide_rect(self, robot):
            coins.remove(self)  # Remove the coin from the group when collected
            return True  # Return True if the coin is collected
        return False  # Return False if the coin is not collected

class LeaderboardEntry:
    def __init__(self, name, score):
        self.name = name
        self.score = score

# Create Random leaderboard entries (SNES THE FULL FIGHTING BASEBALL FTW!)
random_names = ["Ted Balloon", "Moises Jirardi", "John Armstrong", "Sleve McDichael", "Bobson Dugnutt", "Onson Sweemey", "Mike McFlanigan", "Jared Nightwish", "Nissan Al Gabe"]
top_5_entries = [LeaderboardEntry(name=random.choice(random_names), score=random.randint(100, 1000)) for _ in range(5)]

## GRAPHICS ##

def logo(): # Start screen Logo graphics 
    logo_text = logo_font.render("ROBO HERO", True, (PURPLE))
    logo_rect = logo_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(logo_text, logo_rect)

    logo_text = logo_font.render("ROBO HERO", True, (CYAN))
    logo_acc_rect = logo_text.get_rect(center=(screen_width // 2 + 8, screen_height // 2 - 58))
    screen.blit(logo_text, logo_acc_rect)

    logo_text = logo_font.render("ROBO HERO", True, (WHITE))
    logo_acc2_rect = logo_text.get_rect(center=(screen_width // 2 + 4, screen_height // 2 - 54))
    screen.blit(logo_text, logo_acc2_rect)

    sub_logo_text = sub_logo_font.render("ATTACK OF THE GHOSTS", True, (PURPLE))
    sub_logo_rect = sub_logo_text.get_rect(center=(screen_width // 2, screen_height // 2 + 10))
    screen.blit(sub_logo_text, sub_logo_rect)

    sub_logo_text = sub_logo_font.render("ATTACK OF THE GHOSTS", True, (WHITE))
    sub_logo_acc_rect = sub_logo_text.get_rect(center=(screen_width // 2 + 2, screen_height // 2 + 8))
    screen.blit(sub_logo_text, sub_logo_acc_rect)

def draw_gradient_background(): # Define gradient BG
    num_slices = 15 # Number of vertical slices for gradient
    slice_height = screen_height // num_slices
    for i in range(num_slices):
        # fade colors from blue to black
        color = (int(BLACK[0] * (1 - i / num_slices) + BLUE[0] * (i / num_slices)),
                 int(BLACK[1] * (1 - i / num_slices) + BLUE[1] * (i / num_slices)),
                 int(BLACK[2] * (1 - i / num_slices) + BLUE[2] * (i / num_slices)))
        pygame.draw.rect(screen, color, (0, i * slice_height, screen_width, slice_height))

def draw_background_elements(): #Draw background elements - Moon, road, skyscrapers 
    # Moon
    moon_radius = 70
    moon_position = (screen_width - moon_radius - 100, 100)  # Position of the moon (upper-right corner)
    pygame.draw.circle(screen, MOON_GREY, moon_position, moon_radius)

    # Skyscrapers
    pygame.draw.rect(screen, GREY, (50, 100, 100, 500))  # Skyscraper 1
    for x in range(60, 130, 20):
        for y in range(120, 500, 30):
            pygame.draw.rect(screen, LIGHT_GREY, (x, y, 10, 20))  # Small window block

    pygame.draw.rect(screen, GREY, (200, 200, 100, 400))  # Skyscraper 2
    for x in range(210, 290, 20):
        for y in range(220, 600, 30):
            pygame.draw.rect(screen, LIGHT_GREY, (x, y, 10, 20))  # Small window block

    pygame.draw.rect(screen, GREY, (350, 150, 80, 450))  # Skyscraper 3
    for x in range(360, 420, 20):
        for y in range(170, 600, 30):
            pygame.draw.rect(screen, LIGHT_GREY, (x, y, 10, 20))  # Small window block

    pygame.draw.rect(screen, GREY, (500, 100, 120, 500))  # Skyscraper 4
    for x in range(510, 610, 20):
        for y in range(120, 600, 30):
            pygame.draw.rect(screen, LIGHT_GREY, (x, y, 10, 20))  # Small window block

    # Ground / Road
    pygame.draw.rect(screen, DGREY, (0, screen_height - 40, screen_width, 40))
    pygame.draw.rect(screen, CONCRETE_GREY, (0, screen_height - 50, screen_width, 10))

    # White lane stripes
    for x in range(0, screen_width, 60):  # spacing of the lane stripes 
        pygame.draw.rect(screen, WHITE, (x, screen_height - 25, 30, 5))  # width and height of the lane stripes  

## TEXTS ##
def press_start(): # Blinking "Press any key to start game" text on "lobby screen"
    current_time = pygame.time.get_ticks()
    if current_time % 1000 < 500:  # Blink every 500 milliseconds
        press_start_text = default_font.render("- Press any key to start game -", True, (0, 255, 255))
        press_start_rect = press_start_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(press_start_text, press_start_rect)

def game_over_press_start(): # Blinking "Press any key to start new game on game over screen" (diff position & color than lobby screen)
    current_time = pygame.time.get_ticks()
    if current_time % 1000 < 500:  # Blink every 500 milliseconds
        press_key_text = default_font.render(" - Press any key to start a new game - ", True, (255, 255, 255))
        press_key_rect = press_key_text.get_rect(center=(screen_width // 2, screen_height // 2 + 220))
        screen.blit(press_key_text, press_key_rect)

def game_over_text(): # "GAME OVER" text
    game_over_text = gameover_font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))
    screen.blit(game_over_text, game_over_rect)

def statistics(): # Display statistics
    monsters_text = stats_font.render(f"Ghosts Destroyed: {monster_kills}", True, (255, 255, 255))
    monsters_rect = monsters_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
    screen.blit(monsters_text, monsters_rect)

    coins_text = stats_font.render(f"Coins Collected: {coins_collected}", True, (255, 255, 255))
    coins_rect = coins_text.get_rect(center=(screen_width // 2, screen_height // 2 - 70))
    screen.blit(coins_text, coins_rect)

    total_text = stats_font.render(f"Total score: {coins_collected * 10 + monster_kills}", True, (255, 255, 255))
    total_rect = total_text.get_rect(center=(screen_width // 2, screen_height // 2 - 40))
    screen.blit(total_text, total_rect)

def ingame_statistics(): # Display stats for ingame
    monsters_text = ingame_stats_font.render(f"Ghosts Destroyed: {monster_kills}", True, (255, 255, 255))
    monsters_rect = monsters_text.get_rect(topleft=(10, 10))  
    screen.blit(monsters_text, monsters_rect)

    coins_text = ingame_stats_font.render(f"Coins Collected: {coins_collected}", True, (255, 255, 255))
    coins_rect = coins_text.get_rect(topleft=(10, 26))  
    screen.blit(coins_text, coins_rect)

    total_text = ingame_stats_font.render(f"Total score: {coins_collected * 10 + monster_kills}", True, (255, 255, 255))
    total_rect = total_text.get_rect(topleft=(10, 40))  
    screen.blit(total_text, total_rect)

    
def leaderboard(): # Display the super random leaderboard 
    leaderboard_title_text = leaderboard_font.render("Leaderboard:", True, (255, 255, 255))
    leaderboard_title_rect = leaderboard_title_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
    screen.blit(leaderboard_title_text, leaderboard_title_rect)

    leaderboard_y = screen_height // 2 + 60
    for i, entry in enumerate(top_5_entries):
        entry_text = leaderboard_font.render(f"{i + 1}. {entry.name}: {entry.score}", True, (255, 255, 255))
        entry_rect = entry_text.get_rect(center=(screen_width // 2, leaderboard_y))
        screen.blit(entry_text, entry_rect)
        leaderboard_y += 20  

## SCREENS ##
# Start screen aka Lobby
def draw_start_screen(): 
    draw_gradient_background() # Draw gradient background
    draw_background_elements() # Add BG elements
    logo() # instert logo
    press_start() # insert "press any key to start game text"

 # Story and controls
def draw_second_start_screen():
    screen.fill((BLACK))
    story_text = [
        "As the day turns into the night, mysterious creatures appear in the sky...",
        "",
        "THE CITY IS UNDER ATTACK BY GHOSTS!!",
        "",
        "As the citys last hope, governement sends in ROBO HERO!",
        "Your mission is to destroy ghosts and collect coins to save the city.",
        "Use arrow keys to move and aim, spacebar to jump,",
        "and left CTRL to shoot lasers.",
        "",
        "Don't let the ghosts touch you, ONE TOUCH IS DEADLY!",
        "",
        "Controls:",
        "Left Arrow - Move/aim left",
        "Right Arrow - Move/aim right",
        "Up Arrow - Aim up",
        "Spacebar - Jump",
        "Left CTRL - Shoot lasers",
        "",
        "GEAR UP AND PRESS ANY KEY TO DROP IN AND SAVE THE CITY!"
    ]

    for i, line in enumerate(story_text):
        text_surface = intro_font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_width // 2, 75 + i * 25))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

# Create objects
robot = Robot()
lasers = pygame.sprite.Group()
monsters = pygame.sprite.Group()
coins = pygame.sprite.Group()

# Main game loop
start_screen = True
second_start_screen = False
running = True
clock = pygame.time.Clock()
game_over = False
restart_timer = 0
coins_collected = 0
monster_kills = 0

while running:

    if start_screen:
        draw_start_screen()
        pygame.display.flip()
        
        # Start screen loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start_screen = False
            elif event.type == pygame.KEYDOWN:
                start_screen = False
                second_start_screen = True  # Transition to the "Story" start screen
    elif second_start_screen:
        draw_second_start_screen()
        pygame.display.flip()

        # Handle events in the second start screen loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                second_start_screen = False
            elif event.type == pygame.KEYDOWN:
                second_start_screen = False
                
    # START THE GAME LOOP
    else:

        screen.fill((7, 7, 7))
        draw_background_elements()
        ingame_statistics()
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Move left
                    robot.is_moving_left = True
                elif event.key == pygame.K_RIGHT:  # Move right
                    robot.is_moving_right = True
                elif event.key == pygame.K_SPACE:  # Jump
                    robot.jump()
                elif event.key == pygame.K_LCTRL:  # Shoot laser
                    direction_angle = 0  # Default direction is right
                    if pygame.key.get_pressed()[pygame.K_UP]:  # If up arrow key is pressed
                        direction_angle = 90  # Set direction angle to up
                        if pygame.key.get_pressed()[pygame.K_LEFT]:  # If left arrow key is also pressed
                            direction_angle = 135  # Set direction angle to up-left
                        elif pygame.key.get_pressed()[pygame.K_RIGHT]:  # If right arrow key is also pressed
                            direction_angle = 45  # Set direction angle to up-right
                    elif pygame.key.get_pressed()[pygame.K_LEFT]:  # If left arrow key is pressed
                        direction_angle = 180  # Set direction angle to left
                    laser = Laser(robot.rect.centerx, robot.rect.centery, direction_angle)
                    lasers.add(laser)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    robot.is_moving_left = False
                elif event.key == pygame.K_RIGHT:
                    robot.is_moving_right = False

        # Spawn ghosts and coins randomly
        if random.randint(0, 100) < 3:  # Adjust the spawn rate 
            monster = Monster()
            monsters.add(monster)
        if random.randint(0, 100) < 2:  # Adjust the spawn rate 
            coin = Coin()
            coin.rect.x = random.randint(0, screen_width - coin.rect.width)  # Spawn at random x-coordinate
            coins.add(coin)

        # Check for collisions between lasers and monsters
        laser_hits = pygame.sprite.groupcollide(lasers, monsters, True, False)
        for laser, monster_hit in laser_hits.items():
            for monster in monster_hit:
            
                if 0 <= monster.rect.y <= screen_height:  # Check if ghost is on the screen before destroying it
                    monsters.remove(monster)  # Remove the ghost from the group
                    monster_kills += 1
                    
        # Check for collisions between robot and coins
        for coin in coins.sprites():
            if coin.update():
                coins_collected += 1  # Increment coins_collected if a coin is collected

        # Update objects
        robot.update()
        lasers.update()
        monsters.update()
        coins.update()

        # Draw objects
        for laser in lasers:
            screen.blit(laser.image, laser.rect)
        for monster in monsters:
            screen.blit(monster.image, monster.rect)
        for coin in coins:
            screen.blit(coin.image, coin.rect)
        screen.blit(robot.image, robot.rect)

        pygame.display.flip()
        clock.tick(60)

    # Game over condition
    if pygame.sprite.spritecollide(robot, monsters, False):
        game_over = True
        restart_timer = pygame.time.get_ticks() + 1000  # Restart delay duration: 1000 milliseconds, this to avoid instant new game while spamming lasers!

    # GAME OVER LOOP
    while game_over:
        screen.fill((BLACK)) 
        game_over_text()
        statistics()
        leaderboard()
        game_over_press_start()
        pygame.display.flip()

        # Handle events in the game over loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
            current_time = pygame.time.get_ticks()
            if current_time >= restart_timer: # Allow the player to restart the game ONLY AFTER the restart delay has passed!!
                if event.type == pygame.KEYDOWN:
                    game_over = False
                    # Reset game variables and objects
                    robot = Robot()
                    lasers = pygame.sprite.Group()
                    monsters = pygame.sprite.Group()
                    coins = pygame.sprite.Group()
                    coins_collected = 0  # Reset coins_collected
                    monster_kills = 0 # Reset Monster kills 
                    restart_timer = 0  # Reset restart_timer

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
