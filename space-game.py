import asyncio
import time
import curses


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


def draw(canvas):
    row, column = (5, 20)
    first_coroutine = blink(canvas, row, column, symbol='*')
    second_coroutine = blink(canvas, row=5, column=10, symbol='*')
    third_coroutine = blink(canvas, row=5, column=15, symbol='*')
    fourth_coroutine = blink(canvas, row=5, column=5, symbol='*')
    fifth_coroutine = blink(canvas, row=5, column=0, symbol='*')
    coroutines = [
        first_coroutine,
        second_coroutine,
        third_coroutine,
        fourth_coroutine,
        fifth_coroutine
    ]
    while True:
        for coroutine in coroutines.copy():
            curses.curs_set(False)
            coroutine.send(None)
            canvas.refresh()
        time.sleep(1)
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


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
    curses.curs_set(False)
