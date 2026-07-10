import sqlite3

# Valid values allowed for each field (input validation)
VALID_PRIORITIES = ["low", "medium", "high"]
VALID_STATUSES = ["pending", "completed"]
DB_NAME = "todo.db"


# ---------------------------------------------------
# DATABASE SETUP & CONNECTION HELPERS
# ---------------------------------------------------

def get_db_connection():
    """
    Establishes a connection to the SQLite database.
    Configures row_factory to access columns by name like a dictionary.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Creates the 'tasks' table automatically if it doesn't exist yet.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()


def generate_task_id():
    """
    Returns the next available task ID based on the highest existing row.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM tasks")
    result = cursor.fetchone()[0]
    conn.close()
    return (result or 0) + 1


def find_task_by_id(task_id):
    """
    Queries the database for a single task matching the given task_id.
    Returns the Row object if found, otherwise returns None.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task


def get_valid_input(prompt, valid_options=None):
    """
    Takes user input and validates it.
    If valid_options is provided, keeps asking until input matches one of them.
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
    Creates a new task and inserts it into the SQLite tasks table.
    """
    new_task_id = generate_task_id()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (id, title, description, priority, status) VALUES (?, ?, ?, ?, 'pending')",
        (new_task_id, title, description, priority)
    )
    conn.commit()
    conn.close()
    print(f"\n✅ Task '{title}' created successfully with ID {new_task_id}.\n")


def view_tasks():
    """
    Fetches and displays all tasks currently stored in the SQLite database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        print("\n📭 No tasks found. Your to-do DB is empty.\n")
        return

    print("\n---------------- YOUR TASKS ----------------")
    for task in tasks:
        print(
            f"ID: {task['id']}\n"
            f"Title: {task['title']}\n"
            f"Description: {task['description']}\n"
            f"Priority: {task['priority']}\n"
            f"Status: {task['status']}\n"
            f"---------------------------------------------"
        )
    print()


def update_task(task_id, new_title=None, new_description=None,
                 new_priority=None, new_status=None):
    """
    Updates the specified fields of an existing task identified by task_id.
    """
    task = find_task_by_id(task_id)

    if task is None:
        print(f"\n⚠️ Task with ID {task_id} not found.\n")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    if new_title is not None:
        cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_title, task_id))
    if new_description is not None:
        cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", (new_description, task_id))
    if new_priority is not None:
        cursor.execute("UPDATE tasks SET priority = ? WHERE id = ?", (new_priority, task_id))
    if new_status is not None:
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))

    conn.commit()
    conn.close()
    print(f"\n✅ Task with ID {task_id} updated successfully.\n")


def delete_task(task_id):
    """
    Deletes a specific row matching the given task_id from the database.
    """
    task = find_task_by_id(task_id)

    if task is None:
        print(f"\n⚠️ Task with ID {task_id} not found.\n")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"\n🗑️ Task with ID {task_id} deleted successfully.\n")


def mark_task_complete(task_id):
    """
    Shortcut function to immediately set a specific task's status to 'completed'.
    """
    task = find_task_by_id(task_id)

    if task is None:
        print(f"\n⚠️ Task with ID {task_id} not found.\n")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"\n🎯 Task with ID {task_id} marked as completed.\n")


# ---------------------------------------------------
# MENU / DISPLAY FUNCTIONS
# ---------------------------------------------------

def display_menu():
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
    init_db()
    print("\nWelcome to your Terminal To-Do List App!\n")

    while True:
        display_menu()
        choice = get_valid_input("Enter your choice (1-6): ",
                                  ["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            title = get_valid_input("Enter task title: ")
            description = get_valid_input("Enter task description: ")
            priority = get_valid_input(
                f"Enter priority {VALID_PRIORITIES}: ", VALID_PRIORITIES
            )
            create_task(title, description, priority)

        elif choice == "2":
            view_tasks()

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

        elif choice == "4":
            view_tasks()
            task_id = get_int_input("Enter the ID of the task to delete: ")
            if task_id is None:
                continue
            delete_task(task_id)

        elif choice == "5":
            view_tasks()
            task_id = get_int_input("Enter the ID of the task to mark complete: ")
            if task_id is None:
                continue
            mark_task_complete(task_id)

        elif choice == "6":
            print("\n👋 Exiting the To-Do List App. All your updates have been saved to the database. Goodbye!\n")
            break

if __name__ == "__main__":
    main()