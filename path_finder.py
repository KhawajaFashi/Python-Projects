import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"],
]


def print_maze(maze, stdscr, path=[]):
    blue_black = curses.color_pair(1)
    red_black = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 2, "X", red_black)
            else:
                stdscr.addstr(i, j * 2, value, blue_black)


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j


def path_finder(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)
    q = queue.Queue()
    q.put((start_pos, [start_pos]))
    visited = set()
    while not q.empty():
        current_pos, curr_path = q.get()
        row, col = current_pos
        stdscr.clear()
        print_maze(maze, stdscr, curr_path)
        time.sleep(0.3)
        stdscr.refresh()

        if maze[row][col] == end:
            return curr_path
        neighbors = find_neighbours(maze, row, col)
        for neighbor in neighbors:
            r, c = neighbor
            if neighbor in visited or maze[r][c] == "#":
                continue
            new_path = curr_path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)


def find_neighbours(maze, row, col):
    neighbors = []
    if row > 0:  # UP
        neighbors.append((row - 1, col))
    if col > 0:  # Right
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # Left
        neighbors.append((row, col + 1))
    if row + 1 < len(maze):  # Down
        neighbors.append((row + 1, col))
    return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    path_finder(maze, stdscr)
    stdscr.getch()


wrapper(main)
