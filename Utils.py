import pygame as pg
import math

def vector2ToArray(vec):
    return [vec.x, vec.y]

def arrayToVector2(array):
    return pg.Vector2(array[0], array[1])

def serializeVector2Array(array):
    newArray = []
    for vec in array:
        newArray.append(vector2ToArray(vec))
    return newArray

def deserializeVector2Array(array):
    newArray = []
    for vec in array:
        newArray.append(arrayToVector2(vec))
    return newArray

def angle_between(p1, p2, p3):
    # Calculate angle between three points
    a = math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
    b = math.sqrt((p3.x - p2.x)**2 + (p3.y - p2.y)**2)
    c = math.sqrt((p3.x - p1.x)**2 + (p3.y - p1.y)**2)
    # Avoid division by zero
    if a * b == 0:
        return 180  # Straight line
    angle = math.acos((a**2 + b**2 - c**2) / (2 * a * b))
    return math.degrees(angle)