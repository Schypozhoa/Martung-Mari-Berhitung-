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

    def minus(self, val):
        self.variable -= val
        print(f"{self.name} reduced -{val} to {self.variable}")

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
        self.background.blit(pygame.image.load('gambar/bg_menu.jpg'), (0, 0))
        spasi = pygame.image.load('gambar/spasi.png')
        spasi = pygame.transform.rotozoom(spasi, 0, 0.1)

        fontTitle = pygame.freetype.Font('font/AdigianaUI.ttf', 50)
        fontSubtitle = pygame.freetype.Font('font/AdigianaUI.ttf', 40)
        fontContent = pygame.freetype.Font('font/Alice-Regular.ttf', 30)
        surfCenterW = self.background.get_width() / 2

        y = 90
        if self.text:
            loop = 0
            for line in self.text:
                if loop == 0:
                    fontTitle.render_to(self.background, (surfCenterW - 130, y), line, pygame.Color('black'))
                    fontTitle.render_to(self.background, (surfCenterW - 131, y - 1), line, pygame.Color('white'))
                elif loop == 1:
                    fontSubtitle.render_to(self.background, (surfCenterW - 205, y), line, pygame.Color('black'))
                    fontSubtitle.render_to(self.background, (surfCenterW - 206, y - 1), line, pygame.Color('white'))
                else:
                    fontContent.render_to(self.background, (surfCenterW - 180, y), line, pygame.Color('black'))
                    fontContent.render_to(self.background, (surfCenterW - 181, y - 1), line, pygame.Color('white'))
                y += 70
                loop += 1

        self.background.blit(spasi, (230, 360))
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

        self.rects = []
        x = 200
        y = 150
        for n in range(4):
            if n >= 2:
                if n == 2:
                    x = 200
                rect = pygame.Rect(x, y + 125, 100, 100)
            else:
                rect = pygame.Rect(x, y, 100, 100)
            self.rects.append(rect)
            x += 125

    def start(self, *args):
        score.set_val(0)
        lives.set_val(3)

    def draw(self):
        self.background.blit(pygame.image.load('gambar/bg_menu.jpg'), (0, 0))
        fontTitle = pygame.freetype.Font('font/Archicoco.ttf', 40)
        surfCenter = self.background.get_width() / 2

        fontTitle.render_to(self.background, (surfCenter - 210, 100), 'Pilih Operasi Hitung', pygame.Color('black'))
        fontTitle.render_to(self.background, (surfCenter - 211, 99), 'Pilih Operasi Hitung', pygame.Color('white'))

        n = 0
        for rect in self.rects:
            img = pygame.image.load(f'gambar/{n + 1}.jpg')
            self.background.blit(img, img.get_rect(center=rect.center))
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.background, pygame.Color('green'), rect, 3)
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

        self.on_left = False
        self.on_right = False
        self.rects = [pygame.Rect(55, 320, 60, 60), pygame.Rect(545, 320, 60, 60)]

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
        self.background.blit(pygame.image.load('gambar/bg_play.jpg'), (0, 0))
        fontQ = pygame.freetype.Font('font/Bryndan_Write.ttf', 50)
        fontA = pygame.freetype.Font('font/Bryndan_Write.ttf', 30)
        fontInfo = pygame.freetype.Font('font/Bryndan_Write.ttf', 20)
        fontStat = pygame.freetype.Font('font/Bryndan_Write.ttf', 25)
        surfCenterW = self.background.get_width() / 2
        surfCenterH = self.background.get_height() / 2

        fontQ.render_to(self.background, (surfCenterW - 80, surfCenterH - 45), self.question, pygame.Color('black'))
        fontQ.render_to(self.background, (surfCenterW - 81, surfCenterH - 46), self.question, pygame.Color('white'))

        fontStat.render_to(self.background, (520, 5), f'Skor : {score.get_value()[2]}', pygame.Color('black'))
        fontStat.render_to(self.background, (519, 4), f'Skor : {score.get_value()[2]}', pygame.Color('white'))

        fontStat.render_to(self.background, (surfCenterW - 75, 5), f'Tertinggi : {high}', pygame.Color('black'))
        fontStat.render_to(self.background, (surfCenterW - 75, 4), f'Tertinggi : {high}', pygame.Color('white'))

        fontStat.render_to(self.background, (10, 5), f'Nyawa : {lives.get_value()}', pygame.Color('black'))
        fontStat.render_to(self.background, (9, 4), f'Nyawa : {lives.get_value()}', pygame.Color('white'))

        recs_idx = 0
        self.rect_data = []  # Save rect data in format > [randomizer, index, text]
        for rect in self.rects:
            # if self.on_left and recs_idx == 0:
            #     pygame.draw.rect(self.background, pygame.Color('green'), rect, 3)
            # elif self.on_right and recs_idx == 1:
            #     pygame.draw.rect(self.background, pygame.Color('green'), rect, 3)
            # pygame.draw.rect(self.background, pygame.Color('darkgrey'), rect, 5)
            if self.randomizer == 0:
                if recs_idx == 0:
                    fontA.render_to(self.background, (rect.x + 1, rect.y + 1), str(self.answer),
                                    pygame.Color('black'))
                    fontA.render_to(self.background, (rect.x, rect.y), str(self.answer),
                                    pygame.Color('white'))
                    data = [0, 0, self.answer]
                    self.rect_data.append(data)
                if recs_idx == 1:
                    fontA.render_to(self.background, (rect.x + 1, rect.y + 1), str(self.wrong),
                                    pygame.Color('black'))
                    fontA.render_to(self.background, (rect.x, rect.y), str(self.wrong),
                                    pygame.Color('white'))
                    data = [0, 1, self.wrong]
                    self.rect_data.append(data)

            if self.randomizer == 1:
                if recs_idx == 0:
                    fontA.render_to(self.background, (rect.x + 1, rect.y + 1), str(self.wrong),
                                    pygame.Color('black'))
                    fontA.render_to(self.background, (rect.x, rect.y), str(self.wrong),
                                    pygame.Color('white'))
                    data = [1, 0, self.wrong]
                    self.rect_data.append(data)
                if recs_idx == 1:
                    fontA.render_to(self.background, (rect.x + 1, rect.y + 1), str(self.answer),
                                    pygame.Color('black'))
                    fontA.render_to(self.background, (rect.x, rect.y), str(self.answer),
                                    pygame.Color('white'))
                    data = [1, 1, self.answer]
                    self.rect_data.append(data)

            recs_idx += 1

        if self.on_left:
            fontInfo.render_to(self.background, (surfCenterW - 140, 450),
                               f'Tekan [enter] untuk memilih {self.rect_data[0][2]}', pygame.Color('black'))
            fontInfo.render_to(self.background, (surfCenterW - 141, 449),
                               f'Tekan [enter] untuk memilih {self.rect_data[0][2]}', pygame.Color('white'))
        elif self.on_right:
            fontInfo.render_to(self.background, (surfCenterW - 140, 450),
                               f'Tekan [enter] untuk memilih {self.rect_data[1][2]}', pygame.Color('black'))
            fontInfo.render_to(self.background, (surfCenterW - 141, 449),
                               f'Tekan [enter] untuk memilih {self.rect_data[1][2]}', pygame.Color('white'))

        surfaceToTexture(self.background)

    def update(self, events, dt):
        final_ans = 0
        for event in events:
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     print(event.pos)
            if pos_x <= -0.98:
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
            elif pos_x >= -0.04:
                self.on_right = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    print('Answering...')
                    final_ans = self.rect_data[1][2]
                    print(f'selected ans (right) > {final_ans}')
                    self.gamestate.answer(final_ans)
                    if lives.get_value() == 0:
                        print('game over\n'
                              '-----------------------\n')
                        return ('RESULT', self.gamestate.get_result())
                    elif self.gamestate.n1:
                        return 'GAME', self.gamestate
                    else:
                        return 'GAME', GameState(self.gamestate.difficulty)
            else:
                self.on_left = False
                self.on_right = False


class ResultScene:

    def __init__(self, next_scene, *text):
        self.background = pygame.Surface((640, 480))
        self.text = text
        self.next_scene = next_scene
        self.additional_text = None

    def start(self, text):
        self.additional_text = text

    def draw(self):
        self.background.blit(pygame.image.load('gambar/bg_menu.jpg'), (0, 0))
        spasi = pygame.image.load('gambar/spasi.png')
        spasi = pygame.transform.rotozoom(spasi, 0, 0.1)
        fontTop = pygame.freetype.Font('font/Bryndan_Write.ttf', 50)
        fontBot = pygame.freetype.Font('font/Bryndan_Write.ttf', 30)
        surfCenterW = self.background.get_width() / 2

        fontBot.render_to(self.background, (surfCenterW - 180, 370), 'Tekan           untuk kembali', pygame.Color('black'))
        fontBot.render_to(self.background, (surfCenterW - 181, 370 - 1), 'Tekan           untuk kembali', pygame.Color('white'))

        y = 80
        if self.text:
            for line in self.text:
                fontTop.render_to(self.background, (surfCenterW - 150, y), line, pygame.Color('black'))
                fontTop.render_to(self.background, (surfCenterW - 150, y - 1), line, pygame.Color('white'))
                y += 50

        if self.additional_text:
            y = 180
            for line in self.additional_text:
                fontBot.render_to(self.background, (surfCenterW - 125, y), line, pygame.Color('black'))
                fontBot.render_to(self.background, (surfCenterW - 125, y - 1), line, pygame.Color('white'))
                y += 50

        self.background.blit(spasi, (225, 360))
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

            q.append(f'{self.n1[idx]}{operator}{self.n2[idx]}=???')
            q.append(round(ans, 1))
            q.append(round(wrong1, 1))
            q.append(round(wrong2, 1))
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
        pos_y = -0.9

        if answer == self.current_question[1]:
            score.plus(1)
            print('correct')
        else:
            lives.minus(1)
            print('wrong')

    def get_result(self):
        currScore = score.get_value()[2]
        currHigh = 0
        if currScore > high:
            file_w = open('config.txt', 'w')
            name = 'skor tertinggi'.encode('utf8').hex()
            value = hex(currScore)
            file_w.write(name + ' = ' + value)
            file_w.close()
            currHigh = currScore
        else:
            currHigh = high

        return f'Skor : {currScore}', f'Skor Tertinggi : {currHigh}'


def drawPlayer():
    # Her name? Call her Michi
    leg_L()
    leg_R()
    head()
    skirt()
    shirt()


def head():
    # Hair
    glColor3ub(160, 82, 45)
    glBegin(GL_POLYGON)
    glVertex2f(0.381 + pos_x, 0.905 + pos_y)
    glVertex2f(0.393 + pos_x, 0.929 + pos_y)
    glVertex2f(0.409 + pos_x, 0.950 + pos_y)
    glVertex2f(0.427 + pos_x, 0.967 + pos_y)
    glVertex2f(0.448 + pos_x, 0.982 + pos_y)
    glVertex2f(0.470 + pos_x, 0.991 + pos_y)
    glVertex2f(0.492 + pos_x, 0.997 + pos_y)
    glVertex2f(0.512 + pos_x, 0.999 + pos_y)
    glVertex2f(0.536 + pos_x, 0.998 + pos_y)
    glVertex2f(0.559 + pos_x, 0.994 + pos_y)
    glVertex2f(0.578 + pos_x, 0.987 + pos_y)
    glVertex2f(0.597 + pos_x, 0.977 + pos_y)
    glVertex2f(0.614 + pos_x, 0.964 + pos_y)
    glVertex2f(0.629 + pos_x, 0.949 + pos_y)
    glVertex2f(0.642 + pos_x, 0.935 + pos_y)
    glVertex2f(0.650 + pos_x, 0.917 + pos_y)
    glVertex2f(0.657 + pos_x, 0.901 + pos_y)
    glVertex2f(0.662 + pos_x, 0.882 + pos_y)
    glVertex2f(0.683 + pos_x, 0.697 + pos_y)
    glVertex2f(0.506 + pos_x, 0.679 + pos_y)
    glVertex2f(0.380 + pos_x, 0.692 + pos_y)
    glVertex2f(0.382 + pos_x, 0.728 + pos_y)
    glVertex2f(0.364 + pos_x, 0.694 + pos_y)
    glVertex2f(0.338 + pos_x, 0.688 + pos_y)
    glVertex2f(0.374 + pos_x, 0.877 + pos_y)
    glEnd()

    # Neck
    glColor3ub(255, 229, 180)
    glBegin(GL_QUADS)
    glVertex2f(0.493 + pos_x, 0.681 + pos_y)
    glVertex2f(0.537 + pos_x, 0.678 + pos_y)
    glVertex2f(0.540 + pos_x, 0.760 + pos_y)
    glVertex2f(0.496 + pos_x, 0.760 + pos_y)
    glEnd()

    # Base Face
    glBegin(GL_POLYGON)
    glVertex2f(0.482 + pos_x, 0.748 + pos_y)
    glVertex2f(0.468 + pos_x, 0.753 + pos_y)
    glVertex2f(0.455 + pos_x, 0.759 + pos_y)
    glVertex2f(0.443 + pos_x, 0.767 + pos_y)
    glVertex2f(0.432 + pos_x, 0.777 + pos_y)
    glVertex2f(0.423 + pos_x, 0.788 + pos_y)
    glVertex2f(0.417 + pos_x, 0.798 + pos_y)
    glVertex2f(0.412 + pos_x, 0.807 + pos_y)
    glVertex2f(0.407 + pos_x, 0.819 + pos_y)
    glVertex2f(0.404 + pos_x, 0.834 + pos_y)
    glVertex2f(0.402 + pos_x, 0.847 + pos_y)
    glVertex2f(0.403 + pos_x, 0.860 + pos_y)
    glVertex2f(0.405 + pos_x, 0.873 + pos_y)
    glVertex2f(0.408 + pos_x, 0.885 + pos_y)
    glVertex2f(0.412 + pos_x, 0.896 + pos_y)
    glVertex2f(0.454 + pos_x, 0.904 + pos_y)
    glVertex2f(0.464 + pos_x, 0.939 + pos_y)
    glVertex2f(0.463 + pos_x, 0.903 + pos_y)
    glVertex2f(0.464 + pos_x, 0.939 + pos_y)
    glVertex2f(0.475 + pos_x, 0.899 + pos_y)
    glVertex2f(0.554 + pos_x, 0.899 + pos_y)
    glVertex2f(0.546 + pos_x, 0.932 + pos_y)
    glVertex2f(0.560 + pos_x, 0.900 + pos_y)
    glVertex2f(0.608 + pos_x, 0.884 + pos_y)
    glVertex2f(0.611 + pos_x, 0.872 + pos_y)
    glVertex2f(0.613 + pos_x, 0.861 + pos_y)
    glVertex2f(0.613 + pos_x, 0.852 + pos_y)
    glVertex2f(0.613 + pos_x, 0.842 + pos_y)
    glVertex2f(0.611 + pos_x, 0.830 + pos_y)
    glVertex2f(0.608 + pos_x, 0.818 + pos_y)
    glVertex2f(0.603 + pos_x, 0.806 + pos_y)
    glVertex2f(0.598 + pos_x, 0.797 + pos_y)
    glVertex2f(0.592 + pos_x, 0.788 + pos_y)
    glVertex2f(0.586 + pos_x, 0.780 + pos_y)
    glVertex2f(0.578 + pos_x, 0.772 + pos_y)
    glVertex2f(0.569 + pos_x, 0.765 + pos_y)
    glVertex2f(0.560 + pos_x, 0.759 + pos_y)
    glVertex2f(0.549 + pos_x, 0.754 + pos_y)
    glVertex2f(0.539 + pos_x, 0.749 + pos_y)
    glVertex2f(0.527 + pos_x, 0.747 + pos_y)
    glVertex2f(0.510 + pos_x, 0.745 + pos_y)
    glEnd()

    # Mouth
    glColor3ub(255, 255, 255)
    glBegin(GL_POLYGON)
    glVertex2f(0.473 + pos_x, 0.795 + pos_y)
    glVertex2f(0.484 + pos_x, 0.790 + pos_y)
    glVertex2f(0.498 + pos_x, 0.787 + pos_y)
    glVertex2f(0.511 + pos_x, 0.786 + pos_y)
    glVertex2f(0.528 + pos_x, 0.788 + pos_y)
    glVertex2f(0.525 + pos_x, 0.778 + pos_y)
    glVertex2f(0.518 + pos_x, 0.770 + pos_y)
    glVertex2f(0.506 + pos_x, 0.764 + pos_y)
    glVertex2f(0.495 + pos_x, 0.764 + pos_y)
    glVertex2f(0.485 + pos_x, 0.768 + pos_y)
    glVertex2f(0.478 + pos_x, 0.775 + pos_y)
    glVertex2f(0.473 + pos_x, 0.784 + pos_y)
    glEnd()

    # Nose
    glColor3ub(235, 209, 160)
    glBegin(GL_POLYGON)
    glVertex2f(0.496 + pos_x, 0.826 + pos_y)
    glVertex2f(0.503 + pos_x, 0.809 + pos_y)
    glVertex2f(0.498 + pos_x, 0.810 + pos_y)
    glVertex2f(0.493 + pos_x, 0.815 + pos_y)
    glVertex2f(0.493 + pos_x, 0.821 + pos_y)
    glEnd()

    # Outer Eye R
    glColor3ub(255, 255, 255)
    glBegin(GL_POLYGON)
    glVertex2f(0.520 + pos_x, 0.840 + pos_y)
    glVertex2f(0.522 + pos_x, 0.848 + pos_y)
    glVertex2f(0.527 + pos_x, 0.854 + pos_y)
    glVertex2f(0.534 + pos_x, 0.859 + pos_y)
    glVertex2f(0.542 + pos_x, 0.861 + pos_y)
    glVertex2f(0.550 + pos_x, 0.861 + pos_y)
    glVertex2f(0.557 + pos_x, 0.859 + pos_y)
    glVertex2f(0.563 + pos_x, 0.854 + pos_y)
    glVertex2f(0.567 + pos_x, 0.849 + pos_y)
    glVertex2f(0.570 + pos_x, 0.842 + pos_y)
    glVertex2f(0.570 + pos_x, 0.832 + pos_y)
    glVertex2f(0.565 + pos_x, 0.828 + pos_y)
    glVertex2f(0.558 + pos_x, 0.825 + pos_y)
    glVertex2f(0.550 + pos_x, 0.823 + pos_y)
    glVertex2f(0.542 + pos_x, 0.824 + pos_y)
    glVertex2f(0.534 + pos_x, 0.826 + pos_y)
    glVertex2f(0.528 + pos_x, 0.830 + pos_y)
    glVertex2f(0.523 + pos_x, 0.834 + pos_y)
    glEnd()

    # Outer Eye L
    glBegin(GL_POLYGON)
    glVertex2f(0.426 + pos_x, 0.843 + pos_y)
    glVertex2f(0.426 + pos_x, 0.848 + pos_y)
    glVertex2f(0.428 + pos_x, 0.851 + pos_y)
    glVertex2f(0.429 + pos_x, 0.855 + pos_y)
    glVertex2f(0.432 + pos_x, 0.858 + pos_y)
    glVertex2f(0.435 + pos_x, 0.861 + pos_y)
    glVertex2f(0.438 + pos_x, 0.863 + pos_y)
    glVertex2f(0.442 + pos_x, 0.865 + pos_y)
    glVertex2f(0.447 + pos_x, 0.866 + pos_y)
    glVertex2f(0.451 + pos_x, 0.865 + pos_y)
    glVertex2f(0.455 + pos_x, 0.864 + pos_y)
    glVertex2f(0.459 + pos_x, 0.863 + pos_y)
    glVertex2f(0.462 + pos_x, 0.861 + pos_y)
    glVertex2f(0.464 + pos_x, 0.858 + pos_y)
    glVertex2f(0.467 + pos_x, 0.855 + pos_y)
    glVertex2f(0.468 + pos_x, 0.852 + pos_y)
    glVertex2f(0.470 + pos_x, 0.848 + pos_y)
    glVertex2f(0.468 + pos_x, 0.845 + pos_y)
    glVertex2f(0.467 + pos_x, 0.841 + pos_y)
    glVertex2f(0.465 + pos_x, 0.838 + pos_y)
    glVertex2f(0.462 + pos_x, 0.835 + pos_y)
    glVertex2f(0.459 + pos_x, 0.833 + pos_y)
    glVertex2f(0.456 + pos_x, 0.832 + pos_y)
    glVertex2f(0.453 + pos_x, 0.830 + pos_y)
    glVertex2f(0.448 + pos_x, 0.829 + pos_y)
    glVertex2f(0.444 + pos_x, 0.829 + pos_y)
    glVertex2f(0.439 + pos_x, 0.830 + pos_y)
    glVertex2f(0.435 + pos_x, 0.832 + pos_y)
    glVertex2f(0.431 + pos_x, 0.835 + pos_y)
    glVertex2f(0.428 + pos_x, 0.837 + pos_y)
    glEnd()

    # Inner Eye R
    glColor3ub(0, 0, 0)
    glBegin(GL_POLYGON)
    glVertex2f(0.535 + pos_x, 0.850 + pos_y)
    glVertex2f(0.540 + pos_x, 0.855 + pos_y)
    glVertex2f(0.546 + pos_x, 0.857 + pos_y)
    glVertex2f(0.550 + pos_x, 0.854 + pos_y)
    glVertex2f(0.553 + pos_x, 0.848 + pos_y)
    glVertex2f(0.553 + pos_x, 0.842 + pos_y)
    glVertex2f(0.552 + pos_x, 0.836 + pos_y)
    glVertex2f(0.548 + pos_x, 0.831 + pos_y)
    glVertex2f(0.541 + pos_x, 0.828 + pos_y)
    glVertex2f(0.536 + pos_x, 0.831 + pos_y)
    glVertex2f(0.534 + pos_x, 0.837 + pos_y)
    glVertex2f(0.533 + pos_x, 0.844 + pos_y)
    glEnd()

    # Inner Eye L
    glBegin(GL_POLYGON)
    glVertex2f(0.434 + pos_x, 0.842 + pos_y)
    glVertex2f(0.434 + pos_x, 0.846 + pos_y)
    glVertex2f(0.435 + pos_x, 0.851 + pos_y)
    glVertex2f(0.436 + pos_x, 0.855 + pos_y)
    glVertex2f(0.439 + pos_x, 0.859 + pos_y)
    glVertex2f(0.443 + pos_x, 0.861 + pos_y)
    glVertex2f(0.447 + pos_x, 0.861 + pos_y)
    glVertex2f(0.451 + pos_x, 0.860 + pos_y)
    glVertex2f(0.454 + pos_x, 0.856 + pos_y)
    glVertex2f(0.456 + pos_x, 0.853 + pos_y)
    glVertex2f(0.457 + pos_x, 0.849 + pos_y)
    glVertex2f(0.457 + pos_x, 0.844 + pos_y)
    glVertex2f(0.456 + pos_x, 0.840 + pos_y)
    glVertex2f(0.454 + pos_x, 0.835 + pos_y)
    glVertex2f(0.452 + pos_x, 0.832 + pos_y)
    glVertex2f(0.448 + pos_x, 0.830 + pos_y)
    glVertex2f(0.444 + pos_x, 0.830 + pos_y)
    glVertex2f(0.440 + pos_x, 0.832 + pos_y)
    glVertex2f(0.437 + pos_x, 0.835 + pos_y)
    glVertex2f(0.435 + pos_x, 0.839 + pos_y)
    glEnd()

    # Eyebrow L
    glBegin(GL_QUADS)
    glVertex2f(0.418 + pos_x, 0.876 + pos_y)
    glVertex2f(0.430 + pos_x, 0.881 + pos_y)
    glVertex2f(0.476 + pos_x, 0.886 + pos_y)
    glVertex2f(0.469 + pos_x, 0.881 + pos_y)
    glEnd()

    # Eyebrow R
    glBegin(GL_QUADS)
    glVertex2f(0.521 + pos_x, 0.882 + pos_y)
    glVertex2f(0.522 + pos_x, 0.878 + pos_y)
    glVertex2f(0.572 + pos_x, 0.868 + pos_y)
    glVertex2f(0.568 + pos_x, 0.873 + pos_y)
    glEnd()


def shirt():
    # Base
    glColor3ub(233, 224, 200)
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
    glColor3ub(233, 224, 200)
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
    global texID, clock, info, score, lives, pos_x, pos_y, high, HITAM, PUTIH
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
        'TITLE': TitleScene('LEVEL', 'Mar - Tung', 'M a r i  B e r h i t u n g', '', '',
                            'Tekan                untuk mulai'),
        'LEVEL': LevelScene(),
        'GAME': GameScene(),
        'RESULT': ResultScene('TITLE', 'GAME OVER')
    }
    scene = scenes['TITLE']

    # Game init
    HITAM = (0, 0, 0)
    PUTIH = (255, 255, 255)
    score = Watcher(0, 'score')
    lives = Watcher(3, 'lives')
    pos_x = -0.55
    pos_y = -0.9
    draw = False

    done = False
    while not done:
        # Check high score
        file_r = open('config.txt', 'r')
        name, value = file_r.read().split(' = ')
        name = bytearray.fromhex(name).decode()
        value = int(value, 16)
        if name == 'skor tertinggi':
            high = value

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
