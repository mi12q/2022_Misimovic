import math
from random import choice, randint
import time

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

        if self.x >= WIDTH - self.r:
            self.x = WIDTH - self.r
            self.vx *= -0.7
            self.vy *= 0.7

        if self.x <= self.r:
            self.x = self.r
            self.vx *= -0.7
            self.vy *= 0.7

        if self.y > HEIGHT - 100 - self.r:
            self.y = HEIGHT - 100 - self.r
            self.vy *= -0.7
            self.vx *= 0.7

        if self.y <= self.r:
            self.y = self.r
            self.vy *= -0.7
            self.vx *= 0.7

        if abs(self.vx) < 1:
            self.vx = 0
            self.vy = 0

        self.x += self.vx * t
        self.y -= self.vy * t
        self.vy = self.vy - g * t ** 2

    def draw(self):
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r + 1
        )
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

    def fire2_end(self, event, balls, bullet):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """

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
                self.height += 0.5
            self.color = YELLOW
        else:
            self.color = BLACK
            self.height = 20


class Target():

    def __init__(self, screen, type):
        self.screen = screen
        self.x = None
        self.y = None
        self.r = None
        self.color = None
        self.size = None
        self.vy = 2
        self.vx = 2
        self.points = 0
        self.live = 1
        self.new_target()
        self.type = type

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 700)
        self.y = randint(10, 400)
        self.r = randint(10, 50)
        self.live = 1
        self.color = RED


    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw_ball(self):
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r + 1
        )
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def draw_square(self):
        pygame.draw.rect(self.screen, BLACK, [self.x, self.y, self.r+1, self.r+1])
        pygame.draw.rect(self.screen, BLUE, [self.x, self.y, self.r, self.r])

    def draw_star(self):


    def move_ball(self):

        t = 1
        if self.y > HEIGHT - 100 - self.r:
            self.y = HEIGHT - 100 - self.r
            self.vy *= -1

        if self.y <= self.r:
            self.y = self.r
            self.vy *= -1

        self.y += self.vy

    def move_square(self):
        t = 1

        if self.x > WIDTH - self.r:
            self.vx *= -1

        if self.x < self.r / 2:
            self.vx *= -1

        self.x += self.vx * t

    def draw(self):
        if self.type == 'ball':
            self.draw_ball()
        if self.type == 'square':
            self.draw_square()

    def move(self):
        if self.type == 'ball':
            self.move_ball()
        if self.type == 'square':
            self.move_square()


def rotate_point(point, angle, origin):
    x = origin[0] + math.cos(angle) * (point[0] - origin[0]) - math.sin(angle) * (point[1] - origin[1])
    y = origin[1] + math.sin(angle) * (-point[0] + origin[0]) + math.cos(angle) * (-point[1] + origin[1])

    point[0] = x
    point[1] = y

    return x, y



def write(screen):
    font = pygame.font.Font('freesansbold.ttf', 32)

    # create a text surface object,
    # on which text is drawn on it.
    text = font.render('GUN', True, GREEN, BLUE)

    # create a rectangular object for the
    # text surface object
    rect = text.get_rect()

    # set the center of the rectangular object.
    rect.center = (WIDTH // 2, HEIGHT // 2)

    screen.blit(text, rect)



def game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Gun')
    bullet = 0
    balls = []
    clock = pygame.time.Clock()
    gun = Gun(screen)
    target1 = Target(screen, 'ball')
    target2 = Target(screen, 'square')

    finished = False

    while not finished:
        screen.fill(WHITE)
        gun.draw()
        target1.move()
        target1.draw()
        target2.move()
        target2.draw()


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
                gun.fire2_end(event, balls, bullet)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)



        for b in balls:
            b.move()

            if b.vx == 0:
                balls.remove(b)
            if b.hittest(target1) and target1.live:
                target1.live = 0
                target1.hit()
                target1.new_target()
            if b.hittest(target2) and target2.live:
                target2.live = 0
                target2.hit()
                target2.new_target()

        gun.power_up()

    pygame.quit()

game()