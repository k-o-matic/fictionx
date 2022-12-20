"""
Functions to handle score values.
"""

SCORE = 0


def get():
    """
    :return:    Score value
    """
    global SCORE
    return SCORE


def add(x: int):
    """
    :param x:   points to add to score
    :return:    None
    """
    global SCORE
    SCORE += x


def set(x):
    """
    :param x:   score is set to x
    :return:    None
    """
    global SCORE
    SCORE = x
