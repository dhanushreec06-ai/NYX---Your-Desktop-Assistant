import os
import subprocess


# ==================================================
# OPEN WINDOWS APPLICATION
# ==================================================

def find_and_open_app(app_name):

    app_name = app_name.strip()

    print(f"🔎 Searching Windows for: {app_name}")

    powershell_command = f"""
    $app = Get-StartApps | Where-Object {{
        $_.Name -like '*{app_name}*'
    }} | Select-Object -First 1

    if ($app) {{
        Write-Output $app.AppID
    }}
    """

    try:

        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                powershell_command
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        app_id = result.stdout.strip()

        if not app_id:

            return f"❌ Could not find application: {app_name}"

        print(f"✅ Found application: {app_name}")

        subprocess.Popen(
            [
                "explorer.exe",
                f"shell:AppsFolder\\{app_id}"
            ]
        )

        return f"✅ {app_name} opened successfully."

    except Exception as e:

        return f"❌ Failed to open {app_name}: {e}"


# ==================================================
# OPEN FOLDER
# ==================================================

def open_folder(folder_name):

    folder_name = folder_name.strip().lower()

    home = os.path.expanduser("~")

    folders = {

        "downloads": os.path.join(home, "Downloads"),

        "documents": os.path.join(home, "Documents"),

        "desktop": os.path.join(home, "Desktop"),

        "pictures": os.path.join(home, "Pictures"),

        "videos": os.path.join(home, "Videos"),

        "music": os.path.join(home, "Music"),

        "movies": os.path.join(home, "Movies")
    }

    folder_path = folders.get(folder_name)

    # If folder is not in our known list
    if folder_path is None:

        # Try user's exact folder name
        folder_path = os.path.join(home, folder_name)

    if not os.path.exists(folder_path):

        return f"❌ Folder not found: {folder_name}"

    try:

        os.startfile(folder_path)

        print(f"📁 Opening folder: {folder_path}")

        return f"✅ {folder_name.title()} opened successfully."

    except Exception as e:

        return f"❌ Failed to open folder: {e}"


# ==================================================
# LIST FILES
# ==================================================

def list_files(folder_name):

    folder_name = folder_name.strip().lower()

    home = os.path.expanduser("~")

    folders = {

        "downloads": os.path.join(home, "Downloads"),

        "documents": os.path.join(home, "Documents"),

        "desktop": os.path.join(home, "Desktop"),

        "pictures": os.path.join(home, "Pictures"),

        "videos": os.path.join(home, "Videos"),

        "music": os.path.join(home, "Music"),

        "movies": os.path.join(home, "Movies")
    }

    folder_path = folders.get(folder_name)

    if folder_path is None:

        folder_path = os.path.join(home, folder_name)

    if not os.path.exists(folder_path):

        return f"❌ Folder not found: {folder_name}"

    try:

        files = os.listdir(folder_path)

        if not files:

            return f"📁 {folder_name.title()} is empty."

        result = f"📁 Files in {folder_name.title()}:\n\n"

        for index, file in enumerate(files, start=1):

            result += f"{index}. {file}\n"

        return result

    except Exception as e:

        return f"❌ Could not read folder: {e}"


# ==================================================
# FIND FILES BY TYPE
# ==================================================

def find_files(folder_name, extension=None):

    folder_name = folder_name.strip().lower()

    home = os.path.expanduser("~")

    folders = {

        "downloads": os.path.join(home, "Downloads"),

        "documents": os.path.join(home, "Documents"),

        "desktop": os.path.join(home, "Desktop"),

        "videos": os.path.join(home, "Videos"),

        "movies": os.path.join(home, "Movies")
    }

    folder_path = folders.get(folder_name)

    if folder_path is None:

        folder_path = os.path.join(home, folder_name)

    if not os.path.exists(folder_path):

        return f"❌ Folder not found: {folder_name}"

    try:

        files = os.listdir(folder_path)

        if extension:

            extension = extension.lower()

            files = [
                file for file in files
                if file.lower().endswith(extension)
            ]

        if not files:

            return f"🔍 No matching files found in {folder_name}."

        result = f"🔍 Files found in {folder_name.title()}:\n\n"

        for index, file in enumerate(files, start=1):

            result += f"{index}. {file}\n"

        return result

    except Exception as e:

        return f"❌ Could not search folder: {e}"