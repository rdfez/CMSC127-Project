from colorama import Fore, Back, Style 

from misc import count, get_id, get_input, validator
from view import view_task

status_arr = ("Not started", "In progress", "Done")

# Add task
def add_task (cur, task_total):
    if task_total == None:
        task_total = 0
        
    task_total = task_total + 1

    # Task id
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
    category_total = count("category", cur, False)

    if category_total != None:
        category = get_id("Enter Category ID: ", "category", "\nAdd to existing category? (y/n) ", False, cur)
    else:
        category = None

    cur.execute("INSERT INTO task VALUES (?, ?, ?, ?, ?, ?);", (new_taskid, title, details, status_arr[status-1], duedate, category))
    
    print("\nNew Task: ")
    view_task(cur, new_taskid)

    print("\nTask added successfully!")

# Edit task
def edit_task (cur):
    task_id = get_id("\nEnter Task ID: ", "task", None, None, cur)

    print(f"\nTask Info:")
    view_task(cur, task_id)

    while True:
        print("\nEdit: ")
        print("\t[1] Title")
        print("\t[2] Details")
        print("\t[3] Status")
        print("\t[4] Due date")
        print("\t[5] Category ")
        print("\t[0] Back to Edit Menu")
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
            category_total = count("category", cur, True)

            if category_total != None:
                value = get_id("Enter new Category ID: ", "category", "\nJust remove category? (y/n) ", True, cur)
            else:
                continue

        elif choice == 0:
            break

        else:
            print("Invalid choice!\n")

        if attribute == "status":
            cur.execute(f"UPDATE task SET {attribute} = ? WHERE taskid = ?;", (status_arr[value-1], task_id))
        else:
            cur.execute(f"UPDATE task SET {attribute} = ? WHERE taskid = ?;", (value, task_id))

        print(f"\nUpdated Task Info:")
        view_task(cur, task_id)

        print(f"\nTask's {attribute} was successfully updated!")

    return
            
# Delete task
def delete_task (cur):
    task_id = get_id("\nEnter Task ID: ", "task", None, None, cur)
    cur.execute("DELETE FROM task WHERE taskid = ?", (task_id,))
    print("\nTask deleted.")

    return 

# Delete all task
def delete_all_task (cur):
    cur.execute("DELETE FROM task;")
    print("\nAll tasks deleted.")
    return
