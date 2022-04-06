from tkinter import *
import tkinter.font as font


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


def get_user_catalog_pane(root, frame2):
    root.title("Tools - User Catalog")

    pane = PanedWindow(frame2, width=1400, height=596, bg='#755c36')

    # The search box initialization
    search_pane = PanedWindow(pane, width=1400, height=596, bg='#755c36')

    type_clicked = StringVar()
    type_clicked.set("All")
    type_of_tool_dropdown = OptionMenu(search_pane, type_clicked, *type_options)
    type_of_tool_dropdown.grid(column=0, row=0, padx=(0, 25))

    search_label = Label(search_pane, height=3, text="Search by: ", bg='#755c36')
    search_label.grid(column=1, row=0)

    search_clicked = StringVar()
    search_clicked.set("Barcode")
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
    add_tool_label = Label(modify_pane, text="Add a tool", bg='white', font=label_font)
    add_tool_label.grid(column=1, row=0)
    name_label = Label(modify_pane, text="Tool name: ", bg='white')
    name_label.grid(column=0, row=1, padx=5, pady=(10, 0))
    name_text = Text(modify_pane, width=20, height=1, bg='white')
    name_text.grid(column=1, row=1, pady=(10, 0))

    desc_label = Label(modify_pane, text="Description: ", bg='white')
    desc_label.grid(column=0, row=2, padx=5, pady=(10, 30))
    desc_text = Text(modify_pane, width=20, height=3, bg='white')
    desc_text.grid(column=1, row=2, pady=(10, 0))

    shareable_label = Label(modify_pane, text="Shareable: ", bg='white')
    shareable_label.grid(column=0, row=3, pady=(10, 0))
    shareable_clicked = StringVar()
    shareable_clicked.set("Yes")
    sharable_option = OptionMenu(modify_pane, shareable_clicked, *shareable_option)
    sharable_option.grid(column=1, row=3, pady=(10, 0))

    add_tool_button = Button(modify_pane,
                             text="Add tool",
                             command=lambda: add_tool(name_text, desc_text, shareable_clicked))
    add_tool_button.grid(column=2, row=3, pady=(10, 0))
    # Delete a tool section
    delete_tool_label = Label(modify_pane, text="Delete a tool", bg='white', font=label_font)
    delete_tool_label.grid(column=1, row=4, pady=(10, 0))
    barcode_label = Label(modify_pane, text="Enter a barcode: ", bg='white')
    barcode_label.grid(column=0, row=5, padx=5, pady=(10, 0))
    delete_barcode_text = Text(modify_pane, width=20, height=1, bg='white')
    delete_barcode_text.grid(column=1, row=5, pady=(10, 0))
    delete_tool_button = Button(modify_pane,
                                text="delete tool",
                                command=lambda: delete_tool(delete_barcode_text))
    delete_tool_button.grid(column=2, row=5, pady=(10, 0), padx=(10, 0))
    # Method a tool section
    modify_label = Label(modify_pane, text="Modify a tool ", bg='white', font=label_font)
    modify_label.grid(column=1, row=6, padx=5, pady=(10, 0))
    modify_barcode_label = Label(modify_pane, text="Enter a barcode: ", bg='white')
    modify_barcode_label.grid(column=0, row=7, padx=5, pady=(10, 0))
    modify_barcode_text = Text(modify_pane, width=20, height=1, bg='white')
    modify_barcode_text.grid(column=1, row=7, pady=(10, 0))
    modify_clicked = StringVar()
    modify_clicked.set("Name")
    modify_text = Text(modify_pane, width=20, height=1)
    modify_text.grid(column=1, row=8)
    what_to_modify_option = OptionMenu(modify_pane, modify_clicked, *modify_option)
    what_to_modify_option.grid(column=0, row=8)
    modify_tool_button = Button(modify_pane,
                                text="modify tool",
                                command=lambda: modify_tool(modify_barcode_text, modify_clicked, modify_text))
    modify_tool_button.grid(column=2, row=8, pady=(10, 0), padx=(10, 0))

    initialize_modify_action(modify_clicked, modify_text, modify_tool_button)


def initialize_modify_action(modify_clicked, modify_text, modify_tool_button):
    def update_modify(*args):
        selection = modify_clicked.get()
        if selection == "Name":
            modify_text.configure(width=20, height=1)
            modify_tool_button["text"] = "Modify Name"
        elif selection == "Category":
            modify_text.configure(width=20, height=1)
            modify_tool_button["text"] = "Modify Category"
        else:
            modify_text.configure(width=20, height=3)
            modify_tool_button["text"] = "Modify Desc"
    modify_clicked.trace("w", update_modify)


def add_tool(name_text, desc_text, shareable_clicked):
    print(name_text.get("1.0", END))
    print(desc_text.get("1.0", END))
    print(shareable_clicked.get())
    pass


def delete_tool(barcode_text):
    print(barcode_text.get("1.0", END))
    pass


def modify_tool(barcode_text, modify_clicked, modify_string):
    print("barcode: " + barcode_text.get("1.0", END) + " what to modify: " + modify_clicked.get()
          + " modify: " + modify_string.get("1.0", END))


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