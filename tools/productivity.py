import os
import subprocess
from datetime import datetime


TASK_FILE = "data/tasks.json"
REMINDER_FILE = "data/reminders.json"
PRODUCTIVITY_FILE = "data/NYX_Tasks.txt"


# ==================================================
# LOAD JSON FILE
# ==================================================

def load_json(file_path):

    if not os.path.exists(file_path):
        return []

    try:

        import json

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:
        return []


# ==================================================
# UPDATE NYX PRODUCTIVITY FILE
# ==================================================

def update_productivity_file():

    tasks = load_json(TASK_FILE)
    reminders = load_json(REMINDER_FILE)

    os.makedirs("data", exist_ok=True)

    now = datetime.now().strftime(
        "%d-%b-%Y %I:%M %p"
    )

    content = []

    content.append("=" * 50)
    content.append("                 NYX")
    content.append("            PRODUCTIVITY")
    content.append("=" * 50)

    # ==================================================
    # TASKS
    # ==================================================

    content.append("")
    content.append("📋 TASKS")
    content.append("-" * 50)

    if not tasks:

        content.append("No tasks.")

    else:

        for task in tasks:

            if task.get("status") == "completed":
                status = "✅"
            else:
                status = "⏳"

            content.append(
                f"{status} "
                f"{task.get('id')}. "
                f"{task.get('task')}"
            )


    # ==================================================
    # REMINDERS
    # ==================================================

    content.append("")
    content.append("⏰ REMINDERS")
    content.append("-" * 50)

    if not reminders:

        content.append("No reminders.")

    else:

        for reminder in reminders:

            if reminder.get("status") == "completed":
                status = "✅"
            else:
                status = "⏳"

            content.append(
                f"{status} "
                f"{reminder.get('id')}. "
                f"{reminder.get('reminder')}"
            )

            content.append(
                f"   🕐 {reminder.get('time')}"
            )


    # ==================================================
    # FOOTER
    # ==================================================

    content.append("")
    content.append("=" * 50)

    content.append(
        f"Last Updated: {now}"
    )

    content.append("=" * 50)

    with open(
        PRODUCTIVITY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(content)
        )

    return PRODUCTIVITY_FILE


# ==================================================
# OPEN PRODUCTIVITY FILE
# ==================================================

def open_productivity():

    file_path = update_productivity_file()

    try:

        subprocess.Popen([
            "notepad.exe",
            os.path.abspath(file_path)
        ])

        return "📋 NYX task list opened in Notepad."

    except Exception as e:

        return (
            f"❌ Could not open NYX task list: "
            f"{e}"
        )


# ==================================================
# SHOW PRODUCTIVITY
# ==================================================

def show_productivity():

    return open_productivity()


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    print(
        update_productivity_file()
    )

    print(
        open_productivity()
    )