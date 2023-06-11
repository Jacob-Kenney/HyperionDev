import os
from datetime import datetime, date
DATETIME_STRING_FORMAT = "%Y-%m-%d"

class Task_manager:

    def __init__(self):
        # Operational properties
        self.users = self.update_existing_users()
        self.tasks = self.update_tasks()
        self.tasks_for_current = []
        self.logged_in = False
        self.current_user = None
        self.is_admin = False
        self.reports_generated = False
    
        self.menu()

    def menu(self):

        print('\n-----Kenney Task Manager Menu-----')
        print('Action code:          Action')
        print('1:                   Log in')
        print('2:                   Exit')

        # Check if the user is logged in to prevent them from selecting options restricted to specific users
        if self.logged_in == False:
            valid_action = False
            while valid_action == False:
                action = input('Enter action code:')
                if action.isnumeric() == False:
                    print('ERROR: Action code must be numeric')
                    continue
                action = int(action)
                if (action < 1) or (action > 2):
                    print('ERROR: Invalid action code')
                    continue
                else:
                    valid_action = True
            

        # Check the user privileges to ensure that only the admin can take certain actions
        elif self.is_admin == False:
            print('3:                   Add task')
            print('4:                   View my tasks')
            valid_action = False
            while valid_action == False:
                action = input('Enter action code:')
                if action.isnumeric() == False:
                    print('ERROR: Action code must be numeric')
                    continue
                action = int(action)
                if (action < 1) or (action > 4):
                    print('ERROR: Invalid action code')
                    continue
                else:
                    valid_action = True
            

        # If the current user is the admin then all actions are unlocked
        else:
            print('3:                   Add task')
            print('4:                   View my tasks')
            print('5:                   View all tasks')
            print('6:                   Generate reports')
            print('7:                   Display statistics')
            print('8:                   Register new user')
            valid_action = False
            while valid_action == False:
                action = input('Enter action code:')
                if action.isnumeric() == False:
                    print('ERROR: Action code must be numeric')
                    continue
                action = int(action)
                if (action < 1) or (action > 8):
                    print('ERROR: Invalid action code')
                    continue
                else:
                    valid_action = True

        # Take the user action to its respective function
        self.execute_action(action)

    def execute_action(self, action: int):
        if action == 1:
            self.login()
        elif action == 2:
            self.exit_program()
        elif action == 3:
            self.add_task()
        elif action == 4:
            self.view_mine()
        elif action == 5:
            self.view_all()
        elif action == 6:
            self.generate_reports()
        elif action == 7:
            self.display_stats()
        elif action == 8:
            self.reg_user()
            
            
    def get_current_user(self):

        # Ensure that the inputted username exists 
        username = input('\nUsername:')
        while username not in self.users:
            print('ERROR: Invalid username')
            username = input('Username:')

        # Ensure that the inputted password matches the password of the user
        password = input('\nPassword:')
        if self.password_check(username, password) == False:
            print('ERROR: Incorrect password')
            return self.get_current_user()
        else:
            return username

    def password_check(self, username, password):

        # Check the user file for the password of the requested username, return True if given password is correct
        with open('user.txt', 'r+') as existing_users:
            for user in existing_users:
                curr_username = user.split(';')[0]
                if username == curr_username:
                    # .rstrip is used here to remove trailing newline characters
                    curr_password = (user.split(';')[1]).rstrip()
            if password == curr_password:
                return True
            return False

    def login(self):

        # Use helper functions to login to an account, updating local properties as needed
        print('\n-----Login-----')
        username = self.get_current_user()
        self.logged_in = True

        # Update the current user property for tracking
        self.current_user = username
        if username == 'admin':
            self.is_admin = True
        else:
            self.is_admin = False
        print('\n|--------------------------------|')
        print(f'|  Logged in as: {username}')
        print('|--------------------------------|')

        # Return the user to the menu for further actions
        self.menu()

    def exit_program(self):

        # Terminate the script when the user requests it from the menu
        quit()

    def get_new_user(self):

        # Get the usersname, with some input sanitisation to ensure that usernames are sensible
        valid_username = False
        print('New usernames must be between 3 and 15 characters long and alphanumerical')
        while valid_username == False:
            new_username = input('New Username:')
            if (len(new_username) < 3) or (len(new_username) > 15):
                print('ERROR: New username is not between 3 and 15 characters long\n')
                continue
            elif new_username.isalnum() == False:
                print('ERROR: New username is not alphanumerical\n')
                continue
            elif new_username in self.users:
                print('ERROR: This user already exists\n')
                continue
            else:
                valid_username = True

        # Get the password, with some input sanitisation to ensure that passwords are sensible 
        valid_password = False
        print('\nPassword must be between 3 and 15 characters long and alphanumerical')
        while valid_password == False:
            password = input('New Password:')
            if (len(password) < 3) or (len(password) > 15):
                print('ERROR: Password is not between 3 and 15 characters long\n')
                continue
            elif password.isalnum() == False:
                print('ERROR: Password is not alphanumerical\n')
                continue
            else:
                valid_password = True

        # Ensure that the confirm password matches to guarantee that the user does want this password
        confirm_password = input('Confirm Password:')
        while confirm_password != password:
            print('ERROR: Passwords do not match\n')
            confirm_password = input('Confirm Password:')

        return new_username, password

    def reg_user(self):

        # Use helper functions to get new username and password
        print('\n-----Register new user-----')
        username, password = self.get_new_user()

        # Write the new user details to the user file
        with open('user.txt', 'a') as existing_file_handle:
            existing_file_handle.write(f'\n{username};{password}')

        # Update the property which countains usernames
        self.users = self.update_existing_users()
        print('\n|--------------------------------|')
        print(f'|  Registered {username}')
        print('|--------------------------------|')

        # Return the user to the menu for further actions
        self.menu()
            
    def update_existing_users(self):

        # Read then return all usernames in the user file as an array
        users = []
        with open('user.txt', 'r+') as existing_users:
            for user in existing_users:
                username = user.split(';')[0]
                users.append(username)
        return users
    
    def update_tasks(self):
        
        # Read all tasks from the task file
        with open('tasks.txt', 'r') as task_file:
            task_data = task_file.read().split('\n')
            task_data = [task for task in task_data if task != '']

        # Return tasks as an array of dictionarys containg sensible key: value pairs
        task_list = []
        task_ID = 0
        for task in task_data:
            curr_task = {}

            task_components = task.split(';')
            curr_task['username'] = task_components[0]
            curr_task['title'] = task_components[1]
            curr_task['description'] = task_components[2]
            curr_task['due_date'] = task_components[3]
            curr_task['assigned_date'] = task_components[4]
            curr_task['completed'] = True if task_components[5] == "Yes" else False
            curr_task['ID'] = task_ID
            task_ID += 1
            task_list.append(curr_task)

        return task_list

    def add_task(self):

        # Use helper functions to get task parameters
        print('\n-----Add task-----')
        username, title, description, due_date, curr_date = self.get_task_parameters()

        # Write a new task to the tasks file
        with open('tasks.txt', 'a') as tasks_file:
            new_task = f'{username};{title};{description};{due_date};{curr_date};No\n'
            tasks_file.write(new_task)
        print('\n|---------------------------------|')
        print('|  Successfully created new task  |')
        print('|---------------------------------|')

        # Update the property which contains an array of dictionarys for each task as new tasks are present
        self.tasks = self.update_tasks()

        # Return the user to the menu for further actions
        self.menu()

    def get_task_parameters(self):

        # Ensure that the inputted username exists
        username = input('\nUsername of user to assign task to:')
        while username not in self.users:
            print('ERROR: Invalid username')
            username = input('Username:')

        title = input('Enter the title of this task:')
        description = input('Enter a description for this task:')

        # Ensure that the due date is in the requested format
        due_date = input('Enter due date as "YYYY-MM-DD":')
        while self.is_datetime_string(due_date) == False:
            print('ERROR: Incorrect input form')
            due_date = input('\nEnter new due date as "YYYY-MM-DD":')

        curr_date = str(datetime.today()).split()[0]

        return username, title, description, due_date, curr_date
        
    def view_all(self):

        # Print all tasks from the tasks property in a readable fashion 
        print('\n-----View all tasks-----')
        for task in self.tasks:
            print('\n-------------------------')
            print('Task:          '+str(task['title']))
            print('Assigned to:   '+str(task['username']))
            print('Date assigned: '+str(task['assigned_date']))
            print('Date due:      '+str(task['due_date']))
            print('Complete:      '+str(task['completed']))
            print('Task ID:       '+str(task['ID']))
            print('Description:   \n\n'+str(task['description']))
            print('\n-------------------------')

        # Return the user to the menu for further actions
        self.menu()

    def view_mine(self):

        # Print each task from the tasks property that is assigned to the current user
        print('\n-----View my tasks-----')
        self.tasks_for_current = []
        for task in self.tasks:
            if task['username'] == self.current_user:
                self.tasks_for_current.append(task['ID'])
                print('\n-------------------------')
                print('Task:          '+str(task['title']))
                print('Assigned to:   '+str(task['username']))
                print('Date assigned: '+str(task['assigned_date']))
                print('Date due:      '+str(task['due_date']))
                print('Complete:      '+str(task['completed']))
                print('Task ID:       '+str(task['ID']))
                print('Description:   \n\n'+str(task['description']))
                print('\n-------------------------')

        # Allow users with tasks to select a task for editing
        if not self.tasks_for_current:
            print('No tasks for current user')
            # If the user has no tasks they are returned to the menu for further actions
            self.menu()
        else:
            valid_task = False
            while valid_task == False:
                task_selected = input('To select a task enter a task ID, or enter -1 to return to the menu:')
                if task_selected == '-1':
                    print('Returning to menu...')
                    self.menu()
                elif task_selected.isnumeric() == False:
                    print('ERROR: Task ID must be numeric')
                    continue
                task_selected = int(task_selected)
                if task_selected not in self.tasks_for_current:
                    print('ERROR: Task not assigned to this user')
                    continue
                else:
                    valid_task = True

        # Take the user action to the necessary function
        self.task_edit_selection(task_selected)
        
    def task_edit_selection(self, task_id: int):

        print(f'\n-----Selected task: {task_id}-----')
        print('Action code:         Action')
        print('1:                   Return to menu')

        # Ensure that the task selected is not complete (as complete tasks should not be edited)
        for task in self.tasks:
            if task['ID'] == task_id:
                task_status = task['completed']
        if task_status == True:
            action = input('Enter action code:')
            while action != '1':
                print('ERROR: Invalid action code')
                action = input('Enter action code:')
            action = int(action)   
        else:
            print('2:                   Mark complete')
            print('3:                   Edit task')
            valid_action = False
            while valid_action == False:
                action = input('Enter action code:')
                if action.isnumeric() == False:
                    print('ERROR: Action code must be numeric')
                    continue
                action = int(action)
                if (action < 1) or (action > 3):
                    print('ERROR: Invalid action code')
                    continue
                else:
                    valid_action = True

        # Take the user action to the necessary function
        self.edit_task_action(task_id, action)

    def edit_task_action(self, task_id: int, action: int):

        if action == 1:
            self.menu()
        elif action == 2:
            self.set_task_complete(task_id)
        elif action == 3:
            self.edit_my_task(task_id)

    def set_task_complete(self, task_id):
        
        # Mark the selected task as complete in the task file
        # Credit for editing specific line of txt file: https://stackoverflow.com/questions/55030437/how-can-i-change-one-line-in-text-file-with-python
        with open('tasks.txt', 'r') as original_tasks, open('temporary_tasks.txt', 'w') as new_tasks:
            for task in original_tasks:
                if task_id == 0:
                    new_tasks.write(task[:-3]+'Yes\n')
                    task_id = -1
                else:
                    new_tasks.write(task)
                    task_id = task_id - 1

        os.remove('tasks.txt')
        os.rename('temporary_tasks.txt', 'tasks.txt')

        # Update the task property as tasks have been edited
        self.tasks = self.update_tasks()
        print('\n|-----------------|')
        print('|  Task complete  |')
        print('|-----------------|')

        # Return the user to the menu for further actions
        self.menu()
        
    def edit_my_task(self, task_id):

        print(f'\n-----Editing task {task_id}-----')
        print('Action code:         Action')
        print('1:                   Return to menu')
        print('2:                   Assign task to another user')
        print('3:                   Edit due date')

        # Ensure that the user has selected a valid action
        valid_action = False
        while valid_action == False:
            action = input('Enter action code:')
            if action.isnumeric() == False:
                print('ERROR: Action code must be numeric')
                continue
            action = int(action)
            if (action < 1) or (action > 3):
                print('ERROR: Invalid action code')
                continue
            else:
                valid_action = True

        # Take the user action to the necessary function
        self.edit_my_task_selection(task_id, action)

    def edit_my_task_selection(self, task_id: int, action: int):

        if action == 1:
            self.menu()
        elif action == 2:
            self.change_task_assignee(task_id)
        elif action == 3:
            self.change_task_due_date(task_id)

    def change_task_assignee(self, task_id):

        # Ensure that the user that the task will be re-assigned to exists
        print(f'\n-----Assign task: {task_id} to a different user-----')
        new_username = input('\nUsername of user to recieve task:')
        while new_username not in self.users:
            print('ERROR: Invalid username')
            new_username = input('Username of user to recieve task:')

        # Update the task in the task file
        # Credit for editing specific line of txt file: https://stackoverflow.com/questions/55030437/how-can-i-change-one-line-in-text-file-with-python
        with open('tasks.txt', 'r') as original_tasks, open('temporary_tasks.txt', 'w') as new_tasks:
            for task in original_tasks:
                if task_id == 0:
                    task_components = task.split(';')
                    new_task = (f'{new_username};{task_components[1]};{task_components[2]};{task_components[3]};{task_components[4]};{task_components[5]}')
                    new_tasks.write(new_task)
                    task_id = -1
                else:
                    new_tasks.write(task)
                    task_id = task_id - 1

        # Rename the temporary updated tasks file to tasks.txt
        os.remove('tasks.txt')
        os.rename('temporary_tasks.txt', 'tasks.txt')

        # Update the tasks property as tasks have changed
        self.tasks = self.update_tasks()
        print('\n|--------------------------------|')
        print('f|  Task {task_id} assigned to: {new_username}')
        print('|--------------------------------|')

        # Return the user to the menu for further actions
        self.menu()

    def change_task_due_date(self, task_id):

        # Ensure that the inputted date is a real date
        print(f'\n-----Change due date for task: {task_id}-----')
        new_date = input('\n Enter new due date as "YYYY-MM-DD":')
        while self.is_datetime_string(new_date) == False:
            print('ERROR: Incorrect input form')
            new_date = input('\n Enter new due date as "YYYY-MM-DD":')

        # Update the task in the task file
        # Credit for editing specific line of txt file: https://stackoverflow.com/questions/55030437/how-can-i-change-one-line-in-text-file-with-python
        with open('tasks.txt', 'r') as original_tasks, open('temporary_tasks.txt', 'w') as new_tasks:
            for task in original_tasks:
                if task_id == 0:
                    task_components = task.split(';')
                    print(task_components)
                    print(len(task_components))
                    new_task = (f'{task_components[0]};{task_components[1]};{task_components[2]};{new_date};{task_components[4]};{task_components[5]}')
                    new_tasks.write(new_task)
                    task_id = -1
                else:
                    new_tasks.write(task)
                    task_id = task_id - 1

        # Rename the temporary updated tasks file to tasks.txt
        os.remove('tasks.txt')
        os.rename('temporary_tasks.txt', 'tasks.txt')

        # Update the task property as tasks have changed
        self.tasks = self.update_tasks()
        print('\n|--------------------------------|')
        print(f'| Task {task_id} due date set to: {new_date}')
        print('|--------------------------------|')

        # Return the user to the menu for further actions
        self.menu()


    # Helper function to check if an inputted string is in datetime format
    def is_datetime_string(self, string): 

        # Credit for determining if a string is of the right form: https://stackoverflow.com/questions/63424175/determine-datetime-format-from-string
        try:
            datetime.strptime(string, DATETIME_STRING_FORMAT)
            return True
        except ValueError:
            return False
                            
    def generate_reports(self, helper: bool = False):

        # Use helper functions to generate usage reports to external text files
        self.reports_generated = True
        self.generate_task_overview()
        self.generate_user_overview()
        print('\n|---------------------|')
        print('|  Reports generated  |')
        print('|---------------------|')

        # This is to ensure that when this function is called by self.display_stats, it does not return to the menu
        if helper == False:
            # Return the user to the menu for further actions
            self.menu()
        
    def generate_task_overview(self):

        tasks_count = len(self.tasks)

        # Credit for getting todays date: https://stackoverflow.com/questions/32490629/getting-todays-date-in-yyyy-mm-dd-in-python
        curr_date = str(datetime.today()).split()[0]
        curr_date = datetime.strptime(curr_date, DATETIME_STRING_FORMAT)

        # Loop through each task in the tasks file to count the number of tasks complete, uncomplete, and overdue
        complete_count, uncomplete_count, overdue_count = 0, 0, 0
        with open('tasks.txt', 'r') as tasks_file:
            for task in tasks_file:
                task_components = task.split(';')
                if task_components[5] == 'Yes':
                    complete_count += 1
                else:
                    uncomplete_count += 1
                    due_date = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
                    if due_date > curr_date:
                        overdue_count += 1

        # Calculate percentages for report
        incomplete_percent = (uncomplete_count // tasks_count) * 100
        overdue_percent = (overdue_count // tasks_count) * 100
        
        # Use helper function to write the generated report
        self.write_task_overview(tasks_count, complete_count, uncomplete_count, overdue_count, incomplete_percent, overdue_percent)

    # Helper function to write the user report to an external file
    def write_task_overview(self, task_count, complete_count, uncomplete_count, overdue_count, incomplete_percent, overdue_percent):
        
        with open('task_overview.txt', 'w') as task_overview:
            task_overview.write(f'Total tasks:              {task_count}\n')
            task_overview.write(f'Complete tasks:           {complete_count}\n')
            task_overview.write(f'Incomplete tasks:         {uncomplete_count}\n')
            task_overview.write(f'Overdue tasks:            {overdue_count}\n')
            task_overview.write(f'Percentage incomplete:    {incomplete_percent}\n')
            task_overview.write(f'Percentage overdue:       {overdue_percent}\n')

    def generate_user_overview(self):

        total_tasks = len(self.tasks)

        # Credit for getting todays date: https://stackoverflow.com/questions/32490629/getting-todays-date-in-yyyy-mm-dd-in-python
        curr_date = str(datetime.today()).split()[0]
        curr_date = datetime.strptime(curr_date, DATETIME_STRING_FORMAT)

        # Loop through each task in the task file to count stats for the report
        tasks_count, complete_count, uncomplete_count, overdue_count = 0, 0, 0, 0
        with open('tasks.txt', 'r') as tasks_file:
            for task in tasks_file:
                task_components = task.split(';')
                if task_components[0] == self.current_user:
                    tasks_count += 1
                    if task_components[5] == 'Yes':
                        complete_count += 1
                    else:
                        uncomplete_count += 1
                        due_date = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
                        if due_date > curr_date:
                            overdue_count += 1
        
        # Calculate percentages for the report
        task_percent = (tasks_count // total_tasks) * 100
        complete_percent = (complete_count // tasks_count) * 100
        incomplete_percent = (uncomplete_count // tasks_count) * 100
        overdue_percent = (overdue_count // tasks_count) * 100

        # Use a helper function to write the report to an external file
        self.write_user_overview(tasks_count, task_percent, complete_percent, incomplete_percent, overdue_percent)

    # Helper function to write the user report to an external file
    def write_user_overview(self, task_count, task_percent, complete_percent, incomplete_percent, overdue_percent):

        with open('user_overview.txt', 'w') as user_overview:
            user_overview.write(f'{self.current_user} tasks:         {task_count}\n')
            user_overview.write(f'Percent of total tasks:   {task_percent}\n')
            user_overview.write(f'Percent of own complete:  {complete_percent}\n')
            user_overview.write(f'Percent of own incomplete:{incomplete_percent}\n')
            user_overview.write(f'Percent of own overdue:   {overdue_percent}\n')
        
    def display_stats(self):

        # Generate reports if not already done so that stats can be displayed
        if self.reports_generated == False:
            self.generate_reports(True)

        print('\n-----Task report-----')
        # Get the information stored in the task_overview.txt report
        with open('task_overview.txt', 'r') as task_report:
            for line in task_report:
                # Display each line of the task report as it is already formatted to a user friendly output
                print(line)

        print('\n-----User report-----')
        # Get the information stored in the user_overview.txt report
        with open('user_overview.txt', 'r') as user_report:
            for line in user_report:
                # Display each line of the task report as it is already formatted to a user friendly output
                print(line)

        # Return to the menu so further engagement with the program can continue
        self.menu()
            
# Create an instance of Task_manager to use the task manager
new = Task_manager()
