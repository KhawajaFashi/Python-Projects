import random

COLORS = ["Y", "G", "B", "W", "R", "O"]
TRIES = 10


def generate_code(colors):
    rand_code = []
    for i in range(4):
        rand_num = random.randrange(0, 6)
        rand_code.append(colors[rand_num])
    return rand_code


def check_code(correct_code, entered_code, correct_pos, wrong_pos):
    for i, code in enumerate(entered_code):
        if code in correct_code:
            if code == correct_code[i]:
                correct_pos += 1
            else:
                wrong_pos += 1
    return correct_pos, wrong_pos


def start_game(colors, correct_code):
    print(
        f"Welcome to Master Mind Game! You will have {TRIES} to guess the correct code"
    )
    print(
        f"You can guess the code using these codes: {' '.join(colors)}\nLet's Start the Game......\n"
    )
    for try_no in range(TRIES):
        enter_c = input("Enter Your 4 - letter code: ")
        entered_code = enter_c.split(" ")
        correct_position, wrong_position = check_code(correct_code, entered_code, 0, 0)
        print(
            f"Correct Position: {correct_position} | Incorrect Position: {wrong_position}"
        )
        if correct_position == 4:
            print(f"You have guessed the correct Word in {try_no+1}")
            break


def main():
    while True:
        correct_code = generate_code(COLORS)
        print(correct_code)
        start_game(COLORS, correct_code)
        check_input = input("Want to Play the Game(y/n): ")
        if check_input == "n":
            print("Exiting the Game!")
            break


if __name__ == "__main__":
    main()
