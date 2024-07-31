import pygame
import random

s_width = 1200          # загальна ширина вікна
s_height = 1000         # загальна висота вікна
play_width = 450        # ширина ігрового поля
play_height = 900       # висота ігрового поля
block_size = 30         # розміри одного блоку

top_left_x = (s_width - play_width) // 2    # координата х ігрового поля у вікні
top_left_y = s_height - play_height         # координата у ігрового поля у вікні

# фігури викладені в масиві
s1 = [['*****',
       '*****',
       '**00*',
       '*00**',
       '*****'],
      ['*****',
       '**0**',
       '**00*',
       '***0*',
       '*****']]

s2 = [['*****',
       '*****',
       '*00**',
       '**00*',
       '*****'],
      ['*****',
       '**0**',
       '*00**',
       '*0***',
       '*****']]

s3 = [['**0**',
       '**0**',
       '**0**',
       '**0**',
       '*****'],
      ['*****',
       '0000*',
       '*****',
       '*****',
       '*****']]

s4 = [['*****',
       '*****',
       '*00**',
       '*00**',
       '*****']]

s5 = [['*****',
       '*0***',
       '*000*',
       '*****',
       '*****'],
      ['*****',
       '**00*',
       '**0**',
       '**0**',
       '*****'],
      ['*****',
       '*****',
       '*000*',
       '***0*',
       '*****'],
      ['*****',
       '**0**',
       '**0**',
       '*00**',
       '*****']]

s6 = [['*****',
       '***0*',
       '*000*',
       '*****',
       '*****'],
      ['*****',
       '**0**',
       '**0**',
       '**00*',
       '*****'],
      ['*****',
       '*****',
       '*000*',
       '*0***',
       '*****'],
      ['*****',
       '*00**',
       '**0**',
       '**0**',
       '*****']]

s7 = [['*****',
       '**0**',
       '*000*',
       '*****',
       '*****'],
      ['*****',
       '**0**',
       '**00*',
       '**0**',
       '*****'],
      ['*****',
       '*****',
       '*000*',
       '**0**',
       '*****'],
      ['*****',
       '**0**',
       '*00**',
       '**0**',
       '*****']]

shapes = [s1, s2, s3, s4, s5, s6, s7]  # список фігур
shape_colors = [                       # список кольорів
    (0, 255, 0),    # green
    (255, 0, 0),    # red
    (0, 255, 255),  # cyan
    (255, 255, 0),  # yellow
    (255, 165, 0),  # orange
    (0, 0, 255),    # blue
    (128, 0, 128)   # patriarch
]

pygame.font.init()  # ініціалізація модуля шрифта


# фукнція для створення шрифта за розміром, для налагодження шрифта за замовчуванням
def get_font(size):
    # size - розмір шрифта
    return pygame.font.Font("font.ttf", size)


# Клас, що описує фігуру
class Figure(object):
    def __init__(self, x, y, shape):
        self.x = x                                      # координата x
        self.y = y                                      # координата y
        self.shape = shape                              # форма фігури
        self.color = shape_colors[shapes.index(shape)]  # колір фігури, береться за номером фігури зі списку
        self.rotation = 0                               # початковий поворот


# фукція генерації наступної фігури
def get_figure():
    return Figure(7, 0, random.choice(shapes))


# Клас для кнопки
class Button(object):
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

    # функция малювання кнопки меню
    def update(self, win):
        if self.image is not None:
            win.blit(self.image, self.rect)
        win.blit(self.text, self.text_rect)

    # функция перевірки чи знаходится 'position' в межах кнопки
    def check_for_input(self, position):
        # position - координата (x, y) миші, що перевіряється
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    # функция зміни кольору коли 'position' в межах кнопки
    def change_color(self, position):
        # position - координата (x, y) миші, що перевіряється
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


# функция для створення ігрового поля
def create_grid(locked_pos={}):
    # locked_pos - контейнер із фігурами (або залишками) що впали
    grid = []
    # цикл початкого заповнення ігрового поля чорним кольором, який використовується як пустий блок
    for j in range(30):
        line = []
        for i in range(15):
            line.append((0, 0, 0))
        grid.append(line)
    # цикл заповнення ігрового поля фиксованими фігурами (та/або залишками)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


# функция для трансофрмації фігури в список координат
def convert_figure_format(figure):
    # figure - об'єкт класу фігури
    positions = []
    # вибираємо форму фігури згідно повороту та даної форми
    format = figure.shape[figure.rotation % len(figure.shape)]

    # збираємо координати фігури с її форми
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((figure.x + j, figure.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


# функция для перевірки чи валідна фігура на ігровому полі (чи не перетинається із зафіксованими (залишками) фігурами)
def is_valid(figure, grid):
    # figure - об'єкт класу фігури
    # grid - ігрове поле
    accepted_pos = []
    # збираємо допустимі координати для фігури
    for j in range(15):
        for i in range(30):
            if grid[i][j] == (0, 0, 0):
                accepted_pos.append((j, i))
    formatted = convert_figure_format(figure)

    # перевіряємо, чи всі координати фігур знаходяться на допустимих позиціях
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


# функция для перевірки чи ігрок програв
def is_lost(positions):
    for _, y in positions:
        if y < 1:
            return True

    return False


# функция для відмальовки тексту посередині
def draw_text_middle(win, text, size, color):
    # win - об'єкт вікна
    # text - текст що потрібно намалювати
    # size - розмір шрифта
    # color - колір тексту
    font = get_font(size)
    label = font.render(text, 1, color)

    win.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))


# функция для відмальовки сітки ігрового поля
def draw_grid(win, grid):
    # win - об'єкт вікна
    # grid - ігрове поле
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(win, (128, 128, 128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(win, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))


# функция для видалення повністю заповнених ліній
def clear_rows(grid, locked):
    # grid - ігрове поле
    # locked - список координат в яких залишки фігур
    inc = 0
    # проходимо по лініях та видаляємо позиції із залишками фігур
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                del locked[(j, i)]

    # проходимо та змінюємо координати фігур (залишки фугір) що залишились після видалення заповнених ліній
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


# функция для малювання наступної фігури, на панелі праворуч
def draw_next_figure(figure, win):
    # figure - об'єкт фігури яка буде наступна
    # win - об'єкт вікна
    font = get_font(20)
    label = font.render('Next Figure', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    # беремо форму наступної фігури згідно
    format = figure.shape[figure.rotation % len(figure.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(win, figure.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    win.blit(label, (sx + 10, sy - 30))


# функция для запису пойнтів у файл
def update_score(nscore):
    # nscore - кількість, яку потрібно записати
    score = max_score()
    if int(score) < nscore:
        with open('scores.txt', 'w') as f:
            f.write(str(nscore))


# функция для зчитування пойнтів із файлу
def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
        return score

    return 0


# функция для малювання ігрового поля, назви та кількості пойнтів
def draw_window(win, grid, score=0, last_score=0):
    # win - об'єкт вікна
    # grid - ігрове поле
    # score - кількість пойнтів ігрока
    # last_score - максимальна кількість пойнтів що була набрана
    win.fill((0, 0, 0))

    pygame.font.init()
    font = get_font(50)
    label = font.render('Tetris', 1, (255, 255, 255))

    win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # current score
    font = get_font(20)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    win.blit(label, (sx + 20, sy + 160))
    # last score
    label = font.render('High Score: ' + last_score, 1, (255, 255, 255))

    sx = top_left_x - 350
    sy = top_left_y + 200

    win.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(win, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(win, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(win, grid)


# функция для малювання тексту
def blit_text(win, text, pos, font, color):
    # win - об'єкт вікна
    # text - текст що потрібно намалювати
    # pos - координати, де потрібно намалювати текст
    # font - шрифт для малювання
    # color - колір тексту

    # розбиваємо текст на слова
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = win.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            win.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


# функция для малювання меню
def settings_menu(win):
    # win - об'єкт вікна
    run = True
    while run:
        win.fill((80, 80, 80))
        text =  '''Tetris (Russian: Тетрис[a]) is a puzzle video game created in 1985 by Alexey Pajitnov, a Soviet software engineer. It has been published by several companies for multiple platforms, most prominently during a dispute over the appropriation of the rights in the late 1980s. After a significant period of publication by Nintendo, in 1996 the rights reverted to Pajitnov, who co-founded the Tetris Company with Henk Rogers to manage licensing.
        In Tetris, players complete lines by moving differently shaped pieces (tetrominoes), which descend onto the playing field. The completed lines disappear and grant the player points, and the player can proceed to fill the vacated spaces. The game ends when the uncleared lines reach the top of the playing field. The longer the player can delay this outcome, the higher their score will be. In Multiplayer games, players must last longer than their opponents; in certain versions, players can inflict penalties on opponents by completing a significant number of lines. Some versions add variations on the rules, such as three-dimensional displays or a system for reserving pieces.'''
        blit_text(win, text, (70, 150), get_font(20), (255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        pygame.display.update()


# функция для малювання ігри
def main(win):
    # win - об'єкт вікна
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_figure = False
    run = True
    current_figure = get_figure()
    next_figure = get_figure()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.35
    level_time = 0
    score = 0

    while run:
        # будуємо ігрове поле
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_figure.y += 1
            if not (is_valid(current_figure, grid)) and current_figure.y > 0:
                current_figure.y -= 1
                change_figure = True

        # перевіряємо доступні івенти
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(win)

                if event.key == pygame.K_LEFT:
                    current_figure.x -= 1
                    if not (is_valid(current_figure, grid)):
                        current_figure.x += 1
                if event.key == pygame.K_RIGHT:
                    current_figure.x += 1
                    if not (is_valid(current_figure, grid)):
                        current_figure.x -= 1
                if event.key == pygame.K_DOWN:
                    current_figure.y += 1
                    if not (is_valid(current_figure, grid)):
                        current_figure.y -= 1
                if event.key == pygame.K_UP:
                    current_figure.rotation += 1
                    if not (is_valid(current_figure, grid)):
                        current_figure.rotation -= 1

        figure_pos = convert_figure_format(current_figure)

        # заповнюємо ігрове поле коліром фігури в її координатах
        for i in range(len(figure_pos)):
            x, y = figure_pos[i]
            if y > -1:
                grid[y][x] = current_figure.color
        # якщо фігура зафіксована, добавляємо в контейнер кольори цієї фігури
        if change_figure:
            for pos in figure_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_figure.color
            # беремо наступну фігуру
            current_figure = next_figure
            # створюємо фігуру для наступного кроку
            next_figure = get_figure()
            change_figure = False
            # відаляємо заповнені фігури та рахуємо пойнти
            points = clear_rows(grid, locked_positions)
            # граємо звук
            if (points != 0):
                pygame.mixer.music.load('line.wav')
                pygame.mixer.music.play()
            score += points * 10

        draw_window(win, grid, score, last_score)
        draw_next_figure(next_figure, win)
        pygame.display.update()

        # GAME OVER
        if is_lost(locked_positions):
            pygame.mixer.music.load('game_over.wav')
            pygame.mixer.music.play()
            draw_text_middle(win, "GAME OVER!", 80, (255, 0, 0))
            pygame.display.update()
            pygame.time.delay(2500)
            run = False
            update_score(score)


# функция для малювання головного меню
def main_menu(win):
    # win - об'єкт вікна
    run = True
    while run:
        win.fill((50, 50, 50))

        menu_mouse_pos = pygame.mouse.get_pos()
        font = get_font(100)
        menu_text = font.render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(s_width / 2, 100))

        btn_font = get_font(75)

        play_button = Button(image=pygame.image.load("btn.svg"),
                             pos=(s_width / 2, 300),
                             text_input="PLAY",
                             font=btn_font,
                             base_color=(255, 87, 51),
                             hovering_color=(200, 200, 200))
        options_button = Button(image=pygame.image.load("btn.svg"),
                                pos=(s_width / 2, 500),
                                text_input="OPTIONS",
                                font=btn_font,
                                base_color=(255, 87, 51),
                                hovering_color=(200, 200, 200))
        quit_button = Button(image=pygame.image.load("btn.svg"),
                             pos=(s_width / 2, 700),
                             text_input="QUIT",
                             font=btn_font,
                             base_color=(255, 87, 51),
                             hovering_color=(200, 200, 200))

        win.blit(menu_text, menu_rect)

        # перевіряємо чи потрібно змінити колір кнопки над якою миша
        for button in [play_button, options_button, quit_button]:
            button.change_color(menu_mouse_pos)
            button.update(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    main(win)

                if options_button.check_for_input(menu_mouse_pos):
                    settings_menu(win)

                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()

        pygame.display.update()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
pygame.mixer.init()
main_menu(win)
# pygame.display.quit()
pygame.quit()
