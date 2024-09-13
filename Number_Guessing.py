from random import randint

print("Welcome to number Guessing Game ")
print("You only have 10 guesses. Let's Start!")
num = randint(0, 1000)
guesses = 0
while True:
    guess = int(input("Guess a number between 0 and 1000: "))
    if guess == num:
        print(f"Congratulations you guessed correctly in {guess} guesses")
        break
    elif guess > num:
        print("Too high, try again")
    else:
        print("Too low, try again")
    guesses += 1
    if guesses == 10:
        break
print(f"The Number was {num}")
