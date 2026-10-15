import time
import pyautogui
from urllib.parse import quote_plus

from tools.web_manager import open_website


# ==================================================
# YOUTUBE SEARCH + PLAY FIRST VIDEO
# ==================================================

def youtube_play_search(query, browser=None):

    try:

        if not query:
            return "❌ Please tell me what you want to watch."

        query = query.strip()

        print(f"🔎 Searching YouTube for: {query}")

        # ------------------------------------------
        # Create YouTube search URL
        # ------------------------------------------

        search_url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(query)
        )

        # ------------------------------------------
        # Open YouTube search
        # ------------------------------------------

        success = open_website(
            search_url,
            browser
        )

        if not success:
            return "❌ Could not open YouTube."

        # Wait for YouTube results
        time.sleep(5)

        # ------------------------------------------
        # Maximize browser
        # ------------------------------------------

        pyautogui.hotkey("alt", "space")
        time.sleep(0.5)

        pyautogui.press("x")
        time.sleep(1)

        # ------------------------------------------
        # Click first video result
        # ------------------------------------------

        screen_width, screen_height = pyautogui.size()

        # First YouTube result is normally
        # around the upper-middle part of the page.

        x = int(screen_width * 0.38)
        y = int(screen_height * 0.30)

        print("🎬 Selecting first YouTube video...")

        pyautogui.click(x, y)

        # Wait for video page
        time.sleep(5)

        # ------------------------------------------
        # Give video player focus
        # ------------------------------------------

        x = screen_width // 2
        y = int(screen_height * 0.45)

        pyautogui.click(x, y)

        time.sleep(1)

        # ------------------------------------------
        # Play video
        # ------------------------------------------

        pyautogui.press("k")

        print("▶️ YouTube video playing.")

        return (
            f"▶️ Playing first YouTube result for: "
            f"{query}"
        )

    except Exception as e:

        return f"❌ YouTube play failed: {e}"


# ==================================================
# OPEN YOUTUBE
# ==================================================

def open_youtube(target=None):

    try:

        browser = None

        if isinstance(target, dict):
            browser = target.get("browser")

        elif isinstance(target, str):
            browser = target

        success = open_website(
            "https://www.youtube.com",
            browser
        )

        if success:

            time.sleep(3)

            return "▶️ YouTube opened successfully."

        return "❌ Could not open YouTube."

    except Exception as e:

        return f"❌ Could not open YouTube: {e}"


# ==================================================
# PLAY / PAUSE
# ==================================================

def youtube_play(target=None):

    try:

        pyautogui.press("k")

        return "▶️ YouTube playing."

    except Exception as e:

        return f"❌ Could not play YouTube: {e}"


def youtube_pause(target=None):

    try:

        pyautogui.press("k")

        return "⏸️ YouTube paused."

    except Exception as e:

        return f"❌ Could not pause YouTube: {e}"


# ==================================================
# NEXT VIDEO
# ==================================================

def youtube_next(target=None):

    try:

        pyautogui.hotkey("shift", "n")

        time.sleep(2)

        return "⏭️ Next YouTube video."

    except Exception as e:

        return f"❌ Could not move to next video: {e}"


# ==================================================
# PREVIOUS VIDEO
# ==================================================

def youtube_previous(target=None):

    try:

        pyautogui.hotkey("shift", "p")

        time.sleep(2)

        return "⏮️ Previous YouTube video."

    except Exception as e:

        return f"❌ Could not move to previous video: {e}"


# ==================================================
# OPEN SHORTS
# ==================================================

def youtube_shorts(target=None):

    try:

        browser = None

        if isinstance(target, dict):
            browser = target.get("browser")

        elif isinstance(target, str):
            browser = target

        success = open_website(
            "https://www.youtube.com/shorts",
            browser
        )

        if not success:
            return "❌ Could not open YouTube Shorts."

        time.sleep(5)

        return "📱 YouTube Shorts opened."

    except Exception as e:

        return f"❌ Could not open Shorts: {e}"


# ==================================================
# SHORTS PLAY / PAUSE
# ==================================================

def youtube_short_play(target=None):

    try:

        pyautogui.press("k")

        return "▶️ Short playing."

    except Exception as e:

        return f"❌ Could not play Short: {e}"


def youtube_short_pause(target=None):

    try:

        pyautogui.press("k")

        return "⏸️ Short paused."

    except Exception as e:

        return f"❌ Could not pause Short: {e}"


# ==================================================
# NEXT SHORT
# ==================================================

def youtube_next_short(target=None):

    try:

        pyautogui.press("down")

        time.sleep(1)

        return "⏭️ Next Short."

    except Exception as e:

        return f"❌ Could not move to next Short: {e}"


# ==================================================
# PREVIOUS SHORT
# ==================================================

def youtube_previous_short(target=None):

    try:

        pyautogui.press("up")

        time.sleep(1)

        return "⏮️ Previous Short."

    except Exception as e:

        return f"❌ Could not move to previous Short: {e}"