import pandas as pd
from facial_req import reg_face
from headshot_picam2 import headshot
from train_model import train_model


def run_login():
    valid = False
    def login(firstName, lastName):
        nonlocal valid
        userData = pd.read_csv('Face Recognition Code/User Database/Current User Names.txt', delimiter=',')
        existing_user = userData[(userData['First Name'] == firstName) & (userData['Last Name'] == lastName)]
        if not existing_user.empty:
            print("FOUND NAME")
            scanned_face = reg_face(firstName + "_" + lastName)
            print(f"FOUND: {scanned_face}")
            if scanned_face == firstName + "_" + lastName:
                valid = True
                return firstName, lastName
            else:
                valid = False
        else:
            print("USER NOT FOUND")
            print("Username not found")
            valid = False
                
    def register_user(firstName, lastName, employee_number):
        # Read the existing CSV file
        userData = pd.read_csv('Face Recognition Code/User Database/Current User Names.txt', delimiter=',')

        # Check if the combination already exists
        existing_user = userData[(userData['First Name'] == firstName) & (userData['Last Name'] == lastName) & (userData['Employee Number'] == employee_number)]
        if not existing_user.empty:
            print("The user already exists.")
        else:
            print("The user does not already exist.")
            # Create a new DataFrame with the new user data
            new_user = pd.DataFrame({'First Name': [firstName], 'Last Name': [lastName], 'Employee Number': [employee_number], 'Pan Angle': [60], 'Tilt Angle': [20]})
            # Append the new user data to the existing DataFrame
            userData = pd.concat([userData, new_user], ignore_index=True)
            # Write the updated DataFrame back to the CSV file
            userData.to_csv("Face Recognition Code/User Database/Current User Names.txt", index=False)

        print("TRAINING MODEL STEP")
        headshot(firstName + "_" + lastName)
        print("BUILDING MODEL STEP")
        train_model(firstName + "_" + lastName) 

    
        
        
    while valid == False:
        print("Welcome, please enter your desired option")
        print("[1] User login \n[2] Create an account \n[3] Exit")
        menu_option = input(" -> ")
        if menu_option == "1":
            print("Please enter your FIRST NAME")
            firstName = input(" -> ")
            print("Please enter your LAST NAME")
            lastName = input(" -> ")
            auth_FN, auth_LN = login(firstName, lastName)
        elif menu_option == "2":
            print("Please enter your FIRST NAME")
            firstName = input(" -> ")
            print("Please enter your LAST NAME")
            lastName = input(" -> ")
            print("Please enter your EMPLOYEE #")
            employee_num = input(" -> ")
            register_user(firstName, lastName, employee_num)
        elif menu_option == "3":
            exit(0)
            
    return auth_FN, auth_LN

             
        