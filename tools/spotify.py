import os
import subprocess
import time
import pyautogui


# ==================================================
# FIND SPOTIFY
# ==================================================

def find_spotify():

    possible_paths = [

        # Microsoft Store / Windows installation
        os.path.expandvars(
            r"%APPDATA%\Spotify\Spotify.exe"
        ),

        # Normal installation
        r"C:\Users\Public\Spotify\Spotify.exe",

        # User installation
        os.path.expandvars(
            r"%LOCALAPPDATA%\Spotify\Spotify.exe"
        ),

        # Program Files
        r"C:\Program Files\Spotify\Spotify.exe",

        r"C:\Program Files (x86)\Spotify\Spotify.exe"
    ]

    for path in possible_paths:

        if os.path.exists(path):
            return path

    return None


# ==================================================
# OPEN SPOTIFY
# ==================================================

def open_spotify():

    try:

        spotify_path = find_spotify()

        # ------------------------------------------
        # If Spotify.exe is found
        # ------------------------------------------

        if spotify_path:

            subprocess.Popen(
                [spotify_path]
            )

            time.sleep(3)

            return "🎵 Spotify opened successfully."

        # ------------------------------------------
        # Try Windows Spotify URI
        # ------------------------------------------

        subprocess.Popen(
            [
                "explorer.exe",
                "spotify:"
            ]
        )

        time.sleep(3)

        return "🎵 Spotify opened successfully."

    except Exception as e:

        return f"❌ Could not open Spotify: {e}"


# ==================================================
# PLAY
# ==================================================

def spotify_play():

    try:

        pyautogui.press("playpause")

        return "▶️ Spotify playing."

    except Exception as e:

        return f"❌ Could not play Spotify: {e}"


# ==================================================
# PAUSE
# ==================================================

def spotify_pause():

    try:

        pyautogui.press("playpause")

        return "⏸️ Spotify paused."

    except Exception as e:

        return f"❌ Could not pause Spotify: {e}"


# ==================================================
# NEXT SONG
# ==================================================

def spotify_next():

    try:

        pyautogui.press("nexttrack")

        return "⏭️ Next Spotify song."

    except Exception as e:

        return f"❌ Could not change Spotify song: {e}"


# ==================================================
# PREVIOUS SONG
# ==================================================

def spotify_previous():

    try:

        pyautogui.press("prevtrack")

        return "⏮️ Previous Spotify song."

    except Exception as e:

        return f"❌ Could not change Spotify song: {e}"

def spotify_play(song=None):

    try:

        # ------------------------------------------
        # PLAY / RESUME CURRENT SONG
        # ------------------------------------------

        if not song:
            pyautogui.press("playpause")
            return "▶️ Spotify playing."

        song = song.strip()

        print(f"🔎 Searching Spotify for: {song}")

        # ------------------------------------------
        # Make sure Spotify is open
        # ------------------------------------------

        spotify_path = find_spotify()

        if spotify_path:
            subprocess.Popen([spotify_path])

        time.sleep(4)

        # ------------------------------------------
        # Bring Spotify window to foreground
        # ------------------------------------------

        powershell = r"""
        Add-Type @"
        using System;
        using System.Runtime.InteropServices;

        public class Win32 {
            [DllImport("user32.dll")]
            public static extern bool SetForegroundWindow(IntPtr hWnd);
        }
"@

        $process = Get-Process spotify -ErrorAction SilentlyContinue |
                   Where-Object {$_.MainWindowHandle -ne 0} |
                   Select-Object -First 1

        if ($process) {
            [Win32]::SetForegroundWindow($process.MainWindowHandle)
        }
        """

        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                powershell
            ],
            capture_output=True,
            text=True
        )

        time.sleep(2)

        # ------------------------------------------
        # Open Spotify search
        # ------------------------------------------

        pyautogui.hotkey("ctrl", "k")

        time.sleep(1)

        pyautogui.hotkey("ctrl", "a")

        pyautogui.write(
            song,
            interval=0.05
        )

        pyautogui.press("enter")

        time.sleep(4)

        # ------------------------------------------
        # Move from search box to first result
        # ------------------------------------------

        pyautogui.press("tab")

        time.sleep(0.5)

        pyautogui.press("down")

        time.sleep(0.5)

        pyautogui.press("enter")

        time.sleep(3)

        return f"🎵 Playing {song} on Spotify."

    except Exception as e:

        return f"❌ Could not play {song}: {e}"


    

        
      
        

# ==================================================
# STOP
# ==================================================

def spotify_stop():

    try:

        pyautogui.press("playpause")

        return "⏹️ Spotify playback stopped."

    except Exception as e:

        return f"❌ Could not stop Spotify: {e}"


  
# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    print(open_spotify())