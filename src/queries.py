from psycopg2.sql import SQL, Identifier
from .db.utils import *


# def create_account(**kwargs):
#     """
#     This function will take in a users information and store it into the account. Affectively adding the user
#     into the database. After they create an account they will be able to log in and view their previously added
#     tools, borrow requests, and other users tools.
#
#     param kwargs:     Given arguments
#     :return:           Boolean value denoting if the action was completed successfully.
#     """
#     commit("""
#         INSERT INTO ts_user (first_name, last_name, username, password, email)
#         VALUES (%s, %s, %s, %s, %s)
#     """), (tuple(kwargs.values()))


# def log_in(username, password):
#     """
#     This function will allow users to log in and see their data.
#
#     :param username: The username of the user.
#     :param password: The password of the user.
#     :return:         Boolean value denoting if the action was completed successfully.
#     """
#     correct_password = fetch_one("""
#         SELECT password FROM user WHERE username = %s """, (username,))
#     return password == correct_password


# def add_ownership(**kwargs):
#     """
#     This function is used to add ownership to a tool.
#
#     :param kwargs:
#     """
#     commit("""
#         INSERT INTO ownership (username, barcode, purchase_price, purchase_date)
#         VALUES (%s, %s, %s, %s)
#     """, (tuple(kwargs.values())))


# def add_tool(**kwargs):
#     """
#     This function allows the user to add a tool into the database. It will use add_ownership() to also add
#     ownership of the tool to the user.
#
#     Function exists in tool.py
#
#     :param kwargs:
#     :return:            Boolean value denoting if the action was completed successfully.
#     """
#     commit("""
#         INSERT INTO tool (barcode, category, shareable, name, description)
#         VALUES (%s, %s, %s, %s, %s)
#     """, (tuple(kwargs.values())))


# def remove_ownership(barcode):
#     """
#     This function is used to remove the ownership of a tool when it is removed completely from the database.
#
#     :param barcode: The barcode of the tool to remove ownership.
#     :return:        Boolean value denoting if the action was completed successfully.
#     """
#     commit("""
#         DELETE FROM ownership WHERE barcode = %s
#     """, (barcode,))
#     return True


# def delete_tool(barcode):
#     """
#     This function is used to delete a tool in the database. It will use remove_ownership() and remove_tool_history()
#     to remove the ownership and tool history completely from the database.
#
#     :param barcode:
#     :return:
#     """
#     commit("""
#         DELETE FROM tool WHERE barcode = %s
#     """, (barcode,))


# def edit_tool_description(barcode, new_description):
#     """
#     This function edits the tools name, given the barcode
#     :param barcode: The barcode of the tool
#     :param new_description: The new name of the tool
#     :return: Boolean value denoting if the action was completed successfully
#     """
#     commit("""
#         UPDATE tool SET description = %s WHERE barcode = %s,
#     """, (new_description, barcode,))
#
#
# def edit_tool_name(barcode, new_name):
#     """
#     This function edits the tools name, given the barcode
#     :param barcode: The barcode of the tool
#     :param new_name: The new name of the tool
#     :return: Boolean value denoting if the action was completed successfully
#     """
#     commit("""
#         UPDATE tool SET name = %s WHERE barcode = %s,
#     """, (new_name, barcode,))


# def view_user_tools(username):
#     """
#     This will allow the user to view all the tools they own. NOT TOOLS BORROWING
#
#     :param username: The username of the user.
#     :return:         The list of tools that the user owns.
#     """
#     return fetch_many("""
#         SELECT name FROM tool WHERE holder = %s,
#     """, (username,))


# def create_category(**kwargs):
#     """
#     This function allows users to make a category. It will run through the database and check if the category
#     already exists. If the category exists it will return a 1. If the category does not exist it will return a 0 and
#     add the category. If there was an error the function will return a -1.
#
#     :param kwargs:
#     :return:              An integer value denoting the status:
#                             -1: There was an error adding the category.
#                              0: The category was added successfully.
#                              1: The category already exists.
#     """
#     commit("""
#         INSERT INTO category (tag_name, barcode, username)
#         VALUES (%s, %s, %s)
#     """, (tuple(kwargs.values())))


# def sort_tool_name(sort_ascending):
#     """
#     This function would be responsible for searching for a tool. If the tool is found then it will return it.
#     :param sort_ascending: Whether the user wants to sort ascending or descending
#     :return:
#     """
#     if sort_ascending:
#         return fetch_many("""
#         SELECT name FROM tool ORDER BY sort_by ASC
#         """)
#     elif not sort_ascending:
#         return fetch_many("""
#         SELECT name FROM tool ORDER BY sort_by DESC
#         """)
#
#
# def sort_tool_category(sort_ascending):
#     """
#     This function would be responsible for searching for a tool. If the tool is found then it will return it.
#     :param sort_ascending:
#     :return:
#     """
#     if sort_ascending:
#         return fetch_many("""
#         SELECT category FROM tool ORDER BY sort_by ASC
#         """)
#     elif not sort_ascending:
#         return fetch_many("""
#         SELECT category FROM tool ORDER BY sort_by DESC
#         """)


# def get_users_borrowed_tools(username):
#     """
#     This function will return the users borrowed tools, so they can see what they are currently borrowing from other
#     users.
#
#     :param username: The username of the user.
#     :return:         The dictionary of tools {barcode, return_date} that the user is currently borrowing.
#     """
#     return fetch_many("""
#         SELECT barcode FROM request WHERE username = %s AND status = TRUE
#     """, (username,))
#
#
# def request_borrow(**kwargs):
#     """
#     This function will create a new request in the database. Adding to the REQUEST table. The request_id will
#     be autogenerated based on the previous request in the database.
#
#     :param kwargs: The period of time the user would like to borrow.
#     :return:              Boolean value denoting if the action was completed successfully.
#     """
#     commit("""
#             INSERT INTO category (request_id, username, barcode, status, borrow_period, request_date)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """, (tuple(kwargs.values())))


# # TODO
# def get_users_requests_received(username):
#     """
#     This function is used to find the borrow requests the user has received.
#
#     :param username: The name of the user that would like their received requests history.
#     :return:         The received request history of the user.
#     """
#     return fetch_many("""
#         SELECT username = %s FROM OWNERSHIP WHERE barcode
#         IN (SELECT barcode FROM request)
#     """, (username,))


# def get_users_requests_made(kwargs):
#     """
#     This function is used to find the borrow requests the user has made.
#
#     :param kwargs:
#     :return:         The made requests history of the user.
#     """
#     return fetch_many("""
#         SELECT request_id, barcode, borrow_period, request_date, status
#         FROM request WHERE username = %s
#     """, (tuple(kwargs.values())))


# # TODO
# def handle_request(is_accepted, request_id):
#     """
#     This function is here to either accept or reject a borrow request.
#
#     :param is_accepted: The boolean value of if the user accepted the request.
#     :param request_id:  The id of the request the user would like to reject or accept.
#     :return:            Boolean value denoting if the action was completed successfully.
#     """
#     if is_accepted:
#         pass
#     else:
#         # do not accept
#         num = 1
#

# def get_lent_tools():
#     """
#     This function is used to pull of the lent tools from the database. It will return an ordered (by date lent
#     ascending) list that will display the tool and who is using the tool. The function returns a dictionary of
#     {barcode, borrower} that will be printed out.
#
#     :return: A dictionary of the {barcode, borrower} of the tools that are currently lent out.
#     """
#     return fetch_many("""
#         SELECT barcode FROM request WHERE request_date < (request_date + borrow_period)
#     """)


# # TODO
# def get_borrowed_tools():
#     """
#     This function is used to pull of the borrowed tools from the database. It will return an ordered (by lend date
#     ascending) list that will display the tool and who owns the tool. The function returns a dictionary of
#     {barcode, owner} that will be printed out.
#
#     :return: A dictionary of the {barcode, owner} of the tools that are currently being borrowed out.
#     """

#
# def get_overdue_tools():
#     """
#     This function will find all the tools that are currently being borrowed and are overdue to be returned. It will
#     should then print them out with emphasis wherever it is called. This list returns the dictionary of
#     {barcode, "borrower - overdue return date"}
#
#     :return: The dictionary of {barcode, "borrower - overdue return date"} of the tools that overdue to be returned.
#     """
#
#
# def get_available_tools():
#     """
#     This function is used to pull of the available tools from the database. It will return an alphabetized list that
#     will display the list of tools to that are available.
#
#     :return: An ordered list of the available tools.
#     """

# TODO
def search_for_tool(identifier, identifier_type):
    """
    This function is responsible for searching for a tool. If the tool is found then it will return it. Otherwise,
    it will return None.

    :param identifier:      What to search for
    :param identifier_type: The field we will search (barcode, name, category)
    :return:                The list of tools found by the search.
    """
    pass


# TODO
def remove_tool_history(barcode):
    """
    This function is used to delete the history of the previous requests the two has been in. As we are deleting the
    tool from the database we also want to delete all traces of the tool. This function performs that action.

    :param barcode: The tool that is to be fully deleted from the database.
    :return:        Boolean value denoting if the action was completed successfully.
    """


def get_users_requests(username):
    """
    This function is used to find the borrow requests the user has made and received.

    :param username: The name of the user that would like their request history.
    :return:         The total request history of the user.
    """
    get_users_requests_received(username)
    get_users_requests_made(username)


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
