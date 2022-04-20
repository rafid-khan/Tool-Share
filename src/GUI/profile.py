from tkinter import *
import tkinter.font as font
import GUI.global_variables as gbl_var
import src.db.user as user
import re

def get_profile_pane(root, frame2):
    root.title("Tools - Profile")

    pane = PanedWindow(frame2, width=1400, height=596, bg='#EFE2BA')
    user_dict = user.fetch_user(gbl_var.username)
    left_pane = PanedWindow(pane, width=200, height=596, bg='#417154')
    left_pane.grid(column=0, row=0, pady=0, padx=0)
    middle_pane = PanedWindow(pane, width=1000, height=596, bg='#EFE2BA')

    bottomPane = PanedWindow(middle_pane, width=1400, height=596, bg='#EFE2BA')
    # Logo
    top_pane = PanedWindow(bottomPane, width=1400, height=150, bg='#A67B5C')
    logo_label_font = font.Font(size=48, family='Meiryo')
    logo_text = user_dict['first_name']
    if logo_text[len(logo_text)-1] == 's' or logo_text[len(logo_text)-1] == 'S':
        logo_text += "' Shed"
    else:
        logo_text += "'s Shed"
    logo_label = Label(top_pane, text=logo_text, bg='#A67B5C', fg='#EFE2BA', font=logo_label_font)
    logo_label.pack(pady=(30, 30), padx=285)
    top_pane.pack(pady=0, padx=0)
    # Bottom
    info_pane = PanedWindow(bottomPane, width=1400, height=446, bg='#EFE2BA')
    get_profile(root, info_pane)
    info_pane.pack(pady=(53, 53))

    bottomPane.pack(padx=0, pady=0)
    middle_pane.grid(column=1, row=0, pady=0, padx=0)

    right_pane = PanedWindow(pane, width=200, height=596, bg='#417154')
    right_pane.grid(column=2, row=0, pady=0, padx=0)

    return pane


def get_profile(root, bottom_pane):

    user_information_pane = PanedWindow(bottom_pane, width=700, height=446, bg='#EFE2BA')
    user_info = user.fetch_user(gbl_var.username)
    user_info_font = font.Font(size=20, family='Meiryo')
    user_small_info_font = font.Font(size=14, family='Meiryo')
    # Name: first last
    name_string = user_info['first_name'] + " " + user_info['last_name']
    name_label = Label(user_information_pane, bg='#EFE2BA', fg='#A67B5C', text="Name", font=user_info_font)
    name_label.pack(pady=(0, 8))
    name = Label(user_information_pane, bg='#EFE2BA', fg='#A67B5C', text=name_string, font=user_small_info_font)
    name.pack(pady=(0, 15))
    # Username
    username_string = user_info['username']
    username_label = Label(user_information_pane, bg='#EFE2BA', fg='#A67B5C', text="Username", font=user_info_font)
    username_label.pack(pady=(0, 8))
    username = Label(user_information_pane, bg='#EFE2BA', fg='#A67B5C', text=username_string, font=user_small_info_font)
    username.pack(pady=(0, 15))
    # Creation Date
    date_string = str(user_info['creation_date'])
    name_label = Label(user_information_pane, bg='#EFE2BA', fg='#A67B5C', text="Creation Date", font=user_info_font)
    name_label.pack(pady=(0, 8))
    creation_date_label = Label(user_information_pane, bg='#EFE2BA', fg='#A67B5C', text=date_string, font=user_small_info_font)
    creation_date_label.pack(pady=(0, 15))
    # Email
    has_email = False
    try:
        email_string = user_info['email']
        has_email = True
    except KeyError:
        email_string = "None"
    email_label = Label(user_information_pane, bg='#EFE2BA', fg='#A67B5C', text="Email", font=user_info_font)
    email_label.pack(pady=(0, 8))
    email = Label(user_information_pane, bg='#EFE2BA', fg='#A67B5C', text=email_string, font=user_small_info_font)
    email.pack(pady=0)

    user_information_pane.grid(column=0, row=0, padx=(70, 48))

    user_modification_pane = PanedWindow(bottom_pane, width=700, height=446, bg='#EFE2BA')

    # Name: Email
    big_font = font.Font(size=20, family='Calibri')
    small_font = font.Font(size=14, family='Calibri')
    add_email_label = Label(user_modification_pane, text="Modify your email", bg='#EFE2BA', fg='#A67B5C', font=big_font)
    add_email_label.grid(column=1, row=0)
    email_label = Label(user_modification_pane, text="Email: ", bg='#EFE2BA', fg='#A67B5C', font=small_font)
    email_label.grid(column=0, row=1, padx=5, pady=(0, 10))
    email_text = Text(user_modification_pane, width=20, height=1, bg='gray85', font=small_font)
    email_text.grid(column=1, row=1, pady=(0, 10))
    email_error_label = Label(user_modification_pane, text="Format: johndoe12@gmail.com", bg='#EFE2BA', fg='#EFE2BA')
    email_error_label.grid(column=2, row=0)
    email_button = Button(user_modification_pane, text="Update Email", font=small_font,
                          command=lambda: updateEmail(email_text, has_email, email_error_label))
    email_button.grid(column=2, row=1, pady=(0, 10), padx=(0, 20))
    # Password
    change_password_label = Label(user_modification_pane, text="Change Password", bg='#EFE2BA', fg='#A67B5C', font=big_font)
    change_password_label.grid(column=1, row=2)
    password_label = Label(user_modification_pane, text="New Password: ", bg='#EFE2BA', fg='#A67B5C', font=small_font)
    password_label.grid(column=0, row=3, padx=5, pady=10)
    password_text = Text(user_modification_pane, width=20, height=1, bg='gray85', font=small_font)
    password_text.grid(column=1, row=3, pady=10)
    password_error_label = Label(user_modification_pane, text="", bg='#EFE2BA', fg='#EFE2BA')
    # Confirm Password
    confirm_password_label = Label(user_modification_pane, text="Confirm Password: ", bg='#EFE2BA', fg='#A67B5C', font=small_font)
    confirm_password_label.grid(column=0, row=4, padx=5, pady=10)
    confirm_password_text = Text(user_modification_pane, width=20, height=1, bg='gray85', font=small_font)
    confirm_password_text.grid(column=1, row=4, pady=10)
    confirm_password_button = Button(user_modification_pane, text="Change Password", font=small_font,
                          command=lambda: updatePassword(password_text, confirm_password_text, password_error_label))
    confirm_password_button.grid(column=2, row=4, padx=(20, 0))

    user_modification_pane.grid(column=1, row=0, padx=(0, 70))


def updateEmail(email_text, has_email, email_error_label):
    email = email_text.get("1.0", END).split("\n")[0]
    if re.search("\w+@\w+.\w+", email):
        if has_email:
            user.update_email(gbl_var.username, email=email)
        else:
            user.insert_email(username=gbl_var.username, email=email)
            email_error_label.configure(fg='#EFE2BA')
    else:
        email_error_label.configure(fg='red')


def update_password(password_text, confirm_password_text, password_error_label):
    password = password_text.get("1.0", END).split("\n")[0]
    confirm_password = confirm_password_text.get("1.0", END).split("\n")[0]
    if password == confirm_password:
        if re.search("\w+@\w+.\w+", email):
            pass
    else:
        password_error_label.configure(text="Password do\nnot match!!")