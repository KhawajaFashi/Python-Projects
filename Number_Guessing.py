from random import randint

print("\nWelcome to number Guessing Game\n")
print("\nYou only have 10 guesses. Let's Start!\n")
num = randint(0, 1000)
guesses = 0
while True:
    guess = int(input("Guess a number between 0 and 1000: "))
    if guess == num:
        print(f"Congratulations you guessed correctly in {guesses} guesses")
        break
    elif guess > num:
        print("Too high, try again")
    else:
        print("Too low, try again")
    guesses += 1
    if guesses == 10:
        break
print(f"The Number was {num}")
