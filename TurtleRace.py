import turtle
import time
import random


WIDTH, HEIGHT = 700, 600
COLORS = [
    "red",
    "orange",
    "green",
    "blue",
    "yellow",
    "black",
    "cyan",
    "purple",
    "pink",
    "brown",
]


def init_turtle():
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title("Turtle Racing")


def get_number_of_racers():
    racers = 0
    while True:
        racers = input("Enter the number of turtles you want to race(2 - 10): ")
        if not racers.isdigit():
            print("Invalid input. Please enter a number.")
            continue
        else:
            racers = int(racers)
            if 2 <= racers <= 10:
                return racers
            else:
                print("Invalid input. Please enter a number between 2 and 10.")


def create_turtles(colors):
    turtles = []
    spacingx = WIDTH // (len(colors) + 1)
    for i, color in enumerate(colors):
        t = turtle.Turtle()
        t.color(color)
        t.shape("turtle")
        t.penup()
        t.left(90)
        t.setpos(-WIDTH // 2 + (i + 1) * spacingx, -HEIGHT // 2 + 20)
        t.pendown()
        turtles.append(t)
    return turtles


def race(colors):
    turtles = create_turtles(colors)
    while True:
        for racer in turtles:
            distance = random.randrange(1, 20)
            racer.forward(distance)

            x, y = racer.pos()
            if y >= HEIGHT // 2 - 10:
                return colors[turtles.index(racer)]


racers = get_number_of_racers()
init_turtle()
random.shuffle(COLORS)
colors = COLORS[:racers]

winner = race(colors)
print(f"The winner is turtle with color {winner}!")
time.sleep(4)
