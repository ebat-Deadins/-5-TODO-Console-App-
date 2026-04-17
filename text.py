import csv
from pathlib import Path

FILE_PATH = Path(_file_).parent / "tasks.csv"

def load_tasks():
    tasks = []
    if not FILE_PATH.exists():
        return tasks
    
    try:
        with FILE_PATH.open(mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tasks.append({
                    "id": int(row["id"]),
                    "description": row["description"],
                    "is_done": row["is_done"] == "True",
                    "priority": row.get("priority", "low")
                })
    except Exception as e:
        print(f"Error reading file: {e}")
    return tasks

def save_tasks(tasks):
    with FILE_PATH.open(mode="w", encoding="utf-8", newline="") as f:
        # Added 'priority' to the fieldnames
        writer = csv.DictWriter(f, fieldnames=["id", "description", "is_done", "priority"])
        writer.writeheader()
        for t in tasks:
            writer.writerow(t)

def add_task(description: str, priority: str):
    tasks = load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({
        "id": new_id, 
        "description": description, 
        "is_done": False, 
        "priority": priority
    })
    save_tasks(tasks)
    print(f"Task '{description}' (Priority: {priority}) added with ID: {new_id}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("\nYour task list is empty.")
        return

    # Sort logic: Unfinished tasks first, then High priority before Low priority
    tasks = sorted(tasks, key=lambda x: (x["is_done"], x["priority"] != "high"))
    
    print("\n--- YOUR TASKS ---")
    print(f"{'ID':<4} | {'PRIORITY':<8} | {'STATUS':<8} | {'DESCRIPTION'}")
    print("-" * 55)
    for t in tasks:
        status = "[DONE]" if t["is_done"] else "[ ]"
        p_label = t["priority"].upper()
        print(f"{t['id']:<4} | {p_label:<8} | {status:<8} | {t['description']}")

def toggle_task(task_id: int):
    tasks = load_tasks()
    found = False
    for t in tasks:
        if t["id"] == task_id:
            t["is_done"] = not t["is_done"]
            found = True
            state = "DONE" if t["is_done"] else "NOT DONE"
            print(f"Task {task_id} marked as {state}.")
            break
    if found:
        save_tasks(tasks)
    else:
        print(f"Task with ID {task_id} not found.")

def delete_task(task_id: int):
    tasks = load_tasks()
    filtered = [t for t in tasks if t["id"] != task_id]
    
    if len(tasks) == len(filtered):
        print(f"Task with ID {task_id} not found.")
    else:
        save_tasks(filtered)
        print(f"Task {task_id} deleted successfully.")

def main_menu():
    while True:
        print("\n" + "="*30)
        print("      TODO CONSOLE APP")
        print("="*30)
        print("1. View Tasks")
        print("2. Toggle Status (Check/Uncheck)")
        print("3. Add New Task")
        print("4. Delete Task")
        print("0. Exit")
        
        choice = input("\nSelect an option: ").strip()
        
        if choice == "1":
            list_tasks()
        elif choice == "2":
            try:
                tid = int(input("Enter Task ID: "))
                toggle_task(tid)
            except ValueError:
                print("Error: ID must be a number.")
        elif choice == "3":
            desc = input("Task description: ").strip()
            if desc:
                print("Select Priority:")
                print("1. High")
                print("2. Low")
                p_input = input("Choice (1 or 2): ").strip()
                priority = "high" if p_input == "1" else "low"
                add_task(desc, priority)
            else:
                print("Error: Description cannot be empty.")
        elif choice == "4":
            try:
                tid = int(input("Enter ID to delete: "))
                delete_task(tid)
            except ValueError:
                print("Error: ID must be a number.")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid selection. Please try again.")

if _name_ == "_main_":
    main_menu()
