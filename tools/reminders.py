import json
import os
from datetime import datetime
from tools.productivity import update_productivity_file

REMINDER_FILE = "data/reminders.json"


# ==================================================
# LOAD REMINDERS
# ==================================================

def load_reminders():

    if not os.path.exists(REMINDER_FILE):
        return []

    try:
        with open(
            REMINDER_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return []


# ==================================================
# SAVE REMINDERS
# ==================================================

def save_reminders(reminders):

    os.makedirs("data", exist_ok=True)

    with open(
        REMINDER_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            reminders,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==================================================
# ADD REMINDER
# ==================================================

def add_reminder(reminder, reminder_time):

    reminder = str(reminder).strip()
    reminder_time = str(reminder_time).strip()

    if not reminder:
        return "❌ Reminder cannot be empty."

    if not reminder_time:
        return "❌ Reminder time is missing."

    reminders = load_reminders()

    new_reminder = {
        "id": len(reminders) + 1,
        "reminder": reminder,
        "time": reminder_time,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }

    reminders.append(new_reminder)

    save_reminders(reminders)

    update_productivity_file()

    return (
        f"⏰ Reminder added:\n"
        f"📝 {reminder}\n"
        f"🕐 {reminder_time}"
    )


# ==================================================
# SHOW REMINDERS
# ==================================================

def show_reminders():

    reminders = load_reminders()

    if not reminders:
        return "⏰ You have no reminders."

    result = "⏰ NYX REMINDERS\n\n"

    for reminder in reminders:

        status = (
            "✅"
            if reminder["status"] == "completed"
            else "⏳"
        )

        result += (
            f"{status} "
            f"{reminder['id']}. "
            f"{reminder['reminder']}\n"
            f"   🕐 {reminder['time']}\n"
        )

    return result


# ==================================================
# COMPLETE REMINDER
# ==================================================

def complete_reminder(reminder_id):

    reminders = load_reminders()

    try:
        reminder_id = int(reminder_id)

    except ValueError:
        return "❌ Invalid reminder number."

    for reminder in reminders:

        if reminder["id"] == reminder_id:

            reminder["status"] = "completed"

            save_reminders(reminders)

            update_productivity_file()

            return (
                f"✅ Reminder completed: "
                f"{reminder['reminder']}"
            )

    return f"❌ Reminder {reminder_id} not found."


# ==================================================
# DELETE REMINDER
# ==================================================

def delete_reminder(reminder_id):

    reminders = load_reminders()

    try:
        reminder_id = int(reminder_id)

    except ValueError:
        return "❌ Invalid reminder number."

    for reminder in reminders:

        if reminder["id"] == reminder_id:

            deleted = reminder["reminder"]

            reminders.remove(reminder)

            save_reminders(reminders)

            update_productivity_file()

            return f"🗑️ Reminder deleted: {deleted}"

    return f"❌ Reminder {reminder_id} not found."