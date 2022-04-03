import tkinter as tk
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
from index import build_sign_in_pane
import sign_in
import user_catalog as uc




global widget_index


def main():
    root = tk.Tk()
    root.title('Tools - Home')
    root.geometry("1400x700")

    global widget_index
    widget_index = 0

    img_resize = Image.open("images/Logo.png").resize((100, 100))
    img = ImageTk.PhotoImage(img_resize)

    frame1 = Frame(root, width=1400, height=105, bg='#5D460E')
    frame2 = Frame(root, width=1400, height=596)
    pane = PanedWindow(frame2, width=1400, height=596, bg='green')
    pane.pack()

    initialize_header(frame1, img, frame2, root)

    frame1.pack()
    frame2.pack()

    root.mainloop()


def initialize_header(frame1, logo, frame2, root):
    header_panel = PanedWindow(frame1, width=1400, height=105, bg='white')

    panel = Label(header_panel, image=logo)
    panel.grid(column=0, row=0)

    myFont = font.Font(size=11)

    dashboard_button = Button(header_panel,
                              height=3,
                              width=11,
                              text="Dashboard",
                              font=myFont,
                              bg='white',
                              command=lambda: dashboard(frame2))
    dashboard_button.grid(column=1, row=0, padx=(15,0))

    user_catalog_button = Button(header_panel,
                                 height=3,
                                 width=13,
                                 text="Your Catalog",
                                 font=myFont,
                                 bg='white',
                                 command=lambda: user_catalog(frame2))
    user_catalog_button.grid(column=2, row=0)

    full_catalog_button = Button(header_panel,
                                 height=3,
                                 width=13,
                                 text="Full Catalog",
                                 font=myFont,
                                 bg='white',
                                 command=lambda: full_catalog(frame2))
    full_catalog_button.grid(column=3, row=0)

    make_request_button = Button(header_panel,
                                 height=3,
                                 width=15,
                                 text="Make a Request",
                                 font=myFont,
                                 bg='white',
                                 command=lambda: request_tool(frame2))
    make_request_button.grid(column=4, row=0)

    view_request_button = Button(header_panel,
                                 height=3,
                                 width=20,
                                 text="View your Requests",
                                 font=myFont,
                                 bg='white',
                                 command=lambda: view_request(frame2))
    view_request_button.grid(column=5, row=0)

    sign_in_out_button = Button(header_panel,
                                height=3,
                                width=15,
                                text="Sign out",
                                font=myFont,
                                bg='white',
                                command=lambda: sign_in_out(root))
    sign_in_out_button.grid(column=6, row=0, padx=(440, 0))

    header_panel.pack()


def sign_in_out(root):
    root.destroy()
    sign_in.main()
    return


def dashboard(frame2):
    prev_pane = frame2.winfo_children()

    prev_pane[len(prev_pane) - 1].pack_forget()
    pane = PanedWindow(frame2, width=1400, height=596, bg='purple')
    pane.pack()
    frame2.pack()
    return


def full_catalog(frame2):
    prev_pane = frame2.winfo_children()

    prev_pane[len(prev_pane) - 1].pack_forget()
    pane = PanedWindow(frame2, width=1400, height=596, bg='brown')
    pane.pack()
    frame2.pack()
    return


def user_catalog(frame2):
    prev_pane = frame2.winfo_children()

    prev_pane[len(prev_pane) - 1].pack_forget()
    pane = uc.get_user_catalog_pane(frame2)
    pane.pack()
    frame2.pack()
    return


def view_request(frame2):
    prev_pane = frame2.winfo_children()

    prev_pane[len(prev_pane) - 1].pack_forget()
    pane = PanedWindow(frame2, width=1400, height=596, bg='orange')
    pane.pack()
    frame2.pack()
    return


def request_tool(frame2):
    prev_pane = frame2.winfo_children()

    prev_pane[len(prev_pane) - 1].pack_forget()
    pane = PanedWindow(frame2, width=1400, height=596, bg='yellow')
    pane.pack()
    frame2.pack()
    return


if __name__ == '__main__':
    main()
