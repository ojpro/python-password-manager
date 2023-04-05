# import needed libraries
import time
import sqlite3
import string
import secrets

# open connection to the database
def db():
    return sqlite3.connect("database.db")

# execute a query into the database
def execute(query):
    cursor = db().cursor()
    return cursor.execute(query)

# insert into the database
def insert(query):
    connect = db()
    cursor = connect.cursor()
    cursor.execute(query)
    return connect.commit()

# search for an app
def search(query):
    res = execute(query)
    return res.fetchall()

def prompt(msg,can_quit = True):
    res = str(input("\n"+msg))
    if (res == 'q' or res == 'Q') and can_quit == True:
        exit()
    return res

def displayAppsMenu(apps):
    
        print("\n\n++++++++++++++++ Results ++++++++++++++++\n")
        for i in range(len(apps)):
            app = apps[i]
            print("["+(str(i+1))+"] => "+ app[1] + " - " + str(apps[i][0]))

        app = []
        if len(apps) >= 1:
            print("\n------------- Which App -------------\n")
            app_id = int(prompt("Choice App : "))
            app = apps[app_id-1]

        elif len(apps) == 1:
            app = apps[0]
        else :
            print("No apps with this name")
            exit()

        # ask for options
        print("\n--------------------- App Menu ---------------------\n")
        print("================= " + app[1] + " ===============")
        print("1. See Password.")
        print("2. Change Password.")
        print("3. Random Password.")
        print("4. Delete Application.")
        option = int(prompt("Choice a number : "))
        
        # do what need to be done
        if option == 1:
            selected_app = search("SELECT username,password FROM applications WHERE `id`="+str(app[0]))
            print("\n\n\n------ Password for user  [ "+selected_app[0][0]  +" ]  is : [ "+selected_app[0][1] + " ]\n\n")
        elif option == 2:
            password = prompt("New Password : ")
            insert("UPDATE applications SET `password`='"+password+"' WHERE `id`="+str(app[0]))
            print("Password Changed\n\n")
        elif option == 3:
            password = randomPassword()
            insert("UPDATE applications SET `password`='"+password+"' WHERE `id`="+str(app[0]))
            # print success message
            print(app[1] +"'s password changed to : "+password)

        elif option == 4:
            remove = prompt("Are You Sure You wanna Delete it [Y]es / [N]o : ")
            if remove == 'y':
                insert("DELETE FROM applications WHERE `id`="+str(app[0]))
                print("Application Deleted.\n\n")
            displayMenu()
        
    # create the applications table
def init():
    execute("CREATE TABLE IF NOT EXISTS applications(id INTEGER primary key ,name TEXT, username TEXT, password TEXT, status TEXT, update_at DATETIME);")


# generate random password
def randomPassword():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))
    return password


# initialize the database
init()

# display the options of the first menu
def displayMenu():
    print("\n--------------------- Menu ---------------------\n")
    print("1. Add new application.")
    print("2. Search for an application.")
    print("3. List all the applications.")
    # ask for an option
    first_option = int(prompt("Enter a number to process : "))
    # prompt for adding new application
    if first_option == 1 :
            # ask for app name and password
            print("\n------------- Add New Application -------------\n")
            name = prompt("Application Name : ")
            username = prompt("Username for ["+ name +"] : ")
            password = prompt("Password for ["+ name +"] : ")

            # add the new application
            res = insert("INSERT INTO applications(`name`,`username`,`password`,`update_at`) VALUES('"+name+"','"+username+"','"+password+"','"+time.ctime()+"')")

            if res is None:
                print("\n\n ##### Application Added Successfully. ##### \n")
                displayMenu()
            else:
                print("Something wrong please try again")


    # prompt to search for an application
    elif first_option == 2:
        # find an application
        print("\n------------- Search 4 Application -------------\n")
        app_name = prompt("Search for : ",False)

        apps = search("SELECT * FROM applications WHERE `name` LIKE '%"+app_name+"%' OR `username`  LIKE '%"+app_name+"%' ")

        displayAppsMenu(apps)
    
    # list all the existed applications
    elif first_option == 3:
        apps = search("SELECT * FROM applications")
        displayAppsMenu(apps)


    # otherwise re-display the menu
    else:
        print("Something wrong!, Please try again.")
        displayMenu()

displayMenu()
