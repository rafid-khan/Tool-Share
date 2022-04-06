from tkinter import *
import tkinter.font as font
from tkcalendar import Calendar

type_options = [
    "All",
    "Available",
]


search_options = [
    "Barcode",
    "Category",
    "Name"
]


def get_full_catalog_pane(root, frame2):
    root.title("Tools - User Catalog")

    pane = PanedWindow(frame2, width=1400, height=596, bg='#755c36')

    # The search box initialization
    search_pane = PanedWindow(pane, width=1400, height=596, bg='#755c36')

    type_clicked = StringVar()
    type_clicked.set(type_options[0])
    type_of_tool_dropdown = OptionMenu(search_pane, type_clicked, *type_options)
    type_of_tool_dropdown.grid(column=0, row=0, padx=(0, 25))

    search_label = Label(search_pane, height=3, text="Search by: ", bg='#755c36')
    search_label.grid(column=1, row=0)

    search_clicked = StringVar()
    search_clicked.set(search_options[0])
    search_by_dropdown = OptionMenu(search_pane, search_clicked, *search_options)
    search_by_dropdown.grid(column=2, row=0, padx=5)

    search_box = Text(search_pane, width=50, height=1, bg='gray75', yscrollcommand=False)
    search_box.grid(column=3, row=0)

    search_button = Button(search_pane, height=1, width=10, text="Search",
                           command=lambda: search_database(type_clicked, search_clicked, search_box))
    search_button.grid(column=4, row=0, padx=(5, 10))

    search_pane.pack(padx=(110, 110))

    # The text field initialization

    bottom_pane = PanedWindow(pane, width=1400, height=500, bg='white')

    search_pane = PanedWindow(bottom_pane, width=700, height=500, bg='white')

    text_box = Text(search_pane, height=32, width=70, bg='gray75', yscrollcommand=True, state='normal')
    text_box.pack(expand=True)

    search_pane.grid(column=0, row=0, padx=148, pady=(11, 10))

    modify_pane = PanedWindow(bottom_pane, width=700, height=500, bg='white')

    initialize_user_edit_pane(modify_pane)

    modify_pane.grid(column=1, row=0, padx=(0, 186))

    bottom_pane.pack()
    return pane


def search_database(type_of_tool_dropdown, search_by_dropdown, search_box):
    print(type_of_tool_dropdown.get())
    print(search_by_dropdown.get())
    print(search_box.get("1.0", END))

    return


shareable_option = [
    "Yes",
    "No"
]


modify_option = [
    "Name",
    "Category",
    "Description"
]


def initialize_user_edit_pane(modify_pane):
    label_font = font.Font(size=18)
    # Add a tool section
    add_tool_label = Label(modify_pane, text="Request a tool", bg='white', font=label_font)
    add_tool_label.grid(column=1, row=0)
    barcode_label = Label(modify_pane, text="Enter a barcode:", bg='white')
    barcode_label.grid(column=0, row=1, padx=(40, 0), pady=(10, 0))
    barcode_text = Text(modify_pane, width=20, height=1, bg='white')
    barcode_text.grid(column=1, row=1, pady=(10, 0))

    borrow_period_label = Label(modify_pane, text="Borrow period (in days):", bg='white')
    borrow_period_label.grid(column=0, row=2, pady=(0, 5))
    borrow_period_text = Text(modify_pane, width=20, heigh=1, bg='white')
    borrow_period_text.grid(column=1, row=2, pady=(5, 10))

    cal_label = Label(modify_pane, text="Enter the requested date:", bg='white')
    cal_label.grid(column=0, row=3, padx=(0, 5), pady=(0, 170))
    cal = Calendar(modify_pane, selectmode='day',
                   year=2020, month=5,
                   day=22)
    cal.grid(column=1, row=3)

    request_tool_button = Button(modify_pane,
                             text="Request tool",
                             command=lambda: request_tool(barcode_text, cal, borrow_period_text))
    request_tool_button.grid(column=1, row=4, pady=(20, 0))


def request_tool(barcode_text, cal, borrow_period_text):
    print(barcode_text.get("1.0", END))
    date_list =cal.get_date().split("/")
    print("20" + date_list[2] + "/" + date_list[0] + "/" + date_list[1])
    print(borrow_period_text.get("1.0", END))
    pass


"""
Barcode: XXXXXXXX Name: XXXXXXXXXXXXX
Categories: 
Description:

Barcode: XXXXXXXX Name: XXXXXXXXXXXXX
Categories: 
Description:

Barcode: XXXXXXXX Name: XXXXXXXXXXXXX
Categories: 
Description:

"""