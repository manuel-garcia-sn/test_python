from database.database import db_session, init_db
from database.models import Item


def init():
    init_db()


def add_to_list(item):
    i = Item(item)
    db_session.add(i)
    db_session.commit()

    return i


def search_in_list(name):
    return Item.query.filter(Item.name == name).first()


def delete_item_list(name):
    item = Item.query.filter(Item.name == name).first()

    db_session.delete(item)
    db_session.commit()

    return item


def get_all_items():
    items = Item.query.all()

    return {"count": len(items), "items": items}
