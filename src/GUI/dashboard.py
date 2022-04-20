from tkinter import *
from tkinter import font
from faker.generator import random
import src.db.recommendation as rec
import src.db.tool as tool
import GUI.global_variables as gbl_var


def get_dashboard_pane(root, frame2):
    root.title("Tools - Dashboard")

    pane = PanedWindow(frame2, width=1400, height=600, bg='#EFE2BA')
    left_pane = PanedWindow(pane, width=600, height=600, bg='#EFE2BA')

    chart = create_pie_chart(left_pane)
    chart.pack(padx=(50, 10), pady=10)
    label_font = font.Font(size=15)
    latest_requests_label = Label(left_pane, text="Latest Three Requests:", font=label_font, bg='#EFE2BA')
    latest_requests_label.pack()
    latest_requests_text = Text(left_pane, height=12, width=70, bg='gray85'
                                         , yscrollcommand=True)
    load_latest_requests(latest_requests_text)
    latest_requests_text.pack(padx=(10, 0), pady=(5, 13))
    left_pane.grid(column=0, row=0, pady=(0, 5))

    right_pane = PanedWindow(pane, width=800, height=600, bg='#EFE2BA')

    top_lent_tools_label = Label(right_pane, text="Top Lent Tools:", font=label_font, bg='#EFE2BA')
    top_lent_tools_label.grid(column=0, row=0, padx=(95, 0))
    top_lent_tools_text = Text(right_pane, height=33, width=40, bg='gray85', yscrollcommand=False)
    top_lent_tools_text.grid(column=0, row=1, padx=(120, 15), pady=(5, 13))

    top_borrowed_tools_label = Label(right_pane, text="Top Borrowed Tools:", font=label_font, bg='#EFE2BA')
    top_borrowed_tools_label.grid(column=1, row=0, padx=(0, 95))
    top_borrowed_tools_text = Text(right_pane, height=33, width=40, bg='gray85', yscrollcommand=False)
    top_borrowed_tools_text.grid(column=1, row=1, padx=(15, 110), pady=(5, 13))

    load_top_lent(top_lent_tools_text)
    load_top_borrowed(top_borrowed_tools_text)

    right_pane.grid(column=1, row=0, pady=(0, 5))
    return pane


def load_top_lent(top_requested_tools_text):
    tool_list = rec.top_lent_tools(gbl_var.username)
    string_to_print = "\n\n"
    # print(tool_list)
    for i in range(0, len(tool_list) - 1):
        string_to_print += "    " + str(i+1) + ". Name:  " + tool_list[i]['name'] \
                                 + "\n       Average: " + str(tool_list[i]['Average_lent_time']) + "\n\n"

    if len(tool_list) == 10:
        string_to_print += "   10. Name:  " + tool_list[9]['name'] \
                       + "\n       Average: " + str(tool_list[9]['Average_lent_time']) + "\n\n"
    top_requested_tools_text.configure(state='normal')
    top_requested_tools_text.delete(1.0, "end")
    top_requested_tools_text.insert(1.0, string_to_print)
    top_requested_tools_text.configure(state='disabled')


def load_top_borrowed(top_requested_tools_text):
    tool_list = rec.top_lent_tools(gbl_var.username)
    string_to_print = "\n\n"
    # print(tool_list)
    for i in range(0, len(tool_list) - 1):
        string_to_print += "    " + str(i + 1) + ". Name:  " + tool_list[i]['name'] \
                           + "\n       Average: " + str(tool_list[i]['Average_lent_time']) + "\n\n"

    if len(tool_list) == 10:
        string_to_print += "   10. Name:  " + tool_list[9]['name'] \
                       + "\n       Average: " + str(tool_list[9]['Average_lent_time']) + "\n\n"
    top_requested_tools_text.configure(state='normal')
    top_requested_tools_text.delete(1.0, "end")
    top_requested_tools_text.insert(1.0, string_to_print)
    top_requested_tools_text.configure(state='disabled')


def load_latest_requests(latest_user_requests_text):
    requests = rec.latest_requests()
    string_to_print = ""
    for i in range(0, len(requests)):
        string_to_print += "    " + str(i + 1) + ". Request ID:  " + requests[i]['request_id'] \
                           + "\n       Barcode: " + str(requests[i]['barcode']) \
                           + "\n       Username: " + requests[i]['username'] + "\n\n"

    latest_user_requests_text.configure(state='normal')
    latest_user_requests_text.delete(1.0, "end")
    latest_user_requests_text.insert(1.0, string_to_print)
    latest_user_requests_text.configure(state='disabled')

"""

Name:  XXXXXXXX 
Count: XX
       

"""


def create_pie_chart(root):
    # create function

    dict = {}
    data = []
    data_list = rec.pie_chart(gbl_var.username)
    for data_dict in data_list:
        data.append(data_dict['total'])

    data_point_name = ["All", "Lent", "Borrowed"]

    pie_chart_pane = PanedWindow(root, width=600, height=400, bg='#EFE2BA')

    Sum = float(sum(data))

    def prop(n):
        return 360.0 * n / Sum

    Label(pie_chart_pane, text="Tool Distribution", bg='#EFE2BA').grid(column=0, row=0)
    c = Canvas(pie_chart_pane, bg='#EFE2BA', bd=0, highlightthickness=0, width=300, height=300)
    c.grid(column=0, row=1)

    previous_data_extent = 0
    j = 0
    index_list = []
    if Sum != 0:
        for k in range(len(data)):
            if data[k] != 0:
                print(data[k])
                color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
                c.create_arc((2, 2, 296, 296), fill=color, outline=color, start=prop(previous_data_extent)
                             , extent=prop(data[k])-.01)
                previous_data_extent += data[k]
                dict[data_point_name[j]] = color
                index_list.append(j)
                j += 1
    else:
        data_point_name = ["No Data"]
        Sum = 1.0
        color = "#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        c.create_arc((2, 2, 296, 296), fill=color, outline=color, start=0
                     , extent=90)
        c.create_arc((2, 2, 296, 296), fill=color, outline=color, start=90
                     , extent=180)
        c.create_arc((2, 2, 296, 296), fill=color, outline=color, start=180
                     , extent=270)
        c.create_arc((2, 2, 296, 296), fill=color, outline=color, start=270
                     , extent=360)
        dict[data_point_name[0]] = color
    right_pane = PanedWindow(pie_chart_pane, width=300, height=400, bg='#EFE2BA')

    row_num = 0
    for index in index_list:
        canvas = Canvas(right_pane, width=25, height=25, bd=0, highlightthickness=0, bg='#EFE2BA')
        canvas.create_rectangle(1, 1, 100, 100,
                                outline=dict[data_point_name[index]], fill=dict[data_point_name[index]])
        canvas.grid(column=0, row=row_num)

        label = Label(right_pane, height=3, text=data_point_name[index], bg='#EFE2BA')
        label.grid(column=1, row=row_num)
        row_num += 1
    right_pane.grid(column=1, row=1)
    return pie_chart_pane
