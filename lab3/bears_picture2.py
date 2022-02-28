import pygame
import pygame.draw as dr

pygame.init()

FPS = 30
screen = pygame.display.set_mode((500, 700))
screen.fill('cyan')
# surface = pygame.Surface((100,100))
# surface.fill('white')
image = pygame.image.load(r'C:\\Users\\edupc\\2022_Misimovic\\lab3\\bear4.jpg')
image3 = pygame.image.load(r'C:\\Users\\edupc\\2022_Misimovic\\lab3\\bear4.jpg')
image = pygame.transform.scale(image, (150,200))
image2 = pygame.transform.scale(image, (300,350))
image3 = pygame.transform.scale(image3, (150,200))
copy = image.copy()
copy2 = image2.copy()
copy3 = image3.copy()

img_with_flip = pygame.transform.flip(copy, True, False)
image.set_colorkey((255,255,255))
img_with_flip.set_colorkey((255,255,255))

img_with_flip2 = pygame.transform.flip(copy2, True, False)
image.set_colorkey((255,255,255))
img_with_flip2.set_colorkey((255,255,255))

img_with_flip3 = pygame.transform.flip(copy3, True, False)
img_with_flip3.set_colorkey((255,255,255))

dr.polygon(screen, (0, 0, 0), [(0, 700), (500, 700), (500, 400), (0, 400)], 0)
dr.polygon(screen, (255, 255, 255), [(0, 700), (500, 700), (500, 401), (0, 401)], 0)


screen.blit(image,(0,500))
screen.blit(img_with_flip, (160, 370))
screen.blit(img_with_flip2, (260, 430))
screen.blit(img_with_flip3, (320, 300))


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


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()