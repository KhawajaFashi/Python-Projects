from random import randint

print("Welcome to number Guessing Game ")
num = randint(0, 1000)
guesses = 0
while True:
    guess = int(input("Guess a number between 0 and 1000: "))
    if guess == num:
        print("Congratulations you guessed correctly You Won!")
        break
    elif guess > num:
        print("Too high, try again")
    else:
        print("Too low, try again")
    guesses += 1
    if guesses == 10:
        break
print(f"The Number was {num}")
