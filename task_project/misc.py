from datetime import datetime

# Check if entity exists
# - Parameters:
#   1. t (string): entity type (task, category)
#   2. id (int): entity id
#   3. cursor (cursor): mariaDB cursor
def validator (t, id, cur):

    if t == "task":
        cur.execute("SELECT taskid FROM task WHERE taskid = ?", (id,))
        for taskid in cur:
            if id == taskid[0]: return 1   

    elif t == "category": 
        cur.execute("SELECT categoryid, cname FROM category WHERE categoryid = ?", (id))
        for categoryid in cur:
            if id == categoryid[0]: return 1

# Count 
# - Parameters:
#   1. t (string): entity type (task, category)
#   2. cursor (cursor): mariaDB cursor
def count (t, cur):
  cur.execute(f"SELECT COUNT(*) count FROM {t}")
  for count in cur:
    if count[0] == 0:
      print(f"There are currently no {t}s.") if t == "task" else print(f"There are currently no {t[:-1]}ies.")
      return None
    else: return count[0]

# Get user input and validate
# - Parameters:
#   1. msg (string): message prompt for input
#   2. type (string): input type (int, string, date)
#   3. min (int): minimum value
#   4. max (int): maximum value
#   5. optional_msg (string): message prompt for optional attributes ('y/n' prompts)
#   6. optional_rev (bool): False = return NULL if a 'no' input should disregard optional attribute, otherwise True if 'yes'
def get_input (msg, type, min, max, optional_msg, optional_rev):
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

        elif type == "int":
            try:
                int_input = int(input(msg))
                if (int_input >= min and int_input <= max):
                    return int_input
                else:
                    print("Invalid input!")

            except (ValueError, TypeError):
                print("Invalid input!")