from tkinter import *
import tkinter.font as font
import GUI.global_variables as gbl_var


def get_profile_pane(root, frame2):
    root.title("Tools - Profile")

    pane = PanedWindow(frame2, width=1400, height=596, bg='#8bc34a')

    bottomPane = PanedWindow(pane, width=1400, height=596, bg='#8bc34a')

    leftPane = PanedWindow(bottomPane, width=600, height=596, bg='brown')
    leftPane.grid(row=0, column=0)

    rightPane = PanedWindow(bottomPane, width=800, height=596, bg='red')
    rightPane.grid(row=0, column=1)

    bottomPane.pack()
    
    return pane


def get_profile(root, frame2):
    pass
