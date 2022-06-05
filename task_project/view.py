from misc import get_input, get_id, get_categories
from colorama import Fore, Back, Style 

color_dict = {
    "Black": "", 
    "Red": Back.RED, 
    "Green": Back.GREEN, 
    "Yellow": Back.YELLOW, 
    "Blue": Back.BLUE, 
    "Magenta": Back.MAGENTA, 
    "Cyan": Back.CYAN, 
    "White": Fore.BLACK + Back.WHITE,
}

reset_color = Style.RESET_ALL

# View category
def view_category (cur, id):
    if id == 0:
        categoryID = get_id("\nEnter Category ID: ", "category", None, None, cur)
    else:
        categoryID = id

    cur.execute("SELECT * FROM category WHERE categoryid = ?", (categoryID,))

    for categoryid, cname, priority, color in cur:
        if categoryID == categoryid:
            print(f"\n{categoryid}\t{color_dict[color]} {cname} " + Style.RESET_ALL) 
            print(f" \t! {priority}")
    return 

# View all categories
def view_allcategories (cur): 
    cur.execute("SELECT categoryid, cname, priority, color FROM category") 

    for categoryid, cname, priority, color in cur: 
        print(f"\n{categoryid}\t{color_dict[color]} {cname} " + Style.RESET_ALL)
        print(f" \t! {priority}")

    return
        
# View a task
def view_task (cur, id):

    if id == 0:
        taskID = get_id("\nEnter Task ID: ", "task", None, None, cur)
    else:
        taskID = id

    cur.execute("SELECT taskid, title, details, status, duedate, categoryid FROM task WHERE taskid = ?", (taskID,))
    
    for taskid, title, details, status, duedate, categoryid in cur:
        if categoryid != None:
            cur.execute("SELECT categoryid, cname,priority, color FROM category WHERE categoryid = ?", (categoryid,))
            for categoryid, cname, priority, color in cur:
                if taskid == taskID:
                    print(f"\n({categoryid}) {color_dict[color]} {cname} " + Style.RESET_ALL)
                    print(f"\n    {taskid}\t{title}")
                    print(f"\t{details}")
                    print(f"\tStatus: {status}\t Due Date: {duedate}")

        else:
            if taskid == taskID:
                print(f"\n(No category)")
                print(f"    {taskid}\t{title}")
                print(f"\t{details}")
                print(f"\tStatus: {status}\t Due Date: {duedate}")
        
    return

# View all tasks
def view_alltasks (cur):
            
    category_list = get_categories(cur)

    for id in category_list:
        if id is None:
          cur.execute("SELECT taskid, title, details, status, duedate, categoryid FROM task WHERE categoryid IS NULL")
          for taskid, title, details, status, duedate, categoryid in cur:
            print(f"\n(No category)")
            print(f"\n    {taskid}\t{title}")
            print(f"\t{details}")
            print(f"\tStatus: {status}\t Due Date: {duedate}")

        cur.execute("SELECT categoryid, cname, priority, color FROM category WHERE categoryid = ?", (id,))
        for categoryid, cname, priority, color in cur:
          print(f"\n({categoryid}) {color_dict[color]} {cname} " + Style.RESET_ALL)

        cur.execute("SELECT taskid, title, details, status, duedate, categoryid FROM task WHERE categoryid = ?", (id,))
        for taskid, title, details, status, duedate, categoryid in cur:
          print(f"\n    {taskid}\t{title}")
          print(f"\t{details}")
          print(f"\tStatus: {status}\t Due Date: {duedate}")

    return

# View tasks per day
def view_tasksperday (cur): 

    flag = 0
    dueDate = get_input("\nEnter due date (DD-MM-YYYY): ", "date", None, None, None, None)

    cur.execute("SELECT taskid, title, details, status, duedate, categoryid FROM task WHERE duedate = ?", (dueDate,))

    for taskid, title, details, status, duedate, categoryid in cur:
        if flag == 0: print(f"\n  ID\tTitle\t\tStatus\n")
        if duedate == dueDate:
            print(f"  • {taskid}\t{title}\t{status}")
            flag = 1
    
    if flag == 0: print("\nYay! No tasks for this day!")

    return

# View tasks per month
def view_taskspermonth (cur):

    flag = 0
    month = get_input("\nEnter month (MM): ", "month", 1, 12, None, None)

    cur.execute("SELECT taskid, title, details, status, duedate, categoryid FROM task WHERE MONTH(duedate) = ?", (month,))

    for taskid, title, details, status, duedate, categoryid in cur:
        if flag == 0: print("\n  ID\t Title\t\tStatus\t\tDue Date\n") 
        date = str(duedate)
        mm = date[5:7]
        if mm == month:
            print(f"  • {taskid}\t{title}\t{status}\t{duedate}")
            flag = 1

    if flag == 0: print("\nYay! No tasks for this month!")

    return
