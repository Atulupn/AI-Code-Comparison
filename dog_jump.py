import pygame
import random

# --- Настройки ---
WIDTH, HEIGHT = 800, 480
FPS = 60
GRAVITY = 0.6
JUMP_VEL = -14
PLATFORM_WIDTH = 90
PLATFORM_HEIGHT = 15
PLATFORM_SPACING = 80

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (135, 206, 235)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dog Jump")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

dog_img = pygame.transform.scale(pygame.image.load("dog.png"), (40, 40))
bone_img = pygame.transform.scale(pygame.image.load("bone.png"), (25, 25))

try:
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
except:
    print("⚠ Музыка не найдена")

class Player(pygame.sprite.Sprite):
    def __init__(self, start_platform):
        super().__init__()
        self.image = dog_img
        self.rect = self.image.get_rect(midbottom=(start_platform.rect.centerx, start_platform.rect.top))
        self.vel_y = 0
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 5

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        if self.rect.left < -40:
            self.rect.right = WIDTH
        elif self.rect.right > WIDTH + 40:
            self.rect.left = 0

    def jump(self):
        self.vel_y = JUMP_VEL

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill((100, 200, 100))
        self.rect = self.image.get_rect(topleft=(x, y))

class Bone(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bone_img
        self.rect = self.image.get_rect(center=(x, y))

class Cloud:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 100)
        self.y = random.randint(0, HEIGHT // 2)
        self.w = random.randint(60, 100)
        self.h = random.randint(30, 50)
        self.speed = random.uniform(0.2, 0.5)

    def update(self):
        self.x += self.speed
        if self.x > WIDTH:
            self.x = -self.w
            self.y = random.randint(0, HEIGHT // 2)

    def draw(self, surf):
        pygame.draw.ellipse(surf, WHITE, (self.x, self.y, self.w, self.h))

def create_initial_platforms():
    platforms = pygame.sprite.Group()
    y = HEIGHT - 60
    for _ in range(7):
        x = random.randint(0, WIDTH - PLATFORM_WIDTH)
        plat = Platform(x, y)
        platforms.add(plat)
        y -= PLATFORM_SPACING
    return platforms

last_direction = 1

def add_platform(platforms, bones):
    global last_direction
    highest_platform = min(platforms, key=lambda p: p.rect.y)
    prev_x = highest_platform.rect.x

    # Увеличенный горизонтальный сдвиг
    shift_x = random.randint(80, 120) * last_direction
    new_x = prev_x + shift_x

    if new_x < 0:
        new_x = 0
        last_direction = 1
    elif new_x > WIDTH - PLATFORM_WIDTH:
        new_x = WIDTH - PLATFORM_WIDTH
        last_direction = -1
    else:
        if random.random() < 0.3:
            last_direction *= -1

    new_y = highest_platform.rect.y - PLATFORM_SPACING
    plat = Platform(new_x, new_y)
    platforms.add(plat)

    if random.random() < 0.5:
        bones.add(Bone(new_x + PLATFORM_WIDTH // 2, new_y - 20))

def main():
    global last_direction
    platforms = create_initial_platforms()
    bottom_platform = max(platforms, key=lambda p: p.rect.y)
    player = Player(bottom_platform)

    bones = pygame.sprite.Group()
    clouds = [Cloud() for _ in range(5)]
    high_score = 0
    game_over = False
    scroll = 0
    last_direction = 1

    for plat in platforms:
        if random.random() < 0.5:
            bones.add(Bone(plat.rect.centerx, plat.rect.top - 20))

    running = True
    while running:
        clock.tick(FPS)

        if not game_over:
            player.update()

            if player.vel_y > 0:
                hits = pygame.sprite.spritecollide(player, platforms, False)
                if hits:
                    lowest = hits[0]
                    if player.rect.bottom <= lowest.rect.bottom + 10 and player.vel_y >= 0:
                        player.rect.bottom = lowest.rect.top
                        player.jump()

            hits = pygame.sprite.spritecollide(player, bones, True)
            player.score += len(hits)

            if player.rect.top <= HEIGHT // 3:
                scroll = HEIGHT // 3 - player.rect.top
                player.rect.top = HEIGHT // 3
                for plat in platforms:
                    plat.rect.y += scroll
                for bone in bones:
                    bone.rect.y += scroll
                add_platform(platforms, bones)

            platforms = pygame.sprite.Group([p for p in platforms if p.rect.top < HEIGHT])
            bones = pygame.sprite.Group([b for b in bones if b.rect.top < HEIGHT])

            for cloud in clouds:
                cloud.update()

            if player.rect.top > HEIGHT:
                game_over = True
                if player.score > high_score:
                    high_score = player.score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    main()
                    return

        screen.fill(SKY)
        for cloud in clouds:
            cloud.draw(screen)
        platforms.draw(screen)
        bones.draw(screen)
        screen.blit(player.image, player.rect)

        score_text = font.render(f"Счёт: {player.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        record_text = font.render(f"Рекорд: {high_score}", True, BLACK)
        screen.blit(record_text, (WIDTH - 160, 10))

        if game_over:
            over_text = font.render("Ты упал! Нажми R, чтобы перезапустить", True, BLACK)
            screen.blit(over_text, (WIDTH // 2 - 180, HEIGHT // 2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
