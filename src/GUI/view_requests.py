from tkinter import *
import tkinter.font as font
import GUI.global_variables as gbl_var
import src.db.request as request

global text_box

type_options = [
    "All",
    "Your requests",
    "Other's requests"
]


search_options = [
    "Request ID",
    "Barcode",
    "Category",
    "Name"
]


def get_user_request_pane(root, frame2):
    root.title("Tools - Request In/Out box")

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
    global text_box
    text_box = Text(search_pane, height=32, width=70, bg='gray75', yscrollcommand=True, state='normal')
    text_box.pack(expand=True)

    search_pane.grid(column=0, row=0, padx=156, pady=(11, 10))

    accept_request_pane = PanedWindow(bottom_pane, width=700, height=500, bg='white')

    initialize_request_pane(accept_request_pane)

    accept_request_pane.grid(column=1, row=0, padx=(0, 186))
    search_database(type_clicked, search_clicked, search_box)
    bottom_pane.pack()
    return pane


accept_options = [
    "accept",
    "reject"
]


def initialize_request_pane(accept_request_pane):
    label_font = font.Font(size=18)
    # Add a tool section
    request_label = Label(accept_request_pane, text="Handle a request", bg='white', font=label_font)
    request_label.grid(column=1, row=0)
    requestID_label = Label(accept_request_pane, text="Request ID: ", bg='white')
    requestID_label.grid(column=0, row=1, padx=5, pady=(10, 0))
    requestID_text = Text(accept_request_pane, width=20, height=1, bg='white')
    requestID_text.grid(column=1, row=1, pady=(10, 0))

    accept_label = Label(accept_request_pane, text="accept/reject: ", bg='white')
    accept_label.grid(column=0, row=2, padx=5, pady=(10, 0))
    accept_clicked = StringVar()
    accept_clicked.set("accept")
    accept_option = OptionMenu(accept_request_pane, accept_clicked, *accept_options)
    accept_option.grid(column=1, row=2, pady=(10, 0))

    accept_request_button = Button(accept_request_pane,
                                   text="Submit",
                                   command=lambda: handle_request(requestID_text, accept_clicked))
    accept_request_button.grid(column=2, row=2, pady=(10, 0))


def handle_request(requestID_text, accept_clicked):
    if accept_clicked.get() == "accept":
        print("accepted")
        print(requestID_text.get("1.0",END))
    elif accept_clicked.get() == "reject":
        print("rejected")
        print(requestID_text.get("1.0", END))
    else:
        print("error with request")
        print(requestID_text.get("1.0", END))


def search_database(type_of_tool_dropdown, search_by_dropdown, search_box):
    global text_box
    if type_of_tool_dropdown.get() == "All":
        received = request.get_users_requests_received(gbl_var.username)
        made = request.get_users_requests_made(gbl_var.username)
        string_to_print = ""
        for user_tool in received:
            string_to_print += "Request ID:          " + user_tool['request_id'] \
                               + "\nOwner:               " + user_tool['username'] \
                               + "\nDate Requested:      " + str(user_tool['request_date']) \
                               + "\nDate to be returned: " + str(user_tool['owner_expected_date']) + "\n\n"
        for user_tool in made:
            string_to_print += "Request ID:          " + user_tool['request_id'] \
                               + "\nHolder:              " + user_tool['username'] \
                               + "\nDate Requested:      " + str(user_tool['request_date']) \
                               + "\nDate to be returned: " + str(user_tool['owner_expected_date']) + "\n\n"
        text_box.delete(1.0, "end")
        text_box.insert(1.0, string_to_print)
    elif type_of_tool_dropdown.get() == "Your requests":
        made = request.get_users_requests_made(gbl_var.username)
        string_to_print = ""
        for user_tool in made:
            string_to_print += "Request ID:          " + user_tool['request_id'] \
                               + "\nHolder:              " + user_tool['username'] \
                               + "\nDate Requested:      " + str(user_tool['request_date']) \
                               + "\nDate to be returned: " + str(user_tool['owner_expected_date']) + "\n\n"
        text_box.delete(1.0, "end")
        text_box.insert(1.0, string_to_print)
    elif type_of_tool_dropdown.get() == "Other's requests":
        received = request.get_users_requests_received(gbl_var.username)
        string_to_print = ""
        for user_tool in received:
            string_to_print += "Request ID:          " + user_tool['request_id'] \
                               + "\nOwner:               " + user_tool['username'] \
                               + "\nDate Requested:      " + str(user_tool['request_date']) \
                               + "\nDate to be returned: " + str(user_tool['owner_expected_date']) + "\n\n"
        text_box.delete(1.0, "end")
        text_box.insert(1.0, string_to_print)
    return

"""
Request ID:          REQTXXXXXXXX 
Holder:              XXX1234
Date Requested:      XXXX-XX-XX
Date to be returned: XXXX-XX-XX

Request ID:          REQTXXXXXXXX 
Owner:               XXX1234
Date Requested:      XXXX-XX-XX
Date to be returned: XXXX-XX-XX

"""