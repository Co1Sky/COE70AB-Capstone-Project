from main import *
import pandas as pd
import cv2
import os
from imutils import paths
import face_recognition
import pickle
import hashlib
from main import main_page

class registerPage:
    last_employee_number = 0
    
    def __init__(self, root):
        self.root = root
        self.mainFrame = Frame(self.root)
        self.mainFrame.pack()

        self.l0 = Label(self.mainFrame, text="Drowsiness Project", bg="dim grey", width=100, height=2, font=("Calibri", 24))
        self.l0.pack(side=TOP, fill=Y)

        self.l1 = Label(self.mainFrame, text="Please enter details below", font=("Calibri", 16), pady=25)
        self.l1.pack()
        
        self.usernameFrame = Frame(self.mainFrame)
        self.usernameFrame.pack()

        self.l2 = Label(self.usernameFrame, text="Username --> ", font=("Calibri", 16))
        self.l2.pack()

        self.username = StringVar()
        self.username_entry = Entry(self.usernameFrame, textvariable=self.username, font=("Calibri", 16))
        self.username_entry.pack()

        self.status_message = Label(self.usernameFrame, text="", font=("Calibri", 14), fg="red")
        self.status_message.pack()

        self.passwordFrame = Frame(self.mainFrame)
        self.passwordFrame.pack()

        self.l3 = Label(self.passwordFrame, text="Password --> ", font=("Calibri", 16))
        self.l3.pack()

        self.password = StringVar()
        self.password_entry = Entry(self.passwordFrame, textvariable=self.password, font=("Calibri", 16), show="*")
        self.password_entry.pack()

        self.b2 = Button(self.passwordFrame, text="Register", width=10, height=1, font=("Calibri", 16), command=self.register_user)
        self.b2.pack(side=BOTTOM, pady=(20, 0))


    def register_user(self):
        print("REGISTER USER!")
        username = self.username.get()
        password = self.password.get()
        employeeNumber = self.hash_username(username)

        # Read the existing CSV file
        userData = pd.read_csv('Face_Recognition_Code/User_Database/Current User Names.txt', delimiter=',')

        # Check if the combination already exists
        existing_user = userData[(userData['Username'] == username) & (userData['Employee Number'] == employeeNumber)]
        if not existing_user.empty:
            print("The user already exists.")
            self.status_message.config(text="The user already exists. Please try a different username.", fg="red")
            self.clear_fields()
        else:
            print("The user does not already exist.")
            # Create a new DataFrame with the new user data
            new_user = pd.DataFrame({'Username': [username],'Password': [password],
                                     'Employee Number': [employeeNumber], 'Pan Angle': [60], 'Tilt Angle': [20]})
            # Append the new user data to the existing DataFrame
            userData = pd.concat([userData, new_user], ignore_index=True)
            # Write the updated DataFrame back to the CSV file
            userData.to_csv("Face_Recognition_Code/User_Database/Current User Names.txt", index=False)
            self.headshot(username)
            
    def clear_fields(self, success=False):
        # Optionally, clear the fields only if registration was not successful.
        if not success:
            self.username_entry.delete(0, END)
            self.password_entry.delete(0, END)

    def hash_username(self, s):
        # Create a SHA-256 hash object
        sha256 = hashlib.sha256()
        
        # Update the hash object with the string's bytes
        sha256.update(s.encode('utf-8'))
        
        # Get the hexadecimal representation of the hash
        hash_val = sha256.hexdigest()
        
        # Return the hash value
        return hash_val

    def toMainPage(self):
        self.mainFrame.destroy()
        mainPage = main_page(self.root)
        mainPage.start()
        self.root.destroy()

    def start(self):
        self.root.mainloop()
    

    def headshot(self, username):
        image_counter = 0

        dataset_path = "Face_Recognition_Code/User_Database/" + username
        os.makedirs(dataset_path, exist_ok=True)

        cam = cv2.VideoCapture(0)

        cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)

        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("press space to take a photo", frame)

            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = (f"Face_Recognition_Code/User_Database/{username}/image{image_counter}.jpg")
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                image_counter += 1

        cam.release()

        cv2.destroyAllWindows()
        self.train_model(username)

    def train_model(self, name):
        # our images are located in the dataset folder
        print("[INFO] start processing faces...")
        imagePaths = list(paths.list_images(f"Face_Recognition_Code/User_Database/{name}"))

        # initialize the list of known encodings and known names
        knownEncodings = []
        knownNames = []

        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            try:
                # extract the person name from the image path
                print("[INFO] processing image {}/{}".format(i + 1,
                    len(imagePaths)))
                name = imagePath.split(os.path.sep)[-2]

                # load the input image and convert it from RGB (OpenCV ordering)
                # to dlib ordering (RGB)
                image = cv2.imread(imagePath)
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # detect the (x, y)-coordinates of the bounding boxes
                # corresponding to each face in the input image
                boxes = face_recognition.face_locations(rgb, model="hog")

                # compute the facial embedding for the face
                encodings = face_recognition.face_encodings(rgb, boxes)

                # loop over the encodings
                for encoding in encodings:
                    # add each encoding + name to our set of known names and
                    # encodings
                    knownEncodings.append(encoding)
                    knownNames.append(name)

            except Exception as e:
                print(f"Error processing image {imagePath}: {str(e)}")

        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        try:
            data = {"encodings": knownEncodings, "names": knownNames}
            with open(f"{name}/encodings.pickle", "wb") as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"Error serializing encodings: {str(e)}")

        self.toMainPage()



                
