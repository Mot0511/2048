import random
from tkinter import *
import datetime, time

SIZE = 400
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = '#92877d'
BACKGROUND_COLOR_CELL_EMPTY = '#9e948a'

BACKGROUND_COLOR_DICT = {2: "#eee4da",
4: "#ede0c8", 8: "#f2b179",
 16: "#f59563",
32: "#f67c5f", 64: "#f65e3b",
 128: "#edcf72",
256: "#edcc61", 512: "#edc850",
 1024: "#edc53f",
2048: "#edc22e"}

CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65",
8: "#f9f6f2", 16: "#f9f6f2",
 32: "#f9f6f2", 64: "#f9f6f2",
128: "#f9f6f2", 256: "#f9f6f2", 512:
"#f9f6f2", 1024: "#f9f6f2",
 2048: "#f9f6f2"}

FONT = ("Verdana", 40, "bold")
KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"
KEY_BACK = "'b'"

mainframe = Frame()
grid_cells = []
matrix = []

label = Label()

score = 0

can_back = True
state = 'lose'
def init_grid():
    global score
    background = Frame(bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
    background.grid()

    for i in range(GRID_LEN):
        grid_row = []
        for j in range(GRID_LEN):
            cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
            cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
            t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY,justify=CENTER, font=FONT, width=5,height=2)
            t.grid()
            grid_row.append(t)

        global label
        label = Label(background, text=score, bg=BACKGROUND_COLOR_GAME, font=('Arial Bold', 50))
        label.grid(column=1, row=4)

        grid_cells.append(grid_row)


def init_matrix():
    for i in range(GRID_LEN):
        matrix.append([0] * GRID_LEN)

    r_num = random.randint(0, 5)
    if r_num == 2:
        add_four()
        add_four()
    else:
        add_two()
        add_two()



def add_four():
    a = random.randint(0, len(matrix) - 1)
    b = random.randint(0, len(matrix) - 1)

    while (matrix[a][b] != 0):
        a = random.randint(0, len(matrix) - 1)
        b = random.randint(0, len(matrix) - 1)

    matrix[a][b] = 4


def add_two():
    a = random.randint(0, len(matrix)-1)
    b = random.randint(0, len(matrix)-1)

    while(matrix[a][b] != 0):
        a = random.randint(0, len(matrix)-1)
        b = random.randint(0, len(matrix)-1)

    matrix[a][b] = 2

def update_grid_cells():
    for i in range(GRID_LEN):
        for j in range(GRID_LEN):
            if matrix[i][j] == 0:
                grid_cells[i][j].configure(text="",
                bg=BACKGROUND_COLOR_CELL_EMPTY)
            else:
                grid_cells[i][j].configure(text=str(matrix[i][j]), bg=BACKGROUND_COLOR_DICT[matrix[i][j]], fg=CELL_COLOR_DICT[matrix[i][j]])

def cover_up(mat):
    new = []
    for i in range(len(mat)):
        new.append([0] * len(mat))
    done = False
    for i in range(len(mat)):
        count = 0
        for j in range(len(mat)):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return (new, done)


def merge(mat):
    done = False
    for i in range(len(mat)):
        for j in range(len(mat)-1):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                global score
                score += mat[i][j]
                label.configure(text=score)
                mat[i][j+1] = 0
                done = True

    return (mat, done)

def left():
    global matrix
    global save
    save = matrix
    matrix, done = cover_up(matrix)
    temp = merge(matrix)
    matrix = temp[0]
    done = done or temp[1]
    matrix = cover_up(matrix)[0]
    return done

def right():
    global matrix
    global save
    save = matrix
    matrix = reverse(matrix)
    matrix, done = cover_up(matrix)
    temp = merge(matrix)
    matrix = temp[0]
    done = done or temp[1]
    matrix = cover_up(matrix)[0]
    matrix = reverse(matrix)
    return done

def up():
    global matrix
    global save
    save = matrix
    matrix = transpose(matrix)
    matrix, done = cover_up(matrix)
    temp = merge(matrix)
    matrix = temp[0]
    done = done or temp[1]
    matrix = cover_up(matrix)[0]
    matrix = transpose(matrix)
    return done

def down():
    global matrix
    global save
    save = matrix
    matrix = reverse(transpose(matrix))
    matrix, done = cover_up(matrix)
    temp = merge(matrix)
    matrix = temp[0]
    done = done or temp[1]
    matrix = cover_up(matrix)[0]
    matrix = transpose(reverse(matrix))
    return done

def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new

def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new

def game_state():
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 2048:
                return 'win'

    for i in range(len(matrix)-1):
        for j in range(len(matrix[0])-1):
            if matrix[i][j] == matrix[i+1][j] or matrix[i][j+1] == matrix[i][j]:
                return 'not over'

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                return 'not over'
        for k in range(len(matrix) - 1):
            if matrix[len(matrix) - 1][k] == matrix[len(matrix) - 1][k + 1]:
                return 'not over'
        for j in range(len(matrix) - 1):
            if matrix[j][len(matrix) - 1] == matrix[j + 1][len(matrix) - 1]:
                return 'not over'
    return 'lose'


def key_down(event):
    global can_back
    key = repr(event.char)
    if key in mainframe.commands:
        done = mainframe.commands[repr(event.char)]()
        if done:
            r_num = random.randint(0, 5)
            if r_num == 2:
                add_four()
            else:
                add_two()
            update_grid_cells()
            if game_state() == 'win':
                global score
                grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                grid_cells[1][2].configure(text="Win!", bg=BACKGROUND_COLOR_CELL_EMPTY)
                grid_cells[2][1].configure(text="Score:", bg=BACKGROUND_COLOR_CELL_EMPTY)
                grid_cells[2][2].configure(text=score, bg=BACKGROUND_COLOR_CELL_EMPTY)
                can_back = False

            if game_state() == 'lose':
                # ?????????? ??????????????????
                grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                grid_cells[1][2].configure(text="Lose!", bg = BACKGROUND_COLOR_CELL_EMPTY)
                grid_cells[2][1].configure(text="Score:", bg=BACKGROUND_COLOR_CELL_EMPTY)
                grid_cells[2][2].configure(text=score, bg=BACKGROUND_COLOR_CELL_EMPTY)
                can_back = False

def step_back():
    if can_back:
        global matrix
        matrix = save
        update_grid_cells()

# def start_timer():
#     global can_back
#     timing = time.time()
#     while True:
#         if time.time() - timing > 1.0:
#             timing = time.time()
#             break

def main():
    init_grid()
    init_matrix()
    update_grid_cells()
    left()
    for row in matrix:
        print(' '.join([str(elem) for elem in row]))

    mainframe.master.title('2048')
    mainframe.master.bind("<Key>", key_down)
    mainframe.commands = {KEY_UP: up, KEY_DOWN: down, KEY_LEFT: left, KEY_RIGHT: right, KEY_BACK: step_back}
    mainloop()


if __name__ == '__main__':
    main()

