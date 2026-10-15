import json
import os

from google import genai


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY missing")


client = genai.Client(api_key=api_key)


ORCHESTRATOR_PROMPT = """
You are NYX Orchestrator.

You receive a user's natural-language request.

Your job is to:

1. Understand the complete request.
2. Break it into individual tasks.
3. Select the correct NYX tool.
4. Preserve the correct execution order.
5. Return ONLY valid JSON.

Available tools:

open_app
open_website
open_folder
list_files
find_files
spotify_play
youtube_play_search
whatsapp_send
whatsapp_send_contact

Return this structure:

{
    "tasks": [
        {
            "step": 1,
            "action": "tool_name",
            "target": {}
        }
    ]
}

Example:

User:
"Open WhatsApp, message Rahul saying I will call him later,
then play Kadhal Vaithu on Spotify."

Response:

{
    "tasks": [
        {
            "step": 1,
            "action": "whatsapp_send_contact",
            "target": {
                "contact": "Rahul",
                "message": "I will call him later."
            }
        },
        {
            "step": 2,
            "action": "spotify_play",
            "target": {
                "song": "Kadhal Vaithu"
            }
        }
    ]
}

IMPORTANT:
TASK BREAKING RULES:

- There is NO maximum number of tasks.
- The user may give 1, 2, 3, 4, 5, 10, or more tasks.
- Create one task for EVERY action requested by the user.
- NEVER combine multiple actions into one task.
- Preserve the exact order in which the user requested the actions.
- Continue creating tasks until the COMPLETE user request has been converted into executable tasks.
- Do not stop after 2 tasks.

For example:

User:
"Open WhatsApp, send Hi to Rahul, then play Kadhal Vaithu
on Spotify, then open YouTube and play Tamil comedy scenes,
increase volume, and show my reminders."

Return:

{
    "tasks": [
        {
            "step": 1,
            "action": "open_website",
            "target": {
                "url": "https://web.whatsapp.com",
                "browser": null
            }
        },
        {
            "step": 2,
            "action": "whatsapp_send_contact",
            "target": {
                "contact": "Rahul",
                "message": "Hi"
            }
        },
        {
            "step": 3,
            "action": "spotify_play",
            "target": {
                "song": "Kadhal Vaithu"
            }
        },
        {
            "step": 4,
            "action": "youtube_play_search",
            "target": {
                "query": "Tamil comedy scenes"
            }
        },
        {
            "step": 5,
            "action": "increase_volume",
            "target": {}
        },
        {
            "step": 6,
            "action": "show_reminders",
            "target": {}
        }
    ]
}
Return ONLY JSON.
"""


def create_plan(command):

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=f"""
{ORCHESTRATOR_PROMPT}

User request:
{command}
"""
    )

    result = response.text.strip()

    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    try:
        return json.loads(result)

    except json.JSONDecodeError:

        return {
            "tasks": [],
            "error": "Orchestrator returned invalid JSON"
        }