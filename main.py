import pygame
import pygame.freetype
import random
from OpenGL.GL import *
from pygame.locals import *


class Score_Watcher:
    """ A class to watch value of Score """

    def __init__(self, val):
        self.variable = val

    def plus(self, val):
        self.variable += val

        # Change diff and half
        print(f"Score changed to {self.variable}")
        # Explanation, return 2 variable
        # First one is diff and second is half
        if self.variable < 24:
            return 1, 1
        elif 24 <= self.variable < 50:
            return 1, 2
        elif 50 <= self.variable < 90:
            return 2, 1
        elif 90 <= self.variable < 150:
            return 2, 2
        elif 150 <= self.variable < 250:
            return 3, 1
        elif self.variable >= 250:
            return 3, 2

    def get_value(self):
        return self.variable


class SimpleScene:
    FONT = None

    def __init__(self, next_scene, *text):
        self.background = pygame.Surface((640, 480))
        self.text = text
        self.next_scene = next_scene
        self.additional_text = None

    def start(self, *args):
        pass

    def draw(self):
        self.background.fill(pygame.Color('lightgrey'))

        y = 80
        if self.text:
            if SimpleScene.FONT is None:
                SimpleScene.FONT = pygame.font.SysFont(None, 60)
            loop = 0
            for line in self.text:
                if loop == 0:
                    SimpleScene.FONT.render_to(self.background, (230, y), line, pygame.Color('black'))
                    SimpleScene.FONT.render_to(self.background, (229, y - 1), line, pygame.Color('white'))
                elif loop == 1:
                    SimpleScene.FONT.render_to(self.background, (195, y), line, pygame.Color('black'))
                    SimpleScene.FONT.render_to(self.background, (194, y - 1), line, pygame.Color('white'))
                else:
                    SimpleScene.FONT.render_to(self.background, (100, y), line, pygame.Color('black'))
                    SimpleScene.FONT.render_to(self.background, (99, y - 1), line, pygame.Color('white'))
                y += 40
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
        self.background = pygame.Surface((640, 480))

        if SimpleScene.FONT is None:
            SimpleScene.FONT = pygame.freetype.SysFont(None, 32)

        self.rects = []
        x = 185
        y = 170
        for n in range(4):
            rect = pygame.Rect(x, y, 60, 60)
            self.rects.append(rect)
            x += 70

    def start(self, *args):
        pass

    def draw(self):
        self.background.fill(pygame.Color('lightgrey'))
        SimpleScene.FONT.render_to(self.background, (170, 70), 'Pilih Operasi Hitung', pygame.Color('black'))
        SimpleScene.FONT.render_to(self.background, (169, 69), 'Pilih Operasi Hitung', pygame.Color('white'))

        n = 0
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.background, pygame.Color('darkgrey'), rect)
            pygame.draw.rect(self.background, pygame.Color('darkgrey'), rect, 3)
            SimpleScene.FONT.render_to(self.background, (rect.x + 20, rect.y + 20), str(self.level[n]),
                                       pygame.Color('black'))
            SimpleScene.FONT.render_to(self.background, (rect.x + 19, rect.y + 19), str(self.level[n]),
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


class GameScene:
    def __init__(self):
        if SimpleScene.FONT is None:
            SimpleScene.FONT = pygame.freetype.SysFont(None, 32)

        # self.rects = []
        # x = 120
        # y = 120
        # for n in range(4):
        #     rect = pygame.Rect(x, y, 80, 80)
        #     self.rects.append(rect)
        #     x += 100

    def start(self, gamestate):
        self.background = pygame.Surface((640, 480))
        self.background.fill(pygame.Color('lightgrey'))
        self.gamestate = gamestate
        question, answer = gamestate.pop_question()

        # SimpleScene.FONT.render_to(self.background, (120, 50), question, pygame.Color('black'))
        # SimpleScene.FONT.render_to(self.background, (119, 49), question, pygame.Color('white'))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        glColor3ub(255, 255, 255)
        glPointSize(50)
        glBegin(GL_POINTS)
        glVertex2f(100, 50)
        glEnd()
        # n = 1
        # for rect in self.rects:
        #     if rect.collidepoint(pygame.mouse.get_pos()):
        #         pygame.draw.rect(screen, pygame.Color('darkgrey'), rect)
        #     pygame.draw.rect(screen, pygame.Color('darkgrey'), rect, 5)
        #     SimpleScene.FONT.render_to(screen, (rect.x + 30, rect.y + 30), str(n), pygame.Color('black'))
        #     SimpleScene.FONT.render_to(screen, (rect.x + 29, rect.y + 29), str(n), pygame.Color('white'))
        #     n += 1

    def update(self, events, dt):
        for event in events:
            pass
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     n = 1
            #     for rect in self.rects:
            #         if rect.collidepoint(event.pos):
            #             self.gamestate.answer(n)
            #             if self.gamestate.questions:
            #                 return 'GAME', self.gamestate
            #             else:
            #                 return 'RESULT', self.gamestate.get_result()
            #         n += 1


class GameState:
    ans = None

    def __init__(self, difficulty):  # this diff is operator
        # Diff 1
        self.d1h1_1 = [random.randint(1, 10)
                       for a in range(0, 30)]
        self.d1h1_2 = [random.randint(1, 10)
                       for a in range(0, 30)]
        self.d1h2_1 = [random.randint(10, 50)
                       for a in range(0, 30)]
        self.d1h2_2 = [random.randint(10, 50)
                       for a in range(0, 30)]

        # Diff 2
        self.d2h1_1 = [(round(random.uniform(1.00, 10.00), 1))
                       for a in range(0, 50)]
        self.d2h1_2 = [(round(random.uniform(1.00, 10.00), 1))
                       for a in range(0, 50)]
        self.d2h2_1 = [(round(random.uniform(10.00, 50.00), 1))
                       for a in range(0, 70)]
        self.d2h2_2 = [(round(random.uniform(10.00, 50.00), 1))
                       for a in range(0, 70)]

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
        # check diff (self.diff) - its a operator

        if answer == self.current_question[1]:
            self.right += 1
        else:
            self.wrong += 1

    def get_result(self):
        return f'{self.right} answers correct', f'{self.wrong} answers wrong', '', 'Good!' if self.right > self.wrong else 'You can do better!'


def surfaceToTexture(pygame_surface):
    # Function to convert pygame surface to openGL texture
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
    pygame.display.set_mode((640, 480), OPENGL | DOUBLEBUF)
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
        # 'TITLE': SimpleScene('LEVEL', 'MARTUNG', 'Mari Berhitung', '', '', '', '', '',
        #                      'Tekan [SPASI] untuk mulai'),
        'LEVEL': LevelScene()
    }
    scene = scenes['LEVEL']

    done = False
    while not done:
        # Event
        events = pygame.event.get()
        for e in events:
            if e.type == QUIT:
                done = True

        # Prepare to render
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

        # Draw texture openGL Texture
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
