import asyncio
import os
import random
import time
import curses
from itertools import cycle

from dotenv import load_dotenv

from curses_tools import draw_frame, read_controls

TIC_TIMEOUT = 0.1


async def animate_spaceship(canvas, animations, start_row, start_column):
    while True:
        for frame in cycle(animations):
            changed_row, changed_column, changed_pushed = read_controls(canvas)
            start_row += changed_row
            start_column += changed_column
            draw_frame(canvas, start_row, start_column, frame)
            canvas.refresh()
            time.sleep(0.3)
            await asyncio.sleep(0)

            draw_frame(canvas, start_row, start_column, frame, negative=True)


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
        star_params.append([generated_y, generated_x,  chosen_sign])
    return star_params


def get_animations():
    animations_directory = os.getenv('ANIMATIONS_FOLDER')
    animations = []
    for file in os.listdir(animations_directory):
        with open(f'{animations_directory}/{file}', 'r', encoding='KOI8-R') as my_file:
            animation = my_file.read()
        animations.append(animation)

    return animations


def draw(canvas):
    stars_number = 50
    signs = ['+', '*', '.', ':']
    max_y, max_x = canvas.getmaxyx()
    animations = get_animations()
    star_params = create_stars_parameters(signs, max_y, max_x, stars_number)
    coroutines = [blink(canvas, row, column, symbol) for row, column, symbol in star_params]
    coroutines.append(animate_spaceship(canvas, animations, start_row=max_y//3, start_column=max_x//2))
    while True:
        try:
            for coroutine in coroutines.copy():
                canvas.refresh()
                canvas.nodelay(True)
                curses.curs_set(False)
                coroutine.send(None)
                canvas.refresh()
                canvas.border()
            time.sleep(TIC_TIMEOUT)
        except StopIteration:
            coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break


def main():
    load_dotenv()
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == '__main__':
    main()
