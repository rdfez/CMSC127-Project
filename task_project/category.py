from misc import get_input, validator

priority_arr = ("Urgent", "High", "Medium", "Low")
color_arr = ("Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White")

# Add category
def add_category (cur):
    category_name = priority = color = False

    # Category id
    cur.execute("SELECT COUNT(*) count FROM category")

    for count in cur:
        category_total = count[0]+1

    for i in range(1, category_total+1):
        if validator("category", i, cur) == 1:
            continue
        else:
            new_taskid = i
            break
    
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

# Edit category
def edit_category (cur):
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

# Delete category
def delete_category (cur):
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