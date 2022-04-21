from tkinter import *
import tkinter.font as font
import GUI.global_variables as gbl_var
import src.db.request as request
from tkcalendar import Calendar
global text_box
global cal
global tools_list
global tool_index
global max_index

type_options = [
    "All",
    "Made",
    "Received"
]


def get_user_request_pane(root, frame2):
    root.title("Tools - Request In/Out box")

    pane = PanedWindow(frame2, width=1400, height=596, bg='#A67B5C')

    # The search box initialization
    search_pane = PanedWindow(pane, width=1400, height=596, bg='#A67B5C')

    sort_label = Label(search_pane, text="Sort by: ", bg="#A67B5C")
    sort_label.grid(column=0, row=0)

    type_clicked = StringVar()
    type_clicked.set(type_options[0])
    type_of_tool_dropdown = OptionMenu(search_pane, type_clicked, *type_options)
    type_of_tool_dropdown.grid(column=1, row=0, padx=(10, 25))
    sort_button = Button(search_pane, text="Sort", width=11, command=lambda: sort_database(type_clicked))
    sort_button.grid(column=2, row=0)
    search_pane.pack(padx=(110, 110), pady=4)

    # The text field initialization

    bottom_pane = PanedWindow(pane, width=1400, height=500, bg='#EFE2BA')
    output_pane = PanedWindow(bottom_pane, width=700, height=500, bg='#EFE2BA')
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

    accept_request_pane = PanedWindow(bottom_pane, width=700, height=500, bg='#EFE2BA')

    initialize_request_pane(accept_request_pane)

    accept_request_pane.grid(column=1, row=0, padx=(0, 186))
    sort_database(type_clicked)
    bottom_pane.pack()
    return pane


accept_options = [
    "accept",
    "reject"
]


def initialize_request_pane(accept_request_pane):
    label_font = font.Font(size=18)
    # Add a tool section
    request_label = Label(accept_request_pane, text="Handle a request", bg='#EFE2BA', font=label_font)
    request_label.grid(column=1, row=0)
    requestID_label = Label(accept_request_pane, text="Request ID: ", bg='#EFE2BA')
    requestID_label.grid(column=0, row=1, padx=5, pady=(10, 0))
    requestID_text = Text(accept_request_pane, width=20, height=1, bg='gray85')
    requestID_text.grid(column=1, row=1, pady=(10, 0))

    accept_label = Label(accept_request_pane, text="accept/reject: ", bg='#EFE2BA')
    accept_label.grid(column=0, row=2, padx=5, pady=(10, 0))
    accept_clicked = StringVar()
    accept_clicked.set("accept")
    accept_option = OptionMenu(accept_request_pane, accept_clicked, *accept_options)
    accept_option.grid(column=1, row=2, pady=(10, 0))

    global cal
    cal = Calendar(accept_request_pane, selectmode='day',
                   year=2022, month=5,
                   day=22)

    accept_request_button = Button(accept_request_pane,
                                   text="Submit",
                                   command=lambda: handle_request(requestID_text, accept_clicked, cal))
    accept_request_button.grid(column=2, row=2, pady=(10, 0))

    cal_label = Label(accept_request_pane, text="Enter the requested date:", bg='#EFE2BA')
    cal_label.grid(column=0, row=3, padx=(0, 5), pady=(15, 170))

    cal.grid(column=1, row=3, pady=15)


def handle_request(requestID_text, accept_clicked, cal):
    if accept_clicked.get() == "accept":
        date_list = cal.get_date().split("/")
        date_string = "20" + date_list[2] + "/" + date_list[0] + "/" + date_list[1]
        request_id = requestID_text.get("1.0", END).split("\n")[0]
        request.handle_requests(True, request_id, date_string)
    elif accept_clicked.get() == "reject":
        request_id = requestID_text.get("1.0", END).split("\n")[0]
        request.handle_requests(False, request_id, 'null')


def sort_database(type_of_tool_dropdown):
    global text_box
    global tools_list
    global tool_index
    global max_index
    tool_index = 0
    tools_list = {}
    print(type_of_tool_dropdown.get())
    if type_of_tool_dropdown.get() == "All":
        received = request.get_users_requests_received(gbl_var.username)
        made = request.get_users_requests_made(gbl_var.username)
        string_to_print = ""
        j = 0
        if len(received + made) != 0:
            for user_tool in received:
                string_to_print += print_received_string(user_tool)
                j += 1
                if j % 6 == 0:
                    tools_list[tool_index] = string_to_print
                    tool_index += 1
                    string_to_print = ""
            for user_tool in made:
                string_to_print += print_made_string(user_tool)
                j += 1
                if j % 6 == 0:
                    tools_list[tool_index] = string_to_print
                    tool_index += 1
                    string_to_print = ""
            if len(string_to_print) != 0:
                tools_list[tool_index] = string_to_print
                tool_index += 1
            max_index = tool_index
            tool_index = 0
            load_new_page()
        else:
            text_box.configure(state='normal')
            text_box.delete(1.0, "end")
            text_box.insert(1.0, " *** No Tools Found *** ")
            text_box.configure(state='disabled')
    elif type_of_tool_dropdown.get() == "Made":
        made = request.get_users_requests_made(gbl_var.username)
        string_to_print = ""
        j = 0
        tmp_list = []
        if made is not None:
            for user_tool in made:
                string_to_print += print_made_string(user_tool)
                j += 1
                if j % 6 == 0:
                    tools_list[tool_index] = string_to_print
                    tool_index += 1
                    string_to_print = ""
            if len(string_to_print) != 0:
                tools_list[tool_index] = string_to_print
                tool_index += 1
            max_index = tool_index
            tool_index = 0
            load_new_page()
        else:
            text_box.configure(state='normal')
            text_box.delete(1.0, "end")
            text_box.insert(1.0, " *** No Tools Found *** ")
            text_box.configure(state='disabled')
    elif type_of_tool_dropdown.get() == "Received":
        received = request.get_users_requests_received(gbl_var.username)
        string_to_print = ""
        j = 0
        tmp_list = []
        if received is not None:
            for user_tool in received:
                string_to_print += print_received_string(user_tool)
                j += 1
                if j % 6 == 0:
                    tools_list[tool_index] = string_to_print
                    tool_index += 1
                    string_to_print = ""
            if len(string_to_print) != 0:
                tools_list[tool_index] = string_to_print
                tool_index += 1
            max_index = tool_index
            tool_index = 0
            load_new_page()
        else:
            text_box.configure(state='normal')
            text_box.delete(1.0, "end")
            text_box.insert(1.0, " *** No Tools Found *** ")
            text_box.configure(state='disabled')
    return


def print_to_text(string_to_print):
    global text_box
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


def print_received_string(user_tool):
    return (    "Request ID:          | " + user_tool['request_id']
            + "\nRequester:           | " + user_tool['username']
            + "\nDate Requested:      | " + str(user_tool['request_date'])
            + "\nDate to be returned: | " + str(user_tool['owner_expected_date']) + "\n\n")


def print_made_string(user_tool):
    return(    "Request ID:          | " + user_tool['request_id']
           + "\nOwner:               | " + user_tool['username']
           + "\nDate Requested:      | " + str(user_tool['request_date'])
           + "\nDate to be returned: | " + str(user_tool['owner_expected_date']) + "\n\n")
