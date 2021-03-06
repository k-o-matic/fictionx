import pyxel
from random import randrange

class Letter:
    def __init__(self):
        # Animation Color List
        self.stripe_colors = [3,3,3,6,6,6,1,1]

        # charset data
        self.charset = {
            'A': ['00111000',
                  '01111100',
                  '11000110',
                  '11000110',
                  '11111110',
                  '11111110',
                  '11100110',
                  '00000000'],
            'B': ['11111100',
                  '11000110',
                  '11000110',
                  '11111100',
                  '11100110',
                  '11100110',
                  '11111100',
                  '00000000'],
            'C': ['01111100',
                  '11000110',
                  '11000000',
                  '11000000',
                  '11100000',
                  '11100110',
                  '01111100',
                  '00000000'],
            'D': ['11111100',
                  '11001110',
                  '11000110',
                  '11000110',
                  '11000110',
                  '11001110',
                  '11111100',
                  '00000000'],
            'E': ['11111110',
                  '11000000',
                  '11000000',
                  '11111000',
                  '11100000',
                  '11100000',
                  '11111110',
                  '00000000'],
            'F': ['11111110',
                  '11000000',
                  '11000000',
                  '11111000',
                  '11100000',
                  '11100000',
                  '11100000',
                  '00000000'],
            'G': ['01111100',
                  '11100110',
                  '11000000',
                  '11000000',
                  '11001110',
                  '11100110',
                  '01111100',
                  '00000000'],
            'H': ['11000110',
                  '11000110',
                  '11000110',
                  '11111110',
                  '11100110',
                  '11100110',
                  '11100110',
                  '00000000'],
            'I': ['01111100',
                  '00010000',
                  '00010000',
                  '00010000',
                  '00011000',
                  '00011000',
                  '01111100',
                  '00000000'],
            'J': ['11111110',
                  '00000110',
                  '00000110',
                  '00000110',
                  '11001110',
                  '11001110',
                  '01111100',
                  '00000000'],
            'K': ['11000110',
                  '11001100',
                  '11011000',
                  '11111000',
                  '11101100',
                  '11100110',
                  '11100110',
                  '00000000'],
            'L': ['11000000',
                  '11000000',
                  '11000000',
                  '11100000',
                  '11100000',
                  '11100000',
                  '11111110',
                  '00000000'],
            'M': ['11000110',
                  '11101110',
                  '11010110',
                  '11000110',
                  '11100110',
                  '11100110',
                  '11100110',
                  '00000000'],
            'N': ['11000110',
                  '11100110',
                  '11010110',
                  '11001110',
                  '11100110',
                  '11100110',
                  '11100110',
                  '00000000'],
            'O': ['01111100',
                  '11000110',
                  '11000110',
                  '11000110',
                  '11100110',
                  '11100110',
                  '01111100',
                  '00000000'],
            'P': ['11111100',
                  '11000110',
                  '11000110',
                  '11111100',
                  '11100000',
                  '11100000',
                  '11100000',
                  '00000000'],
            'Q': ['01111100',
                  '11000110',
                  '11000110',
                  '11000110',
                  '11011110',
                  '11000111',
                  '01111100',
                  '00000000'],
            'R': ['11111100',
                  '11000110',
                  '11000110',
                  '11111100',
                  '11111000',
                  '11101100',
                  '11100110',
                  '00000000'],
            'S': ['01111100',
                  '11000110',
                  '11000000',
                  '01111100',
                  '00001110',
                  '11001110',
                  '01111100',
                  '00000000'],
            'T': ['11111110',
                  '00110000',
                  '00110000',
                  '00110000',
                  '00111000',
                  '00111000',
                  '00111000',
                  '00000000'],
            'U': ['11000110',
                  '11000110',
                  '11000110',
                  '11000110',
                  '11100110',
                  '11100110',
                  '01111100',
                  '00000000'],
            'V': ['11000110',
                  '11000110',
                  '11100110',
                  '11101110',
                  '01111100',
                  '00111000',
                  '00010000',
                  '00000000'],
            'W': ['11100110',
                  '11100110',
                  '11100110',
                  '11000110',
                  '11010110',
                  '11101110',
                  '11000110',
                  '00000000'],
            'X': ['11000110',
                  '11000110',
                  '01101100',
                  '00111000',
                  '01101100',
                  '11000110',
                  '11000110',
                  '00000000'],
            'Y': ['11000110',
                  '11000110',
                  '01101100',
                  '00111000',
                  '00010000',
                  '00011000',
                  '00011000',
                  '00000000'],
            'Z': ['11111110',
                  '00000110',
                  '00001100',
                  '00111000',
                  '11100000',
                  '11100000',
                  '11111110',
                  '00000000'],
            '1': ['00001000',
                  '00011000',
                  '00111000',
                  '00011000',
                  '00011000',
                  '00011000',
                  '00111100',
                  '00000000'],
            '2': ['01111100',
                  '11000110',
                  '00001100',
                  '00111000',
                  '11100000',
                  '11100000',
                  '11111110',
                  '00000000'],
            '3': ['01111100',
                  '00000110',
                  '00000110',
                  '00111100',
                  '00001110',
                  '11001110',
                  '11111100',
                  '00000000'],
            '4': ['00110110',
                  '01100110',
                  '11000110',
                  '11111110',
                  '00000110',
                  '00001110',
                  '00001110',
                  '00000000'],
            '5': ['11111110',
                  '11000000',
                  '11000000',
                  '11111100',
                  '00001110',
                  '11001110',
                  '01111100',
                  '00000000'],
            '6': ['00011000',
                  '00110000',
                  '01100000',
                  '11111100',
                  '11100110',
                  '11100110',
                  '01111100',
                  '00000000'],
            '7': ['11111110',
                  '00000110',
                  '00001100',
                  '00011000',
                  '00110000',
                  '01100000',
                  '11000000',
                  '00000000'],
            '8': ['00111100',
                  '01100110',
                  '01100110',
                  '00111100',
                  '11100110',
                  '11100110',
                  '01111100',
                  '00000000'],
            '9': ['01111100',
                  '11100110',
                  '11100110',
                  '01111100',
                  '00011000',
                  '00110000',
                  '01100000',
                  '00000000'],
            '0': ['01111100',
                  '11000110',
                  '11001110',
                  '11010110',
                  '11100110',
                  '11100110',
                  '01111100',
                  '00000000'],
            ' ': ['00000000',
                  '00000000',
                  '00000000',
                  '00000000',
                  '00000000',
                  '00000000',
                  '00000000',
                  '00000000'],
            '.': ['00000000',
                  '00000000',
                  '00000000',
                  '00000000',
                  '00000000',
                  '00011000',
                  '00011000',
                  '00000000'],
            ',': ['00000000',
                  '00000000',
                  '00000000',
                  '00000000',
                  '00000000',
                  '00011000',
                  '00011000',
                  '00001000'],
            ':': ['00000000',
                  '00011000',
                  '00011000',
                  '00000000',
                  '00000000',
                  '00011000',
                  '00011000',
                  '00000000'],
            '!': ['00011000',
                  '00011000',
                  '00011000',
                  '00011000',
                  '00000000',
                  '00011000',
                  '00011000',
                  '00000000'],
            '?': ['00111100',
                  '01000010',
                  '00000100',
                  '00011000',
                  '00011000',
                  '00000000',
                  '00011000',
                  '00000000'],
            '+': ['00000000',
                  '00110000',
                  '00110000',
                  '11111100',
                  '11111100',
                  '00110000',
                  '00110000',
                  '00000000'],
            '-': ['00000000',
                  '00000000',
                  '00000000',
                  '01111100',
                  '01111100',
                  '00000000',
                  '00000000',
                  '00000000'],
            '*': ['00010000',
                  '01010100',
                  '00111000',
                  '11111110',
                  '00111000',
                  '01010100',
                  '00010000',
                  '00000000'],
            '/': ['00000011',
                  '00000110',
                  '00001100',
                  '00011000',
                  '00110000',
                  '01100000',
                  '11000000',
                  '00000000'],
            '=': ['00000000',
                  '00000000',
                  '01111100',
                  '00000000',
                  '01111100',
                  '00000000',
                  '00000000',
                  '00000000'],
            ')': ['00100000',
                  '00010000',
                  '00010000',
                  '00010000',
                  '00010000',
                  '00010000',
                  '00100000',
                  '00000000'],
            '(': ['00000100',
                  '00001000',
                  '00001000',
                  '00001000',
                  '00001000',
                  '00001000',
                  '00000100',
                  '00000000'],
            'h':    # heart
                ['01101100',
                 '11111110',
                 '11111110',
                 '01111100',
                 '00111000',
                 '00010000',
                 '00000000',
                 '00000000'],
            's':  # smiley
                ['00111100',
                 '01000010',
                 '10100101',
                 '10000001',
                 '10100101',
                 '10011001',
                 '01000010',
                 '00111100']
        }

    def update(self, fps=60):
        1 == 1
        # cycle through stipe colors of letter animation 5
        divider = round(fps/15)
        if divider > 0:
            if pyxel.frame_count % divider == 0:
                self.stripe_colors.append(self.stripe_colors[0])
                self.stripe_colors.pop(0)


    def draw(self, x: int, y: int, char: str, col=7, anm=0, inv=False):
        """
        :param x: x position
        :param y: y position
        :param char: Character to print out
        :param col: 0-15 => color code
        :param anm: 1 => pixel color chaos with all colors
                    2 => pixel color chaos with colors 3 - 6
                    3 => random color stripes on every frame
                    4 => flashing color for character on every frame
                    5 => scrolling color horizontal stripes
        :param inv: False (default): Character not inverted
                    True: Character inverted

        :return: None: Prints character on screen
        """

        self.char = self.charset[char]
        if anm == 4:
            col = randrange(3,6,1)
        if inv:
            pixel = '0'
        else:
            pixel = '1'
        for r, row in enumerate(self.char):
            if anm == 3:
                col = randrange(3,6,1)
            if anm == 5:
                col = self.stripe_colors[r]
            for c, bit in enumerate(row):
                if bit == pixel:
                    # random pixel color
                    if anm == 1:
                        col = randrange(1,16,1)
                    if anm == 2:
                        col = randrange(3,6,1)
                    pyxel.pset(x + c, y + r, col)

    def text(self, start_x:int, start_y: int, col, text='DUMMY TEXT'):
        # self.text1 = text
        self.x = start_x
        self.y = start_y
        self.read_animation = False
        self.color = col
        self.animation = 0
        inverted = False

        # Split text on line breaks into text list.
        text_rows = text.split('\n')

        for text_row in text_rows:
            # draw(self, x, y, char, col=7, anm=0, inv=False)
            for i, char in enumerate(text_row):

                # check and read animation tag
                if char == '|' and self.read_animation == False:
                    # read animation ON
                    self.read_animation = True
                    continue
                elif char != '|' and self.read_animation == True:
                    if char == 'i':
                        inverted = not inverted     # toggle inverted on or off
                    else:
                        self.animation = int(char)     # set animation
                elif char == '|' and self.read_animation == True:
                    # read animation ON
                    self.read_animation = False
                    continue
                else:
                    # draw character if it is part of charset
                    if char in self.charset:
                        self.draw(self.x, self.y, char, col, self.animation, inverted)
                        self.x += 8
            # set new line position
            self.y += 8
            self.x = start_x