import random


def roll():
    return random.randint(1, 6)


while True:
    players = input("Enter the number of Players(2 - 4): ")
    if players.isdigit():
        players = int(players)
        if 2 <= players <= 4:
            break
        else:
            print("Must be between 2 and 4.")
    else:
        print("Invalid, try again")
max_score = 50
player_score = [0 for _ in range(players)]

while max(player_score) < max_score:
    for i in range(players):
        print(f"\nPlayer {i + 1}'s turn")
        current_score = 0
        while True:
            choice_roll = input("Would you like to roll (y/n): ").lower()
            if choice_roll != "y":
                break
            value = roll()
            if value == 1:
                print("Snake eyes, you rolled a 1, Turn Done")
                current_score = 0
                break
            else:
                current_score += value
                print("You rolled a: ", value)
                if current_score > max_score:
                    break
            print("Your Score is: ", current_score)
        player_score[i] += current_score
        print("Your Total score is: ", player_score[i])
max_score = max(player_score)
winning_idx = player_score.index(max_score)
print(f"Player {winning_idx} is the winner with the score of {max_score}")
