import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("todo_data.json")

class Task:
    def __init__(self, title, priority="medium", deadline=None, completed=False):
        self.title = title
        self.priority = priority.lower()
        self.deadline = deadline
        self.completed = completed

    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "deadline": self.deadline,
            "completed": self.completed,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            title=data["title"],
            priority=data["priority"],
            deadline=data["deadline"],
            completed=data["completed"],
        )


class TodoList:
    def __init__(self):
        self.tasks = []
        self.load()

    def add_task(self, title, priority="medium", deadline=None):
        task = Task(title, priority, deadline)
        self.tasks.append(task)
        self.save()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save()

    def mark_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save()

    def sort_by_deadline(self):
        self.tasks.sort(key=lambda t: datetime.strptime(t.deadline, "%Y-%m-%d")
                        if t.deadline else datetime.max)

    def search(self, keyword):
        return [t for t in self.tasks if keyword.lower() in t.title.lower()]

    def save(self):
        with open(DATA_FILE, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4)

    def load(self):
        if DATA_FILE.exists():
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(d) for d in data]

    def show(self):
        if not self.tasks:
            print("\n📭 No tasks yet.")
            return

        print("\n===== YOUR TO-DO LIST =====")
        for i, task in enumerate(self.tasks):
            status = "✔ DONE" if task.completed else "❗ ACTIVE"
            deadline = f" | ⏰ {task.deadline}" if task.deadline else ""
            print(f"{i}. {task.title} | Priority: {task.priority}{deadline} | {status}")
        print("============================")


def menu():
    todo = TodoList()

    while True:
        print("""
===== TO-DO LIST MENU =====
1. Add task
2. Remove task
3. Mark task as done
4. Show tasks
5. Search tasks
6. Sort by deadline
0. Exit
""")
        choice = input("Select an option: ")

        if choice == "1":
            title = input("Task title: ")
            priority = input("Priority (low/medium/high): ").lower()
            deadline = input("Deadline (YYYY-MM-DD or leave blank): ")
            deadline = deadline if deadline.strip() else None
            todo.add_task(title, priority, deadline)
            print("Task added.")

        elif choice == "2":
            todo.show()
            idx = int(input("Task number to remove: "))
            todo.remove_task(idx)

        elif choice == "3":
            todo.show()
            idx = int(input("Task number to mark done: "))
            todo.mark_done(idx)

        elif choice == "4":
            todo.show()

        elif choice == "5":
            keyword = input("Search keyword: ")
            matches = todo.search(keyword)
            print("\n=== SEARCH RESULTS ===")
            for t in matches:
                print(f"- {t.title} (Priority: {t.priority})")
            if not matches:
                print("No matches found.")

        elif choice == "6":
            todo.sort_by_deadline()
            print("Tasks sorted by deadline.")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    menu()
