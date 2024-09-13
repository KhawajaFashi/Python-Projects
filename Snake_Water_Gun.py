from random import randint

snake = 1
water = 2
gun = 3
print("\nWelcome to the game of Snake, Water and Gun ")
print("\n1 is for Snake, 2 is for Water and 3 is for Gun ")
num = int(input("\nPlease choose a number between 1 and 3: "))
while num >= 1 and num <= 3:
    value = randint(1, 3)
    if num == 1 and value == 2:
        print("\nYou chose Snake and computer chose Water. You win!")
    elif num == 2 and value == 3:
        print("\nYou chose Water and computer chose Gun. You win!")
    elif num == 3 and value == 1:
        print("\nYou chose Gun and computer chose Snake. You win!")
    elif num == 2 and value == 1:
        print("\nYou chose Water and computer chose Snake. Computer win!")
    elif num == 3 and value == 2:
        print("\nYou chose Gun and computer chose Water. Computer win!")
    elif num == 1 and value == 3:
        print("\nYou chose Snake and computer chose Gun. Computer win!")
    else:
        print("\nYou both pick the same number, It's a tie!")
    again = int(input("\nIf you want to play again Press 1, if not then 0: "))
    if again == 0:
        break
    num = int(input("\nPlease choose a number between 1 and 3: "))
    if not (num >= 1 and num <= 3):
        print("\nPlease enter a number between 1 and 3")
