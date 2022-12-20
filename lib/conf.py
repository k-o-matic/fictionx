"""
This file contains all global variables.
"""

VERSION = 'v 0.0.2'
screen_width = 240
screen_hight = 135
FPS_LIMIT = 60
FPS_ACTUAL = FPS_LIMIT

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16
PLAYER_SPEED = 3 * 30 / FPS_ACTUAL  # adjust speed according to fps
PLAYER_X = 0
PLAYER_Y = 0

BULLET_WIDTH = 4
BULLET_HEIGHT = 2

###SCORE = 0

ENEMY_WIDTH = 16
ENEMY_HEIGHT = 16
ENEMY_SPEED = 3 * 30 / FPS_ACTUAL

MUSIC_ON = False

# object lists
enemy_list = []
bullet_list = []
blast_list = []
enemy_bullet_list = []
power_ups_list = []
score_text_list = []
enemy_shield_list = []

all_object_lists = [
    enemy_list,
    bullet_list,
    blast_list,
    enemy_bullet_list,
    power_ups_list,
    score_text_list,
    enemy_shield_list,
]