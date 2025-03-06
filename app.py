import json
import re
from datetime import datetime 

# Users
users = {}
users_file = "users.json"

def save_to_file(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

def load_from_file(file_name):
    try:
        with open(file_name, "r") as f:
            data = f.read().strip()
            return json.loads(data) if data else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {} if "users" in file_name else []

# Projects
projects_file = "projects.json"

# Registration
def register():
    print("<<--------------->> Registration <<--------------->>")
    
    first_name = input("Enter your first name: ")
    while not first_name.isalpha():
        print("!!!First name should contain only letters!!!")
        first_name = input("Enter your first name: ")

    last_name = input("Enter your last name: ")
    while not last_name.isalpha():
        print("!!!Last name should contain only letters!!!")
        last_name = input("Enter your last name: ")
    
    email = input("Enter your email: ")
    users = load_from_file(users_file)
    if email in users:
        print("!!!Email already exists!!!")
        return
    
    while not re.match(r"^[a-zA-Z0-9-_.]+@[a-zA-Z0-9]+\.[a-z]{2,}$", email):
        print("!!!Invalid email address!!!")
        email = input("Please enter your email: ")

    password = input("Enter your password: ")
    while len(password) < 6:
        print("!!!Password should be at least 6 characters!!!")
        password = input("Enter your password: ")

    confirm_password = input("Confirm your password: ")
    while password != confirm_password:
        print("!!!Passwords do not match!!!")
        confirm_password = input("Confirm your password: ")

    phone_number = input("Enter your phone number: ")
    phone_pattern = r"^(\+201|01|00201)[0-2,5]{1}[0-9]{8}$"
    while not re.match(phone_pattern, phone_number):
        print("!!!Invalid phone number. Please enter an Egyptian phone number!!!")
        phone_number = input("Enter your phone number: ")

    users[email] = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "phone_number": phone_number
    }
    
    save_to_file(users_file, users)
    print("*****User registered successfully*****")
    print(" ")

# Login
def login():
    print("<<--------------->> Login <<--------------->>")
    email = input("Enter your email: ")
    users = load_from_file(users_file)
    
    if email not in users:
        print("!!!Email does not exist!!!")
        print(" ")
        return None

    password = input("Enter your password: ")
    if password != users[email]["password"]:
        print("!!!Incorrect password!!!")
        print(" ")
        return None

    print("*****Logged in successfully*****")
    print(" ")
    return email

# Date format validation
def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("!!!Invalid date format, please use YYYY-MM-DD!!! ")
        return None

# Create Project
def create_project(user_email):
    print("<<--------------->> Create Project <<--------------->>")
    projects = load_from_file(projects_file)

    project_name = input("Enter project name: ")
    project_details = input("Enter project details: ")

    total_target = input("Enter project target in EGPs: ")
    while not total_target.isdigit():
        print("!!!Target should be a number!!!")
        total_target = input("Enter project target in EGPs: ")

    start_date = None
    while start_date is None:
        start_date = validate_date(input("Enter project start date in the format YYYY-MM-DD: "))

    end_date = None
    while end_date is None or end_date < start_date:
        end_date = validate_date(input("Enter project end date in the format YYYY-MM-DD: "))
        if end_date and end_date < start_date:
            print("!!!End date should be after start date!!")

    project = {
        "project_name": project_name,
        "project_details": project_details,
        "total_target": total_target,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "user_email": user_email
    }

    projects.append(project)
    save_to_file(projects_file, projects)
    print("*****Project created successfully*****")
    print(" ")

# View Projects
def view_projects(user_email):
    print("<<--------------->> View Projects <<--------------->>")
    projects = load_from_file(projects_file)
    found = False 

    for project in projects:
        if project["user_email"] == user_email:
            found = True
            print(f"Project Name: {project['project_name']}")
            print(f"Project Details: {project['project_details']}")
            print(f"Target: {project['total_target']} EGP")
            print(f"Start Date: {project['start_date']}")
            print(f"End Date: {project['end_date']}")
            print(" ")

    if not found:
        print("!!!No projects found!!!")
        print(" ")

#Edit Project
def edit_project(user_email):
    print("<<--------------->>Edit Project<<--------------->>")
    projects = load_from_file(projects_file)
    project_name = input("Enter the name of the project you want to edit: ")
    # print("DEBUG: Current Projects:", projects)
    for project in projects:
        if project["user_email"] == user_email and project["project_name"] == project_name:
            while True:
                print("what would you like to edit in this project?")
                print("1. Project Name")
                print("2. Project Details")
                print("3. Target")
                print("4. Start Date")
                print("5. End Date")
                print("6. Exit")
                choice = input("Enter your choice: ")
                if choice == "1":
                    project["project_name"] = input("Enter new project name: ")
                elif choice == "2":
                    project["project_details"] = input("Enter new project details: ")
                elif choice == "3":
                    project["total_target"] = input("Enter new project target in EGPs: ")
                elif choice == "4":
                    project["start_date"] = input("Enter new project start date: ")
                elif choice == "5":
                    project["end_date"] = input("Enter new project end date: ")
                elif choice == "6":
                    break
                else:
                    print("!!!Invalid choice!!!")
                    print(" ")
            
            save_to_file(projects_file, projects)
            print("*****Project edited successfully*****")
            print(" ")
            return

    print("Project not found")
    print(" ")

# Delete Project
def delete_project(user_email):
    print("<<--------------->> Delete Project <<--------------->>")
    projects = load_from_file(projects_file)
    project_name = input("Enter the name of the project you want to delete: ")

    new_projects = [p for p in projects if not (p["user_email"] == user_email and p["project_name"] == project_name)]
    
    if len(new_projects) == len(projects):
        print("!!!Project not found!!!")
        print(" ")
    else:
        save_to_file(projects_file, new_projects)
        print("*****Project deleted successfully*****")
        print(" ")

#Search project by date
def search_projects():
    print("<<--------------->>Search Projects by Date<<--------------->>")
    projects = load_from_file(projects_file)
    start_date = validate_date(input("Enter the start date of the project you want to search for: "))

    if start_date:
        found = False
        start_date_str = start_date.strftime("%Y-%m-%d")
        for project in projects:
            if project["start_date"] == start_date_str:
                found = True
                print(f"Project Name: {project['project_name']}")
                print(f"Project Details: {project['project_details']}")
                print(f"Target: {project['total_target']}")
                print(f"Start Date: {project['start_date']}")
                print(f"End Date: {project['end_date']}")
                print(" ")

    if not found:
        print(" ")
        print("!!!No projects found!!!")
        print(" ")

# Main function
def main():
    users.update(load_from_file(users_file))

    while True:
        print("<<--------------->> Welcome to the Crowdfunding Platform <<--------------->>")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            user_email = login()
            if user_email:
                while True:
                     print("Please pick an option:")
                     print("1. Create a New Project")
                     print("2. View Existing Projects")
                     print("3. Edit Your Project")
                     print("4. Delete Your Project")
                     print("5. Search Projects by Date")
                     print("6. Exit")
                     new_choice = input("Enter your choice: ")
                     if new_choice == "1":
                          create_project(user_email)
                     elif new_choice == "2":
                          view_projects(user_email)
                     elif new_choice == "3":
                          edit_project(user_email)
                     elif new_choice == "4":
                          delete_project(user_email)
                     elif new_choice == "5":
                          search_projects()
                     elif new_choice == "6":
                          break
                     else:
                          print("!!!Invalid choice!!!")
                          print(" ")
        elif choice == "3":
            print(" ")
            print("***** Thank you for using our app! *****")
            break
        else:
            print(" ")
            print("!!!Invalid choice!!!")
            print(" ")

main()
