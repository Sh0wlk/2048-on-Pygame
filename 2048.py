import pygame
import random

WIDTH = 400
HEIGHT = 400
FPS = 60
mass = 4
numsize = WIDTH // mass  # Размер плитки, чтобы заполнить экран
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
numcol = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (246, 124, 95),
    32: (246, 94, 59),
    64: (237, 207, 114),
    128: (237, 204, 97),
    256: (237, 200, 80),
    512: (237, 197, 63),
    1024: (237, 194, 46),
    2048: (237, 194, 46)
}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()


class Game:
    def __init__(self):
        self.massp = [[0] * mass for i in range(mass)]
        self.spawn_num()

    def spawn_num(self):
        empty_num = [(i, j) for i in range(mass) for j in range(mass) if self.massp[i][j] == 0]
        if empty_num:
            i, j = random.choice(empty_num)
            self.massp[i][j] = 2

    def compress(self):
        new_massp = [[0] * mass for i in range(mass)]
        for i in range(mass):
            pos = 0
            for j in range(mass):
                if self.massp[i][j] != 0:
                    new_massp[i][pos] = self.massp[i][j]
                    pos += 1
        self.massp = new_massp

    def plus(self):
        for i in range(mass):
            for j in range(mass - 1):
                if self.massp[i][j] == self.massp[i][j + 1] and self.massp[i][j] != 0:
                    self.massp[i][j] *= 2
                    self.massp[i][j + 1] = 0

    def move(self):
        self.compress()
        self.plus()
        self.compress()

    def rotate(self):
        self.massp = [list(i) for i in zip(*self.massp[::-1])]

    def move_left(self):
        self.move()

    def move_right(self):
        self.rotate()
        self.rotate()
        self.move()
        self.rotate()
        self.rotate()

    def move_up(self):
        self.rotate()
        self.rotate()
        self.rotate()
        self.move()
        self.rotate()

    def move_down(self):
        self.rotate()
        self.move()
        self.rotate()
        self.rotate()
        self.rotate()

    def make(self):
        for i in range(mass):
            for j in range(mass):
                pygame.draw.rect(screen, numcol[self.massp[i][j]], (j * numsize, i * numsize, numsize, numsize))
                if self.massp[i][j] != 0:
                    font = pygame.font.Font(None, 55)
                    text = font.render(str(self.massp[i][j]), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(j * numsize + numsize // 2, i * numsize + numsize // 2))
                    screen.blit(text, text_rect)


# Инициализация игры
game = Game()

# Цикл игры
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.move_left()
                game.spawn_num()
            elif event.key == pygame.K_RIGHT:
                game.move_right()
                game.spawn_num()
            elif event.key == pygame.K_UP:
                game.move_up()
                game.spawn_num()
            elif event.key == pygame.K_DOWN:
                game.move_down()
                game.spawn_num()

    screen.fill(BLACK)
    game.make()
    pygame.display.flip()

pygame.quit()