from voice.speechtotext import listen
from voice.texttospeech import speak

from brain.llm import understand, chat
from agent.executor import execute_plan


def start_conversation(user_name):

    speak(
        f"Hello {user_name}. "
        "I am NYX. How can I help you?"
    )

    conversation_history = []

    while True:

        # ==============================
        # LISTEN
        # ==============================

        user_text = listen()

        if not user_text:
            continue

        user_text = user_text.strip()

        print(f"\n👤 {user_name}: {user_text}")

        # ==============================
        # EXIT
        # ==============================

        if user_text.lower() in [
            "goodbye",
            "bye nyx",
            "exit conversation",
            "stop conversation",
            "shutdown nyx",
            "quit"
        ]:

            speak(
                f"Goodbye {user_name}. "
                "I'll be here when you need me."
            )

            break

        # ==============================
        # TRY ORCHESTRATOR
        # ==============================

        print("🧠 NYX is understanding...")

        plan = understand(user_text)

        print(f"🧠 NYX PLAN: {plan}")

        # ==============================
        # ORCHESTRATOR ERROR
        # ==============================

        if plan.get("error"):

            print(
                f"⚠️ Orchestrator error: "
                f"{plan['error']}"
            )

            tasks = []

        else:

            tasks = plan.get("tasks", [])

        # ==============================
        # COMMAND / AUTOMATION
        # ==============================

        if tasks:

            print(
                f"🚀 NYX executing "
                f"{len(tasks)} task(s)..."
            )

            results = execute_plan(tasks)

            # Tell user what happened

            for result in results:

                print(
                    f"Step {result['step']} "
                    f"→ {result['action']} "
                    f"→ {result['result']}"
                )

            speak(
                f"Done {user_name}. "
                "I've completed the requested task."
            )

        # ==============================
        # NORMAL CONVERSATION
        # ==============================

        else:

            print("💬 NYX is having a conversation...")

            response = chat(
                user_text,
                user_name,
                conversation_history
            )

            print(f"🤖 NYX: {response}")

            speak(response)

            # Save conversation

            conversation_history.append({
                "role": "User",
                "content": user_text
            })

            conversation_history.append({
                "role": "NYX",
                "content": response
            })

            # Keep history manageable

            if len(conversation_history) > 10:

                conversation_history = (
                    conversation_history[-10:]
                )