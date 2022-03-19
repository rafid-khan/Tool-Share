import sys

import re
from src.utils import start_server, get_conn
import src.SQL_Queries as sql
import ptui_helper as helper


def log_in():
    username = input("Username: ")
    password = input("Password: ")

    if sql.log_in(username, password):
        return True, username
    else:
        return False, None


def create_account():
    username = input("\tPlease enter a valid username: ")
    password = input("\tPlease enter a valid password: ")
    first_name = input("\tPlease enter your first name: ")
    last_name = input("\tPlease enter your last name: ")
    email = input("\tPlease enter your email address: ")
    while not re.search(".+@.+[.].{3}$", email):
        email = input("\tPlease enter a valid email address (jsmith@example.com): ")

    if sql.create_account(username, password, first_name, last_name, email):
        print("***Account Successfully created***\n")
        sql.log_in(username, password)
        print("You are currently logged in!\n")
        return True, username
    else:
        return False, None


def log_in_menu(USERNAME):
    while 1:
        print("Please specify what you would like to do next:\n"
              "\t 1: Add a new tool.\n"
              "\t 2: Delete a current tool.\n"
              "\t 3: Edit a current tool.\n"
              "\t 4: See your current tools.\n"
              "\t 5: Create a category.\n"
              "\t 6: Search tools.\n"
              "\t 7: Sort Tools.\n"
              "\t 8: View your borrowed tools.\n"
              "\t 9: Request a borrow.\n"
              "\t10: Accept a current borrow request\n"
              "\t11: View Borrowed history.\n"
              "\t12: View received requests.\n"
              "\t13: View lent out tools.\n"
              "\t14: View borrowed tools.\n"
              "\t15: View overdue tools.\n"
              "\t16: Return tool.\n"
              "\t17: Log out.\n")
        choice2 = input("Please select an option (1..16): ")

        match choice2:
            case "1":
                description, name = helper.add_tool()
                sql.add_tool(description, name, USERNAME)
            case "2":
                barcode = helper.delete_tool()
                sql.delete_tool(barcode)
            case "3":
                barcode, edit_string, what_to_edit = helper.edit_tool()
                sql.edit_tool(edit_string, what_to_edit)
            case "4":
                sql.view_user_tools(USERNAME)
            case "5":
                category_name = helper.create_category()
                sql.create_category(category_name)
            case "6":
                barcode = helper.search_for_tool()
                sql.search_for_tool(barcode)
            case "7":
                sort_ascending, sort_name = helper.sort_tools()
                sql.sort_tools(sort_ascending, sort_name)
            case "8":
                sql.get_users_borrowed_tools(USERNAME)
            case "9":
                barcode, borrow_period = helper.request_borrow()
                sql.request_borrow(barcode, borrow_period, USERNAME)
            case "10":
                is_accepted, request_id = helper.handle_request()
                sql.handle_request(is_accepted, request_id)
            case "11":
                sql.get_users_requests(USERNAME)
            case "12":
                sql.get_users_requests_received(USERNAME)
            case "13":
                sql.get_lent_tools()
            case "14":
                sql.get_borrowed_tools()
            case "15":
                sql.get_overdue_tools()
            case "16":
                request_id = helper.return_tool()
                sql.return_tool(request_id, USERNAME)
            case "17":
                return "4"


def main():
    # starting server

    server = start_server()
    server.start()

    # initializing a connection and retrieving a cursor
    conn = get_conn(server)
    curs = conn.cursor()
    run_program = "1"
    while run_program == "1":
        print("Connection to Database Established.\n"
              "Please specify what you would like to do next:\n"
              "\t1: Log in\n"
              "\t2: Create Account\n"
              "\t3: Quit\n")
        choice1 = input("Please select an option (1/2):")
        while choice1 != "4":
            if choice1 == "1":
                # log_in_again = "yes"
                # while log_in_again.lower() == "yes":
                valid_login, USERNAME = log_in()
                if valid_login:
                    print("Log in successful\n"
                          "What would you like to do next")
                    choice1 = log_in_menu(USERNAME)
                else:
                    print("Incorrect username or password. Please try a valid log in.\n")
                    log_in_again = input("Would you like to try logging in again (yes/no): ")
                    if log_in_again.lower() == "no":
                        choice1 = "4"
            elif choice1 == "2":
                valid_creation, USERNAME = create_account()
                if valid_creation:
                    choice1 = log_in_menu(USERNAME)
                else:
                    print("There was an error with your account creation.\n")
                    create_account_again = input("Would you like to try creating an account again (yes/no): ")
                    if create_account_again.lower() == "no":
                        choice1 = "4"
            elif choice1 == "3":
                run_program = "0"
                choice1 = "4"


if __name__ == '__main__':
    main()
