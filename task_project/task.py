from colorama import Fore, Back, Style 

from misc import get_input, validator
from category import priority_arr, color_arr
from view import color_dict, reset_color, view_task

status_arr = ("Not started", "In progress", "Done")

# Add task
def add_task (cur):
    title = details = status = duedate = category = False
    new_taskid = 0

    # Task id
    cur.execute("SELECT COUNT(*) count FROM task")
    
    for count in cur:
        task_total = count[0]+1

    for i in range(1, task_total+1):
        if validator("task", i, cur) == 1:
            continue
        else:
            new_taskid = i
            break

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
    duedate = get_input("Enter due date (DD-MM-YYYY): ", "date", None, None, "\nAdd a due date? (y/n) ", False)

    # Category
    cur.execute("SELECT COUNT(*) count FROM category")

    for count in cur:
        category_total = count[0]

    if category_total > 0:
        flag = 0
        while flag == 0:
            category = get_input("Enter Category ID: ", "int", 1, 99, "\nAdd to existing category? (y/n) ", False)
            flag = validator("category", category, cur)

            if flag == 0:
                print("Invalid input!\n")

    else:
        category = None

    cur.execute("INSERT INTO task VALUES (?, ?, ?, ?, ?, ?);", (new_taskid, title, details, status_arr[status-1], duedate, category))
    cur.execute('''
            SELECT t.taskid, t.title, t.details, t.status, COALESCE(t.duedate,"N/A") duedate, COALESCE(t.categoryid,"N/A") categoryid, CASE
            WHEN t.categoryid IS NULL THEN "N/A"
            ELSE (select cname from category where categoryid = t.categoryid) END cname
            FROM task t WHERE taskid = ?;
        ''', (new_taskid,))

    view_task(cur, new_taskid)

    print("\nTask added successfully!")

# Edit task
def edit_task (cur):
    edit_bool = True

    # Task id
    cur.execute("SELECT COUNT(*) count FROM task")

    for count in cur:
        task_total = count[0]

    if task_total > 0:
        flag = 0
        while flag == 0:
            task_id = get_input("\nEnter Task ID: ", "int", 1, 99, None, None)
            flag = validator("task", task_id, cur)
            
            if flag == 0:
                print("Invalid input!\n")
            elif flag == 1:
                cur.execute('''
                    SELECT t.taskid, t.title, t.details, t.status, COALESCE(t.duedate,"N/A") duedate, COALESCE(t.categoryid,"N/A") categoryid, CASE
                    WHEN t.categoryid IS NULL THEN "N/A"
                    ELSE (select cname from category where categoryid = t.categoryid) END cname
                    FROM task t WHERE taskid = ?;
                ''', (task_id,))
                
                view_task(cur, task_id)
    else:
        print("There are currently no tasks.")
        return None

    while True:
        print("\n" + "Edit task".center(24, "-"))
        print("[1] Title")
        print("[2] Details")
        print("[3] Status")
        print("[4] Due date")
        print("[5] Category ")
        print("[0] Back to Edit Menu")
        print("-----------------------")
        choice = get_input("\nEnter choice: ", "int", 0, 5, None, None)

        # Title
        if choice == 1:
            attribute = "title"
            value = get_input("\nEnter new title (Max length: 50): ", "string", 0, 50, None, None)

        # Details
        elif choice == 2:
            attribute = "details"
            value = get_input("\nEnter new details (Max length: 500): ", "string", 0, 500, None, None)

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
            value = get_input("Enter new due date (DD-MM-YYYY): ", "date", None, None, "\nRemove due date? (y/n) ", True)

        # Category
        elif choice == 5:
            attribute = "categoryid"

            cur.execute("SELECT COUNT(*) count FROM category")

            for count in cur:
                category_total = count[0]

            if category_total > 0:
                flag = 0
                while flag == 0:
                    value = get_input("Enter new Category ID: ", "int", 1, 99, "\nJust remove category? (y/n) ", True)
                    flag = validator("category", value, cur)

                    if flag == 0:
                        print("Invalid input!")
                    elif flag == 1:
                        cur.execute("SELECT * FROM category WHERE categoryid = ?", (value,))

                        for categoryid, cname, priority, color in cur:
                            print(f"\nCategory: ({categoryid}) {color_dict[color]} {cname} {reset_color} | Priority: {priority}")
            else:
                print("There are currently no categories.")

        elif choice == 0:
            break

        else:
            print("Invalid choice!\n")

        cur.execute(f"UPDATE task SET {attribute} = ? WHERE taskid = ?;", (value, task_id))
        cur.execute('''
            SELECT t.taskid, t.title, t.details, t.status, COALESCE(t.duedate,"N/A") duedate, COALESCE(t.categoryid,"N/A") categoryid, CASE
            WHEN t.categoryid IS NULL THEN "N/A"
            ELSE (select cname from category where categoryid = t.categoryid) END cname
            FROM task t WHERE taskid = ?;
        ''', (task_id,))
        
        view_task(cur, task_id)
            
# Delete task
def delete_task (cur):
    # Task ID
    cur.execute("SELECT COUNT(*) count FROM task")

    for count in cur:
        task_total = count[0]

    # print(task_total)

    if task_total > 0:
        task_id = get_input("Enter Task ID: ", "int", 1, 99, None, None)
        cur.execute("DELETE FROM task WHERE taskid = ?", (task_id,))
        print("\nTask deleted.\n")
    else:
        print("There are currently no tasks.")
        return None
