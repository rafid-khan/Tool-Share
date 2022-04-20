import tkinter as tk
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
import GUI.sign_in as sign_in
import GUI.user_catalog as uc
import GUI.full_catalog as fc
import GUI.view_requests as vr
import GUI.dashboard as dash
import src.GUI.profile as pf
import GUI.global_variables as gbl_var


def main(passed_username):
    gbl_var.set_username(passed_username)
    root = tk.Tk()
    root.title('Tools - Home')
    root.geometry("1400x700")

    img_resize = Image.open("images/Logo.png").resize((100, 100))
    img = ImageTk.PhotoImage(img_resize)

    frame1 = Frame(root, width=1400, height=105, bg='#544227')
    frame2 = Frame(root, width=1400, height=596)
    pane = dash.get_dashboard_pane(root, frame2)
    pane.pack()

    initialize_header(frame1, img, frame2, root)

    frame1.pack()
    frame2.pack()

    root.mainloop()


def initialize_header(frame1, logo, frame2, root):
    header_panel = PanedWindow(frame1, width=1400, height=105, bg='#A67B5C')

    panel = Label(header_panel, image=logo)
    panel.grid(column=0, row=0)

    myFont = font.Font(size=11)

    dashboard_button = Button(header_panel,
                              height=3,
                              width=11,
                              text="Dashboard",
                              font=myFont,
                              bg='white',
                              command=lambda: dashboard(root, frame2))
    dashboard_button.grid(column=1, row=0, padx=(15,0))

    user_catalog_button = Button(header_panel,
                                 height=3,
                                 width=13,
                                 text="Your Catalog",
                                 font=myFont,
                                 bg='white',
                                 command=lambda: user_catalog(root, frame2))
    user_catalog_button.grid(column=2, row=0)

    full_catalog_button = Button(header_panel,
                                 height=3,
                                 width=13,
                                 text="Full Catalog",
                                 font=myFont,
                                 bg='white',
                                 command=lambda: full_catalog(root, frame2))
    full_catalog_button.grid(column=3, row=0)

    view_request_button = Button(header_panel,
                                 height=3,
                                 width=20,
                                 text="View your Requests",
                                 font=myFont,
                                 bg='white',
                                 command=lambda: view_request(root, frame2))
    view_request_button.grid(column=4, row=0)

    profile_button = Button(header_panel,
                            height=3,
                            width=10,
                            text="Profile",
                            font=myFont,
                            bg='white',
                            command=lambda: view_profile(root, frame2))
    profile_button.grid(column=5, row=0)

    sign_in_out_button = Button(header_panel,
                                height=3,
                                width=15,
                                text="Sign out",
                                font=myFont,
                                bg='white',
                                command=lambda: sign_in_out(root))
    sign_in_out_button.grid(column=6, row=0, padx=(475, 5))

    header_panel.pack()


def sign_in_out(root):
    root.destroy()
    sign_in.main()
    return


def dashboard(root, frame2):
    prev_pane = frame2.winfo_children()

    prev_pane[len(prev_pane) - 1].pack_forget()
    pane = dash.get_dashboard_pane(root, frame2)
    pane.pack()
    frame2.pack()
    return


def full_catalog(root, frame2):
    prev_pane = frame2.winfo_children()

    prev_pane[len(prev_pane) - 1].pack_forget()
    pane = fc.get_full_catalog_pane(root, frame2)
    pane.pack()
    frame2.pack()
    return


def user_catalog(root, frame2):
    prev_pane = frame2.winfo_children()

    prev_pane[len(prev_pane) - 1].pack_forget()
    pane = uc.get_user_catalog_pane(root, frame2)
    pane.pack()
    frame2.pack()
    return


def view_profile(root, frame2):
    prev_pane = frame2.winfo_children()

    prev_pane[len(prev_pane) - 1].pack_forget()
    pane = pf.get_profile_pane(root, frame2)

    pane.pack(padx=0, pady=0)
    frame2.pack(padx=0, pady=0)
    return


def view_request(root, frame2):
    prev_pane = frame2.winfo_children()

    prev_pane[len(prev_pane) - 1].pack_forget()
    pane = vr.get_user_request_pane(root, frame2)
    pane.pack()
    frame2.pack()
    return


if __name__ == '__main__':
    main("Aaron9932")
