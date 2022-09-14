from enum import Enum


class OrientationEnum(str, Enum):
    portrait = "portrait"
    landscape = "landscape"
    squarish = "squarish"


class ColorEnum(str, Enum):
    black_and_white = "black_and_white"
    black = "black"
    white = "white"
    yellow = "yellow"
    orange = "orange"
    red = "red"
    purple = "purple"
    magenta = "magenta"
    green = "green"
    teal = "teal"
    blue = "blue"
