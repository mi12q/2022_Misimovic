import pygame
from pygame.draw import *
from random import randint
import math


class Ball:
    def __init__(self, x, y, radius, color, screen):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.screen = screen

    def draw(self):
        pygame.draw.circle(self.screen, self.color, [self.x, self.y], self.radius)


def new_ball(screen, COLORS):
    """draws a new ball"""
    x = randint(100, 700)
    y = randint(100, 500)
    r = randint(30, 50)
    color = COLORS[randint(0, 5)]
    ball1 = Ball(x, y, r, color, screen)
    ball1.draw()
    return ball1

# def move_ball(ball):
#     ball.x += 5




def click(event, x, y, r):
    """
    gets circle coordinates and radius

    :param event: - mouse click
    :return:
    """
    print(x, y, r)


def in_circle(event, x, y, r):
    """
    checks if user clicked on a circle

    :param event: - mouse click
    :return:
    """
    x1 = event.pos[0]  # mouse coordinate x
    y1 = event.pos[1]  # mouse coordinate y
    d = math.sqrt((x - x1) ** 2 + (y - y1) ** 2)  # distance between points

    if d <= r:
        print("Circle!")
        return True
    print("Not circle!")
    return False


# def ball_move(x,y,r,color, screen):
#     """
#
#     :param x:
#     :param y:
#     :param r:
#     :param color:
#     :return:
#     """
#
#     x+=1
#     circle(screen, color, (x, y), r)

def game():
    pygame.init()

    FPS = 2
    screen = pygame.display.set_mode((1200, 900))

    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)
    BLACK = (0, 0, 0)
    COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False
    count = 0
    balls = []
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if in_circle(event, x, y, r):
            #         count += 1
            #     print("Score = ", count, "\n")

        for i in range(2):
            ball = new_ball(screen,COLORS)
            balls.append(ball)


        pygame.display.update()
        screen.fill(BLACK)

    pygame.quit()

game()
