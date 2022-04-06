from tkinter import *


search_options = [
    "Request ID",
    "Barcode",
    "Category",
    "Name"
]


def get_full_catalog_pane(root, frame2):
    root.title("Tools - Full Catalog")

    pane = PanedWindow(frame2, width=1400, height=596, bg='#5D460E')

    # The search box initialization
    search_pane = PanedWindow(pane, width=1400, height=596, bg='#5D460E')

    search_label = Label(search_pane, height=3, text="Search by: ", bg='#5D460E')
    search_label.grid(column=0, row=0)

    search_clicked = StringVar()
    search_clicked.set(search_options[0])
    search_by_dropdown = OptionMenu(search_pane, search_clicked, *search_options)
    search_by_dropdown.grid(column=1, row=0, padx=5)

    search_box = Text(search_pane, width=50, height=1, bg='gray75', yscrollcommand=False)
    search_box.grid(column=2, row=0)

    search_button = Button(search_pane, height=1, width=10, text="Search",
                           command=lambda: search_database(search_by_dropdown))
    search_button.grid(column=4, row=0, padx=(5, 10))

    search_pane.pack(padx=(110, 110))

    # The text field initialization

    text_box = Text(pane, height=32, width=140, bg='gray75', yscrollcommand=True)
    text_box.pack(padx=140, pady=(12, 11))

    return pane


def search_database(search_by_dropdown):
    pass