from ..db.ownership import fetch_ownership


def get_user_tools(username):
    return fetch_ownership(user=username)


def get_borrowed_tools(username):
    pass
