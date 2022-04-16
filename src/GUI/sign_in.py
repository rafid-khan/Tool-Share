import tkinter as tk
from tkinter import *
from tkinter import font
from PIL import ImageTk, Image
import GUI.Nav as Nav
import src.db.user as user


global is_signing_in


def sign_in_pane(frame2, right_pane, root, *args):
    global is_signing_in

    if is_signing_in:
        username = frame2.winfo_children()[0].winfo_children()[1].winfo_children()[1].get("1.0", END)
        password = frame2.winfo_children()[0].winfo_children()[2].winfo_children()[1].get("1.0", END)

        username = username.split("\n")[0]
        password = password.split("\n")[0]
        validLogin = False
        if len(username) > 0 and len(password) > 0:
            validLogin = user.log_in(username, password)
        if validLogin:
            root.destroy()
            Nav.main(username)
        else:
            add_error_label(frame2)
    else:
        prev_pane = frame2.winfo_children()
        prev_pane[len(prev_pane) - 1].pack_forget()
        pane = get_sign_in_pane(frame2)
        pane.pack()
        frame2.pack()
        right_pane.pack(padx=215, pady=263)
    return


def add_error_label(frame2):
    frame2.winfo_children()[0].winfo_children()[0].configure(fg='red')


def get_sign_in_pane(frame2):
    global is_signing_in
    is_signing_in = True

    pane = PanedWindow(frame2, width=500, height=450, bg='white')

    error_label = Label(pane, text="Error wrong username or password", bg='white', fg='white')
    error_label.grid(column=0, row=0, pady=10)

    username_pane = PanedWindow(pane, width=400, height=50, bg='white')
    username_label = Label(username_pane, text="Username: ", bg='white')
    username_label.grid(column=0, row=0, padx=5)
    username_text = Text(username_pane, width=20, height=1, bg='white')
    username_text.grid(column=1, row=0)
    username_pane.grid(column=0, row=1, pady=10)

    password_pane = PanedWindow(pane, width=400, height=50, bg='white')
    password_label = Label(password_pane, text="Enter a Password: ", bg='white')
    password_label.grid(column=0, row=0, padx=5)
    password_text = Text(password_pane, width=20, height=1, bg='white')
    password_text.grid(column=1, row=0)

    password_pane.grid(column=0, row=2, pady=10)

    return pane


def create_account_pane(frame2, right_pane, root, *args):
    global is_signing_in

    if not is_signing_in:
        field_error = False

        first_name = frame2.winfo_children()[1].winfo_children()[2].get("1.0", END)
        first_name = first_name.split("\n")[0]
        last_name = frame2.winfo_children()[1].winfo_children()[4].get("1.0", END)
        last_name = last_name.split("\n")[0]
        username = frame2.winfo_children()[1].winfo_children()[6].get("1.0", END)
        username = username.split("\n")[0]
        password = frame2.winfo_children()[1].winfo_children()[8].get("1.0", END)
        password = password.split("\n")[0]
        confirm_password = frame2.winfo_children()[1].winfo_children()[10].get("1.0", END)
        confirm_password = confirm_password.split("\n")[0]

        if len(first_name) == 0:
            frame2.winfo_children()[1].winfo_children()[0].configure(text="Please enter a first name.", fg='red')
            field_error = True
        elif len(last_name) == 0:
            frame2.winfo_children()[1].winfo_children()[0].configure(text="Please enter a last name.", fg='red')
            field_error = True
        elif len(username) == 0:
            frame2.winfo_children()[1].winfo_children()[0].configure(text="Please enter a username.", fg='red')
            field_error = True
        elif len(password) == 0:
            frame2.winfo_children()[1].winfo_children()[0].configure(text="Please enter a password.", fg='red')
            field_error = True
        # Verify the users account was added then go to the Dashboard
        if confirm_password == password and not field_error:
            user.insert_user(a=first_name, b=last_name, c=username, d=password)
            root.destroy()
            Nav.main(username)
        elif confirm_password != password:
            frame2.winfo_children()[1].winfo_children()[0].configure(text="Passwords do not match.", fg='red')
    else:
        prev_pane = frame2.winfo_children()
        prev_pane[len(prev_pane) - 1].pack_forget()
        pane = get_create_account_pane(frame2)
        pane.pack()
        frame2.pack()
        right_pane.pack(padx=210, pady=212)
    return


def confirm_password_error(frame2, right_pane):
    pass


def get_create_account_pane(frame2):
    global is_signing_in
    is_signing_in = False

    pane = PanedWindow(frame2, width=500, height=450, bg='white')

    error_label = Label(pane, text="Error wrong username or password", bg='white', fg='white')
    error_label.grid(column=1, row=0, pady=10)

    first_name_label = Label(pane, text="First Name: ", bg='white')
    first_name_label.grid(column=0, row=1, padx=5, pady=(0,10))
    first_name_text = Text(pane, width=20, height=1, bg='white')
    first_name_text.grid(column=1, row=1, pady=(0,10))

    last_name_label = Label(pane, text="Last Name: ", bg='white')
    last_name_label.grid(column=0, row=2, padx=5, pady=10)
    last_name_text = Text(pane, width=20, height=1, bg='white')
    last_name_text.grid(column=1, row=2, pady=10)

    username_label = Label(pane, text="Username: ", bg='white')
    username_label.grid(column=0, row=3, padx=5, pady=10)
    username_text = Text(pane, width=20, height=1, bg='white')
    username_text.grid(column=1, row=3, pady=10)

    password_label = Label(pane, text="Enter a Password: ", bg='white')
    password_label.grid(column=0, row=4, padx=5, pady=10)
    password_text = Text(pane, width=20, height=1, bg='white')
    password_text.grid(column=1, row=4, pady=10)

    confirm_password_label = Label(pane, text="Confirm password: ", bg='white')
    confirm_password_label.grid(column=0, row=5, padx=5, pady=(10, 0))
    confirm_password_text = Text(pane, width=20, height=1, bg='white')
    confirm_password_text.grid(column=1, row=5, pady=(10, 0))

    return pane


def main():

    root = tk.Tk()
    root.title('Tools - Home')
    root.geometry('1400x700')

    img_resize = Image.open("images/White-Logo.png").resize((350, 350))
    img = ImageTk.PhotoImage(img_resize)

    frame1 = Frame(root, width=700, height=700, bg='white')

    logo_pane = PanedWindow(frame1, width=500, height=500, bg='white')
    logo_font = font.Font(size=25)

    tools_label = Label(logo_pane, text="The Shed", bg='white', fg='black')
    tools_label.configure(font=logo_font)
    logo = Label(logo_pane, image=img, bg='white')

    logo.pack()
    tools_label.pack()
    logo_pane.pack(padx=170, pady=150)
    frame1.grid(column=0, row=0)

    frame2 = Frame(root, width=700, height=700, bg='white')
    right_pane = PanedWindow(frame2, width=500, height=500, bg='white')
    info_pane = PanedWindow(right_pane, width=500, height=450, bg='white')
    info_pane.pack()

    info_child = get_sign_in_pane(info_pane)

    button_pane = PanedWindow(right_pane, width=500, height=50, bg='white')

    sign_in_button = Button(button_pane,
                            height=2,
                            width=11,
                            text='Sign in',
                            command=lambda: sign_in_pane(info_pane, right_pane, root))
    create_account_button = Button(button_pane,
                                   height=2,
                                   width=15,
                                   text='Create account',
                                   command=lambda: create_account_pane(info_pane, right_pane, root))

    info_child.pack()
    create_account_button.grid(column=0, row=0, padx=10)
    sign_in_button.grid(column=1, row=0, padx=10)
    button_pane.pack()
    right_pane.pack(padx=215, pady=262)
    frame2.grid(column=1, row=0)

    root.mainloop()

    return


if __name__ == '__main__':
    main()
