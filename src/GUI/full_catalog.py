from tkinter import *
import tkinter.font as font
from tkcalendar import Calendar
import src.db.tool as tool
import GUI.global_variables as gbl_var
from src.api.utils import SortType
from src.api.utils import SortBy
import src.db.request as request
import random as rand
global text_box
global tools_list
global tool_index
global max_index

type_options = [
    "All",
    "Available",
]

sort_by_options = [
    "Name",
    "Category"
]

sort_type_options = [
    "Ascending",
    "Descending"
]

search_options = [
    "Barcode",
    "Category",
    "Name"
]


def get_full_catalog_pane(root, frame2):
    root.title("Tools - User Catalog")

    pane = PanedWindow(frame2, width=1400, height=596, bg='#A67B5C')

    # The search box initialization
    search_pane = PanedWindow(pane, width=1400, height=596, bg='#A67B5C')
    # Sort:
    sort_label = Label(search_pane, height=3, text="Sort: ", bg='#A67B5C')
    sort_label.grid(column=0, row=0)
    # All or Available
    type_clicked = StringVar()
    type_clicked.set(type_options[0])
    type_of_tool_dropdown = OptionMenu(search_pane, type_clicked, *type_options)
    type_of_tool_dropdown.grid(column=1, row=0, padx=(0, 5))
    # Asc or Desc sort
    sort_type_clicked = StringVar()
    sort_type_clicked.set(sort_type_options[0])
    sort_type_dropdown = OptionMenu(search_pane, sort_type_clicked, *sort_type_options)
    sort_type_dropdown.grid(column=2, row=0, padx=(0, 5))
    # By:
    by_label = Label(search_pane, height=3, text="By: ", bg='#A67B5C')
    by_label.grid(column=3, row=0)
    # Name or Category
    sort_by_clicked = StringVar()
    sort_by_clicked.set(sort_by_options[0])
    sort_by_dropdown = OptionMenu(search_pane, sort_by_clicked, *sort_by_options)
    sort_by_dropdown.grid(column=4, row=0, padx=(0, 25))
    # Search by:
    search_label = Label(search_pane, height=3, text="Search by: ", bg='#A67B5C')
    search_label.grid(column=5, row=0)
    # Barcode, Name, or Category
    search_clicked = StringVar()
    search_clicked.set(search_options[0])
    search_by_dropdown = OptionMenu(search_pane, search_clicked, *search_options)
    search_by_dropdown.grid(column=6, row=0, padx=5)
    # search box
    search_box = Text(search_pane, width=50, height=1, bg='gray75', yscrollcommand=False)
    search_box.grid(column=7, row=0)
    # search button
    search_button = Button(search_pane, height=1, width=10, text="Search",
                           command=lambda: search_database(type_clicked,
                                                           search_clicked,
                                                           sort_type_clicked,
                                                           sort_by_clicked,
                                                           search_box))
    search_button.grid(column=8, row=0, padx=(5, 10))
    search_pane.pack(padx=(110, 110))

    # The text field initialization
    bottom_pane = PanedWindow(pane, width=1400, height=500, bg='#EFE2BA')
    output_pane = PanedWindow(bottom_pane, width=700, height=500, bg='#EFE2BA')
    # Text box for full catalog
    global text_box
    text_box = Text(output_pane, height=30, width=70, bg='gray75', yscrollcommand=True, state='normal')
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
    # Right pane for user requests
    modify_pane = PanedWindow(bottom_pane, width=700, height=500, bg='#EFE2BA')
    initialize_user_edit_pane(modify_pane)
    modify_pane.grid(column=1, row=0, padx=(0, 186))

    search_database(type_clicked,
                    search_clicked,
                    sort_type_clicked,
                    sort_by_clicked,
                    search_box)
    bottom_pane.pack()
    return pane


def search_database(type_of_tool_dropdown, search_clicked, sort_type_clicked, sort_by_clicked, search_box):
    sort_by = SortType.NAME
    sort_type = SortBy.ASCENDING
    if sort_by_clicked.get() == "Category":
        sort_by = SortType.CATEGORY
    if sort_type_clicked.get() == "Descending":
        sort_type = SortBy.DESCENDING
    search = search_box.get("1.0", END).split("\n")[0]
    tools_dict_list = {}
    if search != "":
        tools_dict_list = tool.search_tool(search_clicked.get(), search, sort_type, sort_by)
    elif type_of_tool_dropdown.get() == "All":
        tools_dict_list = tool.fetch_all_tools(sort_type, sort_by)
    else:
        tools_dict_list = tool.fetch_available_tools(sort_type, sort_by)

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


def print_to_text(tools):
    global text_box
    string_to_print = ""
    for user_tool in tools:
        categories = tool.fetch_category(user_tool['barcode'])
        category_string = ""
        for category_list in categories:
            for category in category_list.values():
                category_string += category + ","
        string_to_print += "Barcode:     | " + user_tool['barcode'] \
                           + "\nName:        | " + user_tool['name'] \
                           + "\nCategories:  | " + category_string[:len(category_string) - 1] \
                           + "\nDescription: | " + user_tool['description'] + "\n\n"
    text_box.configure(state='normal')
    text_box.delete(1.0, "end")
    text_box.insert(1.0, string_to_print)
    text_box.configure(state='disabled')


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
    add_tool_label = Label(modify_pane, text="Request a tool", bg='#EFE2BA', font=label_font)
    add_tool_label.grid(column=1, row=0)
    barcode_label = Label(modify_pane, text="Enter a barcode:", bg='#EFE2BA')
    barcode_label.grid(column=0, row=1, padx=(40, 0), pady=(10, 0))
    barcode_text = Text(modify_pane, width=20, height=1, bg='gray85')
    barcode_text.grid(column=1, row=1, pady=(10, 0))

    borrow_period_label = Label(modify_pane, text="Borrow period (in days):", bg='#EFE2BA')
    borrow_period_label.grid(column=0, row=2, pady=(0, 5))
    borrow_period_text = Text(modify_pane, width=20, heigh=1, bg='gray85')
    borrow_period_text.grid(column=1, row=2, pady=(5, 10))

    cal_label = Label(modify_pane, text="Enter the requested date:", bg='#EFE2BA')
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
    barcode = barcode_text.get("1.0", END).split("\n")[0]
    date_list = cal.get_date().split("/")
    date_string = "20" + date_list[2] + "/" + date_list[0] + "/" + date_list[1]
    borrowed_period = borrow_period_text.get("1.0", END).split("\n")[0]
    username = gbl_var.username
    request_id = "REQT" + str(rand.randrange(10000000, 99999999))

    while request.get_request(request_id) is not None:
        request_id = "REQT" + str(rand.randrange(10000000, 99999999))

    request.create_request(a=request_id, b=username, c=barcode, d=borrowed_period, e=date_string)
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