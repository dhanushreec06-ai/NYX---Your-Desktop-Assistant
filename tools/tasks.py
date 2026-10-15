import json
import os
from datetime import datetime
from tools.productivity import update_productivity_file

TASK_FILE = "data/tasks.json"


# ==================================================
# LOAD TASKS
# ==================================================

def load_tasks():

    if not os.path.exists(TASK_FILE):
        return []

    try:

        with open(TASK_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return []


# ==================================================
# SAVE TASKS
# ==================================================

def save_tasks(tasks):

    os.makedirs("data", exist_ok=True)

    with open(
        TASK_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            tasks,
            file,
            indent=4,
            ensure_ascii=False
        )
    tasks.append(new_task)

    save_tasks(tasks)

    update_productivity_file()

    return f"✅ Task added: {task}"

# ==================================================
# ADD TASK
# ==================================================

def add_task(task):

    task = str(task).strip()

    if not task:
        return "❌ Task cannot be empty."

    tasks = load_tasks()

    new_task = {
        "id": len(tasks) + 1,
        "task": task,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }

    tasks.append(new_task)

    save_tasks(tasks)

    return f"✅ Task added: {task}"


# ==================================================
# SHOW TASKS
# ==================================================

def show_tasks():

    tasks = load_tasks()

    if not tasks:
        return "📋 You have no tasks."

    result = "📋 NYX TASKS\n\n"

    for task in tasks:

        status = "✅" if task["status"] == "completed" else "⏳"

        result += (
            f"{status} "
            f"{task['id']}. "
            f"{task['task']}\n"
        )

    return result


# ==================================================
# COMPLETE TASK
# ==================================================

def complete_task(task_id):

    tasks = load_tasks()

    try:
        task_id = int(task_id)
    except ValueError:
        return "❌ Invalid task number."

    for task in tasks:

        if task["id"] == task_id:

            task["status"] = "completed"

            save_tasks(tasks)
           
            update_productivity_file()

            return (
                f"✅ Task completed: "
                f"{task['task']}"
            )

    return f"❌ Task {task_id} not found."


# ==================================================
# DELETE TASK
# ==================================================

def delete_task(task_id):

    tasks = load_tasks()

    try:
        task_id = int(task_id)
    except ValueError:
        return "❌ Invalid task number."

    for task in tasks:

        if task["id"] == task_id:

            deleted = task["task"]

            tasks.remove(task)

            save_tasks(tasks)
  
            update_productivity_file()

            return f"🗑️ Task deleted: {deleted}"

    return f"❌ Task {task_id} not found."