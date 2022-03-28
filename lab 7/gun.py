import math
from random import choice, randint

import pygame

FPS = 200

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        t = 0.1
        g = 9.81

        if self.x >= 800 - self.r:
            self.x = 800 - self.r
            self.vx *= -0.7

        if self.x <= self.r:
            self.x = self.r
            self.vx *= -0.7

        if self.y > 600 - self.r:
            self.y = 600 - self.r
            self.vy *= -0.7

        if self.y <= self.r:
            self.y = self.r
            self.vy *= -0.7

        self.x += self.vx * t
        self.y -= self.vy * t
        self.vy = self.vy - g * t ** 2

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        d = math.sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)

        if d <= obj.r + self.r:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.point1 = [40, 450]
        self.height = 20
        self.width = 10

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        angle = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(angle)
        new_ball.vy = - self.f2_power * math.sin(angle)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            x = event.pos[0] - 20
            y = 450 - event.pos[1]
            if x == 0:
                x = 1
            self.an = math.atan(y / x)
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):

        point2 = [self.point1[0] + self.height, self.point1[1]]
        point3 = [self.point1[0], self.point1[1] - self.width]
        point4 = [self.height + self.point1[0], -self.width + self.point1[1]]
        pygame.draw.polygon(self.screen, self.color, (self.point1, rotate_point(point2, self.an, self.point1),
                                                      rotate_point(point4, self.an, self.point1),
                                                      rotate_point(point3, self.an, self.point1)))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target(Ball):

    def __init__(self, screen):
        self.screen = screen
        self.x = None
        self.y = None
        self.r = None
        self.color = None
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        r = self.r = randint(2, 50)
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


def rotate_point(point, angle, origin):
    x = origin[0] + math.cos(angle) * (point[0] - origin[0]) - math.sin(angle) * (point[1] - origin[1])
    y = origin[1] + math.sin(angle) * (-point[0] + origin[0]) + math.cos(angle) * (-point[1] + origin[1])

    point[0] = x
    point[1] = y

    return x, y

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        # b.vx <= 1 and b.y == HEIGHT - b.r:
        #     balls.remove(b)
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()

    gun.power_up()

pygame.quit()
