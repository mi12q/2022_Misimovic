import pygame
import pygame.draw as dr

pygame.init()

FPS = 30
screen = pygame.display.set_mode((500, 700))
screen.fill('cyan')

dr.polygon(screen, (0, 0, 0), [(0, 700), (500, 700), (500, 400), (0, 400)], 0)
dr.polygon(screen, (255, 255, 255), [(0, 700), (500, 700), (500, 401), (0, 401)], 0)

# лужа
dr.ellipse(screen, (0, 0, 0), (290, 500, 151, 51), 0)
dr.ellipse(screen, (92, 105, 93), (290, 500, 150, 50), 0)
dr.ellipse(screen, (0, 0, 0), (300, 510, 131, 41), 0)
dr.ellipse(screen, (4, 43, 8), (300, 510, 130, 40), 0)


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

# стержень
dr.line(screen, (0, 0, 0), (400, 200), (400, 520))
dr.lines(screen, (0, 0, 0), False, [(200, 400), (300, 280), (400, 200)], 5)
# dr.aalines(screen, (0,0,0),[(170,350),(200,300)],[(400,520),(600,520)],blend=1)
# dr.aalines(screen, (0,0,0), True, [(130,350),(150,350),(150,350),(150,100)], blend=1)

# медведь

# голова

dr.ellipse(screen, (0, 0, 0), (100, 250, 112, 62), 0)
dr.ellipse(screen, (255, 255, 255), (101, 251, 110, 60), 0)
dr.ellipse(screen, (0, 0, 0), (150, 271, 7, 7), 0)
dr.ellipse(screen, (0, 0, 0), (205, 271, 7, 7), 0)
dr.aalines(screen, (0, 0, 0), False, [(210, 290), (190, 295), (150, 295), (140, 295)], blend=1)
dr.ellipse(screen, (0, 0, 0), (105, 257, 17, 17), 0)
dr.ellipse(screen, (255, 255, 255), (106, 258, 15, 15), 0)

# тело

dr.ellipse(screen, (0, 0, 0), (50, 300, 152, 302), 0)
dr.ellipse(screen, (255, 255, 255), (51, 301, 150, 300), 0)
dr.ellipse(screen, (0, 0, 0), (170, 350, 72, 32), 0)
dr.ellipse(screen, (255, 255, 255), (171, 351, 70, 30), 0)
dr.ellipse(screen, (0, 0, 0), (140, 500, 122, 92), 0)
dr.ellipse(screen, (255, 255, 255), (141, 501, 120, 90), 0)
dr.ellipse(screen, (0, 0, 0), (210, 570, 92, 42), 0)
dr.ellipse(screen, (255, 255, 255), (211, 571, 91, 40), 0)


# рыба

def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


draw_polygon_alpha(screen, (151, 199, 147, 100), [(350, 660), (330, 640), (370, 625), (370, 625)])

draw_polygon_alpha(screen, (151, 199, 147, 100), [(370, 625), (370, 625), (410, 590), (410, 625)])
draw_polygon_alpha(screen, (151, 199, 147, 100), [(410, 590), (410, 625), (460, 600), (460, 600)])

draw_circle_alpha(screen, (27, 78, 161, 200), (430, 600), 5)
draw_circle_alpha(screen, (0, 0, 0, 200), (430, 600), 3)
draw_circle_alpha(screen, (255, 255, 255, 200), (428, 598), 3)

draw_polygon_alpha(screen, (255, 17, 0, 100), [(380, 623), (400, 623), (400, 635), (370, 635)])
draw_polygon_alpha(screen, (255, 17, 0, 100), [(400, 590), (410, 590), (410, 600), (370, 600)])
draw_polygon_alpha(screen, (255, 17, 0, 100), [(430, 615), (450, 605), (460, 615), (440, 620)])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
