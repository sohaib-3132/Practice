# This list holds all tasks for the current session only.
# Each task is a dictionary with keys: id, title, description, priority, status
todo_list = []

# Valid values allowed for certain fields (used for input validation)
VALID_PRIORITIES = ["low", "medium", "high"]
VALID_STATUSES = ["pending", "completed"]

# HELPER FUNCTIONS

def generate_task_id():
    """
    Generates a new unique ID for a task.
    Uses max with a generator and default=0 so empty list -> start from 1.
    """
    return max((t["id"] for t in todo_list), default=0) + 1


def find_task_by_id(task_id):
    """
    Searches todo_list for a task matching the given task_id.
    Returns the task dictionary if found, otherwise returns None.
    """
    return next((t for t in todo_list if t["id"] == task_id), None)


def get_valid_input(prompt, valid_options=None):
    """
    Takes user input and validates it.
    If valid_options is provided, keeps asking until input matches one of them.
    Prevents crashes/invalid data from entering the system.
    """
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
    """
    Prompt for integer input. Returns int or None if invalid.
    """
    try:
        return int(input(prompt))
    except ValueError:
        print("\n⚠️ Please enter a valid numeric ID.\n")
        return None


# ---------------------------------------------------
# CRUD FUNCTIONS
# ---------------------------------------------------

def create_task(title, description, priority):
    """
    Creates a new task and adds it to todo_list.
    Parameters:
        title (str): short name of the task
        description (str): details about the task
        priority (str): 'low', 'medium', or 'high'
    New tasks always start with status = 'pending'.
    """
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
    """
    Displays all tasks currently in todo_list in a readable format.
    Shows a message if there are no tasks yet.
    """
    if not todo_list:
        print("\n📭 No tasks found. Your to-do list is empty.\n")
        return

    print("\n---------------- YOUR TASKS ----------------")
    for task in todo_list:
        print(f"ID: {task['id']}\nTitle: {task['title']}\nDescription: {task['description']}\nPriority: {task['priority']}\nStatus: {task['status']}\n---------------------------------------------")
    print()


def update_task(task_id, new_title=None, new_description=None,
                 new_priority=None, new_status=None):
    """
    Updates fields of an existing task identified by task_id.
    Only updates the fields that are provided (not None).
    Leaves other fields unchanged.
    """
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
    """
    Deletes a task from todo_list based on its task_id.
    Prints a confirmation message or an error if not found.
    """
    task = find_task_by_id(task_id)

    if task is None:
        print(f"\n⚠️ Task with ID {task_id} not found.\n")
        return

    todo_list.remove(task)
    print(f"\n🗑️ Task with ID {task_id} deleted successfully.\n")


def mark_task_complete(task_id):
    """
    Shortcut function to mark a task's status as 'completed'.
    Reuses find_task_by_id() to locate the task.
    """
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
    """
    Prints the main menu options for the user.
    """
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
    """
    Main entry point of the program.
    Runs an infinite loop showing the menu and handling user choices
    until the user selects 'Exit'.
    """
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