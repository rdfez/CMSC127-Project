from datetime import datetime, date
import mariadb
import sys

def menu (): #Menu for the main features
  print("\n==========Menu=========")
  print("[1] Add")
  print("[2] Edit")
  print("[3] View")
  print("[4] Delete")
  print("[0] Exit")
  print("=======================")
  choice = get_input("\nEnter Choice: ", "int", 0, 4, None, None)
  return choice

def type (t): #Menu to choose between task or category
  print(f"\n----------{t}----------")
  print("[1] Task")
  print("[2] Category")
  print("[0] Back to Menu")
  print("-----------------------")
  choice = get_input(f"\n{t}: ", "int", 0, 2, None, None)
  return choice

def viewType (t): #Menu specific for different types of view task 
  print(f"\n------View {t}------")
  print(f"[1] a {t}")
  print(f"[2] all {t}")
  if t == "task":
    print("[3] tasks per day")
    print("[4] tasks per month")
    max = 4
  else: max = 2
  print("[0] Back to View Menu")
  print("-----------------------")
  choice = get_input(f"\nView: ", "int", 0, max, None, None)
  return choice

def addmenu (): #Add feature's menu

  while True:
    add = type("Add")
    if add == 1:
      taskTotal = Count("task")
      #Checks if task count is not 0
      if taskTotal is not None:
        print("\n-> Adding a task")
        #call add a task
    elif add == 2:
      categoryTotal = Count("category")
      #Checks if category count is not 0
      if categoryTotal is not None: 
        print("\n-> Adding a category")
        #call add a category
    else: break

  return

def editmenu (): #Edit feature's menu

  while True:
    edit = type("Edit")
    if edit == 1:
      taskTotal = Count("task")
      if taskTotal is not None:
        print("\n-> Editing a task")
        #call edit a task
    elif edit == 2:
      categoryTotal = Count("category")
      if categoryTotal is not None: 
        print("\n-> Editing a category")
        #call edit a category
    else: break

  return

def viewmenu (): #View feature's menu

  while True:
    viewtype = type("View")
    #Task
    if viewtype == 1: 
      taskTotal = Count("task")
      if taskTotal is not None: 
        while True:
          view = viewType("task")
          if view == 1: 
            print("\n-> Viewing a task")
            #call view a task
          elif view == 2:
            print("\n-> Viewing all tasks")
            #call view all task
          elif view == 3:
            print("\n-> Viewing a task per day")
            #call view a task per day
          elif view == 4:
            print("\n-> Viewing a task per month")
            #call view a task per month
          else: break
    #Category
    elif viewtype == 2: 
      categoryTotal = Count("category")
      if categoryTotal is not None: 
        while True:
          view = viewType("category")
          if view == 1:
            print("\n-> Viewing a category")
            #view a category
          elif view == 2:
            print("\n-> Viewing all categories")
            #view all categories
          else: break
    else: break

  return

def deletemenu (): #Delete feature's menu

  while True:
    delete = type("Delete")
    if delete == 1:
      taskTotal = Count("task")
      if taskTotal is not None:
        print("\n-> Deleting a task")
        #call delete a task
    elif delete == 2:
      categoryTotal = Count("category")
      if categoryTotal is not None: 
        print("\n-> Deleting a category")
        #call delete a category
    else: break

  return

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

#For testing purposes
conn = mariadb.connect(
  user="root",
  password="swift", #insert your password here
  host="127.0.0.1",
  database="tryEmpty" #insert your database name here
)

cur = conn.cursor()

########################################################

print("\nWelcome to Notes!")

while True:
  
  choice = menu()
  if choice == 1:
    addmenu()
  elif choice == 2:
    editmenu()
  elif choice == 3:
    viewmenu()
  elif choice == 4:
    deletemenu()
  else:
    print("\n Goodluck on your to-do list! \n")
    break
