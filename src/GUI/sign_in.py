import tkinter as tk
from tkinter import *
from tkinter import font
from PIL import ImageTk, Image
import os
import header

global is_signing_in


def sign_in_pane(frame2, right_pane, root, *args):
    global is_signing_in

    if (is_signing_in):
        username = frame2.winfo_children()[0].winfo_children()[0].winfo_children()[1].get("1.0", END)
        print(username)
        password = frame2.winfo_children()[0].winfo_children()[1].winfo_children()[1].get("1.0", END)
        print(password)

        root.destroy()
        header.main()
    else:
        prev_pane = frame2.winfo_children()
        prev_pane[len(prev_pane) - 1].pack_forget()
        pane = get_sign_in_pane(frame2)
        pane.pack()
        frame2.pack()
        right_pane.pack(padx=215, pady=283)
    return


def get_sign_in_pane(frame2):
    global is_signing_in
    is_signing_in = True

    pane = PanedWindow(frame2, width=500, height=450, bg='white')

    username_pane = PanedWindow(pane, width=400, height=50, bg='white')
    username_label = Label(username_pane, text="Username: ", bg='white')
    username_label.grid(column=0, row=0, padx=5)
    username_text = Text(username_pane, width=20, height=1, bg='white')
    username_text.grid(column=1, row=0)
    username_pane.pack(pady=10)

    password_pane = PanedWindow(pane, width=400, height=50, bg='white')
    password_label = Label(password_pane, text="Enter a Password: ", bg='white')
    password_label.grid(column=0, row=0, padx=5)
    password_text = Text(password_pane, width=20, height=1, bg='white')
    password_text.grid(column=1, row=0)

    password_pane.pack(pady=10)

    return pane


def create_account_pane(frame2, right_pane, root, *args):
    global is_signing_in

    if (not is_signing_in):
        first_name = frame2.winfo_children()[1].winfo_children()[1].get("1.0", END)
        print(first_name)
        first_name = frame2.winfo_children()[1].winfo_children()[3].get("1.0", END)
        print(first_name)
        username = frame2.winfo_children()[1].winfo_children()[5].get("1.0", END)
        print(username)
        password = frame2.winfo_children()[1].winfo_children()[7].get("1.0", END)
        print(password)
        confirm_password = frame2.winfo_children()[1].winfo_children()[9].get("1.0", END)
        print(confirm_password)
        # Verify the users account was added then go to the Dashboard
        root.destroy()
        header.main()
        pass
    else:
        prev_pane = frame2.winfo_children()
        prev_pane[len(prev_pane) - 1].pack_forget()
        pane = get_create_account_pane(frame2)
        pane.pack()
        frame2.pack()
        right_pane.pack(padx=210, pady=236)
    return


def get_create_account_pane(frame2):
    global is_signing_in
    is_signing_in = False

    pane = PanedWindow(frame2, width=500, height=450, bg='white')

    first_name_label = Label(pane, text="First Name: ", bg='white')
    first_name_label.grid(column=0, row=0, padx=5, pady=(0,10))
    first_name_text = Text(pane, width=20, height=1, bg='white')
    first_name_text.grid(column=1, row=0, pady=(0,10))

    last_name_label = Label(pane, text="Last Name: ", bg='white')
    last_name_label.grid(column=0, row=1, padx=5, pady=10)
    last_name_text = Text(pane, width=20, height=1, bg='white')
    last_name_text.grid(column=1, row=1, pady=10)

    username_label = Label(pane, text="Username: ", bg='white')
    username_label.grid(column=0, row=2, padx=5, pady=10)
    username_text = Text(pane, width=20, height=1, bg='white')
    username_text.grid(column=1, row=2, pady=10)

    password_label = Label(pane, text="Enter a Password: ", bg='white')
    password_label.grid(column=0, row=3, padx=5, pady=10)
    password_text = Text(pane, width=20, height=1, bg='white')
    password_text.grid(column=1, row=3, pady=10)

    confirm_password_label = Label(pane, text="Confirm password: ", bg='white')
    confirm_password_label.grid(column=0, row=4, padx=5, pady=(10, 0))
    confirm_password_text = Text(pane, width=20, height=1, bg='white')
    confirm_password_text.grid(column=1, row=4, pady=(10, 0))

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
    right_pane.pack(padx=215, pady=283)
    frame2.grid(column=1, row=0)

    root.mainloop()

    return


if __name__ == '__main__':
    main()
