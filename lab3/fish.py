import pygame
import pygame.draw as dr

pygame.init()

FPS = 30
screen = pygame.display.set_mode((500, 700), 0, 32)
screen.fill('white')

def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius, 30)
    surface.blit(shape_surf, target_rect)


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


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


pygame.image.save(screen, "fish.jpg")


pygame.quit()
