from ..db.tool import fetch_tool, fetch_all_tools, fetch_available_tools, insert_tool, update_tool, delete_tool


def get_tool(barcode):
    return fetch_tool(code=barcode)


def get_all_tools(sort=None):
    return fetch_all_tools(sort)


def get_available_tools():
    return fetch_available_tools()


def create_tool(barcode, category, shareable, name, description):
    insert_tool(barcode=barcode, category=category, shareable=shareable, name=name, description=description)


def edit_tool(barcode, **kwargs):
    update_tool(code=barcode, **kwargs)


def remove_tool(barcode):
    delete_tool(code=barcode)


def return_tool(barcode):
    edit_tool(barcode=barcode, shareable=True)


def to_string(barcode):
    from pprint import pprint

    return pprint(get_tool(barcode=barcode))
