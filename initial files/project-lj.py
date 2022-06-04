import mariadb
import sys
import os
from datetime import datetime, date

conn = mariadb.connect(
        user="root",
        password="0000",
        host="127.0.0.1",
        database="taskproject"
)

cur = conn.cursor()

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

def edit_category():
    edit_bool = True
    flag = 0 #will check if the category isn't deleted
    cur.execute("SELECT COUNT(*) count FROM category")

    for count in cur:
        category_total = count[0]

    # print(category_total)

    if category_total > 0:
        category_id = get_input("Enter Category ID: ", "int", 0, category_total, None, None)
        cur.execute("SELECT * FROM category WHERE categoryid = ?", (category_id,))

        for categoryid, cname, priority, color in cur:
            if category_id == categoryid:
                print(f"\nCategory Id: {categoryid}, Category Name: {cname} Priority: {priority}, Color: {color}\n")
                flag = 1 #the category exist

    else:
        print("There are currently no categories.")
        return None

    if flag==0: 
        print("\nThe category doesn't exist.\n")
        edit_bool = False

    while edit_bool:
        print('''\nEdit:
        [1] Category Name
        [2] Level of Priority
        [3] Color
        [0] Return to Main Menu
        ''')
        choice = get_input("Enter choice: ", "int", 0, 3, None, None)

        # Category name
        if choice == 1:
            attribute = "cname"
            value = get_input("Enter new category name (Max length: 50): ", "string", 0, 50, None, None)

        # Level of Priority
        elif choice == 2:
            attribute = "priority"
            print('''\nStatus:
            Urgent | High | Normal | Low
            ''')
            value = get_input("Enter new level of priority: ", "string", 1, 6, None, None)

        # Color
        elif choice == 3:
            attribute = "color"
            value = get_input("Enter color: ", "string", 0, 10, None, None)

        elif choice == 0:
            break

        else:
            print("Invalid choice!")

        cur.execute("UPDATE category SET " + attribute + " = ? WHERE categoryid = ?;", (value, category_id))

        cur.execute("SELECT categoryid, cname, priority, color FROM category")

        for categoryid, cname, priority, color in cur:
            if category_id == categoryid:
                print(f"\nUpdated Version: \nCategory Id: {categoryid}, Category Name: {cname} Level of Priority: {priority}, Color: {color}")

def delete_task():
    # Task ID
    cur.execute("SELECT COUNT(*) count FROM task")

    for count in cur:
        task_total = count[0]

    # print(task_total)

    if task_total > 0:
        task_id = get_input("Enter Task ID: ", "int", 0, task_total, None, None)
        cur.execute("DELETE FROM task WHERE taskid = ?", (task_id,))
        print("\nTask deleted.\n")
    else:
        print("There are currently no tasks.")
        return None

def delete_category():
    # Task ID
    cur.execute("SELECT COUNT(*) count FROM category")

    for count in cur:
        category_total = count[0]

    # print(category_total)

    if category_total > 0:
        category_id = get_input("Enter Category ID: ", "int", 0, category_total, None, None)
        #we should set to null the category of the tasks in this category
        cur.execute("UPDATE task SET categoryid = NULL WHERE categoryid = ?;", (category_id,))
        cur.execute("DELETE FROM category WHERE categoryid = ?", (category_id,))
        print("\nCategory deleted.\n")

    else:
        print("There are currently no categories.")
        return None

def view_category():
    flag = 0
    # Task ID
    cur.execute("SELECT COUNT(*) count FROM category")

    for count in cur:
        category_total = count[0]

    # print(category_total)

    if category_total > 0:
        category_id = get_input("Enter Category ID: ", "int", 0, category_total, None, None)
        cur.execute("SELECT * FROM category WHERE categoryid = ?", (category_id,))

        for categoryid, cname, priority, color in cur:
            if category_id == categoryid:
                print(f"\nCategory Id: {categoryid}, Category Name: {cname} Priority: {priority}, Color: {color}\n")
                flag = 1
    else:
        print("There are currently no categories.")
        return None
    if flag==0: print("\nThe category doesn't exist.\n")

edit_category()
delete_task()
delete_category()
view_category()


