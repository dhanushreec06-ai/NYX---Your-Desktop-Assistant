import screen_brightness_control as sbc


def get_brightness():
    try:
        brightness = sbc.get_brightness()

        if isinstance(brightness, list):
            brightness = brightness[0]

        return int(brightness)

    except Exception as e:
        print(f"❌ Could not get brightness: {e}")
        return None


def set_brightness(level):
    try:
        level = int(level)

        level = max(0, min(100, level))

        sbc.set_brightness(level)

        return f"☀️ Brightness set to {level}%."

    except Exception as e:
        return f"❌ Failed to set brightness: {e}"


def increase_brightness(amount=10):
    try:
        current = get_brightness()

        if current is None:
            return "❌ Could not read current brightness."

        new_level = min(
            100,
            current + int(amount)
        )

        return set_brightness(new_level)

    except Exception as e:
        return f"❌ Failed to increase brightness: {e}"


def decrease_brightness(amount=10):
    try:
        current = get_brightness()

        if current is None:
            return "❌ Could not read current brightness."

        new_level = max(
            0,
            current - int(amount)
        )

        return set_brightness(new_level)

    except Exception as e:
        return f"❌ Failed to decrease brightness: {e}"