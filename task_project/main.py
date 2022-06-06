import mariadb

from misc import count, get_input
from view import view_category, view_alltasks, view_task, view_tasksperday, view_taskspermonth, view_allcategories
from task import add_task, edit_task, delete_task, delete_all_task
from category import add_category, edit_category, delete_category, delete_all_category

# Initialize database/connection
def init():
    # Connect to MariaDB Platform
    conn_bool = True
    while conn_bool:
        mariadb_password = input("Enter password: ")

        try:
            conn = mariadb.connect(
                user = "root",
                password = mariadb_password,
                host = "localhost",
                autocommit = True
            )

            if(conn):
                conn_bool = False

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

    # Get Cursor
    global cur 
    cur = conn.cursor()

    # Create database/tables on initial boot and use app database
    cur.execute("CREATE DATABASE IF NOT EXISTS `task_app`;")
    cur.execute("USE `task_app`;")
    cur.execute('''
        CREATE TABLE IF NOT EXISTS `category` (
            `categoryid` INT(2) NOT NULL,
            `cname` VARCHAR(50) NOT NULL,
            `priority` VARCHAR(6) NOT NULL,
            `color` VARCHAR(20),
            PRIMARY KEY (`categoryid`)
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS `task` (
            `taskid` INT(2) NOT NULL,
            `title` VARCHAR(50) NOT NULL,
            `details` VARCHAR(500) NOT NULL,
            `status` VARCHAR(11) NOT NULL DEFAULT "not started",
            `duedate` DATE,
            `categoryid` INT(2),
            PRIMARY KEY (`taskid`),
            CONSTRAINT `task_categoryid_fk` FOREIGN KEY (`categoryid`) REFERENCES `category` (`categoryid`)
        );
    ''')

# Menu for the main features
def menu (): 
  print("\n==========Menu=========")
  print("[1] Add")
  print("[2] Edit")
  print("[3] View")
  print("[4] Delete")
  print("[0] Exit")
  print("=======================")
  choice = get_input("\nEnter Choice: ", "int", 0, 4, None, None)
  return choice

# Menu to choose between task or category
# - Parameters:
#   1. t (string): entity type (task, category)
def type (t): 
  print(f"\n----------{t}----------")
  print("[1] Task")
  print("[2] Category")
  print("[0] Back to Menu")
  print("-----------------------")
  choice = get_input(f"\n{t}: ", "int", 0, 2, None, None)
  return choice

# Menu specific for view function
# - Parameters:
#   1. t (string): entity type (task, category)
def viewType (t): 
  print(f"\nView:")
  print(f"\t[1] a {t}")
  print(f"\t[2] all {t}")
  if t == "task":
    print("\t[3] tasks per day")
    print("\t[4] tasks per month")
    max = 4
  else: max = 2
  print("\t[0] Back to View Menu")
  choice = get_input(f"\nView {t}: ", "int", 0, max, None, None)
  return choice

#Menu specific for delete function
# - Parameters:
#   1. t (string): entity type (task, category)
def deleteType (t): 
  print(f"\nDelete:")
  print(f"\t[1] a {t}")
  print(f"\t[2] all {t}")
  print(f"\t[0] Back to Menu")
  max = 2
  choice = get_input(f"\nDelete {t}: ", "int", 0, max, None, None )
  return choice

# Menu for the Add feature
def addmenu (): 

  while True:
    add = type("Add")
    if add == 1:
        taskTotal = count("task", cur, False)
        print("\n-> Adding a task")
        #call add a task
        add_task(cur, taskTotal)
    elif add == 2:
        categoryTotal = count("category", cur, False)
        print("\n-> Adding a category")
        #call add a category
        add_category(cur, categoryTotal)
    else: break

  return

# Menu for the Edit feature
# - Checks if the database is empty before calling specific edit function
def editmenu (): 

  while True:
    edit = type("Edit")
    if edit == 1:
      taskTotal = count("task", cur, True)
      if taskTotal is not None:
        print("\n-> Editing a task")
        #call edit a task
        edit_task(cur)
    elif edit == 2:
      categoryTotal = count("category", cur, True)
      if categoryTotal is not None: 
        print("\n-> Editing a category")
        #call edit a category
        edit_category(cur)
    else: break

  return

# Menu for the View feature
# - Checks if the database is empty before calling specific view function
def viewmenu (): 

  while True:
    viewtype = type("View")
    #Task
    if viewtype == 1: 
      taskTotal = count("task", cur, True)
      if taskTotal is not None: 
        while True:
          view = viewType("task")
          if view == 1: 
            print("\n-> Viewing a task")
            #call view a task
            view_task(cur, 0)
          elif view == 2:
            print("\n-> Viewing all tasks")
            #call view all task
            view_alltasks(cur)
          elif view == 3:
            print("\n-> Viewing a task per day")
            #call view a task per day
            view_tasksperday(cur)
          elif view == 4:
            print("\n-> Viewing a task per month")
            #call view a task per month
            view_taskspermonth(cur)
          else: break
    #Category
    elif viewtype == 2: 
      categoryTotal = count("category", cur, True)
      if categoryTotal is not None: 
        while True:
          view = viewType("category")
          if view == 1:
            print("\n-> Viewing a category")
            #view a category
            view_category(cur, 0)
          elif view == 2:
            print("\n-> Viewing all categories")
            #view all categories
            view_allcategories(cur)
          else: break
    else: break

  return

# Menu for the Delete feature
# - Checks if the database is empty before calling specific delete function
def deletemenu (): 

  while True:
    delete = type("Delete")
    if delete == 1:
      choice = deleteType("task")
      taskTotal = count("task", cur, True)
      if choice == 1:
        if taskTotal is not None:
          print("\n-> Deleting a task")
          #call delete a task
          delete_task(cur)
      else:
          if taskTotal is not None:
            print("\n-> Deleting all tasks")
            #call delete all task
            delete_all_task(cur)
    elif delete == 2:
      choice = deleteType("category")
      categoryTotal = count("category", cur, True)
      if choice == 1:
        if categoryTotal is not None: 
          print("\n-> Deleting a category")
          #call delete a category
          delete_category(cur)
      else:
        if categoryTotal is not None: 
          print("\n-> Deleting all category")
          #call delete all category
          delete_all_category(cur)

    else: break

  return

########################################################

print("\nWelcome to Color Note!")
init()

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
