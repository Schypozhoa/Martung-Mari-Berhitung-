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
                    print(f'space pressed, go to {self.next_scene}')
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
                        print(f'operator selected {n}, go to game')
                        return 'GAME', GameState(n)
                    n += 1


class GameScene:
    def __init__(self):
        if TitleScene.FONT is None:
            TitleScene.FONT = pygame.freetype.SysFont(None, 40)

        self.on_left = False
        self.on_right = False
        self.rects = []
        x = 220
        y = 120
        for n in range(2):
            rect = pygame.Rect(x, y, 60, 60)
            self.rects.append(rect)
            x += 100

    def start(self, gamestate):
        self.background = pygame.Surface((640, 480))
        self.gamestate = gamestate
        diff = score.get_value()[0]
        half = score.get_value()[1]

        print(f'---------------------\n'
              f'Get diff and half...\n'
              f'diff > {diff}\n'
              f'half > {half}\n')

        self.question, self.answer, wrong1, wrong2 = gamestate.pop_question(diff, half)
        self.wrong = random.choice([wrong1, wrong2])
        self.randomizer = random.randint(0, 1)

        print(f'Randomize the wrong ans and answer position...\n'
              f'taken wrong ans > {self.wrong}\n'
              f'randomizer > {self.randomizer}\n')

    def draw(self):
        self.background.fill(pygame.Color('lightgrey'))
        TitleScene.FONT.render_to(self.background, (120, 50), self.question, pygame.Color('black'))
        TitleScene.FONT.render_to(self.background, (119, 49), self.question, pygame.Color('white'))

        TitleScene.FONT.render_to(self.background, (400, 1), f'Score : {score.get_value()[2]}', pygame.Color('black'))
        TitleScene.FONT.render_to(self.background, (399, 0), f'Score : {score.get_value()[2]}', pygame.Color('white'))

        TitleScene.FONT.render_to(self.background, (50, 1), f'Lives : {lives.get_value()}', pygame.Color('black'))
        TitleScene.FONT.render_to(self.background, (49, 0), f'Lives : {lives.get_value()}', pygame.Color('white'))

        recs_idx = 0
        self.rect_data = []  # Save rect data in format > [randomizer, index, text]
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.background, pygame.Color('darkgrey'), rect)
            pygame.draw.rect(self.background, pygame.Color('darkgrey'), rect, 5)
            if self.randomizer == 0:
                if recs_idx == 0:
                    TitleScene.FONT.render_to(self.background, (rect.x + 30, rect.y + 30), str(self.answer),
                                              pygame.Color('black'))
                    TitleScene.FONT.render_to(self.background, (rect.x + 29, rect.y + 29), str(self.answer),
                                              pygame.Color('white'))
                    data = [0, 0, self.answer]
                    self.rect_data.append(data)
                if recs_idx == 1:
                    TitleScene.FONT.render_to(self.background, (rect.x + 30, rect.y + 30), str(self.wrong),
                                              pygame.Color('black'))
                    TitleScene.FONT.render_to(self.background, (rect.x + 29, rect.y + 29), str(self.wrong),
                                              pygame.Color('white'))
                    data = [0, 1, self.wrong]
                    self.rect_data.append(data)

            if self.randomizer == 1:
                if recs_idx == 0:
                    TitleScene.FONT.render_to(self.background, (rect.x + 30, rect.y + 30), str(self.wrong),
                                              pygame.Color('black'))
                    TitleScene.FONT.render_to(self.background, (rect.x + 29, rect.y + 29), str(self.wrong),
                                              pygame.Color('white'))
                    data = [1, 0, self.wrong]
                    self.rect_data.append(data)
                if recs_idx == 1:
                    TitleScene.FONT.render_to(self.background, (rect.x + 30, rect.y + 30), str(self.answer),
                                              pygame.Color('black'))
                    TitleScene.FONT.render_to(self.background, (rect.x + 29, rect.y + 29), str(self.answer),
                                              pygame.Color('white'))
                    data = [1, 1, self.answer]
                    self.rect_data.append(data)

            recs_idx += 1

        if self.on_left:
            TitleScene.FONT.render_to(self.background, (120, 430), f'Tekan [enter] untuk memilih {self.rect_data[0][2]}', pygame.Color('black'))
            TitleScene.FONT.render_to(self.background, (119, 429), f'Tekan [enter] untuk memilih {self.rect_data[0][2]}', pygame.Color('white'))
        elif self.on_right:
            TitleScene.FONT.render_to(self.background, (120, 430), f'Tekan [enter] untuk memilih {self.rect_data[1][2]}', pygame.Color('black'))
            TitleScene.FONT.render_to(self.background, (119, 429), f'Tekan [enter] untuk memilih {self.rect_data[1][2]}', pygame.Color('white'))

        surfaceToTexture(self.background)

    def update(self, events, dt):
        final_ans = 0
        for event in events:
            if pos_x <= -1:
                self.on_left = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    print('Answering...')
                    final_ans = self.rect_data[0][2]
                    print(f'selected ans (left) > {final_ans}')
                    self.gamestate.answer(final_ans)
                    if lives.get_value() == 0:
                        print('game over\n'
                              '-----------------------\n')
                        return 'RESULT', self.gamestate.get_result()
                    elif self.gamestate.n1:
                        return 'GAME', self.gamestate
                    else:
                        return 'GAME', GameState(self.gamestate.difficulty)
            elif pos_x >= -0.02:
                self.on_right = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    print('Answering...')
                    final_ans = self.rect_data[1][2]
                    print(f'selected ans (right) > {final_ans}')
                    self.gamestate.answer(final_ans)
                    if lives.get_value() == 0:
                        print('game over\n'
                              '-----------------------\n')
                        return 'RESULT', self.gamestate.get_result()
                    elif self.gamestate.n1:
                        return 'GAME', self.gamestate
                    else:
                        return 'GAME', GameState(self.gamestate.difficulty)
            else:
                self.on_left = False
                self.on_right = False


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

    def __init__(self, difficulty):  # this diff is operator (+, -, :, /)
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

        print(f'GameState initialized with operator {difficulty}\n'
              f'0 = [+], 1 = [-], 2 = [x], 3 = [:]\n')

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

        print(f'Making Question...\n'
              f'question > {q[0]}\n'
              f'ans > {q[1]}\n'
              f'w1 > {q[2]}\n'
              f'w2 > {q[3]}\n')

        self.current_question = q
        return q

    def answer(self, answer):
        global pos_x, pos_y
        pos_x = -0.55
        pos_y = -0.75

        if answer == self.current_question[1]:
            score.plus(1)
            print('correct')
        else:
            lives.minus(1)
            print('wrong')

    def get_result(self):
        return f'Score : {score.get_value()[2]}'


def drawPlayer():
    # Her name? Call her Michi
    leg_L()
    leg_R()

    skirt()
    shirt()


def shirt():
    # Base
    glColor3ub(253, 244, 220)
    glBegin(GL_POLYGON)
    glVertex2f(0.591 + pos_x, 0.519 + pos_y)
    glVertex2f(0.506 + pos_x, 0.502 + pos_y)
    glVertex2f(0.429 + pos_x, 0.516 + pos_y)
    glVertex2f(0.439 + pos_x, 0.708 + pos_y)
    glVertex2f(0.494 + pos_x, 0.721 + pos_y)
    glVertex2f(0.506 + pos_x, 0.679 + pos_y)
    glVertex2f(0.538 + pos_x, 0.732 + pos_y)
    glVertex2f(0.592 + pos_x, 0.715 + pos_y)
    glEnd()

    # Hand L
    glColor3ub(255, 229, 180)
    glBegin(GL_POLYGON)
    glVertex2f(0.367 + pos_x, 0.529 + pos_y)
    glVertex2f(0.393 + pos_x, 0.518 + pos_y)
    glVertex2f(0.389 + pos_x, 0.498 + pos_y)
    glVertex2f(0.372 + pos_x, 0.494 + pos_y)
    glVertex2f(0.356 + pos_x, 0.503 + pos_y)
    glVertex2f(0.354 + pos_x, 0.519 + pos_y)
    glEnd()

    # Hand R
    glColor3ub(255, 229, 180)
    glBegin(GL_POLYGON)
    glVertex2f(0.635 + pos_x, 0.502 + pos_y)
    glVertex2f(0.651 + pos_x, 0.493 + pos_y)
    glVertex2f(0.673 + pos_x, 0.500 + pos_y)
    glVertex2f(0.673 + pos_x, 0.519 + pos_y)
    glVertex2f(0.661 + pos_x, 0.531 + pos_y)
    glVertex2f(0.634 + pos_x, 0.521 + pos_y)
    glEnd()

    # Base L Arm
    glColor3ub(253, 244, 220)
    glBegin(GL_QUADS)
    glVertex2f(0.592 + pos_x, 0.715 + pos_y)
    glVertex2f(0.672 + pos_x, 0.527 + pos_y)
    glVertex2f(0.629 + pos_x, 0.513 + pos_y)
    glVertex2f(0.591 + pos_x, 0.621 + pos_y)
    glEnd()

    # Base R Arm
    glBegin(GL_QUADS)
    glVertex2f(0.435 + pos_x, 0.615 + pos_y)
    glVertex2f(0.397 + pos_x, 0.513 + pos_y)
    glVertex2f(0.360 + pos_x, 0.530 + pos_y)
    glVertex2f(0.439 + pos_x, 0.708 + pos_y)
    glEnd()

    # Motive L
    glColor3ub(135, 206, 250)
    glBegin(GL_POLYGON)
    glVertex2f(0.440 + pos_x, 0.709 + pos_y)
    glVertex2f(0.436 + pos_x, 0.693 + pos_y)
    glVertex2f(0.440 + pos_x, 0.680 + pos_y)
    glVertex2f(0.445 + pos_x, 0.672 + pos_y)
    glVertex2f(0.453 + pos_x, 0.664 + pos_y)
    glVertex2f(0.463 + pos_x, 0.659 + pos_y)
    glVertex2f(0.474 + pos_x, 0.657 + pos_y)
    glVertex2f(0.485 + pos_x, 0.660 + pos_y)
    glVertex2f(0.498 + pos_x, 0.668 + pos_y)
    glVertex2f(0.515 + pos_x, 0.679 + pos_y)
    glVertex2f(0.494 + pos_x, 0.721 + pos_y)
    glEnd()

    # Motive R
    glColor3ub(135, 206, 250)
    glBegin(GL_POLYGON)
    glVertex2f(0.591 + pos_x, 0.716 + pos_y)
    glVertex2f(0.595 + pos_x, 0.697 + pos_y)
    glVertex2f(0.592 + pos_x, 0.680 + pos_y)
    glVertex2f(0.583 + pos_x, 0.667 + pos_y)
    glVertex2f(0.573 + pos_x, 0.657 + pos_y)
    glVertex2f(0.557 + pos_x, 0.652 + pos_y)
    glVertex2f(0.541 + pos_x, 0.652 + pos_y)
    glVertex2f(0.526 + pos_x, 0.657 + pos_y)
    glVertex2f(0.514 + pos_x, 0.667 + pos_y)
    glVertex2f(0.506 + pos_x, 0.679 + pos_y)
    glVertex2f(0.538 + pos_x, 0.735 + pos_y)
    glEnd()

    # Line
    glColor3ub(0, 0, 0)
    glBegin(GL_LINES)
    glVertex2f(0.510 + pos_x, 0.679 + pos_y)
    glVertex2f(0.506 + pos_x, 0.502 + pos_y)
    glEnd()


def skirt():
    # Base
    glColor3ub(255, 192, 203)
    glBegin(GL_POLYGON)
    glVertex2f(0.400 + pos_x, 0.427 + pos_y)
    glVertex2f(0.446 + pos_x, 0.414 + pos_y)
    glVertex2f(0.484 + pos_x, 0.410 + pos_y)
    glVertex2f(0.533 + pos_x, 0.410 + pos_y)
    glVertex2f(0.596 + pos_x, 0.416 + pos_y)
    glVertex2f(0.633 + pos_x, 0.426 + pos_y)
    glVertex2f(0.591 + pos_x, 0.519 + pos_y)
    glVertex2f(0.506 + pos_x, 0.502 + pos_y)
    glVertex2f(0.429 + pos_x, 0.516 + pos_y)
    glEnd()

    # Line
    glColor3ub(0, 0, 0)
    glBegin(GL_LINES)
    glVertex2f(0.446 + pos_x, 0.414 + pos_y)
    glVertex2f(0.463 + pos_x, 0.511 + pos_y)
    glEnd()

    glBegin(GL_LINES)
    glVertex2f(0.484 + pos_x, 0.410 + pos_y)
    glVertex2f(0.492 + pos_x, 0.505 + pos_y)
    glEnd()

    glBegin(GL_LINES)
    glVertex2f(0.533 + pos_x, 0.410 + pos_y)
    glVertex2f(0.524 + pos_x, 0.505 + pos_y)
    glEnd()

    glBegin(GL_LINES)
    glVertex2f(0.597 + pos_x, 0.416 + pos_y)
    glVertex2f(0.561 + pos_x, 0.513 + pos_y)
    glEnd()


def leg_L():
    # Leg
    glColor3ub(255, 229, 180)
    glBegin(GL_POLYGON)
    glVertex2f(0.439 + pos_x, 0.308 + pos_y)
    glVertex2f(0.455 + pos_x, 0.301 + pos_y)
    glVertex2f(0.473 + pos_x, 0.299 + pos_y)
    glVertex2f(0.477 + pos_x, 0.346 + pos_y)
    glVertex2f(0.486 + pos_x, 0.426 + pos_y)
    glVertex2f(0.446 + pos_x, 0.431 + pos_y)
    glVertex2f(0.445 + pos_x, 0.350 + pos_y)
    glEnd()

    # Shoe
    glColor3ub(11, 11, 69)
    glBegin(GL_POLYGON)
    glVertex2f(0.473 + pos_x, 0.280 + pos_y)
    glVertex2f(0.430 + pos_x, 0.280 + pos_y)
    glVertex2f(0.419 + pos_x, 0.283 + pos_y)
    glVertex2f(0.416 + pos_x, 0.288 + pos_y)
    glVertex2f(0.417 + pos_x, 0.294 + pos_y)
    glVertex2f(0.423 + pos_x, 0.300 + pos_y)
    glVertex2f(0.439 + pos_x, 0.308 + pos_y)
    glVertex2f(0.455 + pos_x, 0.301 + pos_y)
    glVertex2f(0.473 + pos_x, 0.299 + pos_y)
    glEnd()


def leg_R():
    # Leg
    glColor3ub(255, 229, 180)
    glBegin(GL_POLYGON)
    glVertex2f(0.561 + pos_x, 0.308 + pos_y)
    glVertex2f(0.580 + pos_x, 0.304 + pos_y)
    glVertex2f(0.597 + pos_x, 0.305 + pos_y)
    glVertex2f(0.583 + pos_x, 0.353 + pos_y)
    glVertex2f(0.576 + pos_x, 0.432 + pos_y)
    glVertex2f(0.538 + pos_x, 0.429 + pos_y)
    glVertex2f(0.557 + pos_x, 0.349 + pos_y)
    glEnd()

    # Shoe
    glColor3ub(11, 11, 69)
    glBegin(GL_POLYGON)
    glVertex2f(0.561 + pos_x, 0.308 + pos_y)
    glVertex2f(0.580 + pos_x, 0.304 + pos_y)
    glVertex2f(0.597 + pos_x, 0.305 + pos_y)
    glVertex2f(0.600 + pos_x, 0.280 + pos_y)
    glVertex2f(0.552 + pos_x, 0.280 + pos_y)
    glVertex2f(0.545 + pos_x, 0.281 + pos_y)
    glVertex2f(0.539 + pos_x, 0.287 + pos_y)
    glVertex2f(0.540 + pos_x, 0.294 + pos_y)
    glVertex2f(0.547 + pos_x, 0.299 + pos_y)
    glEnd()


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
    global texID, clock, info, score, lives, pos_x, pos_y
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
    scene = scenes['TITLE']

    # Game init
    score = Watcher(0, 'score')
    lives = Watcher(3, 'lives')
    pos_x = -0.55
    pos_y = -0.75
    draw = False

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

        # Update Scene
        result = scene.update(events, dt)
        if result:
            next_scene, state = result
            if next_scene:
                scene = scenes[next_scene]
                scene.start(state)

        scene.draw()

        # Draw scene as openGL Texture
        glEnable(GL_TEXTURE_2D)
        glColor3ub(255, 255, 255)
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
        glDisable(GL_TEXTURE_2D)

        # Draw player
        if result and result[0] == 'GAME':
            draw = True
        elif result and result[0] == 'RESULT':
            draw = False

        if draw:
            glScaled(1.5, 1.5, 1)

            keys = pygame.key.get_pressed()
            if keys[K_LEFT] and pos_x >= -1.02:
                pos_x -= 0.015
            if keys[K_RIGHT] and pos_x <= 0:
                pos_x += 0.015
            if keys[K_q]:  # debug
                print(pos_x)

            drawPlayer()
        pygame.display.flip()
        dt = clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
