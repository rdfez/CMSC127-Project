from datetime import datetime
import mariadb
import sys

def get_input(msg, type, min, max, optional_msg, optional_rev): # Get user input and validate
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

        elif type == "month":
            try:
              month = int(input(msg))
              if (month >= min and month <= max):
                month = str(month).zfill(2)
                return month
              else:
                print("Invalid input!")

            except (ValueError, TypeError):
                print("Invalid input!")

        elif type == "int":
            try:
                int_input = int(input(msg))
                if (int_input >= min and int_input <= max):
                    return int_input
                else:
                    print("Invalid input!")

            except (ValueError, TypeError):
                print("Invalid input!")

def Count (t):
  cur.execute(f"SELECT COUNT(*) count FROM {t}")
  for count in cur:
    if count[0] == 0:
      print(f"There are currently no {t}s.") if t == "task" else print(f"There are currently no {t[:-1]}ies.")
      return None
    else: return count[0]

def validator(t, id):
  
  if t == "task":
    cur.execute("SELECT taskid, title, details, status, duedate, categoryid FROM task WHERE taskid = ?", (id,))
    for taskid, title, details, status, duedate, categoryid in cur:
      if id == taskid: return 1

  elif t == "category": 
    cur.execute("SELECT categoryid, cname, priority, color FROM category WHERE categoryid = ?", (id,))
    for categoryid, cname, priority, color in cur:
      if id == categoryid: return 1

  return 0

def getCategories():
  category_list = []
  cur.execute("SELECT taskid, title, details, status, duedate, categoryid FROM task GROUP BY categoryid")
  for taskid, title, details, status, duedate, categoryid in cur:
    category_list.append(categoryid)
  return category_list    

def viewAllCategory (): #function for view all categories 
  cur.execute("SELECT categoryid, cname, priority, color FROM category") 

  for categoryid, cname, priority, color in cur: #loop for printing category id and category name
    print(f"\n{categoryid}\t{cname} - {color}")
    print(f" \t! {priority}")

  return

def viewTask (totalCount):

  taskID = get_input("\nEnter Task ID: ", "int", 0, totalCount, None, None)
  flag = validator("task", taskID)

  if flag == 0:
    print("\nThe task does not exist.")
  else:

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

      else:
        if taskid == taskID:
          print(f"\n(No category)")
          print(f"    {taskid}\t{title}")
          print(f"\t{details}")
          print(f"\tStatus: {status}\t Due Date: {duedate}")

  return

def getCategories():
  category_list = []
  cur.execute("SELECT taskid, title, details, status, duedate, categoryid FROM task GROUP BY categoryid")
  for taskid, title, details, status, duedate, categoryid in cur:
    category_list.append(categoryid)
  return category_list

def viewAllTasks ():

  category_list = getCategories()

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
      print(f"\n({categoryid}) {cname}")

    cur.execute("SELECT taskid, title, details, status, duedate, categoryid FROM task WHERE categoryid = ?", (id,))
    for taskid, title, details, status, duedate, categoryid in cur:
      print(f"\n    {taskid}\t{title}")
      print(f"\t{details}")
      print(f"\tStatus: {status}\t Due Date: {duedate}")

  return

def viewTaskPerDay (): 

  flag = 0
  dueDate = get_input("\nEnter new due date (DD-MM-YYYY): ", "date", None, None, None, None)

  cur.execute("SELECT taskid, title, details, status, duedate, categoryid FROM task WHERE duedate = ?", (dueDate,))

  for taskid, title, details, status, duedate, categoryid in cur:
    if flag == 0: print(f"\n  ID\tTitle\t\tStatus\n")
    if duedate == dueDate:
      print(f"  • {taskid}\t{title}\t{status}")
      flag = 1
  
  if flag == 0: print("\nYay! No tasks for this day!")

  return

def viewTaskPerMonth ():

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

conn = mariadb.connect(
  user="root",
  password="", #enter password
  host="127.0.0.1",
  database="" #enter database name
)

cur = conn.cursor()

taskTotal = Count("task")
viewTask(taskTotal)
viewAllTasks()
viewTaskPerDay()
viewTaskPerMonth()
