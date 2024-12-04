# Imports
import pygame as p
import tkinter


# Initialise pygame
p.init()

SCREEN = p.display.set_mode((0, 0))

root = tkinter.Tk()
root.winfo_screenwidth()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
root.destroy()


# Needed
NORTH = 0
NORTHEAST = 1
EAST = 2
SOUTHEAST = 3
SOUTH = 4
SOUTHWEST = 5
WEST = 6
NORTHWEST = 7


# Controllers
PLAYER_SIZE = 64
MAX_JUMPS = 2
JUMP_COOLDOWN = 0.3
DASH_COOLDOWN = 1
SHOOT_COOLDOWN = 1
BULLET_LIFESPAN = 5
PLAYER_SPEED = 500
GRAVITY = 2700
JUMP_AMOUNT_PLATFORM = 1600
FRICTION = 0.98
TARGET_FPS = 300
BULLET_SPEED = 1200
VELOCITY_THRESHOLD = 3
POWERUP_TIME = 15
