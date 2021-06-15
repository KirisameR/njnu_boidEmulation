import pygame, random
import tkinter as tk
from tkinter import *
import os
import platform

root = tk.Tk()
embed = tk.Frame(root, width=500, height=500)  # creates embed frame for pygame window

embed.focus_set()
embed.grid(column=0, row=0)  # Adds grid

uiwin = tk.Frame(root, width=400, height=100)
uiwin.grid(row=1, column=0)

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())

if platform.system == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'

pygame.init()
screen = pygame.display.set_mode((500, 500))
screen.fill(pygame.Color(255, 255, 255))

pygame.display.update()


def handle(event):
    if embed is not root.focus_get():
        embed.focus_set()


embed.bind('<Enter>', handle)


def game():
    if embed is root.focus_get():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                screen.fill(pygame.Color(r, g, b))
                pygame.display.update()
    root.after(1000 // 60, game)


def draw():
    pygame.draw.circle(screen, (0, 0, 0), (250, 250), 125)
    pygame.display.update()


button1 = Button(uiwin, text='Draw', command=draw)
button1.grid(row=0, column=1)

entry1 = Entry(uiwin, width=45, font=('StSong', 14), foreground='green')
entry1.grid(row=0, column=0)

root.after(0, game)
root.mainloop()
