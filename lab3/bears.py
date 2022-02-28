import pygame
import pygame.draw as dr

pygame.init()

FPS = 30
screen = pygame.display.set_mode((500, 700))
screen.fill('cyan')

dr.polygon(screen, (0, 0, 0), [(0, 700), (500, 700), (500, 400), (0, 400)], 0)
dr.polygon(screen, (255, 255, 255), [(0, 700), (500, 700), (500, 401), (0, 401)], 0)


def pond(x, y, size):
    dr.ellipse(screen, (0, 0, 0), (x, y, width + 1, height + 1), 0)
    dr.ellipse(screen, (92, 105, 93), (x, y, width, height), 0)
    dr.ellipse(screen, (0, 0, 0), (x + 10, y + 10, width - 19, height - 9), 0)
    dr.ellipse(screen, (4, 43, 8), (x + 10, y + 10, width - 20, height - 10), 0)


# круг
def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius, 30)
    surface.blit(shape_surf, target_rect)


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


draw_circle_alpha(screen, (255, 255, 255, 200), (310, 120), 160)
dr.circle(screen, (255, 255, 255), (310, 120), 15)
draw_rect_alpha(screen, (255, 255, 255, 200), (295, 0, 30, 300))
draw_rect_alpha(screen, (255, 255, 255, 200), (170, 105, 300, 30))

dr.circle(screen, (255, 255, 255), (435, 120), 12)
dr.circle(screen, (255, 255, 255), (185, 120), 12)
dr.circle(screen, (255, 255, 255), (310, 245), 12)


def bear(x, y, size=100):


# x = 100, y = 250
# # стержень
#     dr.line(screen, (0, 0, 0), (x + 300, y - 50), (x + 300, y + 250 + 20))
#     dr.lines(screen, (0, 0, 0), False, [(x * 2, y + 150), (x * 3, y + 30), (x * 4, x * 2)], 5)
#     dr.aalines(screen, (0, 0, 0), [(x + 70, y + 100), (x * 2, x * 3)], [(x * 4, x * 5 + 20), (x * 6, x * 5 + 20)], blend=1)
#     dr.aalines(screen, (0, 0, 0), True, [(x + 30, y + 100), (x + 50, y + 100), (x + 50, y + 100), (x + 50, x)], blend=1)

# # медведь
# x = 100, y = 250, size = 100
# # голова
#
    dr.ellipse(screen, (0, 0, 0), (x, y, size+12, size-38), 0)
    dr.ellipse(screen, (255, 255, 255), (x + 1, y + 1, size+10, size-40), 0)
    dr.ellipse(screen, (0, 0, 0), (x + 50, y + 21, size-93, size-93), 0)
    dr.ellipse(screen, (0, 0, 0), (x + 105, y + 21, size-93, size-93), 0)
    dr.aalines(screen, (0, 0, 0), False, [(x + 110, y + 40), (x + 90, y + 45), (x + 50, y + 45), (x + 40, y + 45)], blend=1)
    dr.ellipse(screen, (0, 0, 0), (x + 5, y + 7, size-83, size-83), 0)
    dr.ellipse(screen, (255, 255, 255), (x + 5, y + 8, size-85, size-85), 0)

# # тело
# x = 100, y = 250
    dr.ellipse(screen, (0, 0, 0), (x - 50, y + 50, 152, 302), 0)
    dr.ellipse(screen, (255, 255, 255), (x - 49, y + 51, 150, 300), 0)
    dr.ellipse(screen, (0, 0, 0), (x + 70, y + 100, 72, 32), 0)
    dr.ellipse(screen, (255, 255, 255), (x + 71, y + 101, 70, 30), 0)
    dr.ellipse(screen, (0, 0, 0), (x + 40, y + 250, 122, 92), 0)
    dr.ellipse(screen, (255, 255, 255), (x + 41, y + 251, 120, 90), 0)
    dr.ellipse(screen, (0, 0, 0), (x + 110, y + 250 + 71, 92, 42), 0)
    dr.ellipse(screen, (255, 255, 255), (x + 111, y + 250 + 71, 91, 40), 0)



# def pond2(a,b):
#     dr.ellipse(screen, (0, 0, 0), (290*a, 500*a, 151*b, 51*b), 0)
#     dr.ellipse(screen, (92, 105, 93), (290*a, 500*a, 150*b, 50*b), 0)
#     dr.ellipse(screen, (0, 0, 0), (300*a, 510*a, 131*b, 41*b), 0)
#     dr.ellipse(screen, (4, 43, 8), (300*a, 510*a, 130*b, 40*b), 0)
#
# pond(300,300,)

#
# # рыба
#
# def draw_polygon_alpha(surface, color, points):
#     lx, ly = zip(*points)
#     min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
#     target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
#     shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
#     pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
#     surface.blit(shape_surf, target_rect)
#
#
# draw_polygon_alpha(screen, (151, 199, 147, 100), [(350, 660), (330, 640), (370, 625), (370, 625)])
#
# draw_polygon_alpha(screen, (151, 199, 147, 100), [(370, 625), (370, 625), (410, 590), (410, 625)])
# draw_polygon_alpha(screen, (151, 199, 147, 100), [(410, 590), (410, 625), (460, 600), (460, 600)])
#
# draw_circle_alpha(screen, (27, 78, 161, 200), (430, 600), 5)
# draw_circle_alpha(screen, (0, 0, 0, 200), (430, 600), 3)
# draw_circle_alpha(screen, (255, 255, 255, 200), (428, 598), 3)
#
# draw_polygon_alpha(screen, (255, 17, 0, 100), [(380, 623), (400, 623), (400, 635), (370, 635)])
# draw_polygon_alpha(screen, (255, 17, 0, 100), [(400, 590), (410, 590), (410, 600), (370, 600)])
# draw_polygon_alpha(screen, (255, 17, 0, 100), [(430, 615), (450, 605), (460, 615), (440, 620)])
#
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
