import subprocess
import re
import time


# ==================================================
# RUN NETSH
# ==================================================

def run_netsh(arguments):

    try:

        result = subprocess.run(
            ["netsh"] + arguments,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=20
        )

        return result.stdout.strip()

    except Exception as e:

        return f"ERROR: {e}"


# ==================================================
# WIFI STATUS
# ==================================================

def wifi_status():

    output = run_netsh([
        "wlan",
        "show",
        "interfaces"
    ])

    if output.startswith("ERROR:"):
        return f"❌ {output}"

    if not output:
        return "❌ No Wi-Fi information available."

    return f"📶 Wi-Fi Status:\n\n{output}"


# ==================================================
# GET CURRENT WIFI
# ==================================================

def get_current_wifi():

    output = run_netsh([
        "wlan",
        "show",
        "interfaces"
    ])

    if output.startswith("ERROR:"):
        return None

    for line in output.splitlines():

        line = line.strip()

        if line.startswith("SSID") and "BSSID" not in line:

            parts = line.split(":", 1)

            if len(parts) == 2:

                ssid = parts[1].strip()

                if ssid:
                    return ssid

    return None


# ==================================================
# SCAN AVAILABLE WIFI
# ==================================================

def scan_wifi():

    output = run_netsh([
        "wlan",
        "show",
        "networks",
        "mode=bssid"
    ])

    if output.startswith("ERROR:"):
        return f"❌ {output}"

    if not output:
        return "❌ Could not scan Wi-Fi networks."

    return f"📡 Available Wi-Fi networks:\n\n{output}"


# ==================================================
# GET AVAILABLE WIFI + SIGNAL
# ==================================================

def get_available_wifi():

    output = run_netsh([
        "wlan",
        "show",
        "networks",
        "mode=bssid"
    ])

    if output.startswith("ERROR:"):
        return []

    networks = []

    current_ssid = None

    for line in output.splitlines():

        line = line.strip()

        # Find SSID
        if line.startswith("SSID ") and "BSSID" not in line:

            parts = line.split(":", 1)

            if len(parts) == 2:

                current_ssid = parts[1].strip()

        # Find signal
        elif line.startswith("Signal") and current_ssid:

            parts = line.split(":", 1)

            if len(parts) == 2:

                signal_text = parts[1].strip()

                match = re.search(
                    r"(\d+)%?",
                    signal_text
                )

                if match:

                    signal = int(match.group(1))

                    networks.append({
                        "ssid": current_ssid,
                        "signal": signal
                    })

    return networks


# ==================================================
# CONNECT TO SPECIFIC WIFI
# ==================================================

def connect_wifi(network_name):

    network_name = str(network_name).strip()

    if not network_name:

        return auto_connect_best_wifi()

    print(
        f"🌐 Connecting to Wi-Fi: "
        f"{network_name}"
    )

    result = subprocess.run(
        [
            "netsh",
            "wlan",
            "connect",
            f"name={network_name}"
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        timeout=20
    )

    output = (
        result.stdout.strip()
        or result.stderr.strip()
    )

    if result.returncode != 0:

        return (
            f"❌ Could not connect to "
            f"'{network_name}'.\n"
            f"{output}"
        )

    time.sleep(3)

    current = get_current_wifi()

    if current:

        return (
            f"✅ Connected to Wi-Fi: "
            f"{current}"
        )

    return (
        f"⚠️ Windows accepted the connection "
        f"request for {network_name}, "
        f"but connection could not be verified."
    )


# ==================================================
# AUTO SELECT BEST WIFI
# ==================================================

def auto_connect_best_wifi():

    print("🔎 Searching for available Wi-Fi...")

    networks = get_available_wifi()

    if not networks:

        return "❌ No Wi-Fi networks found."

    # Remove duplicate SSIDs.
    best_networks = {}

    for network in networks:

        ssid = network["ssid"]
        signal = network["signal"]

        if (
            ssid not in best_networks
            or signal > best_networks[ssid]["signal"]
        ):

            best_networks[ssid] = network

    networks = list(best_networks.values())

    # Highest signal first.
    networks.sort(
        key=lambda x: x["signal"],
        reverse=True
    )

    print("\n📡 Wi-Fi ranking:")

    for index, network in enumerate(
        networks,
        start=1
    ):

        print(
            f"{index}. "
            f"{network['ssid']} "
            f"({network['signal']}%)"
        )

    # Try networks in strongest-signal order.
    for network in networks:

        ssid = network["ssid"]

        print(
            f"\n🔄 Trying: "
            f"{ssid}"
        )

        result = connect_wifi(ssid)

        if result.startswith("✅"):

            return (
                f"🤖 NYX selected the strongest "
                f"available Wi-Fi.\n\n"
                f"{result}"
            )

    return (
        "❌ NYX could not connect to "
        "any available Wi-Fi."
    )


# ==================================================
# DISCONNECT WIFI
# ==================================================

def disconnect_wifi():

    current = get_current_wifi()

    result = subprocess.run(
        [
            "netsh",
            "wlan",
            "disconnect"
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        timeout=15
    )

    output = (
        result.stdout.strip()
        or result.stderr.strip()
    )

    if result.returncode == 0:

        if current:

            return (
                f"✅ Disconnected from "
                f"{current}."
            )

        return "✅ Wi-Fi disconnected."

    return (
        f"❌ Could not disconnect Wi-Fi.\n"
        f"{output}"
    )


# ==================================================
# CHANGE WIFI
# ==================================================

def change_wifi(network_name):

    network_name = str(network_name).strip()

    if not network_name:

        return (
            "❌ Please specify the Wi-Fi "
            "network you want to change to."
        )

    current = get_current_wifi()

    if current:

        print(
            f"🔄 Changing Wi-Fi:\n"
            f"{current} → {network_name}"
        )

        disconnect_wifi()

        time.sleep(2)

    return connect_wifi(network_name)