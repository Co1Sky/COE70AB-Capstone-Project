# Global Imports
from tkinter import *
from Face_Recognition_Code import registerPage


class main_page:
    def __init__(self, root):
        self.root = root 
        self.mainFrame = Frame(self.root)
        self.mainFrame.pack()

        self.l1 = Label(self.mainFrame, text="Drowsiness Project", bg="dim grey", width=100, height=2, font=("Calibri", 24))
        self.l1.pack(side=TOP, fill=Y)  

        self.b1 = Button(self.mainFrame, text="Login", bg="green yellow", font=("Calibri", 16), width=30)
        self.b1.pack(side=TOP, pady=30, ipadx=2, ipady=2)

        self.b2 = Button(self.mainFrame, text="Register", bg="green yellow", font=("Calibri", 16), width=30, command=self.registerPage)
        self.b2.pack(side=TOP, pady=30, ipadx=2, ipady=2)


    def registerPage(self):
        self.mainFrame.destroy()
        register_page = registerPage.registerPage(self.root)
        register_page.start()

    def start(self):
        self.root.mainloop()


if __name__ == '__main__':

    print("--> Initializing the Servo Setting....")
    # SERVO MOTOR SETTINGS - DO NOT CHANGE!! #

    # (UNCOMMENT THIS OUT ONCE WE GET EVERYTHING WORKING) #
    # pan = ss.Servo(pin=13, max_angle=60, min_angle=-60)
    # tilt = ss.Servo(pin=12, max_angle=30, min_angle=-70)

    root = Tk()
    root.geometry("500x500")
    myWindow = main_page(root)
    myWindow.start()