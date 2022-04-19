from random import random
from tkinter import *
import tkinter.font as font
import random as rand
import src.db.tool as tool
import src.db.request as request
import GUI.global_variables as gbl_var
from src.api.utils import SortType
from src.api.utils import SortBy
import src.db.ownership as ownership
global text_box
global tools_list
global tool_index
global max_index
global is_all
global is_overdue

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

    pane = PanedWindow(frame2, width=1400, height=596, bg='#A67B5C')

    # The search box initialization
    search_pane = PanedWindow(pane, width=1400, height=596, bg='#A67B5C')

    type_clicked = StringVar()
    type_clicked.set("All")
    type_of_tool_dropdown = OptionMenu(search_pane, type_clicked, *type_options)
    type_of_tool_dropdown.grid(column=0, row=0, padx=(0, 25))

    search_label = Label(search_pane, height=3, text="Search by: ", bg='#A67B5C')
    search_label.grid(column=1, row=0)

    search_clicked = StringVar()
    search_clicked.set("Barcode")
    search_by_dropdown = OptionMenu(search_pane, search_clicked, *search_options)
    search_by_dropdown.grid(column=2, row=0, padx=5)

    search_box = Text(search_pane, width=50, height=1, bg='gray85', yscrollcommand=False)
    search_box.grid(column=3, row=0)
    search_button = Button(search_pane, height=1, width=10, text="Search",
                           command=lambda: search_database(type_clicked, search_clicked, search_box))
    search_button.grid(column=4, row=0, padx=(5, 10))

    search_pane.pack(padx=(110, 110))

    # The text field initialization

    bottom_pane = PanedWindow(pane, width=1400, height=500, bg='#EFE2BA')

    output_pane = PanedWindow(bottom_pane, width=700, height=500, bg='#EFE2BA')
    # Text box for full catalog
    global text_box
    text_box = Text(output_pane, height=30, width=70, bg='gray85', yscrollcommand=True, state='normal')
    text_box.grid(column=0, row=0)
    # Previous Button
    Prev_button = Button(output_pane, height=1, width=10, text="Prev",
                         command=lambda: prev_list())
    Prev_button.grid(column=0, row=1, padx=(300, 10), pady=(0, 10))
    # Next button
    next_button = Button(output_pane, height=1, width=10, text="Next",
                         command=lambda: next_list())
    next_button.grid(column=0, row=1, padx=(450, 0), pady=(0, 10))

    output_pane.grid(column=0, row=0, padx=148, pady=(11, 10))

    modify_pane = PanedWindow(bottom_pane, width=700, height=500, bg='#EFE2BA')

    initialize_user_edit_pane(modify_pane)

    modify_pane.grid(column=1, row=0, padx=(0, 186))
    search_database(type_clicked,
                    search_clicked,
                    search_box)
    bottom_pane.pack()
    return pane


def search_database(type_of_tool_dropdown, search_by_dropdown, search_box):
    global text_box
    global is_all
    global is_overdue
    sort_by = SortType.NAME
    sort_type = SortBy.ASCENDING
    # if sort_by_clicked.get() == "Category":
    #     sort_by = SortType.CATEGORY
    # if sort_type_clicked.get() == "Descending":
    #     sort_type = SortBy.DESCENDING
    tools_dict_list = {}

    if type_of_tool_dropdown.get() == "All":
        tools_dict_list = tool.view_user_tools(gbl_var.username, sort_type, sort_by)
        is_all = True
        is_overdue = False
    elif type_of_tool_dropdown.get() == "Lent":
        tools_dict_list = tool.fetch_users_lent_tools(gbl_var.username)
        is_all = False
        is_overdue = False
    elif type_of_tool_dropdown.get() == "Borrowed":
        tools_dict_list = tool.fetch_users_borrowed_tools(gbl_var.username)
        is_all = False
        is_overdue = False
    elif type_of_tool_dropdown.get() == "Overdue":
        tools_borrowed = tool.fetch_overdue_borrowed_tools(gbl_var.username)
        tools_lent = tool.fetch_overdue_lent_tools(gbl_var.username)
        tools_dict_list = tools_borrowed + tools_lent
        is_all = False
        is_overdue = True

    global tools_list
    global tool_index
    tool_index = 0
    # loading each page as a key in a new dict
    tools_list = {}
    i = 0
    tmp_list = []
    if tools_dict_list is not None:
        for tool_dict in tools_dict_list:
            tmp_list.append(tool_dict)
            i += 1
            if i % 6 == 0:
                tools_list[tool_index] = tmp_list
                tmp_list = []
                tool_index += 1
                print(tool_index)
        if len(tmp_list) != 0:
            tools_list[tool_index] = tmp_list
            tool_index += 1
        global max_index
        max_index = tool_index
        tool_index = 0
        load_new_page()
    else:
        global text_box
        text_box.configure(state='normal')
        text_box.delete(1.0, "end")
        text_box.insert(1.0, " *** No Tools Found *** ")
        text_box.configure(state='disabled')
    return


def load_new_page():
    global tools_list
    global tool_index
    print_to_text(tools_list[tool_index])


def prev_list():
    global tool_index
    if tool_index - 1 > 0:
        tool_index -= 1
        load_new_page()


def next_list():
    global tool_index
    global max_index
    if tool_index + 1 < max_index:
        tool_index += 1
        load_new_page()


def print_to_text(tools):
    global is_all
    global is_overdue
    string_to_print = ""
    for user_tool in tools:
        if is_overdue:
            string_to_print += "*** OVERDUE ***\n"
        categories = tool.fetch_category(user_tool['barcode'])
        category_string = ""
        for category_list in categories:
            for category in category_list.values():
                category_string += category + ", "
        if is_all:
            string_to_print +=   "Barcode:     | " + user_tool['barcode'] \
                               + "\nName:        | " + user_tool['name'] \
                               + "\nCategories:  | " + category_string[:len(category_string) - 2] \
                               + "\nDescription: | " + user_tool['description'] + "\n\n"
        else:
            string_to_print +=   "Barcode:             | " + user_tool['barcode'] \
                               + "\nName:                | " + user_tool['name'] \
                               + "\nDate to be returned: | " + str(user_tool['owner_expected_date'])\
                               + "\nCategories:          | " + category_string[:len(category_string) - 2] \
                               + "\nDescription:         | " + user_tool['description'] + "\n\n"
    text_box.configure(state='normal')
    text_box.delete(1.0, "end")
    text_box.insert(1.0, string_to_print)
    text_box.configure(state='disabled')

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
    add_tool_label = Label(modify_pane, text="Add a tool", bg='#EFE2BA', font=label_font)
    add_tool_label.grid(column=1, row=0)
    name_label = Label(modify_pane, text="Tool name: ", bg='#EFE2BA')
    name_label.grid(column=0, row=1, padx=5, pady=(10, 0))
    name_text = Text(modify_pane, width=20, height=1, bg='gray85')
    name_text.grid(column=1, row=1, pady=(10, 0))

    price_label = Label(modify_pane, text="Tool price (#.##): ", bg='#EFE2BA')
    price_label.grid(column=0, row=2, padx=5, pady=(10, 0))
    price_text = Text(modify_pane, width=20, height=1, bg='gray85')
    price_text.grid(column=1, row=2, pady=(10, 0))
    price_error_label = Label(modify_pane, text="Error decimal number!", bg='#EFE2BA', fg='#EFE2BA')
    price_error_label.grid(column=2, row=2, padx=5, pady=(0, 0))

    desc_label = Label(modify_pane, text="Description: ", bg='#EFE2BA')
    desc_label.grid(column=0, row=3, padx=5, pady=(10, 30))
    desc_text = Text(modify_pane, width=20, height=3, bg='gray85')
    desc_text.grid(column=1, row=3, pady=(10, 0))

    shareable_label = Label(modify_pane, text="Shareable: ", bg='#EFE2BA')
    shareable_label.grid(column=0, row=4, pady=(10, 0))
    shareable_clicked = StringVar()
    shareable_clicked.set("Yes")
    sharable_option = OptionMenu(modify_pane, shareable_clicked, *shareable_option)
    sharable_option.grid(column=1, row=4, pady=(10, 0))

    add_tool_button = Button(modify_pane,
                             text="Add tool",
                             command=lambda: add_tool(name_text, price_text, price_error_label, desc_text, shareable_clicked))
    add_tool_button.grid(column=2, row=4, pady=(10, 0))
    # Delete a tool section
    delete_tool_label = Label(modify_pane, text="Delete a tool", bg='#EFE2BA', font=label_font)
    delete_tool_label.grid(column=1, row=5, pady=(10, 0))
    barcode_label = Label(modify_pane, text="Enter a barcode: ", bg='#EFE2BA')
    barcode_label.grid(column=0, row=6, padx=5, pady=(10, 0))
    delete_barcode_text = Text(modify_pane, width=20, height=1, bg='gray85')
    delete_barcode_text.grid(column=1, row=6, pady=(10, 0))
    delete_tool_button = Button(modify_pane,
                                text="delete tool",
                                command=lambda: delete_tool(delete_barcode_text))
    delete_tool_button.grid(column=2, row=6, pady=(10, 0), padx=(10, 0))
    # Method a tool section
    modify_label = Label(modify_pane, text="Modify a tool ", bg='#EFE2BA', font=label_font)
    modify_label.grid(column=1, row=7, padx=5, pady=(10, 0))
    modify_barcode_label = Label(modify_pane, text="Enter a barcode: ", bg='#EFE2BA')
    modify_barcode_label.grid(column=0, row=8, padx=5, pady=(10, 0))
    modify_barcode_text = Text(modify_pane, width=20, height=1, bg='gray85')
    modify_barcode_text.grid(column=1, row=8, pady=(10, 0))
    modify_clicked = StringVar()
    modify_clicked.set("Name")
    modify_text = Text(modify_pane, width=20, height=1, bg='gray85')
    modify_text.grid(column=1, row=9)
    what_to_modify_option = OptionMenu(modify_pane, modify_clicked, *modify_option)
    what_to_modify_option.grid(column=0, row=9)
    modify_tool_button = Button(modify_pane,
                                text="modify tool",
                                command=lambda: modify_tool(modify_barcode_text, modify_clicked, modify_text))
    modify_tool_button.grid(column=2, row=9, pady=(10, 0), padx=(10, 0))

    return_tool_label = Label(modify_pane, text="Return a tool", bg='#EFE2BA', font=label_font)
    return_tool_label.grid(column=1, row=10, pady=(10, 0))
    return_label = Label(modify_pane, text="Enter a barcode: ", bg='#EFE2BA')
    return_label.grid(column=0, row=11, padx=5, pady=(10, 0))
    return_tool_text = Text(modify_pane, width=20, height=1, bg='gray85')
    return_tool_text.grid(column=1, row=11, pady=(10, 0))
    return_tool_button = Button(modify_pane,
                                text="Return tool",
                                command=lambda: return_tool(return_tool_text))
    return_tool_button.grid(column=2, row=11, pady=(10, 0), padx=(10, 0))

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


def add_tool(name_text, price_text, price_error_label, desc_text, shareable_clicked):
    name = name_text.get("1.0", END).split("\n")[0]
    desc = desc_text.get("1.0", END).split("\n")[0]
    try:
        price = float(price_text.get("1.0", END).split("\n")[0])
        shareable = shareable_clicked.get()
        if shareable == "Yes":
            shareable = True
        if shareable == "No":
            shareable = False
        barcode = rand.randrange(10000000, 99999999)
        while tool.fetch_tool(str(barcode)) is not None:
            barcode = rand.randrange(10000000, 99999999)
        tool.insert_tool(a=str(barcode), c=shareable, d=name, e=desc, f=gbl_var.username)
        ownership.insert_ownership(a=gbl_var.username, b=barcode, c=price)
        price_error_label.configure(fg='#EFE2BA')
    except ValueError:
        throw_value_error(price_error_label)


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
    barcode = barcode_text.get("1.0", END).split("\n")[0]
    what_to_modify = modify_clicked.get().split("\n")[0]
    modify_string = modify_string.get("1.0", END).split("\n")[0]
    if what_to_modify == "Category":
        tool.create_category(a=modify_string, b=barcode)
    elif what_to_modify == "Name":
        tool.update_tool(barcode, name=modify_string)
    elif what_to_modify == "Description":
        tool.update_tool(barcode, description=modify_string)


def return_tool(return_tool_text):
    barcode = return_tool_text.get("1.0", END).split("\n")[0]
    holder = tool.fetch_tool(barcode)['holder']
    if holder == gbl_var.username:
        request.return_tool(barcode)


def throw_value_error(price_error_label):
    price_error_label.configure(fg='red')


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
