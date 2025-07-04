import pygame
import random
import sys
import os

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Звездный Сборщик")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (100, 0, 200)
BLUE = (0, 0, 100)
CYAN = (0, 255, 255)
GRAY = (150, 150, 150)

# Космический фон (градиент с планетами и туманностями)
def draw_background():
    for y in range(HEIGHT):
        r = max(10 - y // 30, 0)
        g = 0
        b = max(50 - y // 10, 20)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
    for planet in background_planets:
        pygame.draw.circle(screen, planet["color"], (planet["x"], planet["y"]), planet["radius"])
    for nebula in background_nebulas:
        nebula_surface = pygame.Surface((nebula["size"], nebula["size"]), pygame.SRCALPHA)
        pygame.draw.circle(nebula_surface, (*nebula["color"], nebula["alpha"]),
                          (nebula["size"] // 2, nebula["size"] // 2), nebula["size"] // 2)
        screen.blit(nebula_surface, (nebula["x"], nebula["y"]))

# Игрок (пиксельный космический корабль)
player_size = 20
player_surface = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
pixel_size = player_size // 8
player_ship = [
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 1]
]
for y, row in enumerate(player_ship):
    for x, pixel in enumerate(row):
        if pixel:
            pygame.draw.rect(player_surface, WHITE, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))

# Сердечко для здоровья
heart_size = 16
heart_surface = pygame.Surface((heart_size, heart_size), pygame.SRCALPHA)
heart_pixels = [
    [0, 1, 1, 0, 0, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
for y, row in enumerate(heart_pixels):
    for x, pixel in enumerate(row):
        if pixel:
            pygame.draw.rect(heart_surface, RED, (x * 2, y * 2, 2, 2))

# Загрузка звуков
try:
    collect_sound = pygame.mixer.Sound('collect.wav')
except FileNotFoundError:
    collect_sound = None
    print("Файл collect.wav не найден. Звук сбора звезд отключен.")
try:
    collision_sound = pygame.mixer.Sound('collision.wav')
except FileNotFoundError:
    collision_sound = None
    print("Файл collision.wav не найден. Звук столкновения отключен.")
try:
    heart_sound = pygame.mixer.Sound('heart_collect.wav')
except FileNotFoundError:
    heart_sound = None
    print("Файл heart_collect.wav не найден. Звук сбора сердец отключен.")

# Часы для управления FPS
clock = pygame.time.Clock()

# Функция инициализации игры
def init_game():
    global player_x, player_y, player_health, player_speed, score, star_x, star_y
    global super_star_x, super_star_y, super_star_timer, bonus_x, bonus_y
    global asteroids, background_stars, background_planets, background_nebulas, player_trail
    player_x = WIDTH // 2
    player_y = HEIGHT // 2
    player_health = 3
    player_speed = 5
    score = 0
    star_x = random.randint(0, WIDTH)
    star_y = random.randint(0, HEIGHT)
    super_star_x = None
    super_star_y = None
    super_star_timer = 0
    bonus_x = None
    bonus_y = None
    player_trail = []
    asteroids = [
        {
            "x": random.randint(0, WIDTH),
            "y": random.randint(0, HEIGHT),
            "speed_x": random.choice([-2, 2]),
            "speed_y": random.choice([-2, 2])
        } for _ in range(3)
    ]
    background_stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(50)]
    background_planets = [
        {"x": random.randint(100, WIDTH-100), "y": random.randint(100, HEIGHT-100),
         "radius": random.randint(20, 50), "color": (random.randint(50, 150), 0, random.randint(50, 150))}
        for _ in range(3)
    ]
    background_nebulas = [
        {"x": random.randint(50, WIDTH-50), "y": random.randint(50, HEIGHT-50),
         "size": random.randint(100, 200), "color": (random.randint(0, 100), 0, random.randint(50, 150)),
         "alpha": random.randint(50, 100)}
        for _ in range(2)
    ]

# Основные параметры игры
star_size = 10
super_star_size = 20
super_star_interval = 600  # 10 секунд при 60 FPS
bonus_size = 10
asteroid_size = 20
max_health = 5
highscore_file = "highscore.txt"
highscore = 0
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as f:
        highscore = int(f.read().strip() or 0)

# Инициализация игры
init_game()

# Основной цикл игры
while True:
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Управление игроком (WASD)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_d] and player_x < WIDTH - player_size:
            player_x += player_speed
        if keys[pygame.K_w] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_s] and player_y < HEIGHT - player_size:
            player_y += player_speed

        # Обновление шлейфа игрока
        player_trail.append((player_x, player_y))
        if len(player_trail) > 5:
            player_trail.pop(0)

        # Движение астероидов
        for asteroid in asteroids:
            asteroid["x"] += asteroid["speed_x"]
            asteroid["y"] += asteroid["speed_y"]
            if asteroid["x"] <= 0 or asteroid["x"] >= WIDTH - asteroid_size:
                asteroid["speed_x"] = -asteroid["speed_x"]
            if asteroid["y"] <= 0 or asteroid["y"] >= HEIGHT - asteroid_size:
                asteroid["speed_y"] = -asteroid["speed_y"]

        # Появление суперзвезды
        super_star_timer += 1
        if super_star_timer >= super_star_interval and super_star_x is None:
            super_star_x = random.randint(0, WIDTH)
            super_star_y = random.randint(0, HEIGHT)
            super_star_timer = 0

        # Проверка столкновения со звездой
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        star_rect = pygame.Rect(star_x, star_y, star_size, star_size)
        if player_rect.colliderect(star_rect):
            score += 1
            if score > highscore:
                highscore = score
            if collect_sound:
                collect_sound.play()
            star_x = random.randint(0, WIDTH)
            star_y = random.randint(0, HEIGHT)
            if random.random() < 0.1:
                bonus_x = random.randint(0, WIDTH)
                bonus_y = random.randint(0, HEIGHT)
            else:
                bonus_x, bonus_y = None, None
            if score % 5 == 0:
                asteroids.append({
                    "x": random.randint(0, WIDTH),
                    "y": random.randint(0, HEIGHT),
                    "speed_x": random.choice([-3, 3]),
                    "speed_y": random.choice([-3, 3])
                })

        # Проверка столкновения с суперзвездой
        if super_star_x is not None and super_star_y is not None:
            super_star_rect = pygame.Rect(super_star_x, super_star_y, super_star_size, super_star_size)
            if player_rect.colliderect(super_star_rect):
                score += 5
                if score > highscore:
                    highscore = score
                if collect_sound:
                    collect_sound.play()
                super_star_x, super_star_y = None, None

        # Проверка столкновения с бонусным сердцем
        if bonus_x is not None and bonus_y is not None:
            bonus_rect = pygame.Rect(bonus_x, bonus_y, bonus_size, bonus_size)
            if player_rect.colliderect(bonus_rect):
                if player_health < max_health:
                    player_health += 1
                if heart_sound:
                    heart_sound.play()
                bonus_x, bonus_y = None, None

        # Проверка столкновения с астероидами
        for asteroid in asteroids:
            asteroid_rect = pygame.Rect(asteroid["x"], asteroid["y"], asteroid_size, asteroid_size)
            if player_rect.colliderect(asteroid_rect):
                player_health -= 1
                if collision_sound:
                    collision_sound.play()
                asteroid["x"] = random.randint(0, WIDTH)
                asteroid["y"] = random.randint(0, HEIGHT)
                if player_health <= 0:
                    game_over = True

        # Отрисовка
        draw_background()
        for star in background_stars:
            pygame.draw.circle(screen, WHITE, star, 2)
        for i, pos in enumerate(player_trail):
            alpha = int(255 * (1 - i / len(player_trail)))
            trail_surface = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
            pygame.draw.rect(trail_surface, (100, 150, 255, alpha), (0, 0, player_size, player_size))
            screen.blit(trail_surface, pos)
        screen.blit(player_surface, (player_x, player_y))
        if pygame.time.get_ticks() % 20 < 10:
            pygame.draw.circle(screen, YELLOW, (star_x + star_size // 2, star_y + star_size // 2), star_size // 2)
        if super_star_x is not None and super_star_y is not None:
            if pygame.time.get_ticks() % 20 < 10:
                pygame.draw.circle(screen, CYAN, (super_star_x + super_star_size // 2,
                                                super_star_y + super_star_size // 2), super_star_size // 2)
        if bonus_x is not None and bonus_y is not None:
            screen.blit(heart_surface, (bonus_x, bonus_y))
        for asteroid in asteroids:
            pygame.draw.circle(screen, RED, (asteroid["x"] + asteroid_size // 2, asteroid["y"] + asteroid_size // 2),
                              asteroid_size // 2)
        font = pygame.font.SysFont('arial', 36)
        score_text = font.render(f"Очки: {score}", True, WHITE)
        highscore_text = font.render(f"Рекорд: {highscore}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(highscore_text, (10, 50))
        for i in range(player_health):
            screen.blit(heart_surface, (10 + i * (heart_size + 5), 90))
        pygame.display.flip()
        clock.tick(60)

    # Сохранение рекорда
    with open(highscore_file, "w") as f:
        f.write(str(highscore))

    # Экран окончания игры с кнопкой "Начать заново"
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    init_game()  # Перезапуск игры
                    game_over = False

        draw_background()
        font = pygame.font.SysFont('arial', 74)
        game_over_text = font.render(f"Игра окончена! Очки: {score}", True, WHITE)
        highscore_text = font.render(f"Рекорд: {highscore}", True, WHITE)
        # Центрирование текста с правильным отступом
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, HEIGHT // 2 + 20))

        # Отрисовка кнопки
        pygame.draw.rect(screen, GRAY, button_rect)
        font = pygame.font.SysFont('arial', 36)
        button_text = font.render("Начать заново", True, BLACK)
        screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, HEIGHT // 2 + 110))
        pygame.display.flip()
        clock.tick(60)