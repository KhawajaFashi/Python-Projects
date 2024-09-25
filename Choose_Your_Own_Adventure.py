name = input("Enter your Name: ")
print(f"Welcome {name} to your own Adventure")

answer = input("You are on a dirty road, dou you want to turn around? ").lower()
if answer == "no":
    print("You are turning back. Hope to see you again!")
    exit(0)
elif answer == "yes":
    print("Lets Get on with the adventure!")
    choice = input("Well now do you want to go to left or right").lower()
    if choice == "left":
        answer = input(
            "You come to a river, you can walk around it or swim accross? Type walk to walk around and swim to swim accross: "
        )
        if answer == "swim":
            print("You swam acrross and were eaten by an alligator.")
        elif answer == "walk":
            print("You walked for many miles, ran out of water and you lost the game.")
        else:
            print("Not a valid option. You lose.")

    elif choice == "right":
        answer = input(
            "You come to a bridge, it looks wobbly, do you want to cross it or head back (cross/back)? "
        )

    if answer == "back":
        print("You go back and lose.")
    elif answer == "cross":
        answer = input(
            "You cross the bridge and meet a stranger. Do you talk to them (yes/no)? "
        )
        if answer == "yes":
            print("You talk to the stanger and they give you gold. You WIN!")
        elif answer == "no":
            print("You ignore the stranger and they are offended and you lose.")
        else:
            print("Not a valid option. You lose.")
    else:
        print("Not a valid option. You lose.")

else:
    print("Invalid input. You have lost.")
