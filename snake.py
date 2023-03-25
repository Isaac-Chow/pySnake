from tkinter import *
from random import randint

root = Tk()
root.config(bg='black')
root.geometry('800x800')
root.title('Immortal Snake Game')
root.resizable(0, 0)

c = Canvas(root, width=800, height=800, bg='black')
c.place(x=0, y=0)

box = 20
direction = 'DOWN'

snakehead = [240, 240]
food = [int((randint(0, 400))/20)*20,
        int((randint(0, 400))/20)*20]
snake_pos = [[240, 240], [240, 230], [240, 220]]


def draw_snake():
    for position in snake_pos:
        c.create_rectangle(position[0], position[1],
                           position[0]+20, position[1]+20,
                           fill='red')
        c.create_rectangle(snakehead[0], snakehead[1],
                           snakehead[0]+20, snakehead[1]+20,
                           fill='green')


def show_food():
    global food
    c.create_rectangle(food[0], food[1],
                       food[0]+20, food[1]+20,
                       fill='blue')
    if snakehead == food:
        food = [int((randint(0, 400))/20)*20,
                int((randint(0, 400))/20)*20]
        snake_pos.append(food)


def left(e):
    global direction
    direction = 'LEFT'


def right(e):
    global direction
    direction = 'RIGHT'


def up(e):
    global direction
    direction = 'UP'


def down(e):
    global direction
    direction = 'DOWN'


root.bind('<Up>', up)
root.bind('<Down>', down)
root.bind('<Left>', left)
root.bind('<Right>', right)


def detect_move():
    global direction
    global snakehead
    global snake_pos

    if direction == 'DOWN':
        if snakehead[1] == 800:
            snakehead[1] = 0
        else:
            snakehead[1] += box
        snake_pos.insert(0, list(snakehead))
        snake_pos.pop()

    if direction == 'UP':
        if snakehead[1] == 0:
            snakehead[1] = 800
        else:
            snakehead[1] -= box
        snake_pos.insert(0, list(snakehead))
        snake_pos.pop()

    if direction == 'LEFT':
        if snakehead[0] == 0:
            snakehead[0] = 800
        else:
            snakehead[0] -= box
        snake_pos.insert(0, list(snakehead))
        snake_pos.pop()

    if direction == 'RIGHT':
        if snakehead[0] == 800:
            snakehead[0] = 0
        else:
            snakehead[0] += box
        snake_pos.insert(0, list(snakehead))
        snake_pos.pop()


run = True


def update():
    detect_move()
    c.delete('all')
    show_food()
    draw_snake()
    root.update()
    root.after(50, update)


update()
root.mainloop()
