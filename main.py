import pygame
import pygame.freetype
import random
from OpenGL.GL import *
from pygame.locals import *


class SimpleScene:
    FONT = None

    def __init__(self, next_scene, *text):
        self.background = pygame.Surface((1280, 720))
        self.text = text
        self.next_scene = next_scene
        self.additional_text = None

    def start(self, *args):
        pass

    def draw(self):
        self.background.fill(pygame.Color('lightgrey'))

        y = 90
        if self.text:
            if SimpleScene.FONT is None:
                SimpleScene.FONT = pygame.font.SysFont(None, 60)
            loop = 0
            for line in self.text:
                if loop == 0:
                    SimpleScene.FONT.render_to(self.background, (460, y), line, pygame.Color('black'))
                    SimpleScene.FONT.render_to(self.background, (459, y - 1), line, pygame.Color('white'))
                elif loop == 1:
                    SimpleScene.FONT.render_to(self.background, (400, y), line, pygame.Color('black'))
                    SimpleScene.FONT.render_to(self.background, (399, y - 1), line, pygame.Color('white'))
                else:
                    SimpleScene.FONT.render_to(self.background, (220, y), line, pygame.Color('black'))
                    SimpleScene.FONT.render_to(self.background, (219, y - 1), line, pygame.Color('white'))
                y += 60
                loop += 1

        surfaceToTexture(self.background)

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print('space')
                    return self.next_scene, None


class LevelScene:

    def __init__(self):
        self.level = ['+', '-', 'x', ':']
        self.background = pygame.Surface((1280, 720))

        if SimpleScene.FONT is None:
            SimpleScene.FONT = pygame.freetype.SysFont(None, 32)

        self.rects = []
        x = 450
        y = 300
        for n in range(4):
            rect = pygame.Rect(x, y, 80, 80)
            self.rects.append(rect)
            x += 100

    def start(self, *args):
        pass

    def draw(self):
        self.background.fill(pygame.Color('lightgrey'))
        SimpleScene.FONT.render_to(self.background, (370, 100), 'Pilih Operasi Hitung', pygame.Color('black'))
        SimpleScene.FONT.render_to(self.background, (369, 99), 'Pilih Operasi Hitung', pygame.Color('white'))

        n = 0
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.background, pygame.Color('darkgrey'), rect)
            pygame.draw.rect(self.background, pygame.Color('darkgrey'), rect, 5)
            SimpleScene.FONT.render_to(self.background, (rect.x + 25, rect.y + 25), str(self.level[n]),
                                       pygame.Color('black'))
            SimpleScene.FONT.render_to(self.background, (rect.x + 24, rect.y + 24), str(self.level[n]),
                                       pygame.Color('white'))
            n += 1
        surfaceToTexture(self.background)

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                n = 0
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        return 'GAME', GameState(n)
                    n += 1


class GameState:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.questions = [
            ('How many legs has a cow?', 4),
            ('How many legs has a bird?', 2),
            ('What is 1 x 1 ?', 1)
        ]
        self.current_question = None
        self.right = 0
        self.wrong = 0

    def pop_question(self):
        q = random.choice(self.questions)
        self.questions.remove(q)
        self.current_question = q
        return q

    def answer(self, answer):
        if answer == self.current_question[1]:
            self.right += 1
        else:
            self.wrong += 1

    def get_result(self):
        return f'{self.right} answers correct', f'{self.wrong} answers wrong', '', 'Good!' if self.right > self.wrong else 'You can do better!'


def surfaceToTexture(pygame_surface):
    rgb_surface = pygame.image.tostring(pygame_surface, 'RGB')
    glBindTexture(GL_TEXTURE_2D, texID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    surface_rect = pygame_surface.get_rect()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, surface_rect.width, surface_rect.height, 0, GL_RGB, GL_UNSIGNED_BYTE,
                 rgb_surface)
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)


def main():
    global texID, clock, info
    # Pygame init
    pygame.init()
    pygame.display.init()
    pygame.display.set_mode((1280, 720), OPENGL | DOUBLEBUF)
    info = pygame.display.Info()
    dt = 0
    clock = pygame.time.Clock()

    # OpenGl init
    glViewport(0, 0, info.current_w, info.current_h)
    glDepthRange(0, 1)
    glMatrixMode(GL_PROJECTION)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_BLEND)
    texID = glGenTextures(1)

    # Scene init
    scenes = {
        'TITLE': SimpleScene('LEVEL', 'MARTUNG', 'Mari Berhitung', '', '', '', '', '', '',
                             'Tekan [SPASI] untuk mulai'),
        'LEVEL': LevelScene()
    }
    scene = scenes['TITLE']

    done = False
    while not done:
        # Event
        events = pygame.event.get()
        for e in events:
            if e.type == QUIT:
                done = True

        # prepare to render the texture-mapped rectangle
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glLoadIdentity()
        glEnable(GL_TEXTURE_2D)

        # Update Scene
        result = scene.update(events, dt)
        if result:
            next_scene, state = result
            print(result)
            if next_scene:
                scene = scenes[next_scene]
                scene.start(state)

        scene.draw()

        # draw texture openGL Texture
        glBindTexture(GL_TEXTURE_2D, texID)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(-1, 1)
        glTexCoord2f(0, 1)
        glVertex2f(-1, -1)
        glTexCoord2f(1, 1)
        glVertex2f(1, -1)
        glTexCoord2f(1, 0)
        glVertex2f(1, 1)
        glEnd()

        pygame.display.flip()
        dt = clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
