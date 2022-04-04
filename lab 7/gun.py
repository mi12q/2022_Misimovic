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
    def __init__(self, screen: pygame.Surface, x=40, y=450):  # napisati sve u init
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
    def __init__(self, screen, type):
        self.screen = screen
        self.f2_power = 10
        self.x = None
        self.vx = 2
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.point1 = [40, 450]
        self.point_up = [40, 100]
        self.height = 20
        self.width = 10
        self.type = type

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event, balls, bullet):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """

        bullet += 1
        new_ball = Ball(self.screen, self.point1[0], self.point1[1])
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
            if x <= 0:
                x = - (event.pos[0] + 1)
            self.an = math.atan(y / x)
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw1(self):
        a = (self.point1[0] - 25, self.point1[1] + 1)
        b = (self.point1[0] + 25, self.point1[1] + 15)
        c = (self.point1[0] - 25, self.point1[1] + 15)
        d = (self.point1[0] + 25, self.point1[1] + 1)
        point2 = [self.point1[0] + self.height, self.point1[1]]
        point3 = [self.point1[0], self.point1[1] - self.width]
        point4 = [self.height + self.point1[0], -self.width + self.point1[1]]
        pygame.draw.polygon(self.screen, self.color, (self.point1, rotate_point(point2, self.an, self.point1),
                                                      rotate_point(point4, self.an, self.point1),
                                                      rotate_point(point3, self.an, self.point1)))
        pygame.draw.polygon(self.screen, self.color, (a, c, b, d))
        pygame.draw.circle(self.screen, self.color, (self.point1[0] - 15, self.point1[1] + 20), 7)
        pygame.draw.circle(self.screen, self.color, (self.point1[0] + 15, self.point1[1] + 20), 7)

    def draw2(self):
        a = (self.point_up[0] - 25, self.point_up[1] + 1)
        b = (self.point_up[0] + 25, self.point_up[1] - 15)
        c = (self.point_up[0] - 25, self.point_up[1] - 15)
        d = (self.point_up[0] + 25, self.point_up[1] + 1)
        point2 = [self.point_up[0] + self.height, self.point_up[1]]
        point3 = [self.point_up[0], self.point_up[1] - self.width]
        point4 = [self.height + self.point_up[0], -self.width + self.point_up[1]]
        pygame.draw.polygon(self.screen, self.color, (self.point_up, rotate_point(point2, self.an, self.point_up),
                                                      rotate_point(point4, self.an, self.point_up),
                                                      rotate_point(point3, self.an, self.point_up)))
        pygame.draw.polygon(self.screen, self.color, (a, c, b, d))
        pygame.draw.circle(self.screen, self.color, (self.point_up[0] - 15, self.point_up[1] - 20), 7)
        pygame.draw.circle(self.screen, self.color, (self.point_up[0] + 15, self.point_up[1] - 20), 7)

    def draw(self):
        if self.type == 'down':
            self.draw1()
        if self.type == 'up':
            self.draw2()

    def move(self, direction):
        t = 0.7
        if self.type == 'down':

            if self.point1[0] > WIDTH - 25:
                self.vx *= -1

            if self.point1[0] < 25:
                self.vx *= -1

            if direction == 'right':
                self.point1[0] += self.vx * t
            if direction == 'left':
                self.point1[0] -= self.vx * t

        if self.type == 'up':

            if self.point_up[0] > WIDTH - 25:
                self.vx *= -1

            if self.point_up[0] < 25:
                self.vx *= -1

            if direction == 'right':
                self.point_up[0] += self.vx * t
            if direction == 'left':
                self.point_up[0] -= self.vx * t

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
        self.b = None
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
        self.r = randint(20, 70)
        self.b = randint(20, 70)
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
        pygame.draw.rect(self.screen, BLACK, [self.x, self.y, self.r + 1, self.r + 1])
        pygame.draw.rect(self.screen, BLUE, [self.x, self.y, self.r, self.r])

    def draw_ellipse(self):

        pygame.draw.ellipse(self.screen, YELLOW, [self.x, self.y, self.r + 1, self.b + 1], width=5)

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

    def move_ellipse(self):

        t = 1
        self.x += self.vx * t
        self.y += self.vy * t

        if self.x > WIDTH - self.b:
            self.x = WIDTH - self.b
            self.vx *= -1

        if self.y > HEIGHT - 100 - self.r:
            self.y = HEIGHT - 100 - self.r
            self.vy *= -1

        if self.y < self.r:
            self.y = self.r
            self.vy *= -1

        if self.x < self.b:
            self.x = self.b
            self.vx *= -1

    def draw(self):
        if self.type == 'ball':
            self.draw_ball()
        if self.type == 'square':
            self.draw_square()
        if self.type == 'ellipse':
            self.draw_ellipse()

    def move(self):
        if self.type == 'ball':
            self.move_ball()
        if self.type == 'square':
            self.move_square()
        if self.type == 'ellipse':
            self.move_ellipse()


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


def write_score(screen, obj):
    font = pygame.font.SysFont('consolas', 100)
    score = obj.points
    text = "Hit goal in " + str(score)
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (10, 300))


def events(gun1, gun2, balls, bullet):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun1.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun1.fire2_end(event, balls, bullet)
        elif event.type == pygame.MOUSEMOTION:
            gun1.targetting(event)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        gun1.move('right')
    if keys[pygame.K_LEFT]:
        gun1.move('left')
    if keys[pygame.K_a]:
        gun2.move('left')
    if keys[pygame.K_d]:
        gun2.move('right')


def create_game_objects(screen):
    gun1 = Gun(screen, 'down')
    gun2 = Gun(screen, 'up')
    target1 = Target(screen, 'ball')
    target2 = Target(screen, 'square')
    target3 = Target(screen, 'ellipse')

    return gun1, gun2, target1, target2, target3


def move_guns_targets(gun1, gun2, target1, target2, target3):
    gun1.draw()
    gun2.draw()
    target1.move()
    target1.draw()
    target2.move()
    target2.draw()
    target3.move()
    target3.draw()


def check_if_hit(balls, target1, target2, target3):
    for b in balls:
        b.move()

        if b.vx == 0:
            balls.remove(b)
        if b.hittest(target1) and target1.live:
            balls.remove(b)
            target1.live = 0
            target1.hit()
            target1.new_target()
        if b.hittest(target2) and target2.live:
            balls.remove(b)
            target2.live = 0
            target2.hit()
            target2.new_target()
        if b.hittest(target3) and target3.live:
            balls.remove(b)
            target3.live = 0
            target3.hit()
            target3.new_target()


def game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Gun')
    bullet = 0
    balls = []
    clock = pygame.time.Clock()
    finished = False
    gun1, gun2, target1, target2, target3 = create_game_objects(screen)

    while not finished:
        screen.fill(WHITE)
        move_guns_targets(gun1, gun2, target1, target2, target3)
        for b in balls:
            b.draw()
        pygame.display.update()
        clock.tick(FPS)
        events(gun1, gun2, balls, bullet)
        check_if_hit(balls, target1, target2, target3)
        gun1.power_up()


game()
