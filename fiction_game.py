import pyxel
import random
import string
import time
import math
import json
from letter import Letter
from vector import Vector2

VERSION = 'v 0.0.1'
screen_width = 240
screen_hight = 135
FPS_LIMIT = 60
FPS_ACTUAL = FPS_LIMIT

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16
PLAYER_SPEED = 3 * 30 / FPS_ACTUAL      # adjust speed according to fps
PLAYER_X = 0
PLAYER_Y = 0

BULLET_WIDTH = 4
BULLET_HEIGHT = 2

ENEMY_WIDTH = 16
ENEMY_HEIGHT = 16
ENEMY_SPEED = 3 * 30 / FPS_ACTUAL


MUSIC_ON = True

enemy_list = []
bullet_list = []
blast_list = []
enemy_bullet_list = []


def update_list(lst):
    for elem in lst:
        elem.update()


def draw_list(lst):
    for elem in lst:
        elem.draw()


def cleanup_list(lst):
    i = 0
    while i < len(lst):
        elem = lst[i]
        if not elem.alive:
            lst.pop(i)
        else:
            i += 1


class FPS:
    def __init__(self):
        self.start_time = time.time()
        self.frame_counter = 0
        self.fps = FPS_LIMIT

    def update_fps(self):
        """
        Calculate the actual frame per second rate.
        :return: float: fps
        """
        self.frame_counter += 1
        divider = (time.time()-self.start_time)
        if divider > 0:
            self.fps = int(self.frame_counter / divider)
        global FPS_ACTUAL
        FPS_ACTUAL = self.fps
        if (time.time()-self.start_time) > 1:
            self.frame_counter = 0
            self.start_time = time.time()

    def get_fps(self):
        return self.fps


class Scrolltext:

    def __init__(self):
        self.scrolltext = "This is my first prototype / work in progress space shooter game!!! " \
                          "It will take some time to be ready :-)"
        self.scrolltext_pixel_length = len(self.scrolltext)*4
        self.x = 160
        self.y = 88
        self.y_start = 88
        self.y_end = screen_hight - 24
        self.y_acceleration = 1.2   # 36 / FPS_ACTUAL # default: 1.2
        self.y_speed = 1
        self.y_direction_down = True
        self.border_color = 6
        self.stripe_x = 0
        self.stripe_sections = 16   # 8 or 16
        self.border_color = 1
        self.textcolors = [1, 5, 12, 6, 7, 6, 12, 5]
        self.textcolornr = self.textcolors[0]

    def update(self):

        # change x position
        if self.x > (0 - self.scrolltext_pixel_length):
            self.x -= 30 / FPS_ACTUAL
        else:
            self.x = screen_width

        divider = round(FPS_ACTUAL/30)
        if divider > 0:
            if pyxel.frame_count % divider == 0:
                # change x position
                # moving down
                if self.y < self.y_end and self.y_direction_down:
                    self.y_speed *= self.y_acceleration
                    self.y += self.y_speed
                    if self.y > self.y_end:
                        self.y = self.y_end
                # moving up
                elif self.y > self.y_start and not self.y_direction_down:
                    if self.y_speed > 1:
                        self.y_speed /= self.y_acceleration
                    self.y -= self.y_speed
                    if self.y < self.y_start:
                        self.y = self.y_start
                        self.y_speed = 1
                else:
                    self.y_direction_down = not self.y_direction_down

                # textcolor / flashing text
                if self.textcolornr < len(self.textcolors) - 1:
                    self.textcolornr = round(self.textcolornr + 0.2, 1)
                else:
                    self.textcolornr = 0

    def draw(self):
        # draw lines rectangle & scrolling text
        pyxel.rect(0, self.y - 6, screen_width, 17, 0)
        pyxel.line(0, self.y - 4, screen_width, self.y - 4, 2)
        pyxel.line(0, self.y + 8, screen_width, self.y + 8, 2)
        # jumping and scrolling text
        pyxel.text(self.x, self.y, self.scrolltext, self.textcolors[int(self.textcolornr)])
        # draw scrolling stripe lines
        for line_y in [-4, 8]:
            for i in range(0, int((screen_width / self.stripe_sections) - 1)):
                pyxel.line(int(2 * i * screen_width / self.stripe_sections + self.stripe_x),
                           self.y + line_y,
                           int((2 * i * screen_width / self.stripe_sections) +
                               screen_width / self.stripe_sections - 1 + self.stripe_x),
                           self.y + line_y, 4)
            if self.stripe_x < (screen_width / self.stripe_sections):
                self.stripe_x += 30 / FPS_ACTUAL
            else:
                self.stripe_x = - screen_width / self.stripe_sections
            self.stripe_sections = 16   # 8 or 16


class Background:
    def __init__(self):
        self.star_list = []
        self.starcount = 80
        self.star_color_high = 7
        self.star_color_low = 13
        for i in range(self.starcount):
            self.star_list.append(
                (random.random() * pyxel.width, random.random() * pyxel.height, random.random() * 1.5 + 1)
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.star_list):
            if FPS_ACTUAL != 0:
                x -= (speed * 30 / FPS_ACTUAL)
            if x <= 0:
                x += pyxel.width
            self.star_list[i] = (x, y, speed)

    def draw(self):
        for (x, y, speed) in self.star_list:
            pyxel.pset(x, y, self.star_color_high if speed > 1.8 else self.star_color_low)


class Lettering:
    def __init__(self, y_start, word='K-O.MAZI3', animation=True):
        self.word = word
        self.letter_positions_x = []
        self.letter_positions_y = []
        self.letter_img_positions = {'.': (160, 32), '-': (176, 32), ' ': (192, 32)}
        self.animation = animation
        for i, j in enumerate(string.ascii_uppercase):  # Add letter positions in resource image
            if i < 16:
                x = i*16
                y = 16
            else:
                x = i*16 - 256
                y = 32
            self.letter_img_positions[j] = (x, y)
        for i in range(10):     # Add number positions in resource image
            self.letter_img_positions[str(i)] = (i*16, 48)

        self.letter_y_start = y_start
        self.letter_y_range = 8

        self.letter_positions_y = [(num + self.letter_y_start) for num in range(0, self.letter_y_range + 1)] + \
                                  [(num + self.letter_y_start) for num in range(self.letter_y_range - 1, 0, -1)]
        self.letter_frame_count = 0
        self.letters_left_span = (screen_width - (len(self.word) * 16)) / 2

    def update(self):
        # cycle through y positions
        divider = round(FPS_ACTUAL/15)
        if divider > 0:
            if pyxel.frame_count % divider == 0:
                self.letter_positions_y.append(self.letter_positions_y[0])
                self.letter_positions_y.pop(0)

    def draw(self):
        for i, l in enumerate(self.word):
            if self.animation:
                y = self.letter_positions_y[i]
            else:
                y = self.letter_y_start

            pyxel.blt(
                int(self.letters_left_span + (i * 16)),
                y,
                0,
                self.letter_img_positions[l][0],
                self.letter_img_positions[l][1],
                16,
                16,
                0)


class Player:
    def __init__(self, x: int, y: int, mirrored_horizontal=False):
        self.map_pos = [0, 16, 32, 48, 64, 48, 32, 16]
        self.map_nr = 0
        self.w = 16
        self.h = 16
        self.x = x
        self.y = y
        if mirrored_horizontal:
            self.w *= -1
        self.laser_wait_count = 0
        self.shield = 100
        self.shoot_button_released = True
        self.alive = True

    def update(self, scene=None):
        global PLAYER_X
        global PLAYER_Y

        if scene == SCENE_TITLE:
            # Spaceship animation
            divider = round(FPS_ACTUAL/7.5)
            if divider > 0:
                if pyxel.frame_count % divider == 0:
                    self.map_nr += 1
                    if self.map_nr in [6, 7] and self.h > 0:
                        self.h *= -1    # mirror vertical
                    elif self.map_nr not in [6, 7] and self.h < 0:
                        self.h *= -1    # mirror vertical

            if self.map_nr == len(self.map_pos):
                self.map_nr = 0

        if scene == SCENE_PLAY and self.alive:
            if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
                if self.y > 10:
                    self.y -= PLAYER_SPEED
                self.map_nr = 1
            elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
                if self.y < (screen_hight - 16):  # todo: CHANGE 16 as var but be careful if it's negative sometimes
                    self.y += PLAYER_SPEED
                self.map_nr = 1
                if self.h > 0:
                    self.h *= -1    # mirror vertical
            else:
                self.map_nr = 0
                if self.h < 0:
                    self.h *= -1    # reset mirror vertical
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
                if self.x > PLAYER_WIDTH/4:
                    self.x -= PLAYER_SPEED
            elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
                if self.x < screen_width - PLAYER_WIDTH - PLAYER_WIDTH/4:
                    self.x += PLAYER_SPEED
            else:
                if self.x > PLAYER_WIDTH/4:
                    self.x -= 1 * (30/FPS_ACTUAL)
            if pyxel.btn(pyxel.KEY_CTRL) and self.shoot_button_released:
                if self.laser_wait_count <= 0:
                    Bullet(self.x + PLAYER_WIDTH - BULLET_WIDTH, int(self.y + PLAYER_HEIGHT/2 - 1))
                    self.laser_wait_count = 8
                    self.shoot_button_released = False
            elif pyxel.btnr(pyxel.KEY_CTRL):
                self.shoot_button_released = True
            self.laser_wait_count -= 1

        # Update global variables, so that other object can locate player
        PLAYER_X = self.x
        PLAYER_Y = self.y

    def draw(self):
        # draw Spaceship
        if self.alive:
            pyxel.blt(self.x, self.y, 0, self.map_pos[self.map_nr], 0, self.w, self.h, 0)


class ShipBlast:
    def __init__(self, x, y, model='player'):
        self.x = x
        self.y = y
        self.alive = True
        pyxel.play(3, 21)
        self.animation_sprite_quantity = 11     # sprites in a row
        if model == 'player':
            self.map_pos = [80-16, 0]  # 96, 112, 128, 144, 160, 176, 192, 208, 224, 240
        if model == 'enemy':
            self.map_pos = [80-16, 80]

    def update(self):
        if self.map_pos[0] <= 240:
            self.map_pos[0] += 16
        else:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.map_pos[0], self.map_pos[1], 16, 16, 0)


class Bullet:
    def __init__(self, x: int, y: int, col=10, bullet_speed=3):
        self.x = x
        self.y = y
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.color = col
        self.alive = True
        self.bullet_speed = bullet_speed * 30 / FPS_ACTUAL

        bullet_list.append(self)
        pyxel.play(3, 20)

    def update(self):
        self.x += self.bullet_speed
        if self.x + self.w > screen_width:
            self.alive = False

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, self.color)


class Enemy:

    animation_list = list(range(0, 6))

    def __init__(self, x, y, animation=0, variant=0, bullet_variant=0, bullet_aimed=0):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.map_pos = [0, 16, 32, 48]
        self.animation = animation
        self.variant = variant
        self.dir = 1
        self.alive = True
        self.offset = int(random.random() * 60)
        self.out_of_ammu = False
        # 'animation as object'
        self.flight_animation = EnemyFlightAnimation(self, animation, bullet_variant, bullet_aimed)


        enemy_list.append(self)

        image_map_y_pos_list = [80, 96, 112, 128, 144, 160, 176]
        self.image_map_y_pos = image_map_y_pos_list[self.variant]

    def update(self, animation=0, shooting=0):
        # No up and down
        if 1 == 2:
            if (pyxel.frame_count + self.offset) % 60 < 30:
                if self.y < (screen_hight - ENEMY_HEIGHT):
                    self.y += ENEMY_SPEED
                    self.dir = 1
            elif self.y > 8:
                self.y -= ENEMY_SPEED
            else:
                self.dir = -1

        self.flight_animation.update()

        # cycle through sprite list
        divider = round(FPS_ACTUAL/7.5)
        if divider > 0:
            if pyxel.frame_count % divider == 0:
                self.map_pos.append(self.map_pos[0])
                self.map_pos.pop(0)

        if self.x < 0 - ENEMY_WIDTH - 1:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.map_pos[0], self.image_map_y_pos, self.w, self.h, 0)


class EnemyFlightAnimation:

    variant_names = ['flying straight', 'flying up and down', 'enemy with extra speed',
                     'with extra speed toward player', 'flying and shooting straight', 'flying in circle',
                     'swinging']

    def __init__(self, enemy_obj, variant=0, bullet_variant=0, bullet_aimed=0):
        self.enemy = enemy_obj
        self.variant = variant
        # for flying circles
        self.circle_step_sum = 0
        self.radius = 50
        self.flying_circle_started = False
        self.bullet_variant = bullet_variant
        self.bullet_aimed = bullet_aimed
        self.swing_span = 6
        self.swing_y_start = self.enemy.y

    def update(self):

        if self.variant == 0:    # flying straight
            self.enemy.x -= ENEMY_SPEED

        if self.variant == 1:     # flying up and down
            self.enemy.x -= ENEMY_SPEED
            if self.enemy.x < (screen_width - screen_width / 6):
                if self.enemy.y < (screen_hight - self.enemy.h) and self.enemy.dir == 1:
                    self.enemy.y += ENEMY_SPEED
                elif self.enemy.y > 9 and self.enemy.dir == -1:
                    self.enemy.y -= ENEMY_SPEED
                else:
                    self.enemy.dir *= -1

        if self.variant == 2:     # enemy with extra speed
            self.enemy.x -= ENEMY_SPEED * 1.2

        if self.variant == 3:     # with extra speed toward player
            self.enemy.x -= ENEMY_SPEED * 1.2

            if self.enemy.x > PLAYER_X:
                y_factor = Vector2.y_target_factor([self.enemy.x, self.enemy.y], [PLAYER_X, PLAYER_Y])
                if y_factor > 3:
                    y_factor = 3
                elif y_factor < -3:
                    y_factor = -3
                y_factor = y_factor * 30 / FPS_ACTUAL
                self.enemy.y -= y_factor

        if self.variant == 4:     # flying and shooting straight
            self.enemy.x -= ENEMY_SPEED
            if self.enemy.x < (screen_width - screen_width / 6):
                if self.enemy.x < (screen_width - screen_width / 6) and not self.enemy.out_of_ammu:
                    EnemyBullet(self.enemy.x - BULLET_WIDTH, self.enemy.y + ENEMY_HEIGHT/2 - 1)
                    self.enemy.out_of_ammu = True

        if self.variant == 5:     # flying in circle
            if self.enemy.x > screen_width * 3/4 and not self.flying_circle_started:
                self.enemy.x -= ENEMY_SPEED
                self.enemy.mx = screen_width * 3/4
                self.enemy.my = self.enemy.y + self.radius
            else:
                self.flying_circle_started = True
                offset = math.pi * 1.5
                #step_size = 2 / self.radius
                step_size = 0.1 * 30 / FPS_ACTUAL
                if self.circle_step_sum < 2 * math.pi:
                    self.enemy.x = self.enemy.mx - self.radius * math.cos(self.circle_step_sum+offset)
                    self.enemy.y = self.enemy.my + self.radius * math.sin(self.circle_step_sum+offset)
                    self.enemy.mx -= 0.3
                    #radius -= step_size*4
                    self.circle_step_sum += step_size
                else:
                    self.enemy.x -= ENEMY_SPEED

        if self.variant == 6:     # swinging
            self.enemy.x -= ENEMY_SPEED
            span = pyxel.frame_count % self.swing_span

            if self.enemy.x < screen_width:
                if self.enemy.y < self.swing_y_start + self.swing_span and self.enemy.dir == 1:
                    self.enemy.y += ENEMY_SPEED/4
                elif self.enemy.y > self.swing_y_start - self.swing_span and self.enemy.dir == -1:
                    self.enemy.y -= ENEMY_SPEED/4
                else:
                    self.enemy.dir *= -1


        # shooting
        if self.bullet_variant > 0:
            if self.enemy.x < (screen_width - screen_width / 6):
                if self.enemy.x < (screen_width - screen_width / 6) and not self.enemy.out_of_ammu:
                    EnemyBullet(self.enemy.x - BULLET_WIDTH, self.enemy.y + ENEMY_HEIGHT/2 - 1, 8, 5, self.bullet_variant, self.bullet_aimed)
                    self.enemy.out_of_ammu = True

class EnemyBullet:

    variant_names = ['None', 'straight laser', 'circle laser']

    def __init__(self, x: int, y: int, col=8, bullet_speed=5, variant=1, aimed=False):
        self.x = x
        self.y = y
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.color = col
        self.alive = True
        self.bullet_speed = bullet_speed * 30 / FPS_ACTUAL
        self.variant = variant
        self.aimed = aimed
        self.y_factor = 0     # moving vertically
        self.color_range = [8, 8, 2, 8, 8, 7]

        enemy_bullet_list.append(self)
        pyxel.play(3,20)

    def update(self):
        if self.variant == 1:        # straight laser
            self.x -= self.bullet_speed
            if self.x + self.w > screen_width:
                self.alive = False

        if self.variant == 2:       # circle laser
            self.x -= self.bullet_speed
            #if self.x > PLAYER_X:
            if 1 == 1:
                if self.aimed is False:
                    self.y_factor = Vector2.y_target_factor([self.x, self.y], [PLAYER_X, PLAYER_Y])
                    self.aimed = True
                self.y -= self.y_factor * self.bullet_speed
                self.color_range.append(self.color_range[0])
                self.color_range.pop(0)

    def draw(self):
        if self.variant == 1:
            pyxel.rect(self.x, self.y, self.w, self.h, self.color)

        if self.variant == 2:   #Circle
            pyxel.circ(self.x, self.y, 2, self.color_range[0])


class Formation:
    def __init__(self, no, x, y):
        # formation: 0 = nothing; 1 = ship; 2 = ship with y-movement
        self.formation = [
                ['102000020000000010000010000000000'],
                ['00606060606000000000000606060606'],
                ['00005000000000000011112'],
                ['50000000000003',
                 '00500000',
                 '50000000',
                 '00500020',
                 '50000000',
                 '00500200',
                 '50000000',
                 '00500002',
                 '50000000000004',
                 '00500000',
                 '50000000'],
                ['00000000004',
                 '50000000001',
                 '30000000000',
                 '00000000001',
                 '00000000004'],
                ['00500000100',
                 '00050001000',
                 '00111111100',
                 '01101110110',
                 '41111111111',
                 '50111111101',
                 '10100000101',
                 '00011011000'],
                ['30101010101',
                 '00000000000',
                 '03010101010'],
                ['00100100100',
                 '05001001001',
                 '20020020010',
                 '05001001001',
                 '00100100100']
            ]
        self.x = x
        self.y = y

        for i, row in enumerate(self.formation[no]):
            for j, column in enumerate(row):
                if int(row[j]) > 0:
                    anim = int(row[j]) - 1
                    Enemy(x + (j * (ENEMY_WIDTH + 0)), y + (i * ENEMY_HEIGHT), anim)

class Formation2:
    formation_files = ['formation_1644008576.json', 'formation_1644002913.json', 'formation_1643569683.json', 'formation_0001.json', 'formation_1643570322.json']
    def __init__(self, no, x, y):
        self.x = x
        self.y = y
        self.formation_list = []
        #for file in self.formation_files:
        #    temp_list = []
        if 1 == 1:
            #temp_list = []
            file = Formation2.formation_files[no]
            with open(file) as json_file:
                json_data = json.load(json_file)
                for e in json_data['enemies']:
                    #temp_list.append(e)
                    self.formation_list.append(e)
                #self.formations_list.append(temp_list)

        # [{'x': 81, 'y': 97, 'variant': 0, 'enemy_bullet_variant': 1, 'enemy_bullet_aimed': True, 'enemy_flight_animation': 0}]

        for i, formation in enumerate(self.formation_list):
            #for element_dict in formation:
            Enemy(x + formation['x'],
                  y + formation['y'],
                  formation['enemy_flight_animation'],
                  formation['variant'],
                  formation['enemy_bullet_variant'],
                  formation['enemy_bullet_aimed']
                  )

class App:
    def __init__(self):
        pyxel.init(screen_width, screen_hight, title="Starship1", fps=FPS_LIMIT, capture_sec=30)
        self.high_score = 0
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.score = 0
        self.scene = SCENE_TITLE
        # fps calculation initialisation
        self.fps = FPS()
        pyxel.load("assets/test.pyxres")
        if self.scene == SCENE_TITLE:
            self.Spaceship = Player(24, 20)
            self.Spaceship2 = Player(screen_width-40, 20, True)
            self.background = Background()
            self.scrlltxt = Scrolltext()
            self.lettering = Lettering(16, 'FICTION-X')
            self.letter = Letter()
            # Play music
            if MUSIC_ON:
                pyxel.playm(1, loop=True)
            # wobble text
            self.movement_x = [1, 2, 3, 4, 3, 2, 1, 0, -1, -2, -3, -4, -3, -2, -1, 0]
            self.textlines = ['|5|HI, THIS IS A',
                              '|5|PYXEL SHOOTER IN THE GOOD',
                              '|5|OLD |i|8-BIT STYLE|i| LIKE IT',
                              '|5|IS |1|1985|5| OR SO |2|s |4|h']
            # count and subtract control characters in text lines
            self.control_chars = []
            control_char_count = 0
            for line in self.textlines:
                for c in line:
                    if c == '|':
                        control_char_count += 1
                self.control_chars.append(control_char_count)
                control_char_count = 0

        # todo
        # formations
        self.f_max = len(Formation2.formation_files)
        self.f = 0

    def init_scene_play(self):
        self.scene = SCENE_PLAY
        #self.player.alive = True
        #update_list(bullet_list)
        enemy_list.clear()
        blast_list.clear()
        bullet_list.clear()
        enemy_bullet_list.clear()
        self.score = 0

        self.player = Player(int(PLAYER_WIDTH/4), int(screen_hight/2-8))

        self.f = 0 # reset formation no to start formation #todo

        self.shield_bar_value = 10
        self.shield_bar_color = 3

        update_list(bullet_list)
        update_list(enemy_list)
        update_list(blast_list)
        update_list(enemy_bullet_list)
        cleanup_list(bullet_list)
        cleanup_list(enemy_list)
        cleanup_list(blast_list)
        cleanup_list(enemy_bullet_list)


    def update(self):

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()

        self.fps.update_fps()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    def update_title_scene(self):
        self.background.update()
        self.scrlltxt.update()
        self.Spaceship.update(self.scene)
        self.Spaceship2.update(self.scene)
        self.lettering.update()
        self.letter.update(FPS_ACTUAL)
        # wobble text: cycle through x positions
        if pyxel.frame_count % round(FPS_ACTUAL/15) == 0:
            self.movement_x.append(self.movement_x[0])
            self.movement_x.pop(0)
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY
            del self.Spaceship
            del self.Spaceship2
            pyxel.stop()
            self.player = Player(int(PLAYER_WIDTH/4), int(screen_hight/2-8))
            self.init_scene_play()


    def update_play_scene(self):
        self.background.update()
        self.player.update(self.scene)

        if len(enemy_list) < 1:
            f_new = Formation2(self.f, screen_width, 0)
            #self.f_max = len(Formation2.formation_files)
            #print('f_max:', self.f_max)
            if self.f < self.f_max -1:
                self.f += 1
            else:
                self.f = 0

        # Check bullet with enermy collision
        for e in enemy_list:
            for b in bullet_list:
                if (
                        e.x + e.w > b.x
                        and b.x + b.w > e.x
                        and e.y + e.h > b.y
                        and b.y + b.h > e.y
                ):
                    e.alive = False
                    b.alive = False
                    self.score += 10
                    blast_list.append(
                        ShipBlast(e.x, e.y, 'enemy')
                    )

        # Check player with enemy collision
        enemy_and_bullet_list = enemy_list + enemy_bullet_list
        for enemy in enemy_and_bullet_list:
            if (
                    self.player.alive
                    and self.player.x + self.player.w > enemy.x
                    and enemy.x + enemy.w > self.player.x
                    and self.player.y + self.player.h > enemy.y
                    and enemy.y + enemy.h > self.player.y
            ):
                enemy.alive = False

                self.player.shield -= 25
                if self.player.shield <= 0:
                    self.player.alive = False
                blast_list.append(
                    ShipBlast(
                        self.player.x,
                        self.player.y
                    )
                )
                pyxel.play(1, 21)

        # Update Shield value
        self.shield_bar_value = self.player.shield / 10
        if 8 > self.shield_bar_value > 3:
            self.shield_bar_color = 9
        elif self.shield_bar_value <= 3:
            self.shield_bar_color = 8


        update_list(bullet_list)
        update_list(enemy_list)
        update_list(blast_list)
        update_list(enemy_bullet_list)
        cleanup_list(bullet_list)
        cleanup_list(enemy_list)
        cleanup_list(blast_list)
        cleanup_list(enemy_bullet_list)

        if self.player.alive is False and len(blast_list) == 0:  # check blastlist should be eliminated
            self.scene = SCENE_GAMEOVER
            if self.score > self.high_score:
                self.high_score = self.score

    def update_gameover_scene(self):
        self.background.update()
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.init_scene_play()
        update_list(bullet_list)
        update_list(enemy_list)
        update_list(blast_list)
        update_list(enemy_bullet_list)
        cleanup_list(bullet_list)
        cleanup_list(enemy_list)
        cleanup_list(blast_list)
        cleanup_list(enemy_bullet_list)

    def draw(self):
        pyxel.cls(0)
        self.background.draw()  # stars

        # Draw fps on screen
        #fps_string = 'FPS ' + str(self.fps.get_fps())
        #pyxel.text(10, 20, fps_string, 7)

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

    def draw_title_scene(self):
        self.Spaceship.draw()
        self.Spaceship2.draw()
        self.lettering.draw()
        # draw margin
        pyxel.rect(0, 0, 16, screen_hight, self.scrlltxt.border_color)
        pyxel.rect(screen_width - 16, 0, 16, screen_hight, self.scrlltxt.border_color)
        pyxel.rect(0, 0, screen_width, 12, self.scrlltxt.border_color)
        pyxel.rect(0, screen_hight - 12, screen_width, 12, self.scrlltxt.border_color)
        # draw scrolling text
        self.scrlltxt.draw()
        for i, line in enumerate(self.textlines):
            pos = (screen_width - ((len(line)-(self.control_chars[i]/2*3))*8)) / 2
            self.letter.text(pos + self.movement_x[i+i], 46 + (8 * i), 5, line)
        pyxel.text(2, screen_hight-8, VERSION, 5)

    def draw_play_scene(self):
        pyxel.rect(0, 0, screen_width, 7, 1)

        #pyxel.text(4, 1, 'SHIELD', 13)
        pyxel.blt(1, 0, 0, 32, 72, 8, 8, 0)
        pyxel.rectb(9, 1, 12, 5, 5)     # draw shield frame
        pyxel.rect(10, 2, self.shield_bar_value, 3, self.shield_bar_color)
        pyxel.text(70, 1, 'Score: {}    Highscore:{}'.format(self.score, self.high_score), 13)
        draw_list(bullet_list)
        draw_list(enemy_bullet_list)
        draw_list(enemy_list)
        self.player.draw()
        draw_list(blast_list)

    def draw_gameover_scene(self):
        self.draw_play_scene()
        Lettering(screen_hight/2 - 16, 'GAME OVER', animation=False ).draw()
        self.letter.text(int((screen_width - 176) / 2), int(screen_hight/2 + 8), 2, '|2|PRESS SPACE TO RESTART')

if __name__ == '__main__':
    App()
