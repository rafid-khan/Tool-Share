import re

import ptui_helper as helper
import src.queries as sql
from db.utils import connect, create_server
#import api.tool as tools
import api.ownership as ownership
import api.user as user
import api.auth as auth


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


def log_in_menu(username):
    while 1:
        print("Please specify what you would like to do next:\n"
              "\t 1: Add a new tool.\n"
              "\t 2: Delete a current tool.\n"
              "\t 3: Edit a current tool.\n"
              "\t 4: See your current tools.\n"
              "\t 5: Add tool to a category.\n"
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
                description, barcode, name = helper.add_tool()
                #if tools.create_tool( barcode, barcode, None, name, description ):
                    ###"\tDescription: " + description + "\n")
                #else:
                    #print("Failed to add tool. Please try again.")
            case "2":
                barcode = helper.delete_tool()
                if sql.delete_tool(barcode):
                    print("Successfully deleted a tool\n"
                          "\tBarcode: " + barcode + "\n")
                else:
                    print("Failed to delete tool. Please try again.")
            case "3":
                barcode, edit_string, what_to_edit = helper.edit_tool()
                if sql.edit_tool(edit_string, what_to_edit):
                    print("Successfully edited a tool\n"
                    + "\tBarcode: " + barcode + "\n"
                    + "\tName or Description: " + what_to_edit + "\n"
                    + "\tChange: " + edit_string + "\n")
                else:
                    print("Failed to edit tool. Please try again.")
            case "4":
                tool_list = sql.view_user_tools(username)
                for tool in tool_list:
                    print("Barcode: " + tool)
                print("\n")
            case "5":
                barcode, category_name = helper.create_category()
                status = sql.create_category(barcode, category_name)
                if status == -1:
                    print("There was an error with adding the category. Please try again\n")
                elif status == 0:
                    print("Successfully added a category to a tool.\n"
                          "New category: " + category_name + " was added successfully!\n"
                                                             "Barcode: " + barcode + "\n")
                elif status == 1:
                    print("Successfully added a category to a tool.\n"
                          "Category: " + category_name + " already exists.\n"
                                                         "Barcode: " + barcode + "\n")

            case "6":
                identifier, identifier_type = helper.search_for_tool()
                tool_list = sql.search_for_tool(identifier, identifier_type)
                if tool_list is None:
                    print("Error could not find tool(s)! Please try again.")
                else:
                    for tool in tool_list:
                        print(tool)
            case "7":
                sort_ascending, sort_name = helper.sort_tools()
                tool_list = sql.sort_tools(sort_ascending, sort_name)
                if tool_list is None:
                    print("Error could not find tools! Please try again.")
                else:
                    for tool in tool_list:
                        print(tool)
            case "8":
                tool_list = sql.get_users_borrowed_tools(username)
                if tool_list is None:
                    print("Error could not find tools! Please try again.")
                else:
                    for tool in tool_list:
                        print(tool)
            case "9":
                barcode, borrow_period = helper.request_borrow()
                tool_list = sql.request_borrow(barcode, borrow_period, username)
                if tool_list is None:
                    print("Error could not find tools! Please try again.")
                else:
                    for tool in tool_list:
                        print(tool)
            case "10":
                is_accepted, request_id = helper.handle_request()
                if sql.handle_request(is_accepted, request_id):
                    print("Successfully " + is_accepted + "ed the request: " + request_id + "\n")
                else:
                    print("There was an error with your request! Please try again.")
            case "11":
                request_list = sql.get_users_requests(username)
                if request_list is None:
                    print("The user: " + username + " has no request history.")
                else:
                    print("User's requests: ")
                    for request in request_list:
                        print("\t" + request)
            case "12":
                request_list = sql.get_users_requests_received(username)
                if request_list is None:
                    print("The user: " + username + " has no request history.")
                else:
                    print("User's requests: ")
                    for request in request_list:
                        print("\t" + request)
            case "13":
                tool_dict = sql.get_lent_tools()
                if tool_dict is None:
                    print("There are no lent tools")
                else:
                    for tool in tool_dict:
                        print(tool)
            case "14":
                tool_dict = sql.get_borrowed_tools()
                if tool_dict is None:
                    print("There are no borrowed tools")
                else:
                    for tool in tool_dict:
                        print(tool)
            case "15":
                tool_dict = sql.get_overdue_tools()
                if tool_dict is None:
                    print("There are no overdue tools")
                else:
                    for tool in tool_dict:
                        print(tool)
            case "16":
                request_id = helper.return_tool()
                isReturned = sql.return_tool(request_id, username)
                if isReturned:
                    print("You have successfully returned the request: " + request_id)
                else:
                    print("There was an error with returning the request: " + request_id)
            case "17":
                return "4"


def main():
    # starting server
    server = create_server()

    # initializing a connection and retrieving a cursor
    conn = connect()
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
                valid_login, username = log_in()
                if valid_login:
                    print("Log in successful\n"
                          "What would you like to do next")
                    choice1 = log_in_menu(username)
                else:
                    print("Incorrect username or password. Please try a valid log in.\n")
                    log_in_again = input("Would you like to try logging in again (yes/no): ")
                    if log_in_again.lower() == "no":
                        choice1 = "4"
            elif choice1 == "2":
                valid_creation, username = create_account()
                if valid_creation:
                    choice1 = log_in_menu(username)
                else:
                    print("There was an error with your account creation.\n")
                    create_account_again = input("Would you like to try creating an account again (yes/no): ")
                    if create_account_again.lower() == "no":
                        choice1 = "4"
            elif choice1 == "3":
                run_program = "0"
                choice1 = "4"

    server.close()


if __name__ == '__main__':
    main()
