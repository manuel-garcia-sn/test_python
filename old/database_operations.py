import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'mydatabase')
NOT_STARTED = 'Not Started'
IN_PROGRESS = 'In Progress'
COMPLETED = 'Completed'


def add_to_list(item):
    with sqlite3.connect(DB_PATH) as conn:
        try:
            # Once a connection has been established, we use the cursor
            # object to execute queries
            c = conn.cursor()

            # Keep the initial status as Not Started
            c.execute('insert into items(name, status) values(?,?)', (item, NOT_STARTED))

            # We commit to save the change
            conn.commit()
            return {"item": item, "status": NOT_STARTED}
        except Exception as e:
            print('Error: ', e)
            return None


def search_in_list(item_name):
    with sqlite3.connect(DB_PATH) as conn:
        try:
            c = conn.cursor()

            c.execute("select * from items where item='%s'" % item_name)
            db_item = c.fetchone()

            if db_item is None:
                return None

            return {"item": db_item[0], "status": db_item[1]}
        except Exception as e:
            print('Error: ', e)
            return None


def delete_item_list(item_name):
    with sqlite3.connect(DB_PATH) as conn:
        try:
            c = conn.cursor()

            result = c.execute("delete from items where item='%s'" % item_name)

            conn.commit()

            return result
        except Exception as e:
            print('Error: ', e)
            return None


def get_all_items():
    with sqlite3.connect(DB_PATH) as conn:
        try:
            c = conn.cursor()
            c.execute('select * from items')
            rows = c.fetchall()
            return {"count": len(rows), "items": rows}
        except Exception as e:
            print('Error: ', e)
            return None


def truncate_items():
    with sqlite3.connect(DB_PATH) as conn:
        try:
            c = conn.cursor()
            c.execute('DELETE FROM items WHERE true')
        except Exception as e:
            print('Error: ', e)
            return None
