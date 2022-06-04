from misc import get_input, validator

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

    cur.execute("INSERT INTO task VALUES (?, ?, ?, ?, ?, ?);", (new_taskid, title, details, status_arr[status-1], duedate, category))

# Edit task
def edit_task (cur):
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

# Delete task
def delete_task (cur):
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