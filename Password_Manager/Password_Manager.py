def view():
    with open("passwords.txt") as file:
        identify = input("Please Identify yourself: ")
        for line in file.readlines():
            check = False
            username, password, key = line.strip().split("|")
            key = int(key)
            if identify == username:
                if key == pwd:
                    print("You were identified")
                    line.rstrip()
                    for i in range(len(password)):
                        new_char = chr(ord(password[i]) - pwd)
                        if ord(password[i]) + pwd < 97:
                            new_char = chr(ord(password[i]) - pwd + 26)
                        password = password[:i] + new_char + password[i + 1 :]
                    print(f"{line.split('|')[0]} your password is: {password}")
                    check = True
    if not (check):
        print(f"{username} your key didnot match")
    else:
        print("You were not identified")


def add():
    with open("passwords.txt", "a") as file:
        name = input("Please Enter your name: ")
        password = input(
            "Please Enter your password without spaces and only lowercase Alphabets: "
        )
        for i in range(len(password)):
            new_char = chr(ord(password[i]) + pwd)
            if ord(password[i]) + pwd > 122:
                new_char = chr(ord(password[i]) + pwd - 26)
            password = password[:i] + new_char + password[i + 1 :]
        file.write(name + "|" + password + "|" + str(pwd) + "\n")
        print("Password Added Successfully")


pwd = int(
    input(
        "Enter the secret key for storing your Password. Your Password will be encrypted according to your with respective to ascii table: "
    )
)
pwd = pwd % 27

while True:
    choice = input(
        'Do you want to view your password or add a new password. Type "view" to view your password and "add" to add a password or "q" to exit: '
    )
    if choice == "view":
        view()
    elif choice == "add":
        add()
    elif choice == "q":
        break
    else:
        print("Invalid choice. Please try again.")
        continue
