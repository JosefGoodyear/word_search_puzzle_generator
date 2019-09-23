from flask import Flask, render_template, request, session
from flask_session import Session
from random import randrange, choice
from copy import deepcopy


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(__name__)
Session(app)



def horizontal_forward(word):
    """ Place a word horizontally, from left to right """
    attempt = 0
    while attempt < 10:
        attempt += 1
        collision = False
        y = randrange(0, session.get('size'))
        x = randrange(0, session.get('size') - len(word) + 1)
        for i in range(len(word)):
            if grid[y][x + i] != '_' and grid[y][x + i] != word[i]:
                collision = True
                break
        if collision is False:
            break
    if attempt == 10:
        return False
    for count, letter in enumerate(word):
        grid[y][x + count] = letter
    return True


def horizontal_backward(word):
    """ Place a word horizontally, from right to left"""
    attempt = 0
    while attempt < 10:
        attempt += 1
        collision = False
        y = randrange(0, session.get('size'))
        x = randrange(len(word), session.get('size'))
        for i in range(len(word)):
            if grid[y][x - i] != '_' and grid[y][x - i] != word[i]:
                collision = True
                break
        if collision is False:
            break
    if attempt == 10:
        return False
    for count, letter in enumerate(word):
        grid[y][x - count] = letter
    return True


def vertical_down(word):
    """ Place a word vertically, from top to bottom """
    attempt = 0
    while attempt < 10:
        attempt += 1
        collision = False
        y = randrange(0, session.get('size') - len(word) + 1)
        x = randrange(0, session.get('size'))
        for i in range(len(word)):
            if grid[y + i][x] != '_' and grid[y + i][x] != word[i]:
                collision = True
                break
        if collision is False:
            break
    if attempt == 10:
        return False
    for count, letter in enumerate(word):
        grid[y + count][x] = letter
    return True


def vertical_up(word):
    """ Place a word vertically, from bottom to top """
    attempt = 0
    while attempt < 10:
        attempt += 1
        collision = False
        y = randrange(len(word), session.get('size'))
        x = randrange(0, session.get('size'))
        for i in range(len(word)):
            if grid[y - i][x] != '_' and grid[y - i][x] != word[i]:
                collision = True
                break
        if collision is False:
            break
    if attempt == 10:
        return False
    for count, letter in enumerate(word):
        grid[y - count][x] = letter
    return True


def diagonal_up(word):
    """ Place a word diagonally, from bottom-left to top-right """
    attempt = 0
    while attempt < 10:
        attempt += 1
        collision = False
        y = randrange(len(word), session.get('size'))
        x = randrange(0, session.get('size') - len(word) + 1)
        for i in range(len(word)):
            if grid[y - i][x + i] != '_' and grid[y - i][x + i] != word[i]:
                collision = True
                break
        if collision is False:
            break
    if attempt == 10:
        return False
    for count, letter in enumerate(word):
        grid[y - count][x + count] = letter
    return True


def diagonal_down(word):
    """ Place a word diagonally, from top-left to bottom-right"""
    attempt = 0
    while attempt < 10:
        attempt += 1
        collision = False
        y = randrange(0, session.get('size') - len(word) + 1)
        x = randrange(0, session.get('size') - len(word) + 1)
        for i in range(len(word)):
            if grid[y + i][x + i] != '_' and grid[y + i][x+ i] != word[i]:
                collision = True
                break
        if collision is False:
            break
    if attempt == 10:
        return False
    for count, letter in enumerate(word):
        grid[y + count][x + count] = letter
    return True


def randomizer():
    """Randomly choose a placement function, weighted by placement_functions. If placement fails, return False"""
    placement_functions = [vertical_down] * 4 + [vertical_up] * 1 + [diagonal_up] * 2 + [diagonal_down] * 2 + [horizontal_backward] * 1 + [horizontal_forward] * 4
    for word in session.get('word_list'):
        status = choice(placement_functions)(word)
        if status is False:
            return False
    return True


def fill_in_the_blanks():
    """ Fill in random letters for empty squares in grid"""
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in range(session.get('size')):
        for j in range(session.get('size')):
            if grid[i][j] == '_':
                grid[i][j] = choice(alpha)


def initialize_grid():
    """ Replace all letters in grid with '_' """
    for i in range(session.get('size')):
        for j in range(session.get('size')):
            grid[i][j] = '_'


def populate_puzzle(new_word_list):
    """ Populate the grid and answer_grid """
    if 'grid' in globals():
        initialize_grid()
    else:
        global grid
        grid = [['_' for i in range(session.get('size'))] for j in range(session.get('size'))]
    session.get('word_list').clear()
    session.get('word_list').extend(new_word_list)
    status = randomizer()
    if status is False:
        return False
    global answer_grid
    answer_grid = deepcopy(grid)
    fill_in_the_blanks()
    return True


@app.route('/', methods=['POST', 'GET'])
def input_words():
    """ Take words from user and return links to a
    word search puzzle and answer key, or an error message"""
    session['size'] = 20
    session['word_list'] = []
    if request.method == 'POST':
        words = request.form.get('words').upper()
        new_word_list = words.split()
        for word in new_word_list:
            if len(word) > session.get('size'):
                return render_template('error.html')
        status = populate_puzzle(sorted(new_word_list, key=len, reverse=True))
        if status is False:
            return render_template('error_2.html')
        return render_template('home2.html')
    return render_template('home.html')


@app.route('/puzzle', strict_slashes=False)
def puzzle():
    """ Get the generated word search puzzle """
    return render_template('puzzle.html', puzzle=grid, words=session.get('word_list'))


@app.route('/answer', strict_slashes=False)
def answer():
    """ Get the generated answer key s"""
    return render_template('puzzle.html', puzzle=answer_grid, words=session.get('word_list'))

""" disable app.run for deployment with gunicorn """
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug='true')
