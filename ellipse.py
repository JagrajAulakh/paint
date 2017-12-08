from pygame import *

init()

width, height = 800, 600
screen = display.set_mode((width, height))
screen.fill((255, 255, 255))

running = True

radius = 10

while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False

        if evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:
                co = screen.copy()
                fmx, fmy = mx, my

            if evt.button == 4:
                radius += 1

            if evt.button == 5:
                radius -= 1
                if radius < 1:
                    radius = 1

    mb = mouse.get_pressed()
    mx, my = mouse.get_pos()

    if mb[0]:
        screen.blit(co, (0, 0))

        ellipseSurf = Surface((max(abs(mx - fmx), 1), max(abs(my - fmy), 1)), SRCALPHA)
        ellipseSurf.fill((0, 0, 0, 0))

        ellipseRect = Rect(fmx, fmy, mx - fmx, my - fmy)

        if radius > abs(ellipseRect.width) or radius > abs(ellipseRect.height):
            draw.ellipse(ellipseSurf, (0, 0, 0), (0, 0, abs(ellipseRect.width), abs(ellipseRect.height)))
        else:
            draw.ellipse(ellipseSurf, (0, 0, 0), (0, 0, abs(ellipseRect.width), abs(ellipseRect.height)))
            draw.ellipse(ellipseSurf, (255, 255, 255, 0),
                         (radius // 2, radius // 2, abs(ellipseRect.width) - radius, abs(ellipseRect.height) - radius))

        if ellipseRect.width < 0:
            if ellipseRect.height > 0:
                screen.blit(ellipseSurf, (mx, fmy))
            else:
                screen.blit(ellipseSurf, (mx, my))
        else:
            if ellipseRect.height > 0:
                screen.blit(ellipseSurf, (fmx, fmy))
            else:
                screen.blit(ellipseSurf, (fmx, my))

    display.flip()
quit()
