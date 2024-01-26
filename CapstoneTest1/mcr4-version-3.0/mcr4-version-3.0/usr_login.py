from facial_req import reg_face
from headshot_picam2 import headshot
from train_model import train_model

def run_login():
    valid = False
    def login(name):
        nonlocal valid
        name = name.split()
        name = name[0] + "_" + name[1]
        print(name)
        file_path = "User Database/Current User Names"
        with open(file_path, "r") as file:
            col = file.readline().split()
            columns = int(col[0])
            users = [file.readline().strip().split() for _ in range(columns)]
            print(users)
        for user in users:
            print(user)
            if user[0] == name:
                print("FOUND NAME")
                scanned_face = reg_face()
                print(f"FOUND: {scanned_face}")
                if scanned_face == user:
                    valid = True
                    return
                else:
                    valid = False
            else:
                print("USER NOT FOUND")
                print("Username not found")
                valid = False
                
    def register_user(name, employee_number):
        # Add the new user
        first_name, last_name = name.split()
        new_user = [f"{first_name}_{last_name}", str(employee_number)]

        # Read existing data from the file
        file_path = "User Database/Current User Names"
        with open(file_path, "r") as file:
            columns = int(file.readline().strip())
            users = [file.readline().strip().split() for _ in range(columns)]

        # Check if the user already exists
        if new_user in users:
            print(f"User {new_user} is already registered")
        else:
            # Update the list of users
            users.append(new_user)

            # Update the file with the new data
            with open(file_path, "w") as file:
                # Write the number of columns
                file.write(f"{len(users[0])}\n")

                # Write each user's data
                for user in users:
                    file.write(" ".join(user) + "\n")
            
        print("TRAINING MODEL STEP")
        headshot(new_user[0])
        print("BUILDING MODEL STEP")
        train_model()
        

    while valid == False:
        print("Welcome, please enter your desired option")
        print("[1] User login \n[2] Create an account \n[3] Exit")
        menu_option = input(" -> ")
        if menu_option == "1":
            print("Please enter your FULL NAME")
            name = input(" -> ")
            login(name)
        elif menu_option == "2":
            print("Please enter your FULL NAME")
            name = input(" -> ")
            print("Please enter your EMPLOYEE #")
            employee_num = input(" -> ")
            register_user(name, employee_num)
        elif menu_option == "3":
            exit(0)
            
    return "Valid"

             
        