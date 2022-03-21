# def init_tables(curs):
#     curs.execute('CREATE TABLE USER ('
#                  'NAME VARCHAR(255)'
#                  'USERNAME VARCHAR(64)'
#                  'PASSWORD VARCHAR(64)'
#                  'CREATION_DATE DATE'
#                  'LAST_ACCESS_DATE DATE'
#                  'PRIMARY KEY (USERNAME))')
#
#     curs.execute('CREATE TABLE EMAIL ('
#                  'USERNAME VARCHAR(64)'
#                  'EMAIL VARCHAR(255)'
#                  'PRIMARY KEY (USERNAME, EMAIL))')
#
#     curs.execute('CREATE TABLE OWNERSHIP ('
#                  'USERNAME VARCHAR(64)'
#                  'BARCODE VARCHAR(48)'
#                  'PURCHASE_PRICE '
#                  'PURCHASE_DATE DATE'
#                  'PRIMARY KEY (USERNAME, BARCODE))')
#
#     curs.execute('CREATE TABLE TOOL ('
#                  'BARCODE VARCHAR(48)'
#                  'SHAREABLE BOOLEAN'
#                  'NAME VARCHAR(100)'
#                  'DESCRIPTION VARCHAR(160)'
#                  'PRIMARY KEY (BARCODE))')
#
#     # I think he wants us to get rid of category as a whole so I just put category in TOOL table :)
#     curs.execute('CREATE TABLE CATEGORY ('
#                  'TAG_NAME VARCHAR(20)'
#                  'BARCODE VARCHAR(48)'
#                  'PRIMARY KEY (TAG_NAME, BARCODE))')


def create_account(username, password, first_name, last_name, email):
    """
    This function will take in a users information and store it into the account. Affectively adding the user
    into the database. After they create an account they will be able to log in and view their previously added
    tools, borrow requests, and other users tools.

    :param username:   The username the user will use to log in with.
    :param password:   The password the user will use to log in with.
    :param first_name: The first name of the user.
    :param last_name:  The last name of the user.
    :param email:      The email of the user.
    :return:           Boolean value denoting if the action was completed successfully.
    """
    return True


def log_in(username, password):
    """
    This function will allow users to log in and see there data.

    :param username: The username of the user.
    :param password: The password of the user.
    :return:         Boolean value denoting if the action was completed successfully.
    """


def add_ownership(username, barcode, purchase_price):
    """
    This function is used to add ownership to a tool.

    :param username:       The user that will own the tool.
    :param barcode:        The barcode of the tool that is owned by the user.
    :param purchase_price: The price of the tool.
    :return:               Boolean value denoting if the action was completed successfully.
    """


def add_tool(username, name, description):
    """
    This function allows the user to add a tool into the database. It will use add_ownership() to also add
    ownership of the tool to the user.

    :param username:    The user that is adding the tool.
    :param name:        The name of the tool to be added.
    :param description: The description of the tool to be added.
    :return:            Boolean value denoting if the action was completed successfully.
    """


def remove_ownership(barcode):
    """
    This function is used to remove the ownership of a tool when it is removed completely from the database.

    :param barcode: The barcode of the tool to remove ownership.
    :return:        Boolean value denoting if the action was completed successfully.
    """


def remove_tool_history(barcode):
    """
    This function is used to delete the history of the previous requests the two has been in. As we are deleting the
    tool from the database we also want to delete all traces of the tool. This function performs that action.

    :param barcode: The tool that is to be fully deleted from the database.
    :return:        Boolean value denoting if the action was completed successfully.
    """


def delete_tool(barcode):
    """
    This function is used to delete a tool in the database. It will use remove_ownership() and remove_tool_history()
    to remove the ownership and tool history completely from the database.

    :param barcode:
    :return:
    """


def edit_tool(what_to_edit, edit_string):
    """
    This function is here to allow users to edit a tools name or description.

    :param what_to_edit: What the user would like to edit.
    :param edit_string:  What to update the name or description to.
    :return:             Boolean value denoting if the action was completed successfully.
    """
    # match what_to_edit:
    #     case name:
    #         num = 1
    #     case description:
    #         num = 0


def view_user_tools(username):
    """
    This will allow the user to view all of the tools they own. NOT TOOLS BORROWING

    :param username: The username of the user.
    :return:         The list of tools that the user owns.
    """


def create_category(barcode, category_name):
    """
    This function allows users to make a category. It will run through the database and check if the category
    already exists. If the category exists it will return a 1. If the category does not exist it will return a 0 and
    add the category. If there was an error the function will return a -1.

    :param barcode:       The barcode of the tool to add the category to.
    :param category_name: The name of the category to add.
    :return:              An integer value denoting the status:
                            -1: There was an error adding the category.
                             0: The category was added successfully.
                             1: The category already exists.
    """


def search_for_tool(identifier, identifier_type):
    """
    This function is responsible for searching for a tool. If the tool is found then it will return it. Otherwise,
    it will return None.

    :param identifier:      What to search for
    :param identifier_type: The field we will search (barcode, name, category)
    :return:                The list of tools found by the search.
    """


def sort_tools(sort_ascending, sort_name):
    """

    :param sort_ascending: Whether the user wants to sort ascending or descending
    :param sort_name:      Whether the user wants to sort by name or category
    :return:
    """
    if sort_ascending:
        num = 0
    elif not sort_ascending:
        num = 1


def get_users_borrowed_tools(username):
    """
    This function will return the users borrowed tools so they can see what they are currently borrowing from other
    users.

    :param username: The username of the user.
    :return:         The dictionary of tools {barcode, return_date} that the user is currently borrowing.
    """


def request_borrow(username, barcode, borrow_period):
    """
    This function will create a new request in the database. Adding to the REQUEST table. The request_id will
    be autogenerated based on the previous request in the database.

    :param username:      The user that would like to borrow the tool.
    :param barcode:       The barcode of the tool the user would like to borrow.
    :param borrow_period: The period of time the user would like to borrow.
    :return:              Boolean value denoting if the action was completed successfully.
    """


def get_users_requests_received(username):
    """
    This function is used to find the borrow requests the user has received.

    :param username: The name of the user that would like their received requests history.
    :return:         The received request history of the user.
    """


def get_users_requests_made(username):
    """
    This function is used to find the borrow requests the user has made.

    :param username: The name of the user that would like their made requests history.
    :return:         The made requests history of the user.
    """


def get_users_requests(username):
    """
    This function is used to find the borrow requests the user has made and received.

    :param username: The name of the user that would like their request history.
    :return:         The total request history of the user.
    """
    get_users_requests_received(username)
    get_users_requests_made(username)


def handle_request(is_accepted, request_id):
    """
    This function is here to either accept or reject a borrow request.

    :param is_accepted: The boolean value of if the user accepted the request.
    :param request_id:  The id of the request the user would like to reject or accept.
    :return:            Boolean value denoting if the action was completed successfully.
    """
    if is_accepted:
        # accept only put num = 0 so there were no errors
        num = 0
    else:
        # do not accept
        num = 1


def get_lent_tools():
    """
    This function is used to pull of the lent tools from the database. It will return an ordered (by date lent
    ascending) list that will display the tool and who is using the tool. The function returns a dictionary of
    {barcode, borrower} that will be printed out.

    :return: A dictionary of the {barcode, borrower} of the tools that are currently lent out.
    """


def get_borrowed_tools():
    """
    This function is used to pull of the borrowed tools from the database. It will return an ordered (by lend date
    ascending) list that will display the tool and who owns the tool. The function returns a dictionary of
    {barcode, owner} that will be printed out.

    :return: A dictionary of the {barcode, owner} of the tools that are currently being borrowed out.
    """


def get_overdue_tools():
    """
    This function will find all the tools that are currently being borrowed and are overdue to be returned. It will
    should then print them out with emphasis wherever it is called. This list returns the dictionary of
    {barcode, "borrower - overdue return date"}

    :return: The dictionary of {barcode, "borrower - overdue return date"} of the tools that overdue to be returned.
    """


def get_available_tools():
    """
    This function is used to pull of the available tools from the database. It will return an alphabetized list that
    will display the list of tools to that are available.

    :return: An ordered list of the available tools.
    """


def return_tool(request_id, username):
    """
    This function will allow a user to return a tool. It will take in a request id that the user provides and the
    username will be given by who is currently logged in for authentication. That way users cannot return other
    users tools. This function will parse the user's borrowed tools and if it finds the tool it will return it.
    Otherwise, it will return false as the user doesn't have a request with that id number.

    :param request_id: The request to be returned.
    :param username:   The user who is returning the tool.
    :return:           Boolean value denoting if the action was completed successfully.
    """


def tool_to_string(barcode, name, shareable, category, description):
    """
    This function is the to string for a tool. This will make the lists easier as we will be sending back a list of
    to strings for each tool found.

    :param barcode:     The barcode of the tool.
    :param name:        The name of the tool.
    :param shareable:   The boolean value of if the tool can be shared
    :param category:    The category/ies the tool falls under.
    :param description: The description of the tool.
    :return:            The to string of the tool.
    """

    return "Barcode: " + barcode + ", Name: " + name + ", Shareable: " + shareable + "\n" \
           + "Category: " + category + "\n" + "Description: " + description + "\n"


def request_to_string(request_id, username, barcode, status, borrow_period, request_date):
    """
    This function is the to string for a request. This will make the lists easier as we will be sending back a list of
    to strings for each request found.

    :param request_id:    The id of the request.
    :param username:      The username of the user requesting the tool.
    :param barcode:       The tool that is being requested.
    :param status:        The status of the request (accepted, declined).
    :param borrow_period: The date it is to be returned.
    :param request_date:  The date it was requested.
    :return:              The to string of the request.
    """

    return "Request id: " + request_id + "\n\tUsername: " + username + "\n\tBarcode: " + barcode + \
           "\n\tStatus: " + status + "\n\tBorrowed - Return: " + borrow_period + " - " + request_date + "\n"
