from misc import get_input
from colorama import Fore, Back, Style 

color_arr = {
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
def view_category (cur):
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

# View all categories
def view_allcategories (cur): 
    cur.execute("SELECT categoryid, cname, priority, color FROM category") 

    for categoryid, cname, priority, color in cur: 
        print(f"\n{categoryid}\t{cname} - {color}")
        print(f" \t! {priority}")

  return
        
# View a task
def view_task (totalCount, cur):

    flag = 0
    taskID = get_input("\nEnter Task ID: ", "int", 0, totalCount, None, None)

    cur.execute("SELECT taskid, title, details, status, duedate, categoryid FROM task WHERE taskid = ?", (taskID,))
    
    for taskid, title, details, status, duedate, categoryid in cur:
        if categoryid != None:
            cur.execute("SELECT categoryid, cname,priority, color FROM category WHERE categoryid = ?", (categoryid,))
            for categoryid, cname, priority, color in cur:
                if taskid == taskID:
                    print(f"\n({categoryid}) {cname}")
                    print(f"    {taskid}\t{title}")
                    print(f"\t{details}")
                    print(f"\tStatus: {status}\t Due Date: {duedate}")
                    flag = 1
        else:
            if taskid == taskID:
                print(f"\n(No category)")
                print(f"    {taskid}\t{title}")
                print(f"\t{details}")
                print(f"\tStatus: {status}\t Due Date: {duedate}")
                flag = 1
        
    if flag == 0: print("\nThe task does not exist.")

    return

# Get list of categories
def getCategories(cur):
    category_list = []
    cur.execute("SELECT taskid, title, details, status, duedate, categoryid FROM task GROUP BY categoryid")
    for taskid, title, details, status, duedate, categoryid in cur:
        category_list.append(categoryid)
    return category_list

# View all tasks
def view_alltasks (cur):
            
    category_list = getCategories(cur)

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
          print(f"\n({categoryid}) {color_arr[color]} {cname} " + Style.RESET_ALL)

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
