import os
import subprocess
import webbrowser


# --------------------------------------------------
# Browser locations
# --------------------------------------------------

BROWSER_PATHS = {
    "chrome": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ],

    "edge": [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ],

    "firefox": [
        r"C:\Program Files\Mozilla Firefox\firefox.exe",
        r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
    ],

    "brave": [
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
    ]
}


# --------------------------------------------------
# Find browser
# --------------------------------------------------

def find_browser(browser_name):

    browser_name = browser_name.lower()

    if browser_name not in BROWSER_PATHS:
        return None

    for path in BROWSER_PATHS[browser_name]:

        if os.path.exists(path):
            return path

    return None


# --------------------------------------------------
# Open URL
# --------------------------------------------------

def open_url(url, browser=None):

    # ----------------------------------------------
    # No browser specified
    # Use Windows default browser
    # ----------------------------------------------

    if browser is None:

        print("🌐 Opening using default browser...")

        webbrowser.open(url)

        return True


    # ----------------------------------------------
    # Find requested browser
    # ----------------------------------------------

    browser = browser.lower()

    browser_path = find_browser(browser)


    # ----------------------------------------------
    # Browser not found
    # ----------------------------------------------

    if browser_path is None:

        print(f"❌ {browser.title()} is not installed.")

        print("🌐 Opening using default browser...")

        webbrowser.open(url)

        return False


    # ----------------------------------------------
    # Launch browser
    # ----------------------------------------------

    try:

        subprocess.Popen([
            browser_path,
            url
        ])

        print(f"🌐 Opening {url}")
        print(f"🖥️ Browser: {browser.title()}")

        return True

    except Exception as e:

        print(f"❌ Failed to open {browser.title()}")
        print(f"Error: {e}")

        return False

