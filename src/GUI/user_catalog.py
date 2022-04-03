import tkinter as tk
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image


type_options = [
    "All",
    "Lent",
    "Borrowed",
    "Overdue"
]

search_options = [
    "Barcode",
    "Category",
    "Name"
]

def get_user_catalog_pane(root):
    pane = PanedWindow(root, width=1400, height=596, bg='blue')

    search_pane = PanedWindow(pane, width=1400, height=596, bg='white')

    type_clicked = StringVar()
    type_clicked.set("All")
    type_of_tool_dropdown = OptionMenu(search_pane, type_clicked, *type_options)
    type_of_tool_dropdown.grid(column=0, row=0, padx=(0,25))

    search_label = Label(search_pane, height=3, text="Search by: ", bg='white')
    search_label.grid(column=1, row=0)

    search_clicked = StringVar()
    search_clicked.set("Barcode")
    search_by_dropdown = OptionMenu(search_pane, search_clicked, *search_options)
    search_by_dropdown.grid(column=2, row=0, padx=5)

    search_box = Text(search_pane, width=50, height=1)
    search_box.grid(column=3, row=0)

    search_button = Button(search_pane, height=1, width=10, text="Search",
                           command=lambda: search_database(type_of_tool_dropdown, search_by_dropdown))
    search_button.grid(column=4, row=0, padx=(5, 0))

    search_pane.pack(padx=332)

    return pane


def search_database(type_of_tool_dropdown, search_by_dropdown):

    return