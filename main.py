import pygame
import pygame.freetype
import random
from OpenGL.GL import *
from pygame.locals import *


class Watcher:
    """ A class to watch value """

    def __init__(self, val, name):
        self.variable = val
        self.name = name

    def plus(self, val):
        self.variable += val
        print(f"{self.name} added +{val} to {self.variable}")
        if self.name == 'score':
            # TODO effect if score is changed
            pass

    def minus(self, val):
        self.variable -= val
        print(f"{self.name} reduced -{val} to {self.variable}")
        if self.name == 'lives':
            # TODO effect if lives is changed
            pass

    def get_value(self):
        # Change diff and half
        # Explanation, return 2 variable
        # First one is diff and second is half
        if self.name == 'score':
            if self.variable < 24:
                return 1, 1, self.variable
            elif 24 <= self.variable < 50:
                return 1, 2, self.variable
            elif 50 <= self.variable < 90:
                return 2, 1, self.variable
            elif 90 <= self.variable < 150:
                return 2, 2, self.variable
            elif 150 <= self.variable < 250:
                return 3, 1, self.variable
            elif self.variable >= 250:
                return 3, 2, self.variable
        if self.name == 'lives':
            return self.variable

    def set_val(self, val):
        self.variable = val


class TitleScene:
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
            if TitleScene.FONT is None:
                TitleScene.FONT = pygame.freetype.SysFont(None, 60)
            loop = 0
            for line in self.text:
                if loop == 0:
                    TitleScene.FONT.render_to(self.background, (230, y), line, pygame.Color('black'))
                    TitleScene.FONT.render_to(self.background, (229, y - 1), line, pygame.Color('white'))
                elif loop == 1:
                    TitleScene.FONT.render_to(self.background, (195, y), line, pygame.Color('black'))
                    TitleScene.FONT.render_to(self.background, (194, y - 1), line, pygame.Color('white'))
                else:
                    TitleScene.FONT.render_to(self.background, (100, y), line, pygame.Color('black'))
                    TitleScene.FONT.render_to(self.background, (99, y - 1), line, pygame.Color('white'))
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

        if TitleScene.FONT is None:
            TitleScene.FONT = pygame.freetype.SysFont(None, 32)

        self.rects = []
        x = 185
        y = 170
        for n in range(4):
            rect = pygame.Rect(x, y, 60, 60)
            self.rects.append(rect)
            x += 70

    def start(self, *args):
        score.set_val(0)
        lives.set_val(3)

    def draw(self):
        self.background.fill(pygame.Color('lightgrey'))
        TitleScene.FONT.render_to(self.background, (170, 70), 'Pilih Operasi Hitung', pygame.Color('black'))
        TitleScene.FONT.render_to(self.background, (169, 69), 'Pilih Operasi Hitung', pygame.Color('white'))

        n = 0
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.background, pygame.Color('darkgrey'), rect)
            pygame.draw.rect(self.background, pygame.Color('darkgrey'), rect, 3)
            TitleScene.FONT.render_to(self.background, (rect.x + 20, rect.y + 20), str(self.level[n]),
                                      pygame.Color('black'))
            TitleScene.FONT.render_to(self.background, (rect.x + 19, rect.y + 19), str(self.level[n]),
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
        if TitleScene.FONT is None:
            TitleScene.FONT = pygame.freetype.SysFont(None, 40)

        self.rects = []
        x = 120
        y = 120
        for n in range(2):
            rect = pygame.Rect(x, y, 80, 80)
            self.rects.append(rect)
            x += 100

    def start(self, gamestate):
        self.background = pygame.Surface((640, 480))
        self.gamestate = gamestate
        diff = score.get_value()[0]
        half = score.get_value()[1]
        self.question, self.answer, wrong1, wrong2 = gamestate.pop_question(diff, half)
        self.wrong = random.choice([wrong1, wrong2])
        self.randomizer = random.randint(0, 1)

    def draw(self):
        self.background.fill(pygame.Color('lightgrey'))
        TitleScene.FONT.render_to(self.background, (120, 50), self.question, pygame.Color('black'))
        TitleScene.FONT.render_to(self.background, (119, 49), self.question, pygame.Color('white'))

        TitleScene.FONT.render_to(self.background, (400, 1), f'Score : {score.get_value()[2]}', pygame.Color('black'))
        TitleScene.FONT.render_to(self.background, (399, 0), f'Score : {score.get_value()[2]}', pygame.Color('white'))

        TitleScene.FONT.render_to(self.background, (50, 1), f'Lives : {lives.get_value()}', pygame.Color('black'))
        TitleScene.FONT.render_to(self.background, (49, 0), f'Lives : {lives.get_value()}', pygame.Color('white'))

        loop = 0
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.background, pygame.Color('darkgrey'), rect)
            pygame.draw.rect(self.background, pygame.Color('darkgrey'), rect, 5)
            if self.randomizer == 0:
                if loop == 0:
                    TitleScene.FONT.render_to(self.background, (rect.x + 30, rect.y + 30), str(self.answer),
                                              pygame.Color('black'))
                    TitleScene.FONT.render_to(self.background, (rect.x + 29, rect.y + 29), str(self.answer),
                                              pygame.Color('white'))
                if loop == 1:
                    TitleScene.FONT.render_to(self.background, (rect.x + 30, rect.y + 30), str(self.wrong),
                                              pygame.Color('black'))
                    TitleScene.FONT.render_to(self.background, (rect.x + 29, rect.y + 29), str(self.wrong),
                                              pygame.Color('white'))
            if self.randomizer == 1:
                if loop == 1:
                    TitleScene.FONT.render_to(self.background, (rect.x + 30, rect.y + 30), str(self.answer),
                                              pygame.Color('black'))
                    TitleScene.FONT.render_to(self.background, (rect.x + 29, rect.y + 29), str(self.answer),
                                              pygame.Color('white'))
                if loop == 0:
                    TitleScene.FONT.render_to(self.background, (rect.x + 30, rect.y + 30), str(self.wrong),
                                              pygame.Color('black'))
                    TitleScene.FONT.render_to(self.background, (rect.x + 29, rect.y + 29), str(self.wrong),
                                              pygame.Color('white'))
            loop += 1

        surfaceToTexture(self.background)

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        # TODO check specific clicked rect
                        self.gamestate.answer(self.wrong)
                        if lives.get_value() == 0:
                            return 'RESULT', self.gamestate.get_result()
                        elif self.gamestate.n1:
                            return 'GAME', self.gamestate
                        else:
                            return 'GAME', GameState(self.gamestate.difficulty)



class ResultScene:
    FONT = None

    def __init__(self, next_scene, *text):
        self.background = pygame.Surface((640, 480))
        self.text = text
        self.next_scene = next_scene
        self.additional_text = None

    def start(self, *text):
        self.additional_text = text

    def draw(self):
        self.background.fill(pygame.Color('lightgrey'))
        y = 80
        if self.text:
            if ResultScene.FONT is None:
                ResultScene.FONT = pygame.freetype.SysFont(None, 32)
            for line in self.text:
                ResultScene.FONT.render_to(self.background, (120, y), line, pygame.Color('black'))
                ResultScene.FONT.render_to(self.background, (119, y - 1), line, pygame.Color('white'))
                y += 50

        if self.additional_text:
            y = 180
            for line in self.additional_text:
                ResultScene.FONT.render_to(self.background, (120, y), line, pygame.Color('black'))
                ResultScene.FONT.render_to(self.background, (119, y - 1), line, pygame.Color('white'))
                y += 50

        surfaceToTexture(self.background)

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return self.next_scene, None


class GameState:
    ans = None

    def __init__(self, difficulty):   # this diff is operator (+, -, :, /)
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

        # TODO diff pecahan

        self.difficulty = difficulty
        self.current_question = None
        self.n1 = None
        self.n2 = None

    def pop_question(self, diff, half):
        operator = ''
        ans = 0
        q = []

        # Check diff and half based on score
        if diff == 1:
            if half == 1:
                self.n1 = self.d1h1_1
                self.n2 = self.d1h1_2
            elif half == 2:
                self.n1 = self.d1h2_1 + self.d1h1_1
                self.n2 = self.d1h2_2 + self.d1h1_2
        elif diff == 2:
            if half == 1:
                self.n1 = self.d2h1_1 + self.d1h2_1 + self.d1h1_1
                self.n2 = self.d2h1_2 + self.d1h2_2 + self.d1h1_2
            elif half == 2:
                self.n1 = self.d2h2_1 + self.d2h1_1 + self.d1h2_1 + self.d1h1_1
                self.n2 = self.d2h2_2 + self.d2h1_2 + self.d1h2_2 + self.d1h1_2
        elif diff == 3:
            if half == 1:
                self.n1 = self.d2h2_1 + self.d2h1_1 + self.d1h2_1 + self.d1h1_1
                self.n2 = self.d2h2_2 + self.d2h1_2 + self.d1h2_2 + self.d1h1_2
            elif half == 2:
                self.n1 = self.d2h2_1 + self.d2h1_1 + self.d1h2_1 + self.d1h1_1
                self.n2 = self.d2h2_2 + self.d2h1_2 + self.d1h2_2 + self.d1h1_2

        # Make question
        if self.n1 and self.n2:
            idx = random.choice(range(len(self.n1)))
            # Check operator
            if self.difficulty == 0:
                operator = '+'
                ans = self.n1[idx] + self.n2[idx]
            elif self.difficulty == 1:
                operator = '-'
                ans = self.n1[idx] - self.n2[idx]
            elif self.difficulty == 2:
                operator = 'x'
                ans = self.n1[idx] * self.n2[idx]
            elif self.difficulty == 3:
                operator = ':'
                ans = self.n1[idx] / self.n2[idx]

            if int(ans) < 0:
                wrong1 = ans + random.randint(int(ans), -1)
                wrong2 = ans - random.randint(int(ans), -1)
            if int(ans) > 0:
                wrong1 = ans + random.randint(1, int(ans))
                wrong2 = ans - random.randint(1, int(ans))
            else:
                wrong1 = ans + random.randint(1, 5)
                wrong2 = ans - random.randint(1, 5)

            q.append(f'{self.n1[idx]} {operator} {self.n2[idx]} = ???')
            q.append(ans)
            q.append(wrong1)
            q.append(wrong2)
            self.n1.pop(idx)
            self.n2.pop(idx)

        self.current_question = q
        return q

    def answer(self, answer):
        if answer == self.current_question[1]:
            score.plus(1)
        else:
            lives.minus(1)

    def get_result(self):
        return f'Score : {score.get_value()[2]}'


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
    global texID, clock, info, score, lives
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
        'TITLE': TitleScene('LEVEL', 'MARTUNG', 'Mari Berhitung', '', '', '', '', '',
                             'Tekan [SPASI] untuk mulai'),
        'LEVEL': LevelScene(),
        'GAME': GameScene(),
        'RESULT': ResultScene('TITLE', 'GAME OVER')
    }
    scene = scenes['LEVEL']

    # Game init
    score = Watcher(0, 'score')
    lives = Watcher(3, 'lives')

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
