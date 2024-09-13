from random import randint


def generateQuestion(choice):
    score = 0
    for i in range(choice):
        first = randint(1, 100)
        second = randint(1, 100)
        operator = randint(1, 4)
        while first == second:
            second = randint(1, 100)
        if operator == 1:
            ans = int(input(f"What is {first} + {second} ? "))
            if ans == first + second:
                print("Correct")
                score += 1
            else:
                print(f"Sorry, the correct answer is {first + second}")
        if operator == 2:
            ans = int(input(f"What is {first} - {second} ? "))
            if ans == first - second:
                print("Correct")
                score += 1
            else:
                print(f"Sorry, the correct answer is {first - second}")
        if operator == 3:
            ans = int(input(f"What is {first} * {second} ? "))
            if ans == first * second:
                print("Correct")
                score += 1
            else:
                print(f"Sorry, the correct answer is {first * second}")
        if operator == 4:
            print("\nWrite the integer part only\n")
            ans = int(input(f"What is {first} / {second} ? "))
            if ans == int(first / second):
                print("Correct")
                score += 1
            else:
                print(f"Sorry, the correct answer is {first / second}")
    return score


print("Welcome to Computer Quiz ")
print("-------------------------------")

choice = int(input("Choose a number between 5 to 10: "))
while choice < 5 or choice > 10:
    print("Invalid choice.")
    choice = int(input("Choose a number between 5 to 10: "))
score = generateQuestion(choice)
print(f"Your final score is {score} out of {choice}")
if score < choice / 2:
    print("You need to practice more")
