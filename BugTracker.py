# TODO login 
# TODO połączenie z bazą danych
# TODO test

import psycopg3
import datetime
import sys

def login():
    pass

def create_database():
    pass

def connect_to_database():
    conn = psycopg3.connect()
    cur = conn.cursor()

    return cur

def create_table(cur):
    cur.execute(
        """CREATE TABLE bugs(
            id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR NOT NULL,
            date DATETIME,
            description VARCHAR,
            status ENUM(unsolved, in progress, solved) NOT NULL
        );"""
    )
    
    cur.commit()


def add_entry(cur):
    date = datetime.now()
    name = input("Enter bug name")
    desc = input("Enter bug description")
    cur.execute(
        """INSERT INTO bugs (name, date, description, status)
        VALUES (%s, %s, %s, %s)""",
        (name, date, desc, "in progress")
    )

    cur.commit()


def display_list(cur):
    cur.execute(
        """SELECT id, name FROM bugs"""
    )

    for entry in cur:
        print(entry)


def display_entry(cur):
    entry_id = input("Select entry to display")
    
    cur.execute(
        """SELECT * FROM bugs WHERE id = %s""",
        (entry_id)
    )

    print(cur)


def modify_entry(cur):
    entry_id = input("Select entry to modify")

    if input("[1]change name\n[2] change description") == "1":
        column = "name"
        new_value = input("enter new name")
    else:
        column = "description"
        new_value = input("enter new description")

    cur.execute(
        """UPDATE bugs
        SET %s = %s
        WHERE id = %s;
        """,
        (column, new_value, entry_id)
    )

    cur.commit()


def remove_entry(cur):
    entry_id = input("Select entry to remove")

    cur.execute(
        """DELETE FROM bugs WHERE id = %s""",
        (entry_id)
    )


def update_status(cur):
    entry_id = input("Select entry to modify")

    if input("[1] mark entry in progress\n[2] mark entry solved") == "1":
        new_status = "in progress"
    else:
        new_status = "solved"
        
    cur.execute(
        """UPDATE bugs 
        SET status = %s
        WHERE id = %s; 
        """,
        (new_status, entry_id)
    )

###



cursor = connect_to_database()

def menu():
    while(True):
        option = input(
            """Select an option:
            [1] View list
            [2] View entry
            [3] Add entry
            [4] Modify entry
            [5] Remove entry
            [6] Change entry status
            [0] Exit"""
        )

        match (option):
            case "1":
                display_list(cursor)
            case "2":
                display_entry(cursor)
            case "3":
                add_entry(cursor)
            case "4":
                modify_entry(cursor)
            case "5":
                remove_entry(cursor)
            case "6":
                update_status(cursor)
            case "7":
                pass
            case "8":
                pass
            case "9":
                pass
            case "0":
                sys.exit()