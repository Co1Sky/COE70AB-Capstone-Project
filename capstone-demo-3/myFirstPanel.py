from main import *

class myFirstPanel:
    def __init__(self, root):
        self.root = root
        self.mainFrame = Frame(self.root)
        self.mainFrame.grid(row=0, column=0, padx=10, pady=2)
        self.user_login_btn = Button(self.mainFrame, text='First Panels', relief='solid', font=('times new roman', 15),
                                     height=20, width=50, command=self.gotomainpanel)
        self.user_login_btn.grid(row=2, column=0, columnspan=10, sticky=(N, S, E, W))

    def gotomainpanel(self):
        self.mainFrame.destroy()
        myTkWindow = MyTkWindow(self.root)
        myTkWindow.start()
        self.root.destroy()


    def start(self):
        self.root.mainloop()