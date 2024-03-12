from tkinter import *
import MyFirstPanel


class MyTkWindow:
    def __init__(self, root):
        self.root = root  # Makes the window
        self.mainFrame = Frame(self.root, width=500, height=500)
        self.mainFrame.grid(row=0, column=0, padx=10, pady=2)

        self.user_login_btn = Button(self.mainFrame, text='Go To First Frame',     relief='solid', font=('times new roman', 11),
                                     height=1, width=6, command=self.gotofirstpanel)
        self.user_login_btn.grid(row=2, column=0, columnspan=30, sticky=(N, S, E, W))


    def gotofirstpanel(self):
        self.mainFrame.destroy()
        myFirstPanel = MyFirstPanel.MyFirstPanel(self.root)
        myFirstPanel.start()

    def start(self):
        self.root.mainloop()


if __name__ == '__main__':
    root = Tk()
    myWindow = MyTkWindow(root)
    myWindow.start()