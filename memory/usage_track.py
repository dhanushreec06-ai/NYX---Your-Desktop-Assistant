import json
import os
from datetime import datetime


HISTORY_FILE = "data/usage_history.json"


# ==================================================
# LOAD MEMORY
# ==================================================

def load_history():

    if not os.path.exists(HISTORY_FILE):
        return {
            "services": {},
            "browsers": {}
        }

    try:

        with open(HISTORY_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return {
            "services": {},
            "browsers": {}
        }


# ==================================================
# SAVE MEMORY
# ==================================================

def save_history(history):

    os.makedirs("data", exist_ok=True)

    with open(HISTORY_FILE, "w") as file:

        json.dump(
            history,
            file,
            indent=4
        )


# ==================================================
# RECORD SERVICE USAGE
# ==================================================

def record_service_usage(service, target):

    service = service.lower().strip()
    target = target.lower().strip()

    history = load_history()

    if "services" not in history:
        history["services"] = {}

    if service not in history["services"]:

        history["services"][service] = {}

    if target not in history["services"][service]:

        history["services"][service][target] = {
            "count": 0,
            "last_used": None
        }

    history["services"][service][target]["count"] += 1

    history["services"][service][target]["last_used"] = (
        datetime.now().isoformat()
    )

    save_history(history)

    print(
        f"🧠 NYX Memory: "
        f"{service.title()} → "
        f"{target.title()} "
        f"({history['services'][service][target]['count']} use)"
    )


# ==================================================
# GET MOST PREFERRED SERVICE TARGET
# ==================================================

def get_preferred_service_target(service):

    service = service.lower().strip()

    history = load_history()

    services = history.get("services", {})

    if service not in services:
        return None

    targets = services[service]

    if not targets:
        return None

    # Highest count first.
    # If counts are equal, most recently used wins.

    preferred = max(
        targets,
        key=lambda target: (
            targets[target]["count"],
            targets[target]["last_used"] or ""
        )
    )

    return preferred


# ==================================================
# RECORD BROWSER
# ==================================================

def record_browser(browser):

    browser = browser.lower().strip()

    history = load_history()

    if "browsers" not in history:
        history["browsers"] = {}

    if browser not in history["browsers"]:

        history["browsers"][browser] = {
            "count": 0,
            "last_used": None
        }

    history["browsers"][browser]["count"] += 1

    history["browsers"][browser]["last_used"] = (
        datetime.now().isoformat()
    )

    save_history(history)


# ==================================================
# OLD FUNCTION — KEPT FOR COMPATIBILITY
# ==================================================

def get_most_used_browser():

    history = load_history()

    browsers = history.get("browsers", {})

    if not browsers:
        return None

    return max(
        browsers,
        key=lambda browser: (
            browsers[browser]["count"],
            browsers[browser]["last_used"] or ""
        )
    )


# ==================================================
# SHOW MEMORY
# ==================================================

def show_usage():

    history = load_history()

    print("\n==============================")
    print("🧠 NYX MEMORY")
    print("==============================")

    services = history.get("services", {})

    if not services:

        print("No service history yet.")

    else:

        for service, targets in services.items():

            print(f"\n{service.title()}:")

            for target, data in targets.items():

                print(
                    f"   {target.title()} → "
                    f"{data['count']} time(s)"
                )

    print("\n==============================")

    browsers = history.get("browsers", {})

    if browsers:

        print("🌐 Browser Usage:")

        for browser, data in browsers.items():

            print(
                f"   {browser.title()} → "
                f"{data['count']} time(s)"
            )

    print("==============================")


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    record_service_usage(
        "whatsapp",
        "chrome"
    )

    record_service_usage(
        "whatsapp",
        "chrome"
    )

    record_service_usage(
        "whatsapp",
        "edge"
    )

    print(
        "\nPreferred WhatsApp:",
        get_preferred_service_target("whatsapp")
    )

    show_usage()