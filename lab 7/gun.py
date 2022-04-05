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
    def __init__(self, screen: pygame.Surface, x=40, y=450, r=10, vx=0, vy=0, color=choice(GAME_COLORS), live=30):
        """
        Constructor of class ball

        :param screen: - screen
        :param x: - coordinate
        :param y: - coordinate
        :param r: - radius
        :param vx: - x velocity
        :param vy: - y velocity
        :param color: - color
        :param live: - live
        """

        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = color
        self.live = live

    def move(self):
        """
        Function moves ball
        :return:
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
        """
        Function draws a ball
        :return:
        """
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
        """
        Function checks if ball has hit the target
        :param obj: - target
        :return: - True - if ball hit the target
                - False - if ball hasn't hit the target
        """
        d = math.sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)

        if d <= obj.r + self.r:
            return True
        else:
            return False


class Square(Ball):
    def __init__(self, screen, x, y):
        """
        Constructor of class Square
        :param screen: - screen
        :param x: - coordinate x
        :param y: - coordinate y
        """
        super().__init__(screen, x, y)

    def draw(self):
        """
        Function draws a square
        :return:
        """
        pygame.draw.rect(self.screen, BLACK, [self.x, self.y, self.r + 1, self.r + 1])
        pygame.draw.rect(self.screen, self.color, [self.x, self.y, self.r, self.r])


class Gun:
    def __init__(self, screen, types='down', f2_power=10, x=None, vx=2, f2_on=0, an=1, color=GREY, height=20, width=10):
        """

        :param screen: - screen
        :param types: - upper or lower gun
        :param f2_power: - gun power
        :param x: - coordinate x
        :param vx: - x velocity
        :param f2_on: - turn gun on
        :param an: - angle
        :param color: - color
        :param height: - height
        :param width: - width
        """
        self.screen = screen
        self.types = types
        self.f2_power = f2_power
        self.x = x
        self.vx = vx
        self.f2_on = f2_on
        self.an = an
        self.color = color
        self.point1 = [40, 450]
        self.point_up = [50, 100]
        self.height = height
        self.width = width

    def fire2_start(self):
        """
        Function turns the gun on
        :return:
        """
        self.f2_on = 1

    def fire2_end(self, event, balls, bullet):
        """
        Function shoots and creates balls

        :param event: - mouse
        :param balls: - list of bullets on the screen
        :param bullet: - count of bullets
        :return:
        """

        bullet += 1
        if self.types == 'down':
            point = self.point1
        else:
            point = self.point_up
        new_ball = Ball(self.screen, point[0], point[1])
        new_ball.r += 5
        angle = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(angle)
        new_ball.vy = - self.f2_power * math.sin(angle)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def fire3_end(self, event, objects, bullet):
        """
        Function shoots and creates squares

        :param event: - mouse
        :param objects: - list of bullets on the screen
        :param bullet: - count of bullets
        :return:
        """
        bullet += 1
        if self.types == 'down':
            point = self.point1
        else:
            point = self.point_up
        new_square = Square(self.screen, point[0], point[1])
        new_square.r += 5
        angle = math.atan2((event.pos[1] - new_square.y), (event.pos[0] - new_square.x))
        new_square.vx = self.f2_power * math.cos(angle)
        new_square.vy = - self.f2_power * math.sin(angle)
        objects.append(new_square)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """
        Function moves gun depending on mouse position and changes its colour
        :param event: - mouse movement
        :return:
        """
        if event:
            x = event.pos[0] - 20
            y = 450 - event.pos[1]
            if x == 0:
                x = -1
            self.an = math.atan(y / x)
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw1(self):
        """
        Function draws upper gun
        :return:
        """
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
        """
        Function draws lower gun
        :return:
        """
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
        """
        Function checks which gun should be drawn
        :return:
        """
        if self.types == 'down':
            self.draw1()
        if self.types == 'up':
            self.draw2()

    def move(self, direction):
        """
        Function moves gun
        :param direction: - left or right direction
        :return:
        """

        t = 0.7
        if self.types == 'down':

            if self.point1[0] > WIDTH - 25:
                self.vx *= -1

            if self.point1[0] < 25:
                self.vx *= -1

            if direction == 'right':
                self.point1[0] += self.vx * t
            if direction == 'left':
                self.point1[0] -= self.vx * t

        if self.types == 'up':

            if self.point_up[0] > WIDTH - 25:
                self.vx *= -1

            if self.point_up[0] < 25:
                self.vx *= -1

            if direction == 'right':
                self.point_up[0] += self.vx * t
            if direction == 'left':
                self.point_up[0] -= self.vx * t

    def power_up(self):
        """
        Function powers up gun
        :return:
        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
                self.height += 0.5
            self.color = YELLOW
        else:
            self.color = BLACK
            self.height = 20


class Target:

    def __init__(self, screen, types, x=None, y=None, r=None, b=None, color=choice(GAME_COLORS), size=None, vy=2, vx=2,
                 points=0, live=1):
        """
        Constructor of class Target

        :param screen: - screen
        :param types: - ball or square
        :param x: - x coordinate
        :param y: - y coordinate
        :param r: - radius
        :param b: - ellipse parameter
        :param color: - color
        :param size: - size
        :param vy: - y velocity
        :param vx: - x velocity
        :param points: - points
        :param live: - live
        """
        self.screen = screen
        self.types = types
        self.x = x
        self.y = y
        self.r = r
        self.b = b
        self.color = color
        self.size = size
        self.vy = vy
        self.vx = vx
        self.points = points
        self.live = live
        self.new_target()

    def new_target(self):
        """
        Function creates a new target
        :return:
        """
        self.x = randint(600, 700)
        self.y = randint(10, 400)
        self.r = randint(20, 70)
        self.b = randint(20, 70)
        self.live = 1
        self.color = RED

    def hit(self, points=1):
        """
        Function adds up points
        :param points:
        :return:
        """
        self.points += points

    def draw_ball(self):
        """
        Functon draws a ball target
        :return:
        """
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
        """
        Function draws a square target
        :return:
        """

        pygame.draw.rect(self.screen, BLACK, [self.x, self.y, self.r + 1, self.r + 1])
        pygame.draw.rect(self.screen, BLUE, [self.x, self.y, self.r, self.r])

    def draw_ellipse(self):
        """
        Function draws an ellipse target
        :return:
        """

        pygame.draw.ellipse(self.screen, YELLOW, [self.x, self.y, self.r + 1, self.b + 1], width=5)

    def move_ball(self):
        """
        Function moves a ball target
        :return:
        """

        if self.y > HEIGHT - 100 - self.r:
            self.y = HEIGHT - 100 - self.r
            self.vy *= -1

        if self.y <= self.r:
            self.y = self.r
            self.vy *= -1

        self.y += self.vy

    def move_square(self):
        """
        Function moves a square target
        :return:
        """

        t = 1

        if self.x > WIDTH - self.r:
            self.vx *= -1

        if self.x < self.r / 2:
            self.vx *= -1

        self.x += self.vx * t

    def move_ellipse(self):
        """
        Function moves a ellipse target
        :return:
        """

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
        """
        Function checks which target should be drawn
        :return:
        """

        if self.types == 'ball':
            self.draw_ball()
        if self.types == 'square':
            self.draw_square()
        if self.types == 'ellipse':
            self.draw_ellipse()

    def move(self):
        """
        Function checks which target should me moved
        :return:
        """

        if self.types == 'ball':
            self.move_ball()
        if self.types == 'square':
            self.move_square()
        if self.types == 'ellipse':
            self.move_ellipse()


def rotate_point(point, angle, origin):
    """
    Function rotates point around another point, given angle
    :param point: - point coordinates
    :param angle: - angle
    :param origin: - origin coordinates
    :return:
    """
    x = origin[0] + math.cos(angle) * (point[0] - origin[0]) - math.sin(angle) * (point[1] - origin[1])
    y = origin[1] + math.sin(angle) * (-point[0] + origin[0]) + math.cos(angle) * (-point[1] + origin[1])

    point[0] = x
    point[1] = y

    return x, y


def text_objects(text, font):
    """
    Function creates text surface
    :param text: - text
    :param font: - font
    :return:
    """
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


def message_display(text, screen):
    """
    Function displays text
    :param text: - text
    :param screen: - screen
    :return:
    """
    large_text = pygame.font.Font('freesansbold.ttf', 40)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = ((WIDTH / 2), (HEIGHT / 2))
    screen.blit(text_surf, text_rect)

    pygame.display.update()


def scored(screen, bullet):
    """
    Function writes a message if bullet has hit the target
    :param screen: - screen
    :param bullet: - bullet
    :return:
    """
    screen.fill(WHITE)
    text = 'Target destroyed in ' + str(bullet) + ' tries'
    message_display(text, screen)
    pygame.time.delay(500)


def events(gun1, gun2, objects, bullet, n):
    """
    Function checks events
    :param gun1: - lower gun
    :param gun2: - upper gun
    :param objects: - bullets on the screen
    :param bullet: - number of shooted bullets
    :param n: - type of gun
    :return: - returns bullet back to 0 if user has hit the target
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and n == 'down':
            gun1.fire2_start()

        elif event.type == pygame.MOUSEBUTTONDOWN and n == 'up':
            gun2.fire2_start()

        elif event.type == pygame.MOUSEBUTTONUP and n == 'down':
            if len(objects) % 2 == 0:
                gun1.fire2_end(event, objects, bullet)
            else:
                gun1.fire3_end(event, objects, bullet)
            bullet += 1
        elif event.type == pygame.MOUSEBUTTONUP and n == 'up':
            if len(objects) % 2 == 0:
                gun2.fire2_end(event, objects, bullet)
            else:
                gun2.fire3_end(event, objects, bullet)
            bullet += 1
        elif event.type == pygame.MOUSEMOTION and n == 'up':
            gun2.targetting(event)
        elif event.type == pygame.MOUSEMOTION and n == 'down':
            gun1.targetting(event)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        if n == 'down':
            gun1.move('right')
        if n == 'up':
            gun2.move('right')
    if keys[pygame.K_LEFT]:
        if n == 'down':
            gun1.move('left')
        if n == 'up':
            gun2.move('left')

    if n == 'up':
        gun1.move('right')
    if n == 'down':
        gun2.move('right')

    return bullet


def create_game_objects(screen):
    """
    Function creates guns and targets
    :param screen: - screen
    :return:
    """
    gun1 = Gun(screen, 'down')
    gun2 = Gun(screen, 'up')
    target1 = Target(screen, 'ball')
    target2 = Target(screen, 'square')
    target3 = Target(screen, 'ellipse')

    return gun1, gun2, target1, target2, target3


def move_guns_targets(gun1, gun2, target1, target2, target3):
    """
    Function moves guns and targets
    :param gun1: - lower gun
    :param gun2: - upper gun
    :param target1: - ball target
    :param target2: - square target
    :param target3: - ellipse target
    :return:
    """
    gun1.draw()
    gun2.draw()
    target1.move()
    target1.draw()
    target2.move()
    target2.draw()
    target3.move()
    target3.draw()


def check_if_hit(balls, target1, target2, target3, screen, bullet):
    """
    Function checks if bullet has hit the target
    :param balls: - bullets
    :param target1: - ball target
    :param target2: - square target
    :param target3: - ellipse target
    :param screen: - screen
    :param bullet: - number of bullets
    :return:
    """
    t = 1
    for b in balls:

        if b.hittest(target1) and target1.live:
            balls.remove(b)
            target1.live = 0
            target1.hit()
            target1.new_target()
            scored(screen, bullet)
            t = 0

        if b.hittest(target2) and target2.live:
            balls.remove(b)
            target2.live = 0
            target2.hit()
            target2.new_target()
            scored(screen, bullet)
            t = 0

        if b.hittest(target3) and target3.live:
            balls.remove(b)
            target3.live = 0
            target3.hit()
            target3.new_target()
            scored(screen, bullet)
            t = 0
    return t


def game():
    """
    Game gun
    :return:
    """
    print("Choose gun: 'up' or 'down': ")
    n = input()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Gun')
    bullet = 0
    objects = []
    clock = pygame.time.Clock()
    finished = False
    gun1, gun2, target1, target2, target3 = create_game_objects(screen)

    while not finished:
        screen.fill(WHITE)
        move_guns_targets(gun1, gun2, target1, target2, target3)
        for b in objects:
            b.draw()
        pygame.display.update()
        clock.tick(FPS)
        bullet = events(gun1, gun2, objects, bullet, n)
        for b in objects:
            b.move()
            if b.vx == 0:
                objects.remove(b)
            t = check_if_hit(objects, target1, target2, target3, screen, bullet)
            if t == 0:
                bullet = 0

        gun1.power_up()
        gun2.power_up()


game()
