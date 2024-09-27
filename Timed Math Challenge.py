import random
import time

operators = ["+", "-", "*"]
Min_operand = 3
Max_operand = 12
Total_problems = 10


def Generate_problem():
    left = random.randint(Min_operand, Max_operand)
    right = random.randint(Min_operand, Max_operand)
    operator = random.choice(operators)
    expr = str(left) + " " + operator + " " + str(right)
    answer = eval(expr)
    return expr, answer


wrong = 0
input("Press Enter to start! ")
print("\n---------------------")

start_time = time.time()


for i in range(Total_problems):
    expr, answer = Generate_problem()
    while True:
        guess = input("Problem # " + str(i + 1) + ":\n\n " + expr + " = ")
        print("")
        if guess == str(answer):
            break
        wrong += 1
end_time = time.time()
print("Time taken: ", end_time - start_time, " seconds")
print(f"You gave {wrong} wrong answers\n")


print("---------------------")
if wrong < 5:
    print("Nice Work")
else:
    print("Need to improve")
