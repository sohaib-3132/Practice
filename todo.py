#This list holds all tasks for the current session only and each task is a dict w keys
todo_list = []

#Valid values allowed for each field (input validation)
VALID_PRIORITIES = ["low", "medium", "high"]
VALID_STATUSES = ["pending", "completed"]

# HELPER FUNCTIONS

def generate_task_id():
    # create new unique ID for a task.
    # max finds the highest existing ID, then adds 1 for new task.
    return max((t["id"] for t in todo_list), default=0) + 1


def find_task_by_id(task_id):
    #search todo list and return the first task dict which has same id to taskid, none if not found
    return next((t for t in todo_list if t["id"] == task_id), None)


def get_valid_input(prompt, valid_options=None):
    # tell the user write and validate the input.
    # if valid_options given, keep asking until a valid choice is entered.
    while True:
        user_input = input(prompt).strip().lower()
        if valid_options is None:
            if user_input != "":
                return user_input
            print("Input cannot be empty. Please try again.")
        elif user_input in valid_options:
            return user_input
        else:
            print(f"Invalid input. Please choose from {valid_options}.")


def get_int_input(prompt):
    # Ask for an integer and return it, or None if the input is invalid.
    try:
        return int(input(prompt))
    except ValueError:
        print("\n⚠️ Please enter a valid numeric ID.\n")
        return None


# ---------------------------------------------------
# CRUD FUNCTIONS
# ---------------------------------------------------

def create_task(title, description, priority):
    # Create a new task dict and add it to the list.
    # New tasks start with status 'pending'.
    new_task = {
        "id": generate_task_id(),
        "title": title,
        "description": description,
        "priority": priority,
        "status": "pending"
    }
    todo_list.append(new_task)
    print(f"\n✅ Task '{title}' created successfully with ID {new_task['id']}.\n")


def view_tasks():
    # Show all tasks to read, or a message if none exist.
    if not todo_list:
        print("\n📭 No tasks found. Your to-do list is empty.\n")
        return

    print("\n---------------- YOUR TASKS ----------------")
    for task in todo_list:
        print(f"ID: {task['id']}\nTitle: {task['title']}\nDescription: {task['description']}\nPriority: {task['priority']}\nStatus: {task['status']}\n---------------------------------------------")
    print()


def update_task(task_id, new_title=None, new_description=None,
                 new_priority=None, new_status=None):
    # Update the given fields of a task if the task exists.
    task = find_task_by_id(task_id)

    if task is None:
        print(f"\n⚠️ Task with ID {task_id} not found.\n")
        return

    for key, value in (("title", new_title),
                       ("description", new_description),
                       ("priority", new_priority),
                       ("status", new_status)):
        if value is not None:
            task[key] = value

    print(f"\n✅ Task with ID {task_id} updated successfully.\n")


def delete_task(task_id):
    # delete a task by ID and confirm, or warn if it is missing.
    task = find_task_by_id(task_id)

    if task is None:
        print(f"\n⚠️ Task with ID {task_id} not found.\n")
        return

    todo_list.remove(task)
    print(f"\n🗑️ Task with ID {task_id} deleted successfully.\n")


def mark_task_complete(task_id):
    # Mark the task as 'completed' if it exists.
    task = find_task_by_id(task_id)

    if task is None:
        print(f"\n⚠️ Task with ID {task_id} not found.\n")
        return

    task["status"] = "completed"
    print(f"\n🎯 Task with ID {task_id} marked as completed.\n")


# ---------------------------------------------------
# MENU / DISPLAY FUNCTIONS
# ---------------------------------------------------

def display_menu():
    # Print the main menu options for user.
    print("""========== TO-DO LIST MENU ==========
1. Create a new task
2. View all tasks
3. Update a task
4. Delete a task
5. Mark a task as completed
6. Exit
======================================""")


# ---------------------------------------------------
# MAIN PROGRAM LOOP
# ---------------------------------------------------

def main():
    # Main program loop: show menu and handle user choices until exit.
    print("\nWelcome to your Terminal To-Do List App!\n")

    while True:
        display_menu()
        choice = get_valid_input("Enter your choice (1-6): ",
                                  ["1", "2", "3", "4", "5", "6"])

        # ---- CREATE ----
        if choice == "1":
            title = get_valid_input("Enter task title: ")
            description = get_valid_input("Enter task description: ")
            priority = get_valid_input(
                f"Enter priority {VALID_PRIORITIES}: ", VALID_PRIORITIES
            )
            create_task(title, description, priority)

        # ---- VIEW ----
        elif choice == "2":
            view_tasks()

        # ---- UPDATE ----
        elif choice == "3":
            view_tasks()
            task_id = get_int_input("Enter the ID of the task to update: ")
            if task_id is None:
                continue

            print("Leave a field blank if you don't want to change it.")
            new_title = input("New title: ").strip() or None
            new_description = input("New description: ").strip() or None
            new_priority = input(f"New priority {VALID_PRIORITIES}: ").strip() or None
            new_status = input(f"New status {VALID_STATUSES}: ").strip() or None

            update_task(task_id, new_title, new_description,
                        new_priority, new_status)

        # ---- DELETE ----
        elif choice == "4":
            view_tasks()
            task_id = get_int_input("Enter the ID of the task to delete: ")
            if task_id is None:
                continue
            delete_task(task_id)

        # ---- MARK COMPLETE ----
        elif choice == "5":
            view_tasks()
            task_id = get_int_input("Enter the ID of the task to mark complete: ")
            if task_id is None:
                continue
            mark_task_complete(task_id)

        # ---- EXIT ----
        elif choice == "6":
            print("\n👋 Exiting the To-Do List App. All data will be cleared. Goodbye!\n")
            break
if __name__ == "__main__":
    main()