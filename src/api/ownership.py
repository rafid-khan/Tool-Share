from db.ownership import insert_ownership, delete_ownership


def create_ownership(username, barcode, purchase_price, purchase_date):
    insert_ownership(username=username, barcode=barcode, purchase_price=purchase_price, purchase_date=purchase_date)


def remove_ownership(username, barcode):
    delete_ownership(user=username, code=barcode)
