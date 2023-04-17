import pygame
import random

# константы
width = 720
height = 1440
gravity = 0.25
jump_strength = 5
pipe_gap = 150

# инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.SysFont(None, 30)

# класс птицы
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0

    def update(self):
        self.velocity += gravity
        self.y += self.velocity

    def jump(self):
        self.velocity = -jump_strength

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), 20)

# класс трубы
class Pipe:
    def __init__(self, x):
        self.x = x
        self.top_height = random.randint(100, height - pipe_gap - 100)
        self.bottom_height = height - pipe_gap - self.top_height
        self.width = 50
        self.speed = 3
        self.scored = False

    def update(self):
        self.x -= self.speed

    def offscreen(self):
        return self.x < -self.width

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(surface, (0, 255, 0), (self.x, height - self.bottom_height, self.width, self.bottom_height))

# создание объектов
bird = Bird(width/2, height/2)
pipes = [Pipe(width)]

# переменные игры
running = True
score = 0

# главный цикл игры
while running:
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            bird.jump()

    # обновление
    bird.update()
    for pipe in pipes:
        pipe.update()

        if pipe.offscreen():
            pipes.remove(pipe)
            pipes.append(Pipe(width))

        if bird.x > pipe.x and bird.x < pipe.x + pipe.width:
            if bird.y < pipe.top_height or bird.y > height - pipe.bottom_height:
                # restart the game
                bird = Bird(width/2, height/2)
                pipes = [Pipe(width)]
                score = 0

            if bird.x > pipe.x + pipe.width/2 and not pipe.scored:
                pipe.scored = True
                score += 1

    # отрисовка
    screen.fill((255, 255, 255))
    bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()

