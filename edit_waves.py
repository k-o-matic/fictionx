import pyxel
import uuid
import json
import time
import os
from fiction_game import EnemyBullet
from fiction_game import EnemyFlightAnimation

#todo:
# R button = reset
# Import JSON file in editor


VERSION = 'v 0.0.1'
GAME_SCREEN_WIDTH = 240
GAME_SCREEN_HEIGHT = 135
SCREEN_WIDTH = GAME_SCREEN_WIDTH + 80
SCREEN_HEIGHT = GAME_SCREEN_HEIGHT + 80
FPS_LIMIT = 60
FPS_ACTUAL = FPS_LIMIT

image_map_y_pos_list = [80, 96, 112, 128, 144, 160, 176]
SELECTED_SOURCE = 0
SELECTED_DESTINATION = None

enemy_list = []
VMAP_ENEMIES = []
BUTTON_LIST = []

VIRTUAL_MAP_WIDTH = 240
VIRTUAL_MAP_X_OFFSET = 0


def draw_list(lst):
    for elem in lst:
        elem.draw()


def update_list(lst):
    for elem in lst:
        elem.update()


def cleanup_list(lst):
    i = 0
    while i < len(lst):
        elem = lst[i]
        if not elem.alive:
            lst.pop(i)
            del elem
        else:
            i += 1


def mouse_over_object(list_with_objects, extended=True):
    offset_x = 0
    offset_y = 0
    result = False
    for e in list_with_objects:
        if type(e).__name__ == 'Enemy':
            if not e.source:
                # extended check
                if extended:
                    offset_x = e.w
                    offset_y = e.h
        if e.x - offset_x <= pyxel.mouse_x <= e.x + e.w and e.y - offset_y <= pyxel.mouse_y <= e.y + e.h:
            result = True
            break
        else:
            result = False
    return result


###########################
# Editor window functions
###########################

def editor_window_update():
    global VIRTUAL_MAP_WIDTH
    global VIRTUAL_MAP_X_OFFSET
    global SELECTED_DESTINATION

    # mouse position in editor windows
    if 0 < pyxel.mouse_x <= 240 and 8 < pyxel.mouse_y < 135 + 9:
        mx = pyxel.mouse_x - 1
        my = pyxel.mouse_y - 9
        # click in editor window
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and not mouse_over_object(enemy_list):
            if pyxel.btn(pyxel.KEY_SHIFT):  # Raster
                x = pyxel.mouse_x - (pyxel.mouse_x % 8) + 1
                y = pyxel.mouse_y - (pyxel.mouse_y % 8) + 1
            else:
                x = pyxel.mouse_x
                y = pyxel.mouse_y
            SELECTED_DESTINATION = VMapEnemy(Enemy(SELECTED_SOURCE, x, y, 0, False))
            # VMapEnemy(SELECTED_DESTINATION)
            # print('SELECTED_DESTINATION:', SELECTED_DESTINATION)
    else:
        mx = ''
        my = ''

    # Enemy Parameters
    if 2 <= pyxel.mouse_x <= 106 and 171 <= pyxel.mouse_y <= 178:  # 2,164
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if SELECTED_DESTINATION.bullet.variant < (len(EnemyBullet.variant_names) - 1):
                SELECTED_DESTINATION.bullet.variant += 1
            else:
                SELECTED_DESTINATION.bullet.variant = 0
    if 2 <= pyxel.mouse_x <= 106 and 178 <= pyxel.mouse_y <= 184:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            SELECTED_DESTINATION.bullet.aimed = not SELECTED_DESTINATION.bullet.aimed
    # Animation
    if 2 <= pyxel.mouse_x <= 106 and 185 <= pyxel.mouse_y <= 192:  # 2,164
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if SELECTED_DESTINATION.animation.variant < (len(EnemyFlightAnimation.variant_names) - 1):
                SELECTED_DESTINATION.animation.variant += 1
            else:
                SELECTED_DESTINATION.animation.variant = 0

    return mx, my


def editor_window_draw(mx, my):
    global VIRTUAL_MAP_WIDTH
    global VIRTUAL_MAP_X_OFFSET

    # Draw wave windows border
    pyxel.rectb(0, 8, 242, 137, 7)

    # Draw text x and y position
    pyxel.text(2, 1, "x:{}".format(mx), 7)
    pyxel.text(25, 1, "y:{}".format(my), 7)
    pyxel.text(48, 1, "vMapWidth:{}".format(VIRTUAL_MAP_WIDTH), 7)
    pyxel.text(116, 1, "vMapPos:{}".format(VIRTUAL_MAP_X_OFFSET), 7)
    pyxel.text(176, 1, "Enemies:{}".format(len(VMAP_ENEMIES)), 7)

    # Show raster on editor window
    if pyxel.btn(pyxel.KEY_SHIFT):
        for x in range(1, 241, 8):
            for y in range(9, 145, 8):
                pyxel.pset(x, y, 13)

    # Draw scroll bar with arrow buttons
    pyxel.rectb(0, 145, 242, 7, 5)
    pyxel.blt(0, 145, 0, 56, 64, 7, 7, 0)
    pyxel.blt(235, 145, 0, 56, 64, -7, 7, 0)
    # bar 228px = 100%
    bar_width = int((GAME_SCREEN_WIDTH / VIRTUAL_MAP_WIDTH) * 228)
    no_bar_space = (228 - bar_width)
    if VIRTUAL_MAP_X_OFFSET > 0:
        bar_position = no_bar_space * (VIRTUAL_MAP_X_OFFSET / (VIRTUAL_MAP_WIDTH - GAME_SCREEN_WIDTH))
    else:
        bar_position = 0
    pyxel.rect(7 + bar_position, 146, bar_width, 5, 6)

    # mouse position on arrow button
    if 235 <= pyxel.mouse_x <= 241 and 145 <= pyxel.mouse_y <= 152:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if (VIRTUAL_MAP_X_OFFSET + GAME_SCREEN_WIDTH) >= VIRTUAL_MAP_WIDTH:
                VIRTUAL_MAP_WIDTH += 16
            VIRTUAL_MAP_X_OFFSET += 16
    elif 0 <= pyxel.mouse_x <= 6 and 145 <= pyxel.mouse_y <= 152:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and VIRTUAL_MAP_X_OFFSET > 0:
            VIRTUAL_MAP_X_OFFSET -= 16

    pyxel.text(SCREEN_WIDTH-68, SCREEN_HEIGHT - 9, 'Press h for help', 7)

def export_json():
    formation_enemies_list = []
    for formation_enemy in VMAP_ENEMIES:
        vmap_enemy_dict = {'x': formation_enemy.v_map_x,
                           'y': formation_enemy.v_map_y,
                           'variant': formation_enemy.vmap_enemy.variant,
                           'enemy_bullet_variant': formation_enemy.bullet.variant,
                           'enemy_bullet_aimed': formation_enemy.bullet.aimed,
                           'enemy_flight_animation': formation_enemy.animation.variant}
        formation_enemies_list.append(vmap_enemy_dict)
    formation_enemies_list.sort(key=lambda d: d['x'])  # Sort list with dicts by 'x' value
    formation_export = {'enemies': formation_enemies_list}

    # Serializing json and write a file
    json_object = json.dumps(formation_export, indent=4)
    timestamp = int(time.time())
    filename = 'formation_{}.json'.format(str(timestamp))
    with open(filename, "w") as outfile:
        outfile.write(json_object)
    cwd = os.getcwd()
    print('Saved {} to {}'.format(outfile.name, cwd))

class Button:
    def __init__(self, x: int, y: int, text: str, h=9):
        self.x = x
        self.y = y
        self.w = len(text) * 4 + 3
        self.h = h
        self.text = text
        self.colors = {'button': 6, 'frame': 5, 'text': 5, 'mouse_over': 1}
        BUTTON_LIST.append(self)

    def update(self):
        if mouse_over_object(BUTTON_LIST):
            self.colors['button'] = 1
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if self.text == 'Export JSON':
                    export_json()
        else:
            self.colors['button'] = 6

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, self.colors['button'])
        pyxel.text(self.x + 2, self.y + 2, self.text, 5)
        pyxel.rectb(self.x, self.y, self.w, self.h, 5)


class Enemy:

    def __init__(self, variant: int, x, y, animation=0, source=False):
        self.x = x
        self.v_map_x = x + VIRTUAL_MAP_X_OFFSET
        self.y = y
        self.variant = variant
        self.source = source
        self.image_map_x_pos = [0, 16, 32, 48]

        self.w = 16
        self.h = 16
        self.animation = animation
        self.dir = 1
        self.alive = True
        # self.offset = int(random.random() * 60)
        self.out_of_ammu = False
        # for flying circles
        self.circle_step_sum = 0
        self.radius = 50
        self.flying_circle_started = False

        self.image_map_y_pos = image_map_y_pos_list[variant]

        enemy_list.append(self)

    def update(self):
        global SELECTED_SOURCE
        global SELECTED_DESTINATION

        if self.x < pyxel.mouse_x < self.x + self.w and \
                self.y < pyxel.mouse_y < self.y + self.h:

            # select enemy in source bar or in editor window
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if self.source:
                    SELECTED_SOURCE = self.variant
                if not self.source:
                    for i in VMAP_ENEMIES:
                        if i.vmap_enemy == self:
                            SELECTED_DESTINATION = i

        if not self.source:
            # Update x position
            self.x = self.v_map_x - VIRTUAL_MAP_X_OFFSET

    def draw(self):

        if not self.source:
            # Draw enemy on virtual map
            if self.v_map_x - VIRTUAL_MAP_X_OFFSET <= 241:
                w = self.w
                if self.v_map_x - VIRTUAL_MAP_X_OFFSET + self.w > 241:
                    w = self.w - (self.v_map_x - VIRTUAL_MAP_X_OFFSET + self.w - 241)
                pyxel.blt(self.v_map_x - VIRTUAL_MAP_X_OFFSET, self.y, 0, self.image_map_x_pos[0], self.image_map_y_pos,
                          w, self.h, 0)
        else:
            # Draw source enemy at the right side of the editor
            pyxel.blt(self.x, self.y, 0, self.image_map_x_pos[0], self.image_map_y_pos, self.w, self.h, 0)

        # Draw rectangle border if selected in source bar
        if self.source and SELECTED_SOURCE == self.variant:
            pyxel.rectb(self.x, self.y, 16, 16, 8)
        if SELECTED_DESTINATION:
            if SELECTED_DESTINATION.vmap_enemy == self:
                pyxel.rectb(self.x, self.y, 16, 16, 8)


class VMapEnemy:

    def __init__(self, obj):
        self.x = obj.x
        self.y = obj.y
        self.vmap_enemy = obj
        self.v_map_x = obj.x + VIRTUAL_MAP_X_OFFSET
        self.v_map_y = obj.y - 9
        # self.variant = variant
        self.uuid = str(uuid.uuid4())
        self.bullet = EnemyBullet(40, 166, 8, 5, 0)
        self.animation = EnemyFlightAnimation(self.vmap_enemy)
        ####
        self.alive = True
        VMAP_ENEMIES.append(self)

    def update(self):

        if self == SELECTED_DESTINATION:

            # moving object in editor window with arrow keys
            if pyxel.btnp(pyxel.KEY_UP):
                self.v_map_y -= 1
                self.vmap_enemy.y -= 1
            elif pyxel.btnp(pyxel.KEY_DOWN):
                self.v_map_y += 1
                self.vmap_enemy.y += 1
            elif pyxel.btnp(pyxel.KEY_LEFT):
                self.v_map_x -= 1
                self.vmap_enemy.v_map_x -= 1
                self.vmap_enemy.x -= 1
            elif pyxel.btnp(pyxel.KEY_RIGHT):
                self.v_map_x += 1
                self.vmap_enemy.v_map_x += 1
                self.vmap_enemy.x += 1

        if len(VMAP_ENEMIES) > 0:
            if self.vmap_enemy.x < pyxel.mouse_x < self.vmap_enemy.x + self.vmap_enemy.w and \
                    self.vmap_enemy.y < pyxel.mouse_y < self.vmap_enemy.y + self.vmap_enemy.h:
                if pyxel.frame_count % 4 == 0:
                    self.vmap_enemy.image_map_x_pos.append(self.vmap_enemy.image_map_x_pos[0])
                    self.vmap_enemy.image_map_x_pos.pop(0)
                # delete enemy in editor window with right click
                if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) and not self.vmap_enemy.source:
                    self.vmap_enemy.alive = False
                    self.alive = False

    def draw(self):
        if SELECTED_DESTINATION:
            # obj = SELECTED_DESTINATION
            pyxel.text(2, 157, "uuid: {}".format(SELECTED_DESTINATION.uuid), 13)
            pyxel.text(2, 164, "vmap x/y : {}/{}".format(self.v_map_x, self.v_map_y), 13)
            pyxel.text(122, 164, "Ship type: {}".format(self.vmap_enemy.variant), 13)

            shooting_name = EnemyBullet.variant_names[self.bullet.variant]
            pyxel.text(2, 171, "Shooting : {}".format(shooting_name), 5)
            aims = str(self.bullet.aimed)
            pyxel.text(2, 178, "Aims at Player: {}".format(aims), 5)
            animation_variant_name = EnemyFlightAnimation.variant_names[self.animation.variant]
            pyxel.text(2, 185, "Animation: {}".format(animation_variant_name), 5)


class App:
    mx = ''
    my = ''

    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="EDITOR", fps=FPS_LIMIT, capture_sec=30)
        pyxel.load("assets/test.pyxres")
        pyxel.mouse(True)

        # generate enemy source instances
        for i, j in enumerate(image_map_y_pos_list):
            Enemy(i, 260, 2 + i * 24, 0, True)
        ### Editor
        Button(3, SCREEN_HEIGHT - 12, 'Export JSON')

        pyxel.run(self.update, self.draw)

    def update(self):
        global SELECTED_SOURCE

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Mouse wheel
        if pyxel.mouse_wheel > 0:
            if SELECTED_SOURCE > 0:
                SELECTED_SOURCE -= 1
            elif SELECTED_SOURCE <= 0:
                SELECTED_SOURCE = len(image_map_y_pos_list) - 1
        if pyxel.mouse_wheel < 0:
            if SELECTED_SOURCE < len(image_map_y_pos_list) - 1:
                SELECTED_SOURCE += 1
            elif SELECTED_SOURCE >= len(image_map_y_pos_list) - 1:
                SELECTED_SOURCE = 0

        App.mx, App.my = editor_window_update()
        # VMapEnemy.update(SELECTED_DESTINATION)
        update_list(enemy_list)
        update_list(VMAP_ENEMIES)
        update_list(BUTTON_LIST)
        cleanup_list(enemy_list)
        cleanup_list(VMAP_ENEMIES)

    def draw(self):
        pyxel.cls(0)

        if pyxel.btn(pyxel.KEY_H):
            pyxel.text(2, 2, 'Formation Editor help\n'
                             '---------------------\n\n'
                             'mouse scroll wheel: choose ship type\n'
                             'mouse left click: set ship\n'
                             'mouse right click: delete ship\n'
                             'Arrow keys: move ship in editor window\n'
                             'click blue text: change variants\n'
                             'SHIFT: show an use raster'
                       , 7)
        else:
            # EditorWindow.draw()
            draw_list(enemy_list)
            draw_list(BUTTON_LIST)
            editor_window_draw(App.mx, App.my)
            VMapEnemy.draw(SELECTED_DESTINATION)


if __name__ == '__main__':
    App()
