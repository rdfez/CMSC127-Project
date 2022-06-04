# Module Imports
import mariadb
import sys
import os
from datetime import datetime, date

# Initialize database/connection
def init():
    # Connect to MariaDB Platform
    conn_bool = True
    while conn_bool:
        mariadb_password = input("Enter password: ")

        try:
            conn = mariadb.connect(
                user = "root",
                password = mariadb_password,
                host = "localhost",
                autocommit = True
            )

            if(conn):
                conn_bool = False

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

    # Get Cursor
    global cur 
    cur = conn.cursor()

    # Create database/tables on initial boot and use app database
    cur.execute("CREATE DATABASE IF NOT EXISTS `task_app`;")
    cur.execute("USE `task_app`;")
    cur.execute('''
        CREATE TABLE IF NOT EXISTS `category` (
            `categoryid` INT(2) NOT NULL,
            `cname` VARCHAR(50) NOT NULL,
            `priority` VARCHAR(6) NOT NULL,
            `color` VARCHAR(20),
            PRIMARY KEY (`categoryid`)
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS `task` (
            `taskid` INT(2) NOT NULL,
            `title` VARCHAR(50) NOT NULL,
            `details` VARCHAR(500) NOT NULL,
            `status` VARCHAR(11) NOT NULL DEFAULT "not started",
            `duedate` DATE,
            `categoryid` INT(2),
            PRIMARY KEY (`taskid`),
            CONSTRAINT `task_categoryid_fk` FOREIGN KEY (`categoryid`) REFERENCES `category` (`categoryid`)
        );
    ''')

# Add category
def add_category():
    category_name = priority = color = False

    # Category id
    cur.execute("SELECT COUNT(*) count FROM category")

    for count in cur:
        category_id = count[0]+1
    
    # Category name
    category_name = get_input("\nEnter Category name (Max length: 50): ", "string", 0, 50, None, None)

    # Priority
    print('''\nPriority:
    [1] Urgent
    [2] High
    [3] Medium
    [4] Low
    ''')
    priority = get_input("Enter priority: ", "int", 1, 4, None, None)

    # Color
    print('''\nColor:
    [1] None/Black\t[5] Blue
    [2] Red\t\t[6] Magenta
    [3] Green\t\t[7] Cyan
    [4] Yellow\t\t[8] White
    ''')
    color = get_input("Enter color: ", "int", 1, 8, None, None)
            
    cur.execute("INSERT INTO category VALUES (?, ?, ?, ?);", (category_id, category_name, priority_arr[priority-1], color_arr[color-1]))

# Add task
def add_task():
    title = details = status = duedate = category = False

    # Task id
    cur.execute("SELECT COUNT(*) count FROM task")

    for count in cur:
        task_id = count[0]+1

    # Title
    title = get_input("\nEnter Task title (Max length: 50): ", "string", 0, 50, None, None) 
    
    # Details
    details = get_input("\nEnter Task details (Max length: 500): ", "string", 0, 500, None, None)
    
    # Status
    print('''\nStatus:
    [1] Not started
    [2] In progress
    [3] Done
    ''')
    status = get_input("Enter your status choice: ", "int", 1, 3, None, None)

    # Due date
    duedate = get_input("Enter due date (DD-MM-YYYY): ", "date", None, None, "Add a due date? (y/n) ", False)

    # Category
    cur.execute("SELECT COUNT(*) count FROM category")

    for count in cur:
        category_total = count[0]

    if category_total > 0:
        category = get_input("Enter Category ID: ", "int", 1, category_total, "Add to existing category? (y/n) ", False)
    else:
        print("There are currently no categories.")
        category = None

    cur.execute("INSERT INTO task VALUES (?, ?, ?, ?, ?, ?);", (task_id, title, details, status_arr[status-1], duedate, category))

# Get user input and validate
# - Parameters:
#   1. msg (string): message prompt for input
#   2. type (string): input type (int, string, date)
#   3. min (int): minimum value
#   4. max (int): maximum value
#   5. optional_msg (string): message prompt for optional attributes ('y/n' prompts)
#   6. optional_rev (bool): False = return NULL if a 'no' input should disregard optional attribute, otherwise True if 'yes'
def get_input(msg, type, min, max, optional_msg, optional_rev):
    # For optional attributes
    if optional_msg:
        prompt = True
        while prompt:
            user_input = input(optional_msg)
            if user_input in ("y", "n"):
                prompt = False
            else:
                print("Invalid input!")

        if (optional_rev and user_input == "y") or (not optional_rev and user_input == "n"):
            return None
    
    while True:
        if type == "string":
            string_input = input(msg)
            if (len(string_input) <= max) :
                return string_input
            else:
                print("Invalid input!")
        
        elif type == "date":
            date = input(msg)
            try:
                valid_date = datetime.strptime(date, "%d-%m-%Y").date()
                return valid_date
            except ValueError:
                print("Invalid date!")

        elif type == "int":
            try:
                int_input = int(input(msg))
                if (int_input >= min and int_input <= max):
                    return int_input
                else:
                    print("Invalid input!")

            except (ValueError, TypeError):
                print("Invalid input!")

# Edit task
def edit_task():
    edit_bool = True

    # Task id
    cur.execute("SELECT COUNT(*) count FROM task")

    for count in cur:
        task_total = count[0]

    print(task_total)

    if task_total > 0:
        task_id = get_input("Enter Task ID: ", "int", 0, task_total, None, None)
    else:
        print("There are currently no tasks.")
        return None

    while True:
        print('''\nEdit:
        [1] Title
        [2] Details
        [3] Status
        [4] Due date
        [5] Category 
        [0] Return to Main Menu
        ''')
        choice = get_input("Enter choice: ", "int", 0, 5, None, None)

        # Title
        if choice == 1:
            attribute = "title"
            value = get_input("Enter new title (Max length: 50): ", "string", 0, 50, None, None)

        # Details
        elif choice == 2:
            attribute = "details"
            value = get_input("Enter new details (Max length: 500): ", "string", 0, 500, None, None)

        # Status
        elif choice == 3:
            attribute = "status"

            print('''\nStatus:
            [1] Not started
            [2] In progress
            [3] Done
            ''')
            value = get_input("Enter new status: ", "int", 1, 3, None, None)

        # Due date
        elif choice == 4:
            attribute = "duedate"
            value = get_input("Enter new due date (DD-MM-YYYY): ", "date", None, None, "Remove due date? (y/n) ", True)

        # Category
        elif choice == 5:
            attribute = "categoryid"

            cur.execute("SELECT COUNT(*) count FROM category")

            for count in cur:
                category_total = count[0]

            if category_total > 0:
                value = get_input("Enter new Category ID: ", "int", 1, category_total, "Remove from category? (y/n) ", True)
            else:
                print("There are currently no categories.")

        elif choice == 0:
            break

        else:
            print("Invalid choice!")

        cur.execute(f"UPDATE task SET {attribute} = ? WHERE taskid = ?;", (value, task_id))

priority_arr = ("Urgent", "High", "Medium", "Low")
color_arr = ("Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White")
status_arr = ("Not started", "In progress", "Done")

init()
#add_category()
#add_task()
#edit_task()
