import asyncio
import random
import time
import curses

TIC_TIMEOUT = 0.1


async def blink(canvas, row, column, symbol):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(10):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(4):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


def create_stars_parameters(signs, max_y, max_x, stars_number):
    star_params = []
    for _ in range(stars_number):
        generated_x = random.randint(1, max_x - 1)
        generated_y = random.randint(1, max_y - 1)
        chosen_sign = random.choice(signs)
        star_params.append([generated_y, generated_x,  chosen_sign])
    return star_params


def draw(canvas):
    stars_number = 50
    signs = ['+', '*', '.', ':']
    max_y, max_x = canvas.getmaxyx()
    star_params = create_stars_parameters(signs, max_y, max_x, stars_number)
    coroutines = [blink(canvas, row, column, symbol) for row, column, symbol in star_params]
    while True:
        for coroutine in coroutines.copy():
            curses.curs_set(False)
            coroutine.send(None)
            canvas.refresh()
            canvas.border()
        time.sleep(0.1)
        # canvas.border()
        # canvas.addstr(row, column, '*', curses.A_DIM)
        # canvas.refresh()
        # time.sleep(2)
        # canvas.refresh()
        # canvas.addstr(row, column, '*')
        # time.sleep(0.3)
        # canvas.refresh()
        # canvas.addstr(row, column, '*', curses.A_BOLD)
        # canvas.refresh()
        # time.sleep(0.5)
        # canvas.addstr(row, column, '*')
        # time.sleep(0.3)


def main():
    curses.update_lines_cols()
    curses.wrapper(draw)



if __name__ == '__main__':
    main()
