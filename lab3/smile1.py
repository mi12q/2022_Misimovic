import pygame
import pygame.draw as dr

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill('pink')

dr.circle(screen, (0, 0, 0), (200, 175), 101)
dr.circle(screen, (255, 255, 0), (200, 175), 100)
dr.rect(screen, (0, 0, 0), (150, 220, 100, 20))

dr.circle(screen, (0, 0, 0), (150, 150), 21)
dr.circle(screen, (255, 0, 0), (150, 150), 20)
dr.circle(screen, (0, 0, 0), (150, 150), 10)

dr.circle(screen, (0, 0, 0), (250, 150), 16)
dr.circle(screen, (255, 0, 0), (250, 150), 15)
dr.circle(screen, (0, 0, 0), (250, 150), 7)

dr.polygon(screen, (0,0,0), [(115,90),(110,100),(170,140),(175,130)], 0)

dr.polygon(screen, (0,0,0), [(220,140),(225,150),(280,110),(285,95)], 0)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()