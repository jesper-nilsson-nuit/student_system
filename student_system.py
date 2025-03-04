import os
import time
import sys
import re

os.system("cls||clear")

# Make a regular expression for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

display_welcome_message = True

text_colors = {
    "base" : "\033[0m",                 # Default color
    "system_header" :"\033[38;5;21;4m", # Blue and underlined
    "system" : "\033[0;36m",            # Cyan
    "error" : "\033[0;31m",             # Red
    "info_header" : "\033[1;32m",       # Green
    "information" : "\033[1;37m",       # White
    "menu_header" : "\033[38;5;178m",   # Dark yellow
    "menu" : "\033[0;33m",              # Yellow
    "selection" : "\033[38;5;157m",     # Bright green
    "welcome" : "\033[38;5;93m",        # Magenta/Purple
    "green" : "\033[1;32m",             # Green for confirmation at user actions
    "red" : "\033[0;31m",               # Red for confirmation at removal
}

students = [
    {"name": "Tobias Fors", "email": "tobias.fors@yh.nackademin.se", "age": 30,  "student_id": 11230, "grades": {"Pythonprogrammering 1": 1, "Databasteknik": 4}},
    {"name": "Karin Börjell", "email": "karin.borjell@yh.nackademin.se", "age": 32,  "student_id": 11231, "grades": {"Pythonprogrammering 1": 1, "Pythonprogrammering 2": 3}},
    {"name": "Daniel Eliasson", "email": "daniel.eliasson@yh.nackademin.se", "age": 29, "student_id": 11233, "grades": {"Pythonprogrammering 1": 1, "Affärsmannaskap": 2}},
    {"name": "Magdalena Andersson", "email": "magdalena.andersson@yh.nackademin.se", "age": 50, "student_id": 11234, "grades": {"Pythonprogrammering 1": 1, "Webbramverk inom python": 5}},
]

# Add each info_key to a separate list, this way we don't run into issues in our add_student function if the list of students is empty
info_keys = ["name", "email", "age", "student_id", "grades"]

# Function for validating an Email
def validate_email(email):
    # pass the regular expression and the string (email) into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False
    
# Function to handle coloring the menus, this lets me easily update the look of all menus at once
# This function is no longer used, since delayed_print_alt() handles all the output and colors
# I'm leaving it here for posterity because I thought it was a pretty clever way of doing it
def color_menu(input:str):
    # Regular expression to separate out all the menu "shortcuts"
    pattern = "\[.\]"
    spliced_menu_items = re.findall(pattern, input)
    # Replace each menu shortcut in the "menu-string" to add text color to just the menu item
    for menu_item in spliced_menu_items:
        input = input.replace(menu_item, text_colors['menu_header'] + menu_item + text_colors['menu'])
    return input

# I'm leaving my original delayed print function in for comparison
# It functioned very well when using "colorama Fore attributes" but I couldn't switch colors in-line
def delayed_print(string):
    trimmed_color = ""
    for color in text_colors:
        if text_colors[color] in string:
            trimmed_color = text_colors[color]
            string = string.replace(text_colors[color], "")
    
    for char in string:
        sys.stdout.write(trimmed_color + char)
        sys.stdout.flush()
        time.sleep(.02)

# The new delayed_print function that works with tuples of (text, color, True/False)
def delayed_print_alt(text_color_tuples):
    # Loop over each tuple to extract their parts
    for text, color, new_line in text_color_tuples:
        # For each character in the text, print it with the correct color and delay
        for char in text:
            sys.stdout.write(color + char)
            sys.stdout.flush()
            time.sleep(0.02) # - UNCOMMENT THIS TO PRINT WITH DELAY

        # If we're printing a system header, add an additional line-break.
        # "- id" handles selected student submenus, "welcome" handles the welcome message
        # It's a bit ugly and 'hard-coded' but it gets the job done
        if "main menu" in text.lower() or "submenu" in text.lower() or "- id" in text.lower() or "welcome" in text.lower():
            print()
        # If new_line is True we want to add a line-break
        if new_line:
            print()
    # Another line-break at the end to separate the output from the menu
    print()

# Function to add a countdown, used when moving back in menus and/or exiting the program      
def wait():
    for i in range(3, 0, -1):
        delayed_print_alt([(str(i)+"..", text_colors['system'], False)])
        time.sleep(0.5)
    print()

# Function to check if user input can be converted to an int (so that we can handle both 'q' and integers)
def check_numeric(input):
    if input.isnumeric():
        input = int(input)
    return input

# Function to print return message and clear the terminal
def return_from_menu():
    delayed_print_alt([("Returning to previous menu in", text_colors["system"], False)])
    wait()
    os.system("cls||clear")

# Function to retrieve a student's grades
def get_grades(student):
    # Create a list of grades, in tuples for our delayed print function
    grades = []
    for grade in students[student]['grades']:
        grades.append((f"{grade}: ", text_colors['info_header'], False))
        grades.append((f"{students[student]['grades'][grade]}", text_colors['information'], True))
    if grades:
        return grades
    else:
        return False

# Function to retrieve a student's personal information, excluding grades
def get_personal_info(student):
    personal_info = []
    for info in students[student]:
        # Ugly code to better align the info-output using tabs
        try:
            if len(info) > 5:
                tabs = "\t"
            else:
                tabs = "\t\t"
        except Exception:
            pass 
        # Add the personal info to a list of tuples for our delayed print function
        if not info == "grades":
            personal_info.append((f"{str(info).capitalize()}: ", text_colors['info_header'], False))
            personal_info.append((f"{tabs}{students[student][info]}", text_colors['information'], True))
    return personal_info

# Function to display the remove student submenu
def remove_student_submenu():
    while True:
        delayed_print_alt([
            ("Remove student submenu", text_colors["system_header"], True),
            ("Which student would you like to remove?", text_colors["system"], True),
            ("\n[q] ",text_colors["menu_header"], False),
            ("Go back", text_colors["menu"], False)
        ])
        # Print out all the students in the style of a menu
        for index, student in enumerate(students):
            delayed_print_alt([
                (f"[{index}] ", text_colors["menu_header"], False),
                (f"ID: {student['student_id']} - {student['name']}", text_colors["menu"], False)
            ])
        choice = input("\n" + text_colors["information"]).lower()
        # Convert input to int if possible, otherwise leave it as a string
        choice = check_numeric(choice)

        if choice not in range(len(students)) and choice != "q":
            os.system("cls||clear")
            delayed_print_alt([("Please enter a valid choice", text_colors["error"], True)])
        elif choice == "q":
            return_from_menu()
            break
        else:
            os.system("cls||clear")
            # Display student info and confirmation input
            while True:
                delayed_print_alt([
                    ("Selected student is:", text_colors['system_header'], False),
                    (f" - ID {students[choice]['student_id']} - {students[choice]['name']}", text_colors['selection'], False)
                ])
                student_info = get_personal_info(choice)
                delayed_print_alt(student_info)
                delayed_print_alt([("Is this the student you want to remove? (y/n)", text_colors["system"], False)])
                confirmation = input(text_colors["information"]).lower()
                if confirmation != "y" and confirmation != "n":
                    os.system("cls||clear")
                    delayed_print_alt([("Please enter a valid choice", text_colors["error"], True)])
                elif confirmation == "y":
                    os.system("cls||clear")
                    delayed_print_alt([
                        ("Student:", text_colors['system_header'], False),
                        (f" - ID {students[choice]['student_id']} - {students[choice]['name']}", text_colors['selection'], True),
                        ("Has been ", text_colors["system"], False),
                        ("removed", text_colors["info_header"], True)
                    ])
                    students.pop(choice)
                    delayed_print_alt([("Press ENTER to return", text_colors["system"], False)])
                    input(text_colors["information"])
                    os.system("cls||clear")
                    break
                elif confirmation == "n":
                    return_from_menu()
                    os.system("cls||clear")
                    break

#Function to display the student submenu
def student_submenu(choice):
    while True:
        os.system("cls||clear")
        # Display the selected student
        delayed_print_alt([
            ("Selected student is:", text_colors['system_header'], False),
            (f" - ID {students[choice]['student_id']} - {students[choice]['name']}", text_colors['selection'], True),
            ("What would you like to do?", text_colors["system"], True)
        ])
        # Student submenu
        delayed_print_alt([
            ("[q] ", text_colors["menu_header"], False),("Go Back", text_colors["menu"], True),
            ("[0] ", text_colors["menu_header"], False),("Show summary of grades", text_colors["menu"], True),
            ("[1] ", text_colors["menu_header"], False),("Display personal information", text_colors["menu"], True)
        ])
        user_choice = input(text_colors["information"]).lower()

        # Convert input to int if possible, otherwise leave it as a string
        user_choice = check_numeric(user_choice)
        # Return to the last menu
        if user_choice == "q":
            return_from_menu()
            break
        # Display student's grades
        elif user_choice == 0:
            os.system("cls||clear")
            delayed_print_alt([
                ("Selected student is:", text_colors['system_header'], False),
                (f" - ID {students[choice]['student_id']} - {students[choice]['name']}", text_colors['selection'], True),
                ("Their grades are:", text_colors['system'], True)
            ])
            grades = get_grades(choice)
            if grades:
                delayed_print_alt(grades)
            else:
                delayed_print_alt([("No grades", text_colors["error"], True)])
            delayed_print_alt([("Press ENTER to return", text_colors["system"], False)])
            input(text_colors["information"])
        # Display student's personal info
        elif user_choice == 1:
            os.system("cls||clear")
            delayed_print_alt([
                ("Selected student is:", text_colors['system_header'], False),
                (f" - ID {students[choice]['student_id']} - {students[choice]['name']}", text_colors["selection"], True),
                ("Their personal information is:", text_colors['system'], True)
            ])
            personal_info = get_personal_info(choice)
            delayed_print_alt(personal_info)
            delayed_print_alt([("Press ENTER to return", text_colors["system"], False)])
            input(text_colors["information"])

# Function to display the add student submenu
def add_student_submenu():
    while True:
        delayed_print_alt([("Add students submenu", text_colors["system_header"], False)])
        new_student = {}
        for info in info_keys:
            if info == "name":
                while True:
                    delayed_print_alt([("Please enter the student's full name:", text_colors['system'], False)])
                    user_input = input(text_colors["information"]).title()
                    if " " not in user_input:
                        delayed_print_alt([("\nNo space in name, try again", text_colors['error'], True)])
                    else:
                        break
            elif info == "email":
                while True:
                    delayed_print_alt([("Please enter the student's email address:", text_colors['system'], False)])
                    user_input = input(text_colors['information']).lower()
                    if not validate_email(user_input):
                        delayed_print_alt([("\nInvalid email, try again", text_colors['error'], True)])
                    else:
                        break
            elif info == "age":
                while True:
                    delayed_print_alt([("Please enter the student's age:", text_colors['system'], False)])
                    user_input = input(text_colors['information'])
                    if not user_input.isnumeric() or int(user_input) > 120:
                        delayed_print_alt([("\nInvalid age, try again", text_colors['error'], True)])
                    else:
                        break
            elif info == "student_id":
                try:
                    user_input = students[-1]["student_id"] + 1
                # If the list of students is empty the new student_id is set to a default value
                except IndexError:
                    user_input = 11230
            elif info == "grades":
                grades = {}
                while True:
                    delayed_print_alt([("Would you like to add a course? (y/n)", text_colors['system'], False)])
                    add_course_input = input(text_colors['information']).lower()
                    if add_course_input not in "yn":
                        delayed_print_alt([("\nInvalid input, please choose [y]es or [n]o", text_colors['error'], True)])
                    elif add_course_input.lower() == "y": # I'm not even going to attempt to input-validate the course inputs
                        delayed_print_alt([("Please enter the student's course:", text_colors['system'], False)])
                        course_input = input(text_colors['information'])
                        delayed_print_alt([(f"Please enter the student's grade for '{course_input}':", text_colors['system'], False)])
                        grade_input = input(text_colors['information'])
                        grades[course_input] = grade_input
                    elif add_course_input.lower() == "n":
                        break
                user_input = grades

            new_student[info] = user_input
        # I append the student directly to be able to use my info and grades functions
        # to retrieve and display their info in a nice, consistent format
        students.append(new_student)

        new_student_info = get_personal_info(-1)
        new_student_grades = get_grades(-1)
        os.system("cls||clear")
        delayed_print_alt(new_student_info)

        if new_student_grades:
            delayed_print_alt(new_student_grades)

        delayed_print_alt([("Is this information correct? (y/n)", text_colors['system'], False)])
        confirmation_input = input(text_colors['information']).lower()

        if confirmation_input not in "yn":
            delayed_print_alt([("Invalid input, try again", text_colors['error'], True)])
        elif confirmation_input == "y":
            delayed_print_alt([
                ("Student ", text_colors['system'], False),
                ("added", text_colors['green'], True)
            ])
            return_from_menu()
            break
        else:
            # If the user isn't satisfied, remove the student from the list
            # A 'better' solution might be to add an 'update_student()' function which we could call here
            # so that the user could just fix their mistakes instead of starting over from scratch
            students.pop()
            delayed_print_alt([
                ("Student ", text_colors['system'], False),
                ("discarded", text_colors['red'], False),
                (", please start over", text_colors['system'], True)
            ])
            return_from_menu()
            break

# Function to display the students list submenu
def display_students_submenu():
    while True:
        delayed_print_alt([
            ("Display all students submenu", text_colors["system_header"], True),
            ("Please select a student", text_colors["system"], True),
            ("\n[q] ",text_colors["menu_header"], False),
            ("Go back", text_colors["menu"], False)
        ])
        # Print out all the students in the style of a menu
        for index, student in enumerate(students):
            delayed_print_alt([
                (f"[{index}] ", text_colors["menu_header"], False),
                (f"ID: {student['student_id']} - {student['name']}", text_colors["menu"], False)
            ])
        choice = input("\n" + text_colors["information"]).lower()
        # Convert input to int if possible, otherwise leave it as a string
        choice = check_numeric(choice)

        if choice not in range(len(students)) and choice != "q":
            os.system("cls||clear")
            delayed_print_alt([("Please enter a valid choice", text_colors["error"], True)])
        # Return to the last menu
        elif choice == "q":
            return_from_menu()
            break
        # If input is within the range of students, display the submenu
        else:
            student_submenu(choice)

# The main menu loop
while True:
    # At first run print a welcome message
    if display_welcome_message:
        delayed_print_alt([
            ("Main menu", text_colors["system_header"], True),
            ("Welcome to the greatest student system in the world!", text_colors['welcome'], True),
            ("What would you like to do?", text_colors["system"], True)
        ])
    else:
        delayed_print_alt([
            ("Main menu", text_colors["system_header"], True),
            ("What would you like to do?", text_colors["system"], True)])
    # Display the main menu
    delayed_print_alt([
        ("[q] ", text_colors["menu_header"], False),("Exit program", text_colors["menu"], True),
        ("[0] ", text_colors["menu_header"], False),("List all students", text_colors["menu"], True),
        ("[1] ", text_colors["menu_header"], False),("Add a student", text_colors["menu"], True),
        ("[2] ", text_colors["menu_header"], False),("Remove a student", text_colors["menu"], True)
    ])
    user_choice = input(text_colors["information"]).lower() 
    user_choice = check_numeric(user_choice)

    # User has made an input, therefore we will no longer want to print the welcome message
    display_welcome_message = False

    # Simple error-handling to see if user input is within the valid values
    if user_choice not in range(3) and user_choice != "q":
        os.system("cls||clear")
        delayed_print_alt([("Please enter a valid choice", text_colors["error"], True)])
    elif user_choice == 0:
        os.system("cls||clear")
         # If the list of students is empty we don't want to waste time going into the menu to display students
        if students:
            display_students_submenu()
        else:
            delayed_print_alt([("No students to display", text_colors["error"], True)])
            return_from_menu()
    elif user_choice == 1:
        os.system("cls||clear")
        add_student_submenu()
    elif user_choice == 2:
        os.system("cls||clear")
        # If the list of students is empty we don't want to waste time going into the menu to remove students
        if students:
            remove_student_submenu()
        else:
            delayed_print_alt([("No students to remove", text_colors["error"], True)])
            return_from_menu()
    elif user_choice == "q":
        delayed_print_alt([("Exiting program in", text_colors['system'], False)])
        wait()
        os.system("cls||clear")
        delayed_print_alt([("Thank you and goodbye!", text_colors['system'], False)])
        time.sleep(1)
        os.system("cls||clear")
        print("\033[0m")
        exit()