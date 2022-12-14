import asyncio
import curses
import os
import random
import time
from itertools import cycle

from curses_tools import draw_frame, get_frame_size, read_controls

TIC_TIMEOUT = 0.1


async def fill_orbit_with_garbage(canvas, coroutines, garbage_animations):
    rows_number, columns_number = canvas.getmaxyx()
    while True:
        coroutines.append(
            fly_garbage(
                canvas,
                column=random.randint(0, columns_number),
                garbage_frame=random.choice(garbage_animations),
                speed=random.randint(1, 2)
            )
        )
        await count_delay(0.3)


async def fly_garbage(canvas, column, garbage_frame, speed):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def count_delay(seconds):
    for _ in range(int(seconds * 10)):
        await asyncio.sleep(0)


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

        await count_delay(0.3)

        draw_frame(canvas, row, column, frame, negative=True)


async def blink(canvas, row, column, symbol, offset_tics):
    while True:
        if offset_tics == 0:
            canvas.addstr(row, column, symbol, curses.A_DIM)
            await count_delay(2)
            offset_tics += 1

        if offset_tics == 1:
            canvas.addstr(row, column, symbol)
            await count_delay(0.3)
            offset_tics += 1

        if offset_tics == 2:
            canvas.addstr(row, column, symbol, curses.A_BOLD)
            await count_delay(0.5)
            offset_tics += 1

        if offset_tics == 3:
            canvas.addstr(row, column, symbol)
            await count_delay(0.3)
            offset_tics = 0


def create_stars_parameters(signs, max_y, max_x, stars_number):
    star_params = []
    for _ in range(stars_number):
        row = random.randint(1, max_y - 1)
        column = random.randint(1, max_x - 1)
        symbol = random.choice(signs)
        star_params.append([row, column, symbol])
    return star_params


def get_animations(animations_directory, animation_numbers):
    animations = []
    for filename in os.listdir(animations_directory):
        with open(f'{animations_directory}/{filename}', 'r', encoding='KOI8-R') as file:
            animation = file.read()
        for animation_number in range(animation_numbers):
            animations.append(animation)

    return animations


def draw(canvas):
    border = 1
    animations_directory = 'animation_files'
    garbage_animations = 'animation_garbage'
    curses.curs_set(False)
    canvas.nodelay(True)
    height, width = canvas.getmaxyx()  # getmaxyx returns the height, width of window
    stars_number = 50
    signs = '+*.:'
    star_params = create_stars_parameters(signs, height, width, stars_number)
    coroutines = [blink(canvas, row, column, symbol, random.randint(0, 3))
                  for row, column, symbol in star_params]
    garbage_animations = get_animations(garbage_animations, 1)
    coroutines.append(fill_orbit_with_garbage(canvas, coroutines, garbage_animations))
    spaceship_animations = get_animations(animations_directory, 2)
    start_row = height // 3
    start_column = width // 2
    coroutines.append(animate_spaceship(
        canvas, spaceship_animations, border, height, width, row=start_row, column=start_column
    ))
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.border()
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def main():
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == '__main__':
    main()
