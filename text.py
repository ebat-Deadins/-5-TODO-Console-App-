import csv
from pathlib import Path
import os
import calendar
import datetime 

FILE_PATH = Path(__file__).parent / "tasks.csv"

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
PRIORITY_ICON = {"high": "🔴 HIGH  ", "medium": "🟡 MEDIUM", "low": "🟢 LOW   "}

# ✨ ADDED: ANSI color codes for the glowing today highlight
RESET = "\033[0m"
GLOW  = "\033[1;33;43m"  # Bold yellow text on yellow background

now = datetime.datetime.now()

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
                    "priority": row.get("priority", "low"),
                    "deadline": row.get("deadline", "")
                })
    except Exception as e:
        print(f"Error reading file: {e}")
    return tasks

def show_calendar(year, month):
    cal = calendar.monthcalendar(year, month)

    print(f"""
╔══════════════════════════════════╗
║        {calendar.month_name[month].upper()} {year}                ║
╠════╦════╦════╦════╦════╦════╦════╣
║ Mo ║ Tu ║ We ║ Th ║ Fr ║ Sa ║ Su ║
╠════╬════╬════╬════╬════╬════╬════╣""")
    for week in cal:
        row = ""
        for day in week:
            # ✨ CHANGED: added glow highlight for today's date
            if day != 0 and day == now.day and year == now.year and month == now.month:
                row += f"║{GLOW}{str(day).rjust(2)}✨{RESET}"
            else:
                row += f"║ {str(day).rjust(2) if day != 0 else '  '} "
        row += "║"
        print(row)
    print("╚════╩════╩════╩════╩════╩════╩════╝")

def save_tasks(tasks):
    with FILE_PATH.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "description", "is_done", "priority", "deadline"])
        writer.writeheader()
        for t in tasks:
            writer.writerow(t)


def add_task(description: str, priority: str, day: str):
    tasks = load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({
        "id": new_id,
        "description": description,
        "is_done": False,
        "priority": priority,
        "deadline": day
    })
    save_tasks(tasks)
    icon = PRIORITY_ICON[priority]
    print(f"✅ Task '{description}' [{icon}] added with ID: {new_id}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("\nYour task list is empty.")
        return

    tasks = sorted(tasks, key=lambda x: (
        x["id"],
        PRIORITY_ORDER.get(x["priority"], 2),
        x.get("deadline") or "9999-99-99",
        x["is_done"]
    ))

    print("\n" + "=" * 60)
    print(f"{'ID':<4} | {'PRIORITY':<10} | {'STATUS':<8} | {'DESCRIPTION'} | {'DEADLINE'}")
    print("-" * 60)
    for t in tasks:
        status = "✅ DONE " if t["is_done"] else "⬜      "
        icon = PRIORITY_ICON.get(t["priority"], "🟢 LOW   ")
        deadline = t.get("deadline") or "—"
        print(f"{t['id']:<4} | {icon} | {status} | {t['description']} | {deadline}")
    print("=" * 60)
    show_calendar(now.year, now.month)


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
    

def ask_calendar() -> str:
    print("\nChoose the month and day:")
    show_calendar(now.year, now.month)
    while True:
        day_input = input(f"Enter day (1-{calendar.monthrange(now.year, now.month)[1]}): ").strip()
        try:
            day = int(day_input)
            if 1 <= day <= calendar.monthrange(now.year, now.month)[1]:
                return f"{now.year}-{now.month:02d}-{day:02d}"
            else:
                print("❌ Invalid day. Please enter a valid day for this month.")
        except ValueError:
            print("❌ Please enter a number.")


def set_deadline(task_id: int):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            deadline = ask_calendar()
            t["deadline"] = deadline
            save_tasks(tasks)
            print(f"📅 Deadline for task {task_id} set to {deadline}.")
            return
    print(f"Task with ID {task_id} not found.")


def main_menu():
    while True:
        list_tasks()
        print("\n" + "=" * 30)
        print("1. Toggle Status (Check/Uncheck)")
        print("2. Add New Task")
        print("3. Delete Task")
        print("4. Set Deadline")
        print("0. Exit")
        print("=" * 30)
        choice = input("\nSelect an option: ").strip()    
        if choice == "1":
            try:
                tid = int(input("Enter Task ID: "))
                toggle_task(tid)
            except ValueError:
                print("Error: ID must be a number.")
        elif choice == "2":
            desc = input("Task description: ").strip()
            if desc:
                priority = select_priority()
                day = ask_calendar()
                add_task(desc, priority, day)
            else:
                print("Error: Description cannot be empty.")
        elif choice == "3":
            try:
                tid = int(input("Enter ID to delete: "))
                delete_task(tid)
            except ValueError:
                print("Error: ID must be a number.")
        elif choice == "4":
            try:
                tid = int(input("Enter Task ID to set deadline: "))
                set_deadline(tid)
            except ValueError:
                print("Error: ID must be a number.")
        elif choice == "0":
            print("Goodbye! 👋")
            os.system("cls" if os.name == "nt" else "clear")
            break
        else:
            print("Invalid selection. Please try again.")

def show_logo():
    os.system("cls" if os.name == "nt" else "clear")
    print("""
     ████████╗ ██████╗ ██████╗  ██████╗     ██╗     ██╗███████╗████████╗
     ╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗    ██║     ██║██╔════╝╚══██╔══╝
        ██║   ██║   ██║██║  ██║██║   ██║    ██║     ██║███████╗   ██║   
        ██║   ██║   ██║██║  ██║██║   ██║    ██║     ██║╚════██║   ██║   
        ██║   ╚██████╔╝██████╔╝╚██████╔╝    ███████╗██║███████║   ██║   
        ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝     ╚══════╝╚═╝╚══════╝   ╚═╝                                                                   
    """)


show_logo()
if __name__ == "__main__":
    main_menu()
