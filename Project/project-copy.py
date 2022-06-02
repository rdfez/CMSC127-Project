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
  choice = int(input("\nChoice:"))
  return choice

def type (): #Menu to choose between task or category
  print("[1] Task")
  print("[2] Category")
  print("[0] Back to Menu")
  print("-----------------------")
  return 

def viewtype (): #Menu specific for different types of view 
  print("[1] a category")
  print("[2] all categories")
  print("[3] a task")
  print("[4] all tasks")
  print("[5] tasks per day")
  print("[6] tasks per month")
  print("[0] Back to Menu")
  print("-----------------------")
  return 

def addmenu (): #Add feature's menu

  while True:
    print("\n----------Add----------")
    type()
    add = int(input("\nAdd:"))

    if add == 1:
      print("\n-> Adding a task")
        #call add a task

    elif add == 2:
      print("\n-> Adding a category")
        #call add a category

    elif add == 0:
      break

    else:
      print("\n Not a valid input! ")

  return

def editmenu (): #Edit feature's menu

  while True:

    print("\n---------Edit----------")
    type()
    edit = int(input("\nEdit:"))

    if edit == 1:
      print("\n-> editing a task")
        #call edit a task

    elif edit == 2:
      print("\n-> editing a category")
        #call edit a category

    elif edit == 0:
      break

    else:
      print("\n Not a valid input! ")

  return

def viewmenu (): #View feature's menu

  while True:

    print("\n----------view----------")
    viewtype()
    view = int(input("\nView:"))

    if view == 1:
      print("\n--> Viewing a category \n")
        #call view a category

    elif view == 2:
      print("\n--> Viewing all categories\n")
        #call view all categories

    elif view == 3:
      print("\n--> Viewing a task\n")
      #call view a task

    elif view == 4:
      print("\n--> Viewing all tasks\n")
      #call view all tasks

    elif view == 5:
      print("\n--> Viewing tasks per day\n")
      #call view tasks per day

    elif view == 6:
      print("\n--> Viewing tasks per month\n")
      #call view tasks per month

    elif view == 0:
      break

    else:
      print("\n Not a valid input! ")

  return

def deletemenu (): #Delete feature's menu

  while True:

    print("\n----------delete----------")
    type()
    delete = int(input("\ndelete:"))

    if delete == 1:
      print("\n-> deleting a task")
        #call delete a task

    elif delete == 2:
      print("\n-> deleting a category")
        #call delete a category

    elif delete == 0:
      break

    else:
      print("\n Not a valid input! ")

  return

conn = mariadb.connect(
  user="root",
  password="", #insert your password here
  host="127.0.0.1",
  database="" #insert your database name here
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

  elif choice == 0:
    print("\n Goodluck on your to-do list! \n")
    break

  else:
    print("\n Not a valid input! \n")