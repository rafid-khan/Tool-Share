from random import random
from tkinter import *
import tkinter.font as font
import random as rand
import src.db.tool as tool
import GUI.global_variables as gbl_var

global text_box

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
    global text_box
    text_box = Text(search_pane, height=32, width=70, bg='gray75', yscrollcommand=True, state='normal')
    text_box.pack(expand=True)

    search_pane.grid(column=0, row=0, padx=148, pady=(11, 10))

    modify_pane = PanedWindow(bottom_pane, width=700, height=500, bg='white')

    initialize_user_edit_pane(modify_pane)

    modify_pane.grid(column=1, row=0, padx=(0, 186))
    search_database(type_clicked, search_clicked, search_box)
    bottom_pane.pack()
    return pane


def search_database(type_of_tool_dropdown, search_by_dropdown, search_box):
    global text_box
    if type_of_tool_dropdown.get() == "All":
        tools = tool.view_user_tools(gbl_var.username)
        string_to_print = get_tool_string(tools, False, True)
        text_box.configure(state='normal')
        text_box.delete(1.0, "end")
        text_box.insert(1.0, string_to_print)
        text_box.configure(state='disabled')
    elif type_of_tool_dropdown.get() == "Lent":
        tools = tool.fetch_users_lent_tools(gbl_var.username)
        tools_overdue = tool.fetch_overdue_lent_tools(gbl_var.username)
        string_to_print = get_tool_string(tools, False, False)
        string_to_print += get_tool_string(tools_overdue, True, False)
        text_box.configure(state='normal')
        text_box.delete(1.0, "end")
        text_box.insert(1.0, string_to_print)
        text_box.configure(state='disabled')
    elif type_of_tool_dropdown.get() == "Borrowed":
        tools = tool.fetch_users_borrowed_tools(gbl_var.username)
        tools_overdue = tool.fetch_overdue_borrowed_tools(gbl_var.username)
        string_to_print = get_tool_string(tools, False, False)
        string_to_print += get_tool_string(tools_overdue, True, False)
        text_box.configure(state='normal')
        text_box.delete(1.0, "end")
        text_box.insert(1.0, string_to_print)
        text_box.configure(state='disabled')
    elif type_of_tool_dropdown.get() == "Overdue":
        tools_borrowed = tool.fetch_overdue_borrowed_tools(gbl_var.username)
        tools_lent = tool.fetch_overdue_lent_tools(gbl_var.username)
        string_to_print = get_tool_string(tools_borrowed, True, False)
        string_to_print += get_tool_string(tools_lent, True, False)
        text_box.configure(state='normal')
        text_box.delete(1.0, "end")
        text_box.insert(1.0, string_to_print)
        text_box.configure(state='disabled')


    return


def get_tool_string(tools, isOverdue, isAll):
    # print(tools)
    string_to_print = ""
    for user_tool in tools:
        if isOverdue:
            string_to_print += "*** OVERDUE ***\n"
        categories = tool.view_tool_category(user_tool['barcode'])
        category_string = ""
        for category_list in categories:
            for category in category_list.values():
                category_string += category + ","
        if (isAll):
            string_to_print +=   "Barcode:     | " + user_tool['barcode'] \
                               + "\nName:        | " + user_tool['name'] \
                               + "\nCategories:  | " + category_string[:len(category_string) - 1] \
                               + "\nDescription: | " + user_tool['description'] + "\n\n"
        else:
            string_to_print +=   "Barcode:             | " + user_tool['barcode'] \
                               + "\nName:                | " + user_tool['name'] \
                               + "\nDate to be returned: | " + str(user_tool['owner_expected_date'])\
                               + "\nCategories:          | " + category_string[:len(category_string) - 1] \
                               + "\nDescription:         | " + user_tool['description'] + "\n\n"
        # print(string_to_print)
    return string_to_print

"""

Barcode:     XXXXXXXX 
Name:        XXXXXXXXXXXXX
Categories:  
Description:          

"""

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
    name = name_text.get("1.0", END).split("\n")[0]
    desc = desc_text.get("1.0", END).split("\n")[0]
    shareable = shareable_clicked.get()
    if shareable == "Yes":
        shareable = True
    if shareable == "No":
        shareable = False
    barcode = rand.randrange(10000000, 99999999)
    while tool.fetch_tool(str(barcode)) is not None:
        barcode = rand.randrange(10000000, 99999999)
        print(barcode)
    tool.insert_tool(a=str(barcode), c=shareable, d=name, e=desc, f=gbl_var.username)

    pass


def delete_tool(barcode_text):
    barcode = barcode_text.get("1.0", END).split("\n")[0]
    print(tool.fetch_tool(barcode))
    if tool.fetch_tool(barcode) is None:
        print("No tool")
    else:
        tool.delete_tool(barcode)



def modify_tool(barcode_text, modify_clicked, modify_string):
    print("barcode: " + barcode_text.get("1.0", END) + " what to modify: " + modify_clicked.get()
          + " modify: " + modify_string.get("1.0", END))


"""
Barcode: XXXXXXXX Name: XXXXXXXXXXXXX
Categories: 
Description:

*** OVERDUE ***
Barcode: XXXXXXXX Name: XXXXXXXXXXXXX
Categories: 
Return Date:
Description:

*** OVERDUE ***
Barcode: XXXXXXXX Name: XXXXXXXXXXXXX
Categories: 
Return Date:
Description:

*** OVERDUE ***
Barcode: XXXXXXXX Name: XXXXXXXXXXXXX
Categories: 
Return Date:
Description:

"""
