import csv
from pathlib import Path

# Файл хадгалах замыг тодорхойлох
FILE_PATH = Path(__file__).parent / "tasks.csv"

def load_tasks():
    """Файлаас даалгавруудыг уншиж жагсаалт хэлбэрээр буцаах"""
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
                    "is_done": row["is_done"] == "True"
                })
    except Exception as e:
        print(f"Файл уншихад алдаа гарлаа: {e}")
    return tasks

def save_tasks(tasks):
    """Жагсаалтыг CSV файл руу хадгалах"""
    with FILE_PATH.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "description", "is_done"])
        writer.writeheader()
        for t in tasks:
            writer.writerow(t)

def add_task(description: str):
    tasks = load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({"id": new_id, "description": description, "is_done": False})
    save_tasks(tasks)
    print(f"\n✅ “{description}” (ID: {new_id}) амжилттай нэмэгдлээ.")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("\n📭 Одоогоор даалгавар алга.")
        return

    # Дуусаагүйг нь эхэнд харуулахын тулд эрэмбэлэх
    tasks = sorted(tasks, key=lambda x: x["is_done"])
    
    print("\n--- ТАНЫ ДААЛГАВРУУД ---")
    print(f"{'ID':<4} | {'Төлөв':<6} | {'Тайлбар'}")
    print("-" * 35)
    for t in tasks:
        status_symbol = "✔" if t["is_done"] else "✗"
        print(f"{t['id']:<4} | {status_symbol:^6} | {t['description']}")

def toggle_task(task_id: int):
    tasks = load_tasks()
    found = False
    for t in tasks:
        if t["id"] == task_id:
            t["is_done"] = not t["is_done"]
            found = True
            state = "ДУУССАН" if t["is_done"] else "ДУУСААГҮЙ"
            print(f"\n🔄 ID {task_id} төлөв: {state}")
            break
    if found:
        save_tasks(tasks)
    else:
        print(f"\n❌ {task_id} дугаартай даалгавар олдсонгүй.")

def delete_task(task_id: int):
    tasks = load_tasks()
    filtered = [t for t in tasks if t["id"] != task_id]
    
    if len(tasks) == len(filtered):
        print(f"\n❌ {task_id} дугаартай даалгавар олдсонгүй.")
    else:
        save_tasks(filtered)
        print(f"\n🗑 ID {task_id} амжилттай устгагдлаа.")

def main_menu():
    while True:
        print("\n" + "="*25)
        print("   TODO CONSOLE APP")
        print("="*25)
        print("1. Жагсаалт харах")
        print("2. Статус өөрчлөх (Check/Uncheck)")
        print("3. Шинэ даалгавар нэмэх")
        print("4. Даалгавар устгах")
        print("0. Гарах")
        
        choice = input("\nСонголт: ").strip()
        
        if choice == "1":
            list_tasks()
        elif choice == "2":
            try:
                tid = int(input("Даалгаврын ID: "))
                toggle_task(tid)
            except ValueError:
                print("❗ Алдаа: ID тоо байх ёстой.")
        elif choice == "3":
            desc = input("Юу хийх вэ?: ").strip()
            if desc:
                add_task(desc)
            else:
                print("❗ Алдаа: Хоосон утга оруулж болохгүй.")
        elif choice == "4":
            try:
                tid = int(input("Устгах ID: "))
                delete_task(tid)
            except ValueError:
                print("❗ Алдаа: ID тоо байх ёстой.")
        elif choice == "0":
            print("Баяртай! Амжилт хүсэе.")
            break
        else:
            print("❗ Буруу сонголт. Дахин оролдоно уу.")

if __name__ == "__main__":
    main_menu()