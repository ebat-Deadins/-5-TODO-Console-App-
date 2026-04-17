import csv
from pathlib import Path

FILE_PATH = Path(__file__).parent / "tasks.csv"

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
PRIORITY_ICON = {"high": "🔴 HIGH  ", "medium": "🟡 MEDIUM", "low": "🟢 LOW   "}


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
    icon = PRIORITY_ICON[priority]
    print(f"✅ Task '{description}' [{icon}] added with ID: {new_id}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("\nYour task list is empty.")
        return

    # Sort: Unfinished first → then High → Medium → Low
    tasks = sorted(tasks, key=lambda x: (x["is_done"], PRIORITY_ORDER.get(x["priority"], 2)))

    print("\n" + "=" * 60)
    print(f"{'ID':<4} | {'PRIORITY':<10} | {'STATUS':<8} | {'DESCRIPTION'}")
    print("-" * 60)
    for t in tasks:
        status = "✅ DONE " if t["is_done"] else "⬜      "
        icon = PRIORITY_ICON.get(t["priority"], "🟢 LOW   ")
        print(f"{t['id']:<4} | {icon} | {status} | {t['description']}")
    print("=" * 60)


def toggle_task(task_id: int):
    tasks = load_tasks()
    found = False
    for t in tasks:
        if t["id"] == task_id:
            t["is_done"] = not t["is_done"]
            found = True
            state = "DONE ✅" if t["is_done"] else "NOT DONE ⬜"
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


def select_priority() -> str:
    print("\nSelect Priority:")
    print("  1. 🔴 High   — Яаралтай хийх")
    print("  2. 🟡 Medium — Дараа хийх")
    print("  3. 🟢 Low    — Завтай үед")
    while True:
        p_input = input("Choice (1/2/3): ").strip()
        if p_input == "1":
            return "high"
        elif p_input == "2":
            return "medium"
        elif p_input == "3":
            return "low"
        else:
            print("❌ Зөвхөн 1, 2, эсвэл 3 оруулна уу!")


def main_menu():
    while True:
        print("\n" + "=" * 30)
        print("      TODO CONSOLE APP")
        print("=" * 30)
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
                priority = select_priority()
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
            print("Goodbye! 👋")
            break
        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main_menu()
