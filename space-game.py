import asyncio
import time
import curses


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        canvas.refresh()
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        canvas.refresh()
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        await asyncio.sleep(0)


def draw(canvas):
    row, column = (5, 20)
    coroutine = blink(canvas, row, column, symbol='*')
    while True:
        curses.curs_set(False)
        coroutine.send(None)
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
