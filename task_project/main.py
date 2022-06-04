import mariadb
from datetime import datetime, date

from misc import count, get_input
from view import view_category, view_alltasks, view_task, view_tasksperday, view_taskspermonth
from task import add_task, edit_task, delete_task
from category import add_category, edit_category, delete_category


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
      taskTotal = count("task", cur)
      #Checks if task count is not 0
      if taskTotal is not None:
        print("\n-> Adding a task", cur)
        #call add a task
        add_task(cur)
    elif add == 2:
      categoryTotal = count("category", cur)
      #Checks if category count is not 0
      if categoryTotal is not None: 
        print("\n-> Adding a category")
        #call add a category
        add_category(cur)
    else: break

  return

def editmenu (): #Edit feature's menu

  while True:
    edit = type("Edit")
    if edit == 1:
      taskTotal = count("task", cur)
      if taskTotal is not None:
        print("\n-> Editing a task")
        #call edit a task
        edit_task(cur)
    elif edit == 2:
      categoryTotal = count("category", cur)
      if categoryTotal is not None: 
        print("\n-> Editing a category")
        #call edit a category
        edit_category(cur)
    else: break

  return

def viewmenu (): #View feature's menu

  while True:
    viewtype = type("View")
    #Task
    if viewtype == 1: 
      taskTotal = count("task", cur)
      if taskTotal is not None: 
        while True:
          view = viewType("task")
          if view == 1: 
            print("\n-> Viewing a task")
            #call view a task
            view_task(taskTotal, cur)
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
      categoryTotal = count("category", cur)
      if categoryTotal is not None: 
        while True:
          view = viewType("category")
          if view == 1:
            print("\n-> Viewing a category")
            #view a category
            view_category(cur)
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
      taskTotal = count("task", cur)
      if taskTotal is not None:
        print("\n-> Deleting a task")
        #call delete a task
        delete_task(cur)
    elif delete == 2:
      categoryTotal = count("category", cur)
      if categoryTotal is not None: 
        print("\n-> Deleting a category")
        #call delete a category
        delete_category(cur)
    else: break

  return

########################################################

print("\nWelcome to Notes!")
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