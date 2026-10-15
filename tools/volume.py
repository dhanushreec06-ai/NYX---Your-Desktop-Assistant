from ctypes import POINTER, cast

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def get_volume_controller():
    """
    Get the Windows master-volume controller.
    """

    device = AudioUtilities.GetSpeakers()

    interface = device.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )

    volume = cast(
        interface,
        POINTER(IAudioEndpointVolume)
    )

    return volume


def get_volume():
    try:
        volume = get_volume_controller()

        level = volume.GetMasterVolumeLevelScalar()

        return round(level * 100)

    except Exception as e:
        print(f"❌ Could not get volume: {e}")
        return None


def set_volume(level):
    try:
        level = int(level)

        # Keep volume between 0 and 100
        level = max(0, min(100, level))

        volume = get_volume_controller()

        volume.SetMasterVolumeLevelScalar(
            level / 100.0,
            None
        )

        return f"✅ Volume set to {level}%."

    except Exception as e:
        return f"❌ Failed to set volume: {e}"


def increase_volume(amount=10):
    try:

        current = get_volume()

        if current is None:
            return "❌ Could not read current volume."

        new_level = min(
            100,
            current + int(amount)
        )

        return set_volume(new_level)

    except Exception as e:
        return f"❌ Failed to increase volume: {e}"


def decrease_volume(amount=10):
    try:

        current = get_volume()

        if current is None:
            return "❌ Could not read current volume."

        new_level = max(
            0,
            current - int(amount)
        )

        return set_volume(new_level)

    except Exception as e:
        return f"❌ Failed to decrease volume: {e}"


def mute_volume():
    try:

        volume = get_volume_controller()

        volume.SetMute(1, None)

        return "🔇 Volume muted."

    except Exception as e:
        return f"❌ Failed to mute volume: {e}"


def unmute_volume():
    try:

        volume = get_volume_controller()

        volume.SetMute(0, None)

        return "🔊 Volume unmuted."

    except Exception as e:
        return f"❌ Failed to unmute volume: {e}"