import pygame
from random import randint, choice
import math
import operator
# import time
# from sys import exit
from tabulate import tabulate


class Ball:
    def __init__(self, x, y, radius, vx, vy, color, screen):
        """

        :param x: - ball coordinate x
        :param y: - ball coordinate x
        :param radius: - ball radius
        :param vx: - ball velocity in direction x
        :param vy: - ball velocity in direction y
        :param color: - ball color
        :param screen: - screen
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.color = color
        self.screen = screen

    def draw(self):
        """
        Function draws a ball
        :return:
        """
        pygame.draw.circle(self.screen, self.color, [self.x, self.y], self.radius)

    def move(self, width, height, min_velocity, max_velocity):
        """
        Function changes balls coordinates and its direction if ball hits the wall
        :param width: - screen width
        :param height: - screen height
        :return:
        """
        t = 0.1
        self.x += self.vx * t
        self.y += self.vy * t
        if self.x > width - self.radius:
            self.x = width - self.radius
            #self.vx += randint(min_velocity, max_velocity)
            self.vx *= -1
        if self.y > height - self.radius:
            self.y = height - self.radius
            # self.vy += randint(min_velocity, max_velocity)
            self.vy *= -1
        if self.y < self.radius:
            self.y = self.radius
            # self.vy +=  randint(min_velocity, max_velocity)
            self.vy *= -1
        if self.x < self.radius:
            self.x = self.radius
            # self.vx += randint(min_velocity, max_velocity)
            self.vx *= -1

    def score(self, event):
        """
        Function checks if player clicked on the ball
        :param event: - mouse click
        :return: - returns 1 if player clicked on the ball
        """
        score = 0
        x1 = event.pos[0]  # mouse coordinate x
        y1 = event.pos[1]  # mouse coordinate y
        d = math.sqrt((self.x - x1) ** 2 + (self.y - y1) ** 2)  # distance between points

        if d <= self.radius:
            score = 1
        return score


class Square:
    def __init__(self, x, y, size, vx, color, screen):
        """

        :param x: - square coordinate x
        :param y: - square coordinate y
        :param size: - square size
        :param vx: - square velocity in direction x
        :param color: - square color
        :param screen: - screen
        """
        self.x = x
        self.y = y
        self.size = size
        self.vx = vx
        self.color = color
        self.screen = screen

    def draw(self):
        """
        Function draws a square
        :return:
        """
        pygame.draw.rect(self.screen, self.color, [self.x, self.y, self.size, self.size])

    def score(self, event):
        """
        Function checks if player clicked on the square
        :param event: - mouse click
        :return: - returns 5 if player clicked on the square
        """
        score = 0
        x1 = event.pos[0]  # mouse coordinate x
        y1 = event.pos[1]  # mouse coordinate y
        d = math.sqrt((self.x - x1) ** 2 + (self.y - y1) ** 2)  # distance between points

        if d <= self.size:
            score = 5
        return score

    def move(self, width):
        """
        Function changes square coordinates and its direction if square hits the wall
        :param width: - screen width
        :return:
        """
        t = 0.1
        self.x += self.vx * t

        if self.x > width - self.size:
            self.x = width - self.size

            self.vx *= -1

        if self.x < self.size / 2:
            self.x = self.size / 2

            self.vx *= -1


def new_ball(screen, colors, min_velocity, max_velocity, width, height):
    """
    Function draws a new ball
    :param screen: - screen
    :param colors: - ball color
    :param min_velocity: - ball minimum velocity
    :param max_velocity: - ball maximum velocity
    :param width: - screen width
    :param height: - screen height
    :return:
    """
    x = randint(100, width - 100)
    y = randint(100, height - 100)
    r = randint(5, 50)
    vx = choice([-1, 1]) * randint(min_velocity, max_velocity)
    vy = choice([-1, 1]) * randint(min_velocity, max_velocity)
    color = colors[randint(0, 5)]
    ball = Ball(x, y, r, vx, vy, color, screen)
    ball.draw()
    return ball


def new_square(screen, colors, min_velocity, max_velocity, width, height):
    """
    Function draws a new square
    :param screen: - screen
    :param colors: - square color
    :param min_velocity: - square minimum velocity
    :param max_velocity: - square maximum velocity
    :param width: - screen width
    :param height: - screen height
    :return:
    """
    x = randint(100, width - 100)
    y = randint(20, height - 20)
    size = randint(5, 50)
    vx = choice([-1, 1]) * randint(min_velocity, max_velocity)
    color = colors[randint(0, 5)]
    square = Square(x, y, size, vx, color, screen)
    square.draw()
    return square


def game():
    """
    Function starts the game and returns the score of the current player
    :return: - count
    """
    pygame.init()

    min_velocity = 200
    max_velocity = 300
    ball_number = 30
    square_number = 30
    fps = 15
    width = 1000
    height = 700
    screen = pygame.display.set_mode((width, height))

    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    green = (0, 255, 0)
    magenta = (255, 0, 255)
    cyan = (0, 255, 255)
    black = (0, 0, 0)
    colors = [red, blue, yellow, green, magenta, cyan]

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False
    count = 0
    balls = []
    squares = []

    for i in range(ball_number):
        balls.append(new_ball(screen, colors, min_velocity, max_velocity, width, height))
    for i in range(square_number):
        squares.append(new_square(screen, colors, min_velocity, max_velocity, width, height))

    while not finished:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for ball in balls:
                    count += ball.score(event)
                    if ball.score(event) > 0:
                        print("Circle!")
                        balls.remove(ball)

                for square in squares:
                    count += square.score(event)
                    if square.score(event) > 0:
                        print("Square!")
                        squares.remove(square)

                print("Score = ", count, "\n")

        for ball in balls:
            ball.move(width, height, min_velocity, max_velocity)
            ball.draw()

        for square in squares:
            square.move(width)
            square.draw()

        pygame.display.update()
        screen.fill(black)

    pygame.quit()
    return count


def list_of_players():
    """
    Function creates a list of the best players and saves it to file
    :return:
    """
    print("Insert number of players: ")
    n = input()
    scores = {}

    for i in range(1, int(n) + 1):
        score = game()
        scores[i] = score

    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

    a = ['Player number', 'Score']
    with open('players.txt', 'w') as f:
        f.write(tabulate(sorted_scores, headers=a))


list_of_players()
