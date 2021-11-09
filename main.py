import pygame
import random
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


def question_factory():
    pass


def update_fps():
    # Draw text to pygame with openGL
    clock.tick(60)
    fps = str(int(clock.get_fps()))
    textSurface = font.render(fps + " FPS", True, (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(10, 10)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def question_text(text):
    # Draw text to pygame with openGL
    font = pygame.font.SysFont("Arial", 60)
    textSurface = font.render(text, True, (255, 255, 66, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(width/2 - 75, height - 120)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def player():
    glColor3ub(255, 255, 255)
    glPointSize(50)
    glBegin(GL_POINTS)
    glVertex2f(pos_x, height / 2)
    glEnd()


def draw():
    player()
    question_text('Testing')


def keyMapping():
    global pos_x
    # Key mapping - continuous press
    keys = pygame.key.get_pressed()
    if 24 <= pos_x <= 1256:
        if keys[K_LEFT] and pos_x != 24:
            pos_x -= 7
        if keys[K_RIGHT] and pos_x != 1256:
            pos_x += 7
    if keys[K_q]:  # debug
        print(pos_x)


def main():
    global clock, font, width, height, pos_x
    # Pygame init
    pygame.init()
    width, height = 1280, 720
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
    pos_x = width / 2
    screen = pygame.display.set_mode((width, height), OPENGL)

    # OpenGL init
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    loop = 1
    while loop:
        # Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
                print('Quit by X')
        keyMapping()

        # Draw
        glClearColor(255, 0, 0, 255)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw()
        update_fps()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
