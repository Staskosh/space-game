import asyncio
import curses
import os
import random
import time
from itertools import cycle

from dotenv import load_dotenv

from curses_tools import draw_frame, get_frame_size, read_controls

TIC_TIMEOUT = 0.1


async def animate_spaceship(canvas, animations, border, max_row, max_column, row, column):
    for frame in cycle(animations):
        frame_row_numbers, frame_column_numbers = get_frame_size(frame)
        changed_row, changed_column, changed_pushed = read_controls(canvas)

        if changed_row == -1 and border < row < max_row - border:
            row += changed_row
        if changed_row == 1 and row + frame_row_numbers < max_row - border:
            row += changed_row
        if changed_column == -1 and border < column < max_column + border:
            column += changed_column
        if changed_column == 1 and column + frame_column_numbers < max_column - border:
            column += changed_column

        draw_frame(canvas, row, column, frame)
        time.sleep(0.03)
        await asyncio.sleep(0)

        draw_frame(canvas, row, column, frame, negative=True)


async def blink(canvas, row, column, symbol):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(random.randint(0, 20)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(random.randint(0, 8)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(random.randint(0, 10)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(random.randint(0, 8)):
            await asyncio.sleep(0)


def create_stars_parameters(signs, max_y, max_x, stars_number):
    star_params = []
    for _ in range(stars_number):
        generated_x = random.randint(1, max_x - 1)
        generated_y = random.randint(1, max_y - 1)
        chosen_sign = random.choice(signs)
        star_params.append([generated_y, generated_x, chosen_sign])
    return star_params


def get_animations(animations_directory):
    animations = []
    for filename in os.listdir(animations_directory):
        with open(f'{animations_directory}/{filename}', 'r', encoding='KOI8-R') as file:
            animation = file.read()
        animations.append(animation)

    return animations


def draw(canvas):
    border = 1
    animations_directory = 'animation_files'
    curses.curs_set(False)
    canvas.nodelay(True)
    height, width = canvas.getmaxyx()  # getmaxyx returns the height, width of window
    stars_number = 50
    signs = '+*.:'
    star_params = create_stars_parameters(signs, height, width, stars_number)
    coroutines = [blink(canvas, row, column, symbol)
                  for row, column, symbol in star_params]

    animations = get_animations(animations_directory)
    start_row = height // 3
    start_column = width // 2
    coroutines.append(animate_spaceship(
        canvas, animations, border, height, width, row=start_row, column=start_column
    ))
    while True:
        try:
            for coroutine in coroutines.copy():
                canvas.border()
                coroutine.send(None)
                canvas.refresh()
        except StopIteration:
            coroutines.remove(coroutine)
        time.sleep(TIC_TIMEOUT)


def main():
    load_dotenv()
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == '__main__':
    main()
