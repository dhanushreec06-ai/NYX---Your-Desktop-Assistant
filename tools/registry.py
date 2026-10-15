from tools.desktop import (
    find_and_open_app,
    open_folder,
    list_files,
    find_files
)
from tools.volume import (
    increase_volume,
    decrease_volume,
    set_volume,
    mute_volume,
    unmute_volume
)
from tools.brightness import (
    increase_brightness,
    decrease_brightness,
    set_brightness
)

from tools.network import (
    wifi_status,
    scan_wifi,
    connect_wifi,
    disconnect_wifi,
    change_wifi
)

from tools.tasks import (
    add_task,
    show_tasks,
    complete_task,
    delete_task
)

from tools.reminders import (
    add_reminder,
    show_reminders,
    complete_reminder,
    delete_reminder
)

from tools.productivity import (
    show_productivity,
    open_productivity
)
from tools.spotify import (
    open_spotify,
    spotify_play,
    spotify_pause,
    spotify_next,
    spotify_previous,
    spotify_stop
)


from tools.youtube import (
    open_youtube,
    youtube_play_search,
    youtube_play,
    youtube_pause,
    youtube_next,
    youtube_previous,
    youtube_shorts,
    youtube_next_short,
    youtube_previous_short
)

from tools.gmail import (
    open_gmail,
    gmail_compose,
    gmail_send
)

from tools.whatsapp import (
    whatsapp_send,
    whatsapp_send_contact
)

from tools.web_manager import open_website

from tools.youtube import youtube_play_search

from tools.whatsapp import whatsapp_send
TOOLS = {

    "open_app": find_and_open_app,

    "open_website": open_website,

    "open_folder": open_folder,

    "list_files": list_files,

    "find_files": find_files,

    "increase_volume": increase_volume,

    "decrease_volume": decrease_volume,

    "set_volume": set_volume,

    "mute_volume": mute_volume,

    "unmute_volume": unmute_volume,

    "increase_brightness": increase_brightness,

    "decrease_brightness": decrease_brightness,

    "set_brightness": set_brightness,

    "wifi_status": wifi_status,

    "scan_wifi": scan_wifi,

    "connect_wifi": connect_wifi,

    "disconnect_wifi": disconnect_wifi,

    "change_wifi": change_wifi,

    "add_task": add_task,

    "show_tasks": show_tasks,

    "complete_task": complete_task,

    "delete_task": delete_task,

    "add_reminder": add_reminder,

    "show_reminders": show_reminders,

    "complete_reminder": complete_reminder,

    "delete_reminder": delete_reminder,

    "show_productivity": show_productivity,

    "open_productivity": open_productivity,

    "open_spotify": open_spotify,

    "spotify_play": spotify_play,

    "spotify_pause": spotify_pause,

    "spotify_next": spotify_next,

    "spotify_previous": spotify_previous,

    "spotify_stop": spotify_stop,

    "open_youtube": open_youtube,

    "youtube_play": youtube_play,

    "youtube_pause": youtube_pause,

    "youtube_next": youtube_next,

    "youtube_previous": youtube_previous,

    "youtube_search": youtube_play_search,

    "youtube_play_search" : youtube_play_search,
 
    "youtube_shorts": youtube_shorts,

    "youtube_next_short": youtube_next_short,

    "youtube_previous_short": youtube_previous_short,

    "open_gmail": open_gmail,

    "gmail_compose": gmail_compose,

    "gmail_send": gmail_send,

    "whatsapp_send": whatsapp_send,

    "whatsapp_send_contact": whatsapp_send_contact,
    
}


def get_tool(action):

    return TOOLS.get(action)


def list_tools():

    return list(TOOLS.keys())

if __name__ == "__main__":

    print("Available NYX tools:")

    for tool in list_tools():

        print("•", tool)