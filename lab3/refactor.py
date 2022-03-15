import pygame
import pygame.draw as dr

pygame.init()

FPS = 30
SCR_WIDTH = 500
SCR_HEIGHT = 700
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))

WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
LIGHT_MARSH = (92, 105, 93)
DARK_MARSH = (4, 43, 8)
GREEN = (151, 199, 147)
BLUE = (27, 78, 161)
RED = (255, 17, 0)
BLACK = (0, 0, 0)


def draw_circle_alpha(surface, color, center, radius, thick):
    """
    Drawing a transparent circle
    :param surface: Target surface
    :param color: Extended color of the circle, RGB + alpha (tuple of int)
    :param center: Coordinates of center, (x, y) (tuple of int)
    :param radius: Radius of the circle (int)
    :param thick: Thickness of the fill relative to the radius (float)
    """
    target_rect = pygame.Rect((center[0] - radius, center[1] - radius), (radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius, int(radius * thick))
    surface.blit(shape_surf, target_rect)


def draw_rect_alpha(surface, color, rect):
    """
    Drawing a transparent rect
    :param surface: Target surface
    :param color: Extended color of the rect RGB + alpha (tuple of int)
    :param rect: pygame.Rect object
    """
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def draw_polygon_alpha(surface, color, points):
    """
    Drawing a transparent polygon
    :param surface: Target surface
    :param color: Extended color of the rect RGB + alpha (tuple of int)
    :param points: Coordinates of vertexes (list of tuples of int)
    """
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


def draw_background(surface, sky_color, ground_color, ratio):
    """
    Drawing a background consisting of sky and ground
    :param surface: Target surface
    :param sky_color: Color of sky, RGB (tuple of int)
    :param ground_color: Color of ground, RGB (tuple of int)
    :param ratio: Ratio of height of the ground to height of the screen (float)
    """
    screen.fill(sky_color)
    dr.rect(surface, BLACK, (0, SCR_HEIGHT * ratio, SCR_WIDTH, SCR_HEIGHT * (1 - ratio)))
    dr.rect(surface, ground_color, (0, SCR_HEIGHT * ratio + 1, SCR_WIDTH, SCR_HEIGHT * (1 - ratio) - 1))


def draw_sun(surface, color, center, radius):
    """
    Drawing a sun
    :param surface: Target surface
    :param color: Color of sun, RGB (tuple of int)
    :param center: Coordinates of center, (x, y) (tuple of int)
    :param radius: Radius of a sun halo (int)
    """
    alpha = (200,)
    draw_circle_alpha(surface, color + alpha, center, radius, 3 / 14)
    dr.circle(surface, color, center, radius * (3 / 28))

    vertical_rect = (center[0] - radius * (3 / 28), center[1] - radius * 0.9, radius * (3 / 14), radius * (25 / 14))
    draw_rect_alpha(surface, color + alpha, vertical_rect)
    horizontal_rect = (center[0] - radius * 0.9, center[1] - radius * (3 / 28), radius * (25 / 14), radius * (3 / 14))
    draw_rect_alpha(surface, color + alpha, horizontal_rect)

    left_mini_circle_center = (center[0] - radius * (21 / 28), center[1])
    dr.circle(surface, color, left_mini_circle_center, radius * (3 / 35))
    down_mini_circle_center = (center[0], center[1] + radius * (21 / 28))
    dr.circle(surface, color, down_mini_circle_center, radius * (3 / 35))
    right_mini_circle_center = (center[0] + radius * (21 / 28), center[1])
    dr.circle(surface, color, right_mini_circle_center, radius * (3 / 35))


def draw_fish_body(surface, color, alpha, corner, fh, fv, size):
    draw_polygon_alpha(surface, color + alpha,
                       [((corner[0] + (20 + fh * 90) * size), (corner[1] + (70 - fv * 70) * size)),
                        (corner[0] + (fh * 130) * size, corner[1] + (50 - fv * 30) * size),
                        (corner[0] + (40 + fh * 50) * size, corner[1] + 35 * size)])
    draw_polygon_alpha(surface, color + alpha,
                       [(corner[0] + (40 + fh * 50) * size, corner[1] + 35 * size),
                        (corner[0] + (80 - fh * 30) * size, corner[1] + fv * 70 * size),
                        (corner[0] + (130 - fh * 130) * size, corner[1] + (10 + fv * 50) * size),
                        (corner[0] + (80 - fh * 30) * size, corner[1] + 35 * size)])


def draw_fish_eye(surface, color, alpha, corner, fh, fv, size):
    draw_circle_alpha(surface, color + alpha,
                      (corner[0] + (100 - fh * 70) * size, corner[1] + (10 + fv * 50) * size), 5 * size, 1)
    draw_circle_alpha(surface, BLACK + alpha,
                      (corner[0] + (100 - fh * 70) * size, corner[1] + (10 + fv * 50) * size), 3 * size, 1)
    draw_circle_alpha(surface, WHITE + alpha,
                      (corner[0] + (98 - fh * 66) * size, corner[1] + (8 + fv * 54) * size), 3 * size, 1)


def draw_fish_fin(surface, color, alpha, corner, fh, fv, size):
    draw_polygon_alpha(surface, color + alpha,
                       [(corner[0] + (50 + fh * 30) * size, corner[1] + (33 + fv * 4) * size),
                        (corner[0] + (70 - fh * 10) * size, corner[1] + (33 + fv * 4) * size),
                        (corner[0] + (70 - fh * 10) * size, corner[1] + (45 - fv * 20) * size),
                        (corner[0] + (40 + fh * 50) * size, corner[1] + (45 - fv * 20) * size)])
    draw_polygon_alpha(surface, color + alpha,
                       [(corner[0] + (70 - fh * 10) * size, corner[1] + fv * 70 * size),
                        (corner[0] + (80 - fh * 30) * size, corner[1] + fv * 70 * size),
                        (corner[0] + (80 - fh * 30) * size, corner[1] + (10 + fv * 50) * size),
                        (corner[0] + (40 + fh * 50) * size, corner[1] + (10 + fv * 50) * size)])
    draw_polygon_alpha(surface, color + alpha,
                       [(corner[0] + (100 - fh * 70) * size, corner[1] + (25 + fv * 20) * size),
                        (corner[0] + (120 - fh * 110) * size, corner[1] + (15 + fv * 40) * size),
                        (corner[0] + (130 - fh * 130) * size, corner[1] + (25 + fv * 20) * size),
                        (corner[0] + (110 - fh * 90) * size, corner[1] + (30 + fv * 10) * size)])


def draw_fish(surface, body_color, eye_color, fin_color, corner, flip_horizontal, flip_vertical, size):
    """
    Drawing a fish
    :param surface: Target surface
    :param body_color: Color of fish body, RGB (tuple of int)
    :param eye_color: Color of fish eye, RGB (tuple of int)
    :param fin_color: Color of fish fin, RGB (tuple of int)
    :param corner: Coordinates of left up corner of image, (x, y) (tuple of int)
    :param flip_horizontal: Is reflected horizontally (bool)
    :param flip_vertical: Is reflected vertically (bool)
    :param size: Size relative to base size 130x70 (float)
    """
    alpha_body = (100,)
    alpha_eye = (200,)

    fh = int(flip_horizontal)
    fv = int(flip_vertical)

    draw_fish_body(surface, body_color, alpha_body, corner, fh, fv, size)
    draw_fish_eye(surface, eye_color, alpha_eye, corner, fh, fv, size)
    draw_fish_fin(surface, fin_color, alpha_body, corner, fh, fv, size)


def draw_hole(surface, water_color, ice_color, corner, size):
    """
    Drawing an ice hole
    :param surface: Target surface
    :param water_color: Color of water in hole, RGB (tuple of int)
    :param ice_color: Color of ice, RGB (tuple of int)
    :param corner: Coordinates of left up corner of image, (x, y) (tuple of int)
    :param size: Size relative to base size 150x50 (float)
    """
    dr.ellipse(surface, BLACK, (corner[0], corner[1], 151 * size, 51 * size), 0)
    dr.ellipse(surface, ice_color, (corner[0], corner[1], 150 * size, 50 * size), 0)
    dr.ellipse(surface, BLACK, (corner[0] + 10 * size, corner[1] + 10 * size, 131 * size, 41 * size), 0)
    dr.ellipse(surface, water_color, (corner[0] + 10 * size, corner[1] + 10 * size, 130 * size, 40 * size), 0)


def draw_fishing_rod(surface, corner, fh, size):
    dr.line(surface, BLACK, (corner[0] + (350 - fh * 350) * size, corner[1]),
            (int(corner[0] + (350 - fh * 350) * size), corner[1] + 320 * size), 1)
    dr.lines(surface, BLACK, False, [(corner[0] + (150 + fh * 50) * size, corner[1] + 200 * size),
                                     (corner[0] + (250 - fh * 125) * size, corner[1] + 80 * size),
                                     (corner[0] + (350 - fh * 350) * size, corner[1])], int(7 * size))


def draw_bear_head(surface, color, corner, fh, size):
    dr.ellipse(surface, BLACK, (corner[0] + (50 + fh * (250 - 112)) * size, corner[1] + 50 * size, 112 * size, 62 * size), 0)
    dr.ellipse(surface, color, (corner[0] + (53 + fh * (244 - 106)) * size, corner[1] + 53 * size, 106 * size, 56 * size), 0)
    dr.ellipse(surface, BLACK, (corner[0] + (100 + fh * (150 - 9)) * size, corner[1] + 71 * size, 9 * size, 9 * size), 0)
    dr.ellipse(surface, BLACK, (corner[0] + (155 + fh * (40 - 9)) * size, corner[1] + 71 * size, 9 * size, 9 * size), 0)
    dr.aalines(surface, BLACK, False, [(corner[0] + (160 + fh * 30) * size, corner[1] + 90 * size),
                                       (corner[0] + (140 + fh * 70) * size, corner[1] + 95 * size),
                                       (corner[0] + (100 + fh * 150) * size, corner[1] + 95 * size),
                                       (corner[0] + (90 + fh * 170) * size, corner[1] + 95 * size)], blend=1)
    dr.ellipse(surface, BLACK, (corner[0] + (55 + fh * (240 - 17)) * size, corner[1] + 57 * size, 17 * size, 17 * size), 0)
    dr.ellipse(surface, color, (corner[0] + (58 + fh * (234 - 11)) * size, corner[1] + 60 * size, 11 * size, 11 * size), 0)


def draw_bear_body(surface, color, corner, fh, size):
    dr.ellipse(surface, BLACK, (corner[0] + (fh * (350 - 152)) * size, corner[1] + 100 * size,
                                152 * size, 302 * size), 0)
    dr.ellipse(surface, color, (corner[0] + (3 + fh * (344 - 146)) * size, corner[1] + 103 * size,
                                146 * size, 296 * size), 0)
    dr.ellipse(surface, BLACK, (corner[0] + (120 + fh * (110 - 72)) * size, corner[1] + 150 * size,
                                72 * size, 32 * size), 0)
    dr.ellipse(surface, color, (corner[0] + (123 + fh * (104 - 66)) * size, corner[1] + 153 * size,
                                66 * size, 26 * size), 0)
    dr.ellipse(surface, BLACK, (corner[0] + (90 + fh * (170 - 122)) * size, corner[1] + 300 * size,
                                122 * size, 92 * size), 0)
    dr.ellipse(surface, color, (corner[0] + (93 + fh * (164 - 116)) * size, corner[1] + 303 * size,
                                116 * size, 86 * size), 0)
    dr.ellipse(surface, BLACK, (corner[0] + (160 + fh * (30 - 92)) * size, corner[1] + 370 * size,
                                92 * size, 42 * size), 0)
    dr.ellipse(surface, color, (corner[0] + (163 + fh * (24 - 86)) * size, corner[1] + 373 * size,
                                86 * size, 36 * size), 0)


def draw_bear(surface, body_color, corner, flip_horizontal, size):
    """
    Drawing a bear with fishing rod
    :param surface: Target surface
    :param body_color: Color of bear's body, RGB (tuple of int)
    :param corner: Coordinates of left up corner of image, (x, y) (tuple of int)
    :param flip_horizontal: Is reflected horizontally (bool)
    :param size: Size relative to base size 350x411 (float)
    """
    fh = int(flip_horizontal)

    draw_fishing_rod(surface, corner, fh, size)
    draw_bear_head(surface, body_color, corner, fh, size)
    draw_bear_body(surface, body_color, corner, fh, size)


def draw_fisherman(surface, corner, flip_horizontal, size):
    """
    Drawing a fisherman bear with catch
    :param surface: Target surface
    :param corner: Coordinates of left up corner of image, (x, y) (tuple of int)
    :param flip_horizontal: Is reflected horizontally (bool)
    :param size: Size relative to base size 450x500 (float)
    """
    fh = int(flip_horizontal)
    small_size = 0.6

    draw_hole(surface, DARK_MARSH, LIGHT_MARSH, (corner[0] + (250 - fh * 200) * size, corner[1] + 300 * size), size)
    draw_bear(surface, WHITE, (corner[0] + 100 * fh * size, corner[1]), flip_horizontal, size)
    draw_fish(surface, GREEN, BLUE, RED, (corner[0] + (195 - fh * 18) * size, corner[1] + 245 * size),
              flip_horizontal, True, size * small_size)
    draw_fish(surface, GREEN, BLUE, RED, (corner[0] + (240 - fh * 108) * size, corner[1] + 235 * size),
              flip_horizontal, False, size * small_size)
    draw_fish(surface, GREEN, BLUE, RED, (corner[0] + (325 - fh * 278) * size, corner[1] + 245 * size),
              flip_horizontal, True, size * small_size)
    draw_fish(surface, GREEN, BLUE, RED, (corner[0] + (270 - fh * 220) * size, corner[1] + 365 * size),
              flip_horizontal, False, size)
    draw_fish(surface, GREEN, BLUE, RED, (corner[0] + (280 - fh * 240) * size, corner[1] + 385 * size),
              flip_horizontal, False, size)
    draw_fish(surface, GREEN, BLUE, RED, (corner[0] + (310 - fh * 300) * size, corner[1] + 415 * size),
              not flip_horizontal, False, size)


def draw_picture(surface):
    """
    Draw a frozen river with fishermen bears
    :param surface: Target surface
    """
    draw_background(surface, CYAN, WHITE, 4 / 7)
    draw_sun(surface, WHITE, (310, 120), 140)

    fishermen = (((325, 350), True, 0.3), ((160, 420), True, 0.3), ((25, 550), False, 0.3), ((285, 535), True, 0.5))

    for i in range(4):
        draw_fisherman(surface, fishermen[i][0], fishermen[i][1], fishermen[i][2])


draw_picture(screen)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
