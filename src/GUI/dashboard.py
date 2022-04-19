from tkinter import *
from tkinter import font
from faker.generator import random
import src.db.recommendation as rec
import src.db.tool as tool
import src.GUI.global_variables as gbl_var


def get_dashboard_pane(root, frame2):
    root.title("Tools - Dashboard")

    pane = PanedWindow(frame2, width=1400, height=600, bg='#5D460E')
    left_pane = PanedWindow(pane, width=600, height=600, bg='white')

    chart = create_pie_chart(left_pane)
    chart.pack(padx=(50, 10), pady=10)
    label_font = font.Font(size=15)
    user_top_requested_tools_label = Label(left_pane, text="Top Lent Tools:", font=label_font, bg='white')
    user_top_requested_tools_label.pack()
    user_top_requested_tools_text = Text(left_pane, height=12, width=70, bg='gray50'
                                         , yscrollcommand=True)
    user_top_requested_tools_text.pack(padx=(10, 0), pady=(5, 13))
    left_pane.grid(column=0, row=0)

    right_pane = PanedWindow(pane, width=800, height=600, bg='white')

    top_requested_tools_label = Label(right_pane, text="Top Borrowed Tools:", font=label_font, bg='white')
    top_requested_tools_label.pack()
    top_requested_tools_text = Text(right_pane, height=33, width=80, bg='gray50', yscrollcommand=True)

    top_requested_tools_text.pack(expand=True, padx=(135, 125), pady=(16, 13))

    # load_top_borrowed(top_requested_tools_text)

    right_pane.grid(column=1, row=0)
    return pane


def load_top_borrowed(top_requested_tools_text):
    tool_list = rec.top_borrowed_tools(gbl_var.username)
    string_to_print = ""
    for user_tool in tool_list:
        categories = tool.fetch_category(user_tool['barcode'])
        category_string = ""
        for category_list in categories:
            for category in category_list.values():
                category_string += category + ","
        string_to_print += "Barcode:     | " + user_tool['barcode'] \
                           + "\nName:        | " + user_tool['name'] \
                           + "\nCategories:  | " + category_string[:len(category_string) - 1] \
                           + "\nDescription: | " + user_tool['description'] + "\n\n"
    top_requested_tools_text.configure(state='normal')
    top_requested_tools_text.delete(1.0, "end")
    top_requested_tools_text.insert(1.0, string_to_print)
    top_requested_tools_text.configure(state='disabled')


"""

Barcode:     XXXXXXXX 
Name:        XXXXXXXXXXXXX
Categories:  
Description:          

"""


data = [
    3,
    7,
    5,
    8
]

dict = {}

def create_pie_chart(root):
    # create function

    pie_chart_pane = PanedWindow(root, width=600, height=400, bg='white')

    Sum = sum(data)

    def prop(n):
        return 360.0 * n / Sum

    Label(pie_chart_pane, text="Catalogs Requested").grid(column=0, row=0)
    c = Canvas(pie_chart_pane, width=300, height=300)
    c.grid(column=0, row=1)

    previous_data_extent = 0
    for datapoint in data:
        color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        c.create_arc((2, 2, 296, 296), fill=color, outline=color, start=prop(previous_data_extent)
                     , extent=prop(datapoint))
        previous_data_extent += datapoint
        dict[datapoint] = color

    right_pane = PanedWindow(pie_chart_pane, width=300, height=400, bg='white')

    index = 0
    for key in dict:

        canvas = Canvas(right_pane, width=25, height=25, bg='white')
        canvas.create_rectangle(1, 1, 100, 100,
                                outline=dict[key], fill=dict[key])
        canvas.grid(column=0, row=index)

        label = Label(right_pane, height=3, text=key, bg='white')
        label.grid(column=1, row=index)
        index += 1
    right_pane.grid(column=1, row=1)
    return pie_chart_pane
