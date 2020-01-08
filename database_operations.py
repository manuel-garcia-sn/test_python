import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "mydatabase")
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
            c.execute('insert into items(item, status) values(?,?)', (item, NOT_STARTED))

            # We commit to save the change
            conn.commit()
            return {"item": item, "status": NOT_STARTED}
        except Exception as e:
            print('Error: ', e)
            return None
