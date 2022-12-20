import pyxel
from lib import score
import random
import string
import time
import math
import json
from letter import Letter
from vector import Vector2
import lib.conf as conf     # import global variables and configurations

# todo: ideas
# enemies should be able to shoot more then one time
# powerup: long laser


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
            del elem
        else:
            i += 1


class FPS:
    def __init__(self):
        self.start_time = time.time()
        self.frame_counter = 0
        self.fps = conf.FPS_LIMIT

    def update_fps(self):
        """
        Calculate the actual frame per second rate.
        :return: float: fps
        """
        self.frame_counter += 1
        divider = (time.time() - self.start_time)
        if divider > 0:
            self.fps = int(self.frame_counter / divider)
        #global conf.FPS_ACTUAL
        conf.FPS_ACTUAL = self.fps
        if (time.time() - self.start_time) > 1:
            self.frame_counter = 0
            self.start_time = time.time()

    def get_fps(self):
        return self.fps


class Scrolltext:

    def __init__(self):
        self.scrolltext = "This is my first prototype / work in progress space shooter game!!! " \
                          "It will take some time to be ready :-)"
        self.scrolltext_pixel_length = len(self.scrolltext) * 4
        self.x = 160
        self.y = 88
        self.y_start = 88
        self.y_end = conf.screen_hight - 24
        self.y_acceleration = 1.2  # 36 / conf.FPS_ACTUAL # default: 1.2
        self.y_speed = 1
        self.y_direction_down = True
        self.border_color = 6
        self.stripe_x = 0
        self.stripe_sections = 16  # 8 or 16
        self.border_color = 1
        self.textcolors = [1, 5, 12, 6, 7, 6, 12, 5]
        self.textcolornr = self.textcolors[0]

    def update(self):

        # change x position
        if self.x > (0 - self.scrolltext_pixel_length):
            self.x -= 30 / conf.FPS_ACTUAL
        else:
            self.x = conf.conf.screen_width

        divider = round(conf.FPS_ACTUAL / 30)
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
        pyxel.rect(0, self.y - 6, conf.screen_width, 17, 0)
        pyxel.line(0, self.y - 4, conf.screen_width, self.y - 4, 2)
        pyxel.line(0, self.y + 8, conf.screen_width, self.y + 8, 2)
        # jumping and scrolling text
        pyxel.text(self.x, self.y, self.scrolltext, self.textcolors[int(self.textcolornr)])
        # draw scrolling stripe lines
        for line_y in [-4, 8]:
            for i in range(0, int((conf.screen_width / self.stripe_sections) - 1)):
                pyxel.line(int(2 * i * conf.screen_width / self.stripe_sections + self.stripe_x),
                           self.y + line_y,
                           int((2 * i * conf.screen_width / self.stripe_sections) +
                               conf.screen_width / self.stripe_sections - 1 + self.stripe_x),
                           self.y + line_y, 4)
            if self.stripe_x < (conf.screen_width / self.stripe_sections):
                self.stripe_x += 30 / conf.FPS_ACTUAL
            else:
                self.stripe_x = - conf.screen_width / self.stripe_sections
            self.stripe_sections = 16  # 8 or 16


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
            if conf.FPS_ACTUAL != 0:
                x -= (speed * 30 / conf.FPS_ACTUAL)
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
                x = i * 16
                y = 16
            else:
                x = i * 16 - 256
                y = 32
            self.letter_img_positions[j] = (x, y)
        for i in range(10):  # Add number positions in resource image
            self.letter_img_positions[str(i)] = (i * 16, 48)

        self.letter_y_start = y_start
        self.letter_y_range = 8

        self.letter_positions_y = [(num + self.letter_y_start) for num in range(0, self.letter_y_range + 1)] + \
                                  [(num + self.letter_y_start) for num in range(self.letter_y_range - 1, 0, -1)]
        self.letter_frame_count = 0
        self.letters_left_span = (conf.screen_width - (len(self.word) * 16)) / 2

    def update(self):
        # cycle through y positions
        divider = round(conf.FPS_ACTUAL / 15)
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

        self.heat_bar_value = 0
        self.heat_bar_color = 3
        self.heat_bar_cooling_factor = 0.04
        self.active_power_ups = []

    def update(self, scene=None):
        #global conf.PLAYER_X
        #global conf.PLAYER_Y

        if scene == conf.SCENE_TITLE:
            # Spaceship animation
            divider = round(conf.FPS_ACTUAL / 7.5)
            if divider > 0:
                if pyxel.frame_count % divider == 0:
                    self.map_nr += 1
                    if self.map_nr in [6, 7] and self.h > 0:
                        self.h *= -1  # mirror vertical
                    elif self.map_nr not in [6, 7] and self.h < 0:
                        self.h *= -1  # mirror vertical

            if self.map_nr == len(self.map_pos):
                self.map_nr = 0

        if scene == conf.SCENE_PLAY and self.alive:
            if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                if self.y > 10:
                    self.y -= conf.PLAYER_SPEED
                self.map_nr = 1
            elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                if self.y < (conf.screen_hight - 16):  # todo: CHANGE 16 as var but be careful if it's negative sometimes
                    self.y += conf.PLAYER_SPEED
                self.map_nr = 1
                if self.h > 0:
                    self.h *= -1  # mirror vertical
            else:
                self.map_nr = 0
                if self.h < 0:
                    self.h *= -1  # reset mirror vertical
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                if self.x > conf.PLAYER_WIDTH / 4:
                    self.x -= conf.PLAYER_SPEED
            elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                if self.x < conf.screen_width - conf.PLAYER_WIDTH - conf.PLAYER_WIDTH / 4:
                    self.x += conf.PLAYER_SPEED
            else:
                if self.x > conf.PLAYER_WIDTH / 4:
                    self.x -= 1 * (30 / conf.FPS_ACTUAL)
            if (pyxel.btn(pyxel.KEY_CTRL) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)) and self.shoot_button_released:
                if self.laser_wait_count <= 0 and self.heat_bar_value < 9:
                    self.heat_bar_value += 1
                    # multi or single laser
                    if 1 in self.active_power_ups:
                        multi_bullet_list = [(0, 0), (-3, -5), (-3, 5)]
                    else:
                        multi_bullet_list = [(0, 0)]
                    # create bullet / laser
                    for bullet_offset in multi_bullet_list:
                        Bullet(self.x + conf.PLAYER_WIDTH - conf.BULLET_WIDTH + bullet_offset[0],
                               int(self.y + conf.PLAYER_HEIGHT / 2 - 1) + bullet_offset[1])
                    self.laser_wait_count = 8
                    self.shoot_button_released = False
            elif pyxel.btnr(pyxel.KEY_CTRL):
                self.shoot_button_released = True
            elif pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A):
                self.shoot_button_released = True
            self.laser_wait_count -= 1
            if self.heat_bar_value > 0:  # todo FPS
                self.heat_bar_value -= self.heat_bar_cooling_factor * (30 / conf.FPS_ACTUAL)

        # Update global variables, so that other object can locate player
        conf.PLAYER_X = self.x
        conf.PLAYER_Y = self.y

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
        self.animation_sprite_quantity = 11  # sprites in a row
        if model == 'player':
            self.map_pos = [80 - 16, 0]  # 96, 112, 128, 144, 160, 176, 192, 208, 224, 240
        if model == 'enemy':
            self.map_pos = [80 - 16, 80]
        pyxel.play(1, 21)

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
        self.w = conf.BULLET_WIDTH
        self.h = conf.BULLET_HEIGHT
        self.color = col
        self.alive = True
        self.bullet_speed = bullet_speed * 30 / conf.FPS_ACTUAL

        conf.bullet_list.append(self)
        pyxel.play(3, 20)

    def update(self):
        self.x += self.bullet_speed
        if self.x + self.w > conf.screen_width:
            self.alive = False

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, self.color)


class Enemy:
    animation_list = list(range(0, 6))

    def __init__(self, x, y, animation=0, variant=0, bullet_variant=0,
                 bullet_aimed=False, powerup=0, shield_max_hits=0):
        self.x = x
        self.y = y
        self.w = conf.ENEMY_WIDTH
        self.h = conf.ENEMY_HEIGHT
        self.map_pos = [0, 16, 32, 48]
        self.animation = animation
        self.variant = variant
        self.powerup = powerup  ### Achtung später unten ein Objekt wie iflight animation
        self.dir = 1
        self.alive = True
        self.offset = int(random.random() * 60)
        self.out_of_ammu = False
        # 'animation as object'
        self.flight_animation = EnemyFlightAnimation(self, animation, bullet_variant, bullet_aimed)
        image_map_y_pos_list = [80, 96, 112, 128, 144, 160, 176]
        self.image_map_y_pos = image_map_y_pos_list[self.variant]

        ### TEST
        if shield_max_hits > 0:
            self.shield = EnemyShield(self.x, self.y, self.w, self)

        conf.enemy_list.append(self)

    def update(self):
        self.flight_animation.update()
        # cycle through sprite list
        divider = round(conf.FPS_ACTUAL / 7.5)
        if divider > 0:
            if pyxel.frame_count % divider == 0:
                self.map_pos.append(self.map_pos[0])
                self.map_pos.pop(0)
        if self.x < 0 - conf.ENEMY_WIDTH - 1:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.map_pos[0], self.image_map_y_pos, self.w, self.h, 0)


class EnemyShield:

    def __init__(self, x, y, w, enemy, shield_max_hits=4):
        self.x = x
        self.y = y
        self.w = w
        self.r = self.w * 0.75 + 1
        self.enemy = enemy
        self.shield_offset = [[-1, -1], [0, -1], [-1, 0], [0, 0]]
        self.shield_colors = [3, 9, 4, 8]
        self.hits = 0
        self.shield_color = self.shield_colors[self.hits]
        self.max_hits = shield_max_hits
        self.alive = True
        conf.enemy_shield_list.append(self)

    def update(self):
        self.x = self.enemy.x
        self.y = self.enemy.y
        divider = round(conf.FPS_ACTUAL / 3)

        if not self.enemy.alive or self.hits >= self.max_hits:
            self.alive = False
            self.hits = 0

        self.shield_color = self.shield_colors[self.hits]

    def draw(self):
        pyxel.circb(self.x + (self.w / 2) - 1, self.y + (self.w / 2) - 1, self.r, self.shield_color)
        pyxel.circb(self.x + (self.w / 2) - 0, self.y + (self.w / 2) - 1, self.r, self.shield_color)
        pyxel.circb(self.x + (self.w / 2) - 1, self.y + (self.w / 2) - 0, self.r, self.shield_color)
        pyxel.circb(self.x + (self.w / 2) - 0, self.y + (self.w / 2) - 0, self.r, self.shield_color)


class EnemyFlightAnimation:
    variant_names = ['flying straight', 'flying up and down', 'enemy with extra speed',
                     'with extra speed toward player', 'flying and shooting straight', 'flying in circle',
                     'swinging', 'stop and shoot']

    def __init__(self, enemy_obj, variant=0, bullet_variant=0, bullet_aimed=False):
        self.enemy = enemy_obj
        self.variant = variant
        # for flying circles
        self.circle_step_sum = 0
        self.radian_offset = 0
        self.radius = 50
        self.flying_circle_started = False
        self.bullet_variant = bullet_variant
        self.bullet_aimed = bullet_aimed
        self.wait_for_next_shot = 10 * (conf.FPS_ACTUAL / 30)
        self.swing_span = 6
        self.swing_y_start = self.enemy.y

    def update(self):
        if self.variant == 0:  # flying straight
            self.enemy.x -= conf.ENEMY_SPEED

        if self.variant == 1:  # flying up and down
            self.enemy.x -= conf.ENEMY_SPEED
            if self.enemy.x < (conf.screen_width - conf.screen_width / 6):
                if self.enemy.y < (conf.screen_hight - self.enemy.h) and self.enemy.dir == 1:
                    self.enemy.y += conf.ENEMY_SPEED
                elif self.enemy.y > 9 and self.enemy.dir == -1:
                    self.enemy.y -= conf.ENEMY_SPEED
                else:
                    self.enemy.dir *= -1

        if self.variant == 2:  # enemy with extra speed
            self.enemy.x -= conf.ENEMY_SPEED * 1.2

        if self.variant == 3:  # with extra speed toward player
            self.enemy.x -= conf.ENEMY_SPEED * 1.2

            if self.enemy.x > conf.PLAYER_X:
                y_factor = Vector2.y_target_factor([self.enemy.x, self.enemy.y], [conf.PLAYER_X, conf.PLAYER_Y])
                if y_factor > 3:
                    y_factor = 3
                elif y_factor < -3:
                    y_factor = -3
                y_factor = y_factor * 30 / conf.FPS_ACTUAL
                self.enemy.y -= y_factor

        if self.variant == 4:  # flying and shooting straight
            self.enemy.x -= conf.ENEMY_SPEED
            if self.enemy.x < (conf.screen_width - conf.screen_width / 6):
                if self.enemy.x < (conf.screen_width - conf.screen_width / 6) and not self.enemy.out_of_ammu:
                    EnemyBullet(int(self.enemy.x - conf.BULLET_WIDTH), self.enemy.y + conf.ENEMY_HEIGHT / 2 - 1)
                    self.enemy.out_of_ammu = True

        if self.variant == 5:  # flying in circle
            if self.enemy.x > conf.screen_width * 3 / 4 and not self.flying_circle_started:
                self.enemy.x -= conf.ENEMY_SPEED
                self.enemy.mx = conf.screen_width * 3 / 4
                self.enemy.my = self.enemy.y + self.radius
            else:
                self.flying_circle_started = True
                offset = math.pi * 1.5
                radian = 0.1 * 30 / conf.FPS_ACTUAL
                if self.circle_step_sum < 2 * math.pi:
                    self.enemy.x = self.enemy.mx - self.radius * math.cos(self.circle_step_sum + offset)
                    self.enemy.y = self.enemy.my + self.radius * math.sin(self.circle_step_sum + offset)
                    self.enemy.mx -= 0.3
                    self.circle_step_sum += radian
                else:
                    self.enemy.x -= conf.ENEMY_SPEED

        if self.variant == 6:  # swinging
            self.enemy.x -= conf.ENEMY_SPEED

            if self.enemy.x < conf.screen_width:
                if self.enemy.y < self.swing_y_start + self.swing_span and self.enemy.dir == 1:
                    self.enemy.y += conf.ENEMY_SPEED / 4
                elif self.enemy.y > self.swing_y_start - self.swing_span and self.enemy.dir == -1:
                    self.enemy.y -= conf.ENEMY_SPEED / 4
                else:
                    self.enemy.dir *= -1

        if self.variant == 7:  # stop and shoot
            if self.enemy.x > conf.screen_width * 0.8:
                self.enemy.x -= conf.ENEMY_SPEED
            else:
                if not self.enemy.out_of_ammu and self.wait_for_next_shot <= 0:
                    radian = math.pi / 6
                    radian_sum = 0
                    while radian_sum < 2 * math.pi:
                        EnemyBullet(int(self.enemy.x + conf.ENEMY_WIDTH / 2),
                                    self.enemy.y + conf.ENEMY_HEIGHT / 2 - 1,
                                    8,
                                    5,
                                    self.bullet_variant,
                                    radian_sum=radian_sum,
                                    radian_offset=self.radian_offset)
                        radian_sum += radian
                    self.radian_offset += 0.1
                    self.wait_for_next_shot = 10 * (conf.FPS_ACTUAL / 30)
                    if self.radian_offset > 1.6:
                        self.enemy.out_of_ammu = True
            self.wait_for_next_shot -= 1

        #############
        # shooting
        #############

        if self.bullet_variant in (1, 2):
            if self.enemy.x < (conf.screen_width - conf.screen_width / 6):
                if self.enemy.x < (conf.screen_width - conf.screen_width / 6) and not self.enemy.out_of_ammu:
                    EnemyBullet(int(self.enemy.x),
                                self.enemy.y + conf.ENEMY_HEIGHT / 2 - 1,
                                8,
                                5,
                                self.bullet_variant,
                                self.bullet_aimed)
                    self.enemy.out_of_ammu = True


class EnemyBullet:
    variant_names = ['None', 'straight laser', 'circle laser', 'spinning lasers']

    def __init__(self, x: int, y: int, col=8, bullet_speed=5, variant=1, aimed=False, radian_sum=0, radian_offset=0):
        bullets_dimension = {
            0: (0, 0),  # nothing
            1: (4, 2),  # straight laser
            2: (4, 4),  # circle laser
            3: (1, 1)  # spinning laser pixel
        }

        self.w, self.h = bullets_dimension.get(variant)

        self.x = x - self.w
        self.y = y
        self.origin_x = self.x
        self.origin_y = self.y
        self.color = col
        self.alive = True
        self.bullet_speed = bullet_speed * 30 / conf.FPS_ACTUAL
        self.variant = variant
        self.aimed = aimed
        self.y_factor = 0  # moving vertically
        self.color_range = [8, 8, 2, 8, 8, 7]
        self.radius = 1
        self.radian_sum = radian_sum
        self.radian_offset = radian_offset
        self.radian_offset = self.radian_offset
        self.spinning_coordinates = []

        conf.enemy_bullet_list.append(self)
        pyxel.play(3, 20)

    def update(self):
        if self.variant == 1:  # straight laser
            self.x -= self.bullet_speed
            if self.x + self.w > conf.screen_width:
                self.alive = False

        if self.variant == 2:  # circle laser
            self.x -= self.bullet_speed
            if self.aimed is False:
                self.y_factor = Vector2.y_target_factor([self.x, self.y], [conf.PLAYER_X, conf.PLAYER_Y])
                self.aimed = True
            self.y -= self.y_factor * self.bullet_speed
            self.color_range.append(self.color_range[0])
            self.color_range.pop(0)

        if self.variant == 3:  # spinning laser
            self.radius += 1  # * (30 / conf.FPS_ACTUAL)    # FPS
            self.x = int(self.origin_x - self.radius * math.cos(self.radian_sum + self.radian_offset))
            self.y = int(self.origin_y + self.radius * math.sin(self.radian_sum + self.radian_offset))

    def draw(self):
        if self.variant == 1:  # straight laser
            pyxel.rect(self.x, self.y, self.w, self.h, self.color)

        if self.variant == 2:  # Circle laser
            pyxel.circ(self.x, self.y, 2, self.color_range[0])

        if self.variant == 3:  # spinning laser
            pyxel.pset(self.x, self.y, 8)


class Formation2:
    ###formation_files = ['formation_0004.json', 'formation_1644008576.json', 'formation_1644002913.json', 'formation_1643569683.json',
    ###                   'formation_0005.json', 'formation_1643570322.json', 'formation_1644621139.json']

    import glob
    formation_files = glob.glob('./assets/formations/*.json')
    print(formation_files)

    def __init__(self, no, x, y):
        self.x = x
        self.y = y
        self.formation_list = []
        if 1 == 1:
            file = Formation2.formation_files[no]
            ###with open('./assets/formations/'+file) as json_file:
            with open(file) as json_file:
                json_data = json.load(json_file)
                for e in json_data['enemies']:
                    self.formation_list.append(e)

        for i, formation in enumerate(self.formation_list):
            enemy_parameter_list = [x + formation['x'],
                                    y + formation['y'],
                                    formation['enemy_flight_animation'],
                                    formation['variant'],
                                    formation['enemy_bullet_variant'],
                                    formation['enemy_bullet_aimed']]
            if 'powerup' in formation:
                enemy_parameter_list.append(formation['powerup'])
            if 'shield_max_hits' in formation:
                enemy_parameter_list.append(formation['shield_max_hits'])

            # create enemy object with parameters from list
            Enemy(*enemy_parameter_list)


class PowerUp:
    variant_names = ['None', 'Laser_Upgrade_1', 'Health', 'Cooling', 'Flash', 'Coin']
    variant_text = ['', 'laser upgrade', 'health 100%', 'faster laser cooling', 'flash', 'space money']

    def __init__(self, x, y, variant):
        self.x = x
        self.y = y
        self.w, self.h = 16, 16
        self.variant = variant
        self.sprite_map_x_position = [64, 80, 96]
        self.sprite_map_y_position = [0, 96, 112, 128, 144, 160]
        self.alive = True
        conf.power_ups_list.append(self)

    def apply_to_player(self, player_object=None):
        if player_object:
            if self.variant == 1:
                player_object.active_power_ups.append(self.variant)
            if self.variant == 2:
                # player_object.active_power_ups.append(self.variant)
                player_object.shield = 100
            if self.variant == 3:
                # faster cooling
                player_object.heat_bar_cooling_factor *= 2
            if self.variant == 4:
                # todo: flash powerUp
                pass
            if self.variant == 5:
                # space money
                score.add(250)
                ScoreText(player_object.x + 50, player_object.y, '250')

        ScoreText(player_object.x, player_object.y, self.variant_text[self.variant])

    def update(self):
        # cycle through sprite list
        divider = round(conf.FPS_ACTUAL / 7.5)
        if divider > 0:
            if pyxel.frame_count % divider == 0:
                self.sprite_map_x_position.append(self.sprite_map_x_position[0])
                self.sprite_map_x_position.pop(0)
                self.x -= random.randrange(1, 3, 1)
                self.y += random.randrange(-1, 2, 1)
        if self.x < 0 - self.w - 1:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.sprite_map_x_position[0], self.sprite_map_y_position[self.variant], self.w,
                  self.h, 0)


class ScoreText:

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.col = 7
        self.text = text
        self.alive = True
        conf.score_text_list.append(self)

    def update(self):
        self.y -= 1
        if self.y == -10:
            self.alive = False
        # self.col = random.randrange(0, 15, 1) # flickering color

    def draw(self):
        pyxel.text(self.x, self.y, str(self.text), self.col)


class App:

    def __init__(self):
        pyxel.init(conf.screen_width, conf.screen_hight, title="Starship1", fps=conf.FPS_LIMIT, capture_sec=30)
        self.high_score = 0
        ###self.score = 0
        score.set(0)
        self.scene = conf.SCENE_TITLE
        self.fps = FPS()  # fps calculation initialisation
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        score.set(0)
        self.scene = conf.SCENE_TITLE
        self.fps = FPS()
        pyxel.load("assets/test.pyxres")
        if self.scene == conf.SCENE_TITLE:
            self.Spaceship = Player(24, 20)
            self.Spaceship2 = Player(conf.screen_width - 40, 20, True)
            self.background = Background()
            self.scrlltxt = Scrolltext()
            self.lettering = Lettering(16, 'FICTION-X')
            self.letter = Letter()
            # Play music
            if conf.MUSIC_ON:
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
        self.scene = conf.SCENE_PLAY
        conf.enemy_list.clear()
        conf.blast_list.clear()
        conf.bullet_list.clear()
        conf.enemy_bullet_list.clear()
        conf.power_ups_list.clear()
        conf.score_text_list.clear()
        conf.enemy_shield_list.clear()
        score.set(0)
        self.player = Player(int(conf.PLAYER_WIDTH / 4), int(conf.screen_hight / 2 - 8))
        self.f = 0  # reset formation no to start formation #todo

        self.shield_bar_value = 10
        self.shield_bar_color = 3

        for l in conf.all_object_lists:
            update_list(l)
            cleanup_list(l)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()
        self.fps.update_fps()
        if self.scene == conf.SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == conf.SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == conf.SCENE_GAMEOVER:
            self.update_gameover_scene()

    def update_title_scene(self):
        self.background.update()
        self.scrlltxt.update()
        self.Spaceship.update(self.scene)
        self.Spaceship2.update(self.scene)
        self.lettering.update()
        self.letter.update(conf.FPS_ACTUAL)
        # wobble text: cycle through x positions
        if pyxel.frame_count % round(conf.FPS_ACTUAL / 15) == 0:
            self.movement_x.append(self.movement_x[0])
            self.movement_x.pop(0)
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.scene = conf.SCENE_PLAY
            del self.Spaceship
            del self.Spaceship2
            pyxel.stop()
            self.player = Player(int(conf.PLAYER_WIDTH / 4), int(conf.screen_hight / 2 - 8))
            self.init_scene_play()

    def update_play_scene(self):
        self.background.update()
        self.player.update(self.scene)
        if len(conf.enemy_list) < 1:
            f_new = Formation2(self.f, conf.screen_width, 0)
            if self.f < self.f_max - 1:
                self.f += 1
            else:
                self.f = 0
        # Check bullet with enemy collision
        for e in conf.enemy_list:
            if hasattr(e, 'shield'):    # Check if enemy has shield
                if e.shield.alive:      # Check if shield is alive
                    continue
            for b in conf.bullet_list:
                if (
                        e.x + e.w > b.x
                        and b.x + b.w > e.x
                        and e.y + e.h > b.y
                        and b.y + b.h > e.y
                ):
                    e.alive = False
                    b.alive = False
                    points = 10
                    ScoreText(e.x, e.y, points)
                    score.add(points)
                    conf.blast_list.append(
                        ShipBlast(e.x, e.y, 'enemy')
                    )
                    # drop powerup if enemy had one
                    if e.powerup > 0:
                        PowerUp(e.x, e.y, e.powerup)

        # Check bullet with enemy shield collision
        for shield in conf.enemy_shield_list:
            for b in conf.bullet_list:
                #  sqrt((Xc- Xn)2 + (Yc- Yn)2)
                distance_to_bullet = math.sqrt(
                    (shield.x - (b.x - b.w)) ** 2 +
                    (shield.y - (b.y - b.h)) ** 2
                )
                if distance_to_bullet <= shield.r:
                    shield.hits += 1
                    b.alive = False

        # Check player with enemy or powerup collision
        collision_object_list = conf.enemy_list + conf.enemy_bullet_list + conf.power_ups_list
        for obj in collision_object_list:
            if (
                    self.player.alive
                    and self.player.x + self.player.w > obj.x
                    and obj.x + obj.w > self.player.x
                    and self.player.y + self.player.h > obj.y
                    and obj.y + obj.h > self.player.y
            ):
                obj.alive = False

                # Check object type ans do object specific things
                if isinstance(obj, EnemyBullet) or isinstance(obj, Enemy):
                    self.player.shield -= 25
                    if self.player.shield <= 0:
                        self.player.alive = False
                    conf.blast_list.append(
                        ShipBlast(
                            self.player.x,
                            self.player.y
                        )
                    )
                elif isinstance(obj, PowerUp):
                    score.add(50)
                    obj.apply_to_player(self.player)

        # Update Shield value
        self.shield_bar_value = self.player.shield / 10
        if 8 > self.shield_bar_value > 3:  # shield bar is orange
            self.shield_bar_color = 9
        elif self.shield_bar_value <= 3:  # shield bar is red
            self.shield_bar_color = 8
        else:
            self.shield_bar_color = 3  # shield bar is green

        for l in conf.all_object_lists:
            update_list(l)
            cleanup_list(l)

        if self.player.alive is False and len(conf.blast_list) == 0:  # check conf.blast_list should be eliminated
            self.scene = conf.SCENE_GAMEOVER
            if score.get() > self.high_score:
                self.high_score = score.get()

    def update_gameover_scene(self):
        self.background.update()
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.init_scene_play()

        for l in conf.all_object_lists:
            update_list(l)
            cleanup_list(l)

    def draw(self):
        pyxel.cls(0)
        self.background.draw()  # stars

        if self.scene == conf.SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == conf.SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == conf.SCENE_GAMEOVER:
            self.draw_gameover_scene()

    def draw_title_scene(self):
        self.Spaceship.draw()
        self.Spaceship2.draw()
        self.lettering.draw()
        # draw margin
        pyxel.rect(0, 0, 16, conf.screen_hight, self.scrlltxt.border_color)
        pyxel.rect(conf.screen_width - 16, 0, 16, conf.screen_hight, self.scrlltxt.border_color)
        pyxel.rect(0, 0, conf.screen_width, 12, self.scrlltxt.border_color)
        pyxel.rect(0, conf.screen_hight - 12, conf.screen_width, 12, self.scrlltxt.border_color)
        # draw scrolling text
        self.scrlltxt.draw()
        for i, line in enumerate(self.textlines):
            pos = (conf.screen_width - ((len(line) - (self.control_chars[i] / 2 * 3)) * 8)) / 2
            self.letter.text(pos + self.movement_x[i + i], 46 + (8 * i), 5, line)
        pyxel.text(2, conf.screen_hight - 8, conf.VERSION, 5)

    def draw_play_scene(self):
        for l in conf.all_object_lists:
            draw_list(l)
        self.player.draw()

        # Status bar
        pyxel.rect(0, 0, conf.screen_width, 7, 1)
        pyxel.blt(1, 0, 0, 32, 72, 8, 8, 0)
        pyxel.rectb(9, 1, 12, 5, 5)  # draw shield frame
        pyxel.rect(10, 2, self.shield_bar_value, 3, self.shield_bar_color)
        pyxel.text(70, 1, 'Score: {}    High-score: {}'.format(score.get(), self.high_score), 13)

        # Heat bar
        pyxel.rect(24, 3, 4, 1, 10)
        pyxel.rectb(29, 1, 12, 5, 5)  # draw heat bar frame
        pyxel.rect(30, 2, self.player.heat_bar_value, 3, self.player.heat_bar_color)

    def draw_gameover_scene(self):
        self.draw_play_scene()
        Lettering(conf.screen_hight / 2 - 16, 'GAME OVER', animation=False).draw()
        self.letter.text(int((conf.screen_width - 176) / 2), int(conf.screen_hight / 2 + 8), 2, '|2|PRESS SPACE TO RESTART')


if __name__ == '__main__':
    App()
