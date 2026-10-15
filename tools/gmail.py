import time
import pyautogui

from tools.web_manager import open_website


# ==================================================
# OPEN GMAIL
# ==================================================

def open_gmail(target=None):

    try:

        browser = None

        if isinstance(target, dict):
            browser = target.get("browser")

        elif isinstance(target, str):
            browser = target

        success = open_website(
            "https://mail.google.com",
            browser
        )

        if success:

            time.sleep(4)

            return "📧 Gmail opened successfully."

        return "❌ Could not open Gmail."

    except Exception as e:

        return f"❌ Gmail opening failed: {e}"


# ==================================================
# COMPOSE EMAIL
# ==================================================

def gmail_compose(target):

    try:

        if not isinstance(target, dict):

            return "❌ Email information is missing."

        recipient = target.get("to")
        subject = target.get("subject", "")
        body = target.get("body", "")

        if not recipient:

            return "❌ Recipient email address is missing."

        # ------------------------------------------
        # Make sure Gmail is active
        # ------------------------------------------

        time.sleep(2)

        # ------------------------------------------
        # Click Compose
        # ------------------------------------------

        pyautogui.click(100, 170)

        time.sleep(2)

        # ------------------------------------------
        # Recipient
        # ------------------------------------------

        pyautogui.write(
            recipient,
            interval=0.02
        )

        pyautogui.press("enter")

        time.sleep(1)

        # ------------------------------------------
        # Subject
        # ------------------------------------------

        pyautogui.press("tab")

        pyautogui.write(
            subject,
            interval=0.02
        )

        # ------------------------------------------
        # Body
        # ------------------------------------------

        pyautogui.press("tab")

        pyautogui.write(
            body,
            interval=0.01
        )

        return (
            "📧 Email draft prepared successfully.\n"
            f"To: {recipient}\n"
            f"Subject: {subject}\n\n"
            "⚠️ Email has NOT been sent."
        )

    except Exception as e:

        return f"❌ Could not prepare email: {e}"


# ==================================================
# SEND EMAIL
# ==================================================

def gmail_send(target=None):

    try:

        # Gmail compose window must already be open

        time.sleep(1)

        # Send button is normally near the bottom-left
        # of the compose window.

        pyautogui.hotkey(
            "ctrl",
            "enter"
        )

        time.sleep(2)

        return "📨 Email sent successfully."

    except Exception as e:

        return f"❌ Could not send email: {e}"