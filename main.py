from voice.speechtotext import listen
from brain.llm import understand
from agent.executor import execute_plan


print("--------------------------------")
print("          NYX AI AGENT")
print("--------------------------------")

print("🧠 NYX Orchestrator Ready")
print("🎤 Listening for commands...")


while True:

    command = listen()

    if not command:
        continue

    command = command.strip()

    print(f"\n👤 You: {command}")

    # ======================================
    # EXIT
    # ======================================

    if command.lower() in [
        "off",
        "close",
        "exit",
        "quit",
        "shutdown",
        "stop running"
    ]:

        print("👋 NYX shutting down...")
        break

    # ======================================
    # LLM ORCHESTRATOR
    # ======================================

    print("🧠 NYX is planning...")

    result = understand(command)

    print(f"\n🧠 NYX PLAN:")
    print(result)

    # ======================================
    # CHECK FOR LLM ERROR
    # ======================================

    if result.get("error"):

        print(
            f"❌ Orchestrator Error: "
            f"{result['error']}"
        )

        continue

    # ======================================
    # GET TASKS
    # ======================================

    tasks = result.get("tasks", [])

    if not tasks:

        print("❌ NYX could not create a task plan.")
        continue

    # ======================================
    # EXECUTE PLAN
    # ======================================

    print(
        f"\n🚀 NYX executing "
        f"{len(tasks)} task(s)..."
    )

    results = execute_plan(tasks)

    # ======================================
    # FINAL RESULT
    # ======================================

    print("\n================================")
    print("        NYX TASK SUMMARY")
    print("================================")

    for result in results:

        print(
            f"Step {result['step']} "
            f"→ {result['action']} "
            f"→ {result['result']}"
        )

    print("\n🎤 NYX Listening...")