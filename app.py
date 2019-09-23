from flask import Flask, render_template, request, redirect, url_for
from random import randrange, choice
from copy import deepcopy

app = Flask(__name__)

size = 20
word_list = []

def horizontal_forward(word):
    while True:
        collision = False
        y = randrange(0, size)
        x = randrange(0, size - len(word) + 1)
        for i in range(len(word)):
            if grid[y][x + i] != '_' and grid[y][x + i] != word[i]:
                collision = True
                print("collision")
                break
        if collision is False:
            print("found a spot")
            break
    for count, letter in enumerate(word):
        grid[y][x + count] = letter
def horizontal_backward(word):
    while True:
        collision = False
        y = randrange(0, size)
        x = randrange(len(word), size)
        for i in range(len(word)):
            if grid[y][x - i] != '_' and grid[y][x - i] != word[i]:
                collision = True
                print("collision")
                break
        if collision is False:
            print("found a spot")
            break
    for count, letter in enumerate(word):
        grid[y][x - count] = letter
def vertical_down(word):
    while True:
        collision = False
        y = randrange(0, size - len(word) + 1)
        x = randrange(0, size)
        for i in range(len(word)):
            if grid[y + i][x] != '_' and grid[y + i][x] != word[i]:
                collision = True
                print("collision")
                break
        if collision is False:
            print("found a spot")
            break
    for count, letter in enumerate(word):
        grid[y + count][x] = letter
def vertical_up(word):
    while True:
        collision = False
        y = randrange(len(word), size)
        x = randrange(0, size)
        for i in range(len(word)):
            if grid[y - i][x] != '_' and grid[y - i][x] != word[i]:
                collision = True
                print("collision")
                break
        if collision is False:
            print("found a spot")
            break
    for count, letter in enumerate(word):
        grid[y - count][x] = letter
def diagonal_up(word):
    while True:
        collision = False
        y = randrange(len(word), size)
        x = randrange(0, size - len(word) + 1)
        for i in range(len(word)):
            if grid[y - i][x + i] != '_' and grid[y - i][x + i] != word[i]:
                collision = True
                print("collision")
                break
        if collision is False:
            print("found a spot")
            break
    for count, letter in enumerate(word):
        grid[y - count][x + count] = letter
def diagonal_down(word):
    while True:
        collision = False
        y = randrange(0, size - len(word) + 1)
        x = randrange(0, size - len(word) + 1)
        for i in range(len(word)):
            if grid[y + i][x + i] != '_' and grid[y + i][x+ i] != word[i]:
                collision = True
                print("collision")
                break
        if collision is False:
            print("found a spot")
            break
    for count, letter in enumerate(word):
        grid[y + count][x + count] = letter
def randomizer():
    placement_functions = [vertical_down] * 4 + [vertical_up] * 1 + [diagonal_up] * 2 + [diagonal_down] * 2 + [horizontal_backward] * 1 + [horizontal_forward] * 4
    for word in word_list:
        choice(placement_functions)(word)
def fill_in_the_blanks():
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in range(size):
        for j in range(size):
            if grid[i][j] == '_':
                grid[i][j] = choice(alpha)
def initialize_grid():
    for i in range(size):
        for j in range(size):
            grid[i][j] = '_'
def populate_puzzle(new_word_list):
    if 'grid' in globals():
        initialize_grid()
    else:
        global grid
        grid = [ [ '_' for i in range(size)] for j in range(size)]
    word_list.clear()
    word_list.extend(new_word_list)
    randomizer()
    global answer_grid
    answer_grid = deepcopy(grid)
    fill_in_the_blanks()

@app.route('/', methods=['POST', 'GET'])
def input_words():
    if request.method == 'POST':
        words = request.form.get("words").upper()
        populate_puzzle(sorted(words.split(), key=len, reverse=True))
        return render_template("home2.html")
    return render_template("home.html")

@app.route('/puzzle', strict_slashes=False)
def puzzle():
    return render_template("puzzle.html", puzzle=grid, words=word_list)
    
@app.route('/answer', strict_slashes=False)
def answer():
    return render_template('puzzle.html', puzzle=answer_grid, words=word_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug='true')