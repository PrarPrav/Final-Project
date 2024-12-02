import pygame
import random

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (space-themed)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (0, 255, 255)
YELLOW = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player settings
player_width = 50
player_height = 40
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - 60
player_speed = 5

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

# Enemy settings
enemy_radius = 20
enemy_speed = 3
enemies = []

# Scoring
score = 0
font = pygame.font.Font(None, 36)

# Victory condition
enemies_defeated = 0
target_score = 50  # You win when score reaches 50

# Static star field (generated once)
star_field = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
               random.randint(1, 3)) for _ in range(200)]  # 200 stars


def draw_text(text, size, color, x, y):
    """Draw text on the screen."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_player(x, y):
    """Draw the player's spaceship as a triangle."""
    points = [(x, y), (x - player_width // 2, y + player_height), (x + player_width // 2, y + player_height)]
    pygame.draw.polygon(screen, CYAN, points)


def draw_enemy(x, y):
    """Draw enemy spaceships as glowing circles."""
    pygame.draw.circle(screen, MAGENTA, (x, y), enemy_radius)


def show_victory_screen():
    """Display the Victory screen."""
    screen.fill(BLACK)
    draw_text("YOU WIN!", 72, NEON_GREEN, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50)
    draw_text("Press R to Restart or Q to Quit", 36, WHITE, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()


def reset_game():
    """Reset game variables for a new session."""
    global player_x, bullets, enemies, score, enemies_defeated
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    bullets.clear()
    enemies.clear()
    score = 0
    enemies_defeated = 0


def draw_star_field():
    """Create a static starry background effect."""
    for star in star_field:
        star_x, star_y, star_radius = star
        pygame.draw.circle(screen, WHITE, (star_x, star_y), star_radius)


# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Draw the starry background (static, no flickering)
    draw_star_field()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > player_width // 2:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width // 2:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:  # Limit bullets on screen
            bullet = pygame.Rect(player_x - bullet_width // 2, player_y, bullet_width, bullet_height)
            bullets.append(bullet)

    # Update bullet positions
    bullets = [bullet.move(0, -bullet_speed) for bullet in bullets if bullet.y > 0]

    # Generate enemies
    if random.randint(1, 30) == 1:  # Adjust spawn rate as needed
        enemy_x = random.randint(enemy_radius, SCREEN_WIDTH - enemy_radius)
        enemy_y = 0
        enemies.append((enemy_x, enemy_y))

    # Update enemy positions
    enemies = [(x, y + enemy_speed) for (x, y) in enemies if y + enemy_radius < SCREEN_HEIGHT]

    # Check for collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            enemy_x, enemy_y = enemy
            enemy_rect = pygame.Rect(enemy_x - enemy_radius, enemy_y - enemy_radius, 2 * enemy_radius, 2 * enemy_radius)
            if bullet.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1  # Increment score for hitting an enemy
                enemies_defeated += 1

    # Draw player (spaceship as triangle)
    draw_player(player_x, player_y)

    # Draw bullets (laser beams)
    for bullet in bullets:
        pygame.draw.rect(screen, NEON_BLUE, bullet)

    # Draw enemies (spaceships as glowing circles)
    for enemy in enemies:
        draw_enemy(enemy[0], enemy[1])

    # Draw score
    draw_text(f"Score: {score}", 36, WHITE, 10, 10)

    # Victory condition
    if score >= target_score:
        show_victory_screen()

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

shoot_sound = pygame.mixer.Sound('shoot.wav')  
hit_sound = pygame.mixer.Sound('hit.wav')      
victory_sound = pygame.mixer.Sound('victory.wav')  


# Quit Pygame
pygame.quit()
