import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабиринт Сокровищ")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BLUE = (0, 0, 255)

# Размер клетки лабиринта
CELL_SIZE = 40

# Лабиринт (1 - стена, 0 - путь, 'T' - сокровище, 'E' - выход, 'L' - ловушка)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 'T', 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 'T', 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'E', 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Игрок
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE - 5, CELL_SIZE - 5))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE + 2
        self.rect.y = y * CELL_SIZE + 2
        self.speed = CELL_SIZE
        self.treasures = 0
    
    def move(self, dx, dy):
        new_x = (self.rect.x // CELL_SIZE) + dx
        new_y = (self.rect.y // CELL_SIZE) + dy
        
        # Проверка на выход за границы
        if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze):
            cell = maze[new_y][new_x]
            
            # Если это стена - не двигаться
            if cell == 1:
                return False
            
            # Если это сокровище - собрать
            elif cell == 'T':
                maze[new_y][new_x] = 0  # Убираем сокровище
                self.treasures += 1
                self.rect.x = new_x * CELL_SIZE + 2
                self.rect.y = new_y * CELL_SIZE + 2
                return True
            
            # Если это выход - проверить, собраны ли все сокровища
            elif cell == 'E':
                if self.treasures == 2:  # Все сокровища собраны
                    return "WIN"
                else:
                    return False
            
            # Если это ловушка - проигрыш
            elif cell == 'L':
                return "LOSE"
            
            # Пустая клетка
            else:
                self.rect.x = new_x * CELL_SIZE + 2
                self.rect.y = new_y * CELL_SIZE + 2
                return True
        return False

# Основная функция игры
def main():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 24)
    
    # Создание игрока (начальная позиция)
    player = Player(1, 1)
    all_sprites = pygame.sprite.Group(player)
    
    game_state = "PLAYING"  # PLAYING, WIN, LOSE
    
    # Главный игровой цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if game_state == "PLAYING" and event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_LEFT:
                    moved = player.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    moved = player.move(1, 0)
                elif event.key == pygame.K_UP:
                    moved = player.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    moved = player.move(0, 1)
                
                # Проверка исхода движения
                if moved == "WIN":
                    game_state = "WIN"
                elif moved == "LOSE":
                    game_state = "LOSE"
        
        # Отрисовка
        screen.fill(BLACK)
        
        # Рисуем лабиринт
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                cell = maze[y][x]
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if cell == 1:  # Стена
                    pygame.draw.rect(screen, WHITE, rect)
                elif cell == 'T':  # Сокровище
                    pygame.draw.rect(screen, GOLD, rect)
                elif cell == 'E':  # Выход
                    pygame.draw.rect(screen, GREEN, rect)
                elif cell == 'L':  # Ловушка
                    pygame.draw.rect(screen, RED, rect)
                
                pygame.draw.rect(screen, BLACK, rect, 1)  # Сетка
        
        # Рисуем игрока
        all_sprites.draw(screen)
        
        # Отображение счёта
        score_text = font.render(f"Сокровища: {player.treasures}/2", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Сообщения о победе/поражении
        if game_state == "WIN":
            win_text = font.render("Победа! Найден выход и все сокровища!", True, GREEN)
            screen.blit(win_text, (WIDTH // 2 - 200, HEIGHT // 2))
        elif game_state == "LOSE":
            lose_text = font.render("Поражение! Вы попали в ловушку!", True, RED)
            screen.blit(lose_text, (WIDTH // 2 - 150, HEIGHT // 2))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()