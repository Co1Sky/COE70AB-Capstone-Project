import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

def login():
    username = username_entry.get()
    password = password_entry.get()
    # Here you can implement your login logic
    print("Username:", username)
    print("Password:", password)
    # For demonstration purposes, just printing the inputs

root = tk.Tk()
root.title("Modern Login")

# Apply ttkbootstrap style
style = Style(theme='flatly')

# Creating a container frame
container = ttk.Frame(root, padding="20", borderwidth=2, relief="solid")
container.grid(row=0, column=0, sticky="nsew")

# Username Label and Entry
username_label = ttk.Label(container, text="Username:", borderwidth=1, relief="solid")
username_label.grid(row=0, column=0, pady=(10, 5), sticky="w")
Style.configure('custom.TEntry', background='green', foreground='white', font=('Helvetica', 24))
username_entry = ttk.Entry(container, style="custom.TEntry")
username_entry.grid(row=0, column=1, pady=(10, 5), padx=(0, 10), sticky="we")

# Password Label and Entry
password_label = ttk.Label(container, text="Password:", borderwidth=1, relief="solid")
password_label.grid(row=1, column=0, pady=(5, 10), sticky="w")
password_entry = ttk.Entry(container, show="*")
password_entry.grid(row=1, column=1, pady=(5, 10), padx=(0, 10), sticky="we")

# Login Button
login_button = ttk.Button(container, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="we")

# Configure container grid to scale with the window and center the container
container.columnconfigure(0, weight=1)
container.columnconfigure(1, weight=1)

root.mainloop()
