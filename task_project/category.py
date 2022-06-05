from misc import get_input, validator, get_id
from view import view_category

priority_arr = ("Urgent", "High", "Medium", "Low")
color_arr = ("Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White")

# Add category
def add_category (cur, category_total):
    if category_total == None:
        category_total = 0

    category_total = category_total + 1
    
    # Category id
    for i in range(1, category_total+1):
        if validator("category", i, cur) == 1:
            continue
        else:
            new_categoryid = i
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
            
    cur.execute("INSERT INTO category VALUES (?, ?, ?, ?);", (new_categoryid, category_name, priority_arr[priority-1], color_arr[color-1]))

    print("\nNew Category: ")
    view_category(cur, new_categoryid)

    print("\nCategory added successfully!")

# Edit category
def edit_category (cur):
    category_id = get_id("\nEnter Category ID: ", "category", None, None, cur)
    
    print(f"\nCategory Info:")
    view_category(cur, category_id)

    while True:
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
            print('''\nPriority:
            [1] Urgent
            [2] High
            [3] Medium
            [4] Low
            ''')
            int_value = get_input("Enter new level of priority: ", "int", 1, 4, None, None)
            value = priority_arr[int_value-1]

        # Color
        elif choice == 3:
            attribute = "color"
            print('''\nColor:
            [1] None/Black\t[5] Blue
            [2] Red\t\t[6] Magenta
            [3] Green\t\t[7] Cyan
            [4] Yellow\t\t[8] White
            ''')
            int_value = get_input("Enter color: ", "int", 1, 8, None, None)
            value = color_arr[int_value-1]

        elif choice == 0:
            break

        else:
            print("Invalid choice!")

        cur.execute("UPDATE category SET " + attribute + " = ? WHERE categoryid = ?;", (value, category_id))

        print(f"\nUpdated Task Info:")
        view_category(cur, category_id)

        print(f"\nTask's {attribute} was successfully updated!")
    return
        
# Delete category
def delete_category (cur):
    category_id = get_id("\nEnter Category ID: ", "category", None, None, cur)
    #we should set to null the category of the tasks in this category
    cur.execute("UPDATE task SET categoryid = NULL WHERE categoryid = ?;", (category_id,))
    cur.execute("DELETE FROM category WHERE categoryid = ?", (category_id,))
    print("\nCategory deleted.")

    return 

def delete_all_category (cur):
    cur.execute("UPDATE task SET categoryid = NULL;")
    cur.execute("DELETE FROM category;")
    print("\nAll category deleted.")

    return 

