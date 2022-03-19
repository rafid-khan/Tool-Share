import psycopg2
from sshtunnel import SSHTunnelForwarder
from src.utils import start_server, get_conn

server = start_server()
server.start()

conn = get_conn(server)
curs = conn.cursor()


def init_tables():
    curs.execute('CREATE TABLE USER ('
                 'NAME VARCHAR(255)'
                 'USERNAME VARCHAR(64)'
                 'PASSWORD VARCHAR(64)'
                 'CREATION_DATE DATE'
                 'LAST_ACCESS_DATE DATE'
                 'PRIMARY KEY (USERNAME))')

    curs.execute('CREATE TABLE EMAIL ('
                 'USERNAME VARCHAR(64)'
                 'EMAIL VARCHAR(255)'
                 'PRIMARY KEY (USERNAME, EMAIL))')

    curs.execute('CREATE TABLE OWNERSHIP ('
                 'USERNAME VARCHAR(64)'
                 'BARCODE VARCHAR(48)'
                 'PURCHASE_PRICE '
                 'PURCHASE_DATE DATE'
                 'PRIMARY KEY (USERNAME, BARCODE))')

    curs.execute('CREATE TABLE TOOL ('
                 'BARCODE VARCHAR(48)'
                 'SHAREABLE BOOLEAN'
                 'NAME VARCHAR(100)'
                 'DESCRIPTION VARCHAR(160)'
                 'PRIMARY KEY (BARCODE))')

    curs.execute('CREATE TABLE CATEGORY ('
                 'TAG_NAME VARCHAR(20)'
                 'BARCODE VARCHAR(48)'
                 'PRIMARY KEY (TAG_NAME, BARCODE))')

    # I think he wants us to get rid of category as a whole so I just put category in TOOL table :)
    # curs.execute('CREATE TABLE CATEGORY ('
    #              'TAG_NAME VARCHAR(20)'
    #              'BARCODE VARCHAR(48)'
    #              'PRIMARY KEY (TAG_NAME, BARCODE) )')


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
    match what_to_edit:
        case name:
            return
        case description:
            return


def create_category(category_name):
    """
    This function allows users to make a category. It will run through the database and check if the category
    already exists. If the category exists it will return a 1. If the category does not exist it will return a 0 and
    add the category. If there was an error the function will return a -1.

    :param category_name: The name of the category to add.
    :return:              An integer value denoting the status:
                            -1: There was an error adding the category.
                             0: The category was added successfully.
                             1: The category already exists.
    """

def search_for_tool(barcode):
    """
    This function is responsible for searching for a tool. If the tool is found then it will return it. Otherwise,
    it will return None.

    :param barcode: The barcode of the tool to find.
    :return:        The tool, if found. If not found it will return None.
    """

def sort_tools(sort_ascending, sort_name):
    if sort_ascending:
        num = 0
    elif not sort_ascending:
        num = 1

def request_borrow(username, barcode, borrow_period):
    """
    This function will create a new request in the database. Adding to the REQUEST table. The request_id will
    be autogenerated based on the previous request in the database.

    :param username:      The user that would like to borrow the tool.
    :param barcode:       The barcode of the tool the user would like to borrow.
    :param borrow_period: The period of time the user would like to borrow.
    :return:              Boolean value denoting if the action was completed successfully.
    """

def get_users_requests(username):
    """
    This function is used to find the borrow requests the user has made and received.

    :param username: The name of the user that would like their request history.
    :return:         The total request history of the user.
    """
    get_users_requests_received(username)
    get_users_requests_made(username)


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

def handle_request(is_accepted, request_id):
    """
    This function is here to either accept or reject a borrow request.

    :param is_accepted: The boolean value of if the user accepted the request.
    :param request_id:  The id of the request the user would like to reject or accept.
    :return:            Boolean value denoting if the action was completed successfully.
    """
    if is_accepted:
        #accept only put num = 0 so there were no errors
        num = 0
    else:
        #do not accept
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