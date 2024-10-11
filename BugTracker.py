
# TODO dodać sprawdzanie czy tabela 'bugs' istnieje
# TODO dodać sprawdzanie czy typ 'status' istnieje

import psycopg
import datetime
import sys


def connect_to_database():
    password = input("Enter your password: ")

    conn = psycopg.connect("dbname=bugtracker user=postgres password=" + password)
    # cur = conn.cursor()

    return conn

def create_table(cur, conn):
    cur.execute(
        """CREATE TYPE status AS ENUM('unsolved', 'in progress', 'solved');"""
    )
    cur.execute(
        """CREATE TABLE bugs(
            id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR NOT NULL,
            date TIMESTAMP,
            description VARCHAR,
            status STATUS NOT NULL
        );"""
    )
    
    conn.commit()


def add_entry(cur, conn):
    date = datetime.datetime.now()
    name = input("Enter bug name:\n")
    desc = input("Enter bug description:\n")
    cur.execute(
        """INSERT INTO bugs (name, date, description, status)
        VALUES (%s, %s, %s, %s)""",
        (name, date, desc, "unsolved")
    )

    conn.commit()


def display_list(cur):
    cur.execute(
        """SELECT id, name FROM bugs"""
    )

    for entry in cur:
        print(entry)


def display_entry(cur):
    entry_id = input("Select entry to display\n")
    
    cur.execute(
        """SELECT * FROM bugs WHERE id = %s;""",
        (entry_id,)
    )
    
    for entry in cur:
        print(entry)


def modify_entry(cur, conn):
    entry_id = int(input("Select entry to modify\n"))

    if input("[1] change name\n[2] change description\n") == "1":
        new_value = input("enter new name")
        
        cur.execute(
        """UPDATE bugs
        SET name = %s
        WHERE id = %s;
        """,
        (new_value, entry_id)
        )

    else:
        new_value = input("enter new description")

        cur.execute(
            """UPDATE bugs
            SET description = %s
            WHERE id = %s;
            """,
            (new_value, entry_id)
        )

    conn.commit()


def remove_entry(cur):
    entry_id = int(input("Select entry to remove\n"))

    cur.execute(
        """DELETE FROM bugs WHERE id = %s""",
        (entry_id,)
    )


def update_status(cur, conn):
    entry_id = int(input("Select entry to modify\n"))

    if input("[1] mark entry in progress\n[2] mark entry solved\n") == "1":
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

    conn.commit()


def menu(cursor, conn):
    while(True):
        option = input(
            """Select an option:
            [1] View list
            [2] View entry
            [3] Add entry
            [4] Modify entry
            [5] Remove entry
            [6] Change entry status
            [0] Exit\n"""
        )

        match (option):
            case "1":
                display_list(cursor)
            case "2":
                display_entry(cursor)
            case "3":
                add_entry(cursor, conn)
            case "4":
                modify_entry(cursor, conn)
            case "5":
                remove_entry(cursor)
            case "6":
                update_status(cursor, conn)
            case "7":
                pass
            case "8":
                pass
            case "9":
                pass
            case "0":
                sys.exit()

### PROGRAM CODE ###

conn = connect_to_database()
cursor = conn.cursor()

# create_table(cursor, conn)

menu(cursor, conn)