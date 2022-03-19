import re
import datetime


def read_barcode():
    barcode = input("\tPlease enter a barcode (< 48 char): ")
    while len(barcode) > 48:
        print("Please enter a barcode less than 48 characters")
        barcode = input("\tPlease enter a barcode (< 48 char): ")
    return barcode


def read_description():
    description = input("\tPlease enter a description (< 160 char): ")
    while len(description) > 160:
        print("Please enter a description less than 160 characters")
        description = input("\tPlease enter a description (< 160 char): ")
    return description


def read_name():
    name = input("\tPlease enter a name (< 100 char): ")
    while len(name) > 100:
        print("Please enter a name less than 100 characters")
        name = input("\tPlease enter a name (< 100 char): ")
    return name


def add_tool():
    name = read_name()
    description = read_description()

    return description, name


def delete_tool():
    return read_barcode()


def edit_tool():
    barcode = read_barcode()

    what_to_edit = input("\tPlease enter what you would like to edit (name/description): ")
    while what_to_edit.lower() != "name" and what_to_edit.lower() != "description":
        what_to_edit = input("\tPlease enter either name or description: ")

    if what_to_edit == "name":
        edit_string = read_name()
    elif what_to_edit == "description":
        edit_string = read_description()

    return barcode, edit_string, what_to_edit


def create_category():
    barcode = read_barcode()
    category_name = input("\tPlease enter a category name (< 20 char): ")
    while len(category_name) > 20:
        print("Please enter a category name less than 20 characters")
        category_name = input("\tPlease enter a category name (< 20 char): ")

    return barcode, category_name


def search_for_tool():
    return read_barcode()


def sort_tools():
    sort_ascending = input("\tSort ascending or descending: ")
    while sort_ascending.lower() != "ascending" and sort_ascending.lower() != "descending":
        sort_ascending = input("\tPlease enter either ascending or descending: ")

    sort_name = input("\tPlease enter what you would like to sort (name/category): ")
    while sort_name.lower() != "name" and sort_name.lower() != "category":
        sort_name = input("\tPlease enter either name or category:")

    return sort_ascending, sort_name


def request_borrow():
    barcode = read_barcode()

    valid_date = False
    while not valid_date:
        try:
            year = int(input("\tYear: "))
            month = int(input("\tMonth: "))
            day = int(input("\tDay: "))
            datetime.date(year, month, day)
            borrow_period = str(year) + "-" + str(month) + "-" + str(day)
            valid_date = True
        except ValueError as err:
            print(err)
    return barcode, borrow_period


def handle_request():
    is_accepted = input("\tDo you accept this request (accept/decline): ")
    while is_accepted.lower() != "accept" and is_accepted.lower() != "decline":
        is_accepted = input("\tPlease enter either yes or no: ")

    request_id = input("\tPlease enter a request id (< 48 char): ")
    while len(request_id) > 48:
        print("Please enter a request id less than 48 characters")
        request_id = input("\tPlease enter a request id (< 48 char): ")
    return is_accepted, request_id


def return_tool():
    request_id = input("\tPlease enter a request id (< 48 char): ")
    while len(request_id) > 48:
        print("Please enter a request id less than 48 characters")
        request_id = input("\tPlease enter a request id (< 48 char): ")
    return request_id
