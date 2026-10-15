import inspect

from tools.registry import get_tool

def execute(action, target=None):

    if target is None:
        target = {}

    # -------------------------------------------------
    # Normalize invalid LLM action
    # -------------------------------------------------

    if action == "youtube_play_search":
        action = "youtube_search"

    tool = get_tool(action)

    if tool is None:
        return f"❌ No tool available: {action}"

    ...
# ==========================================
# EXECUTE ONE TOOL
# ==========================================

def execute(action, target=None):

    if target is None:
        target = {}

    tool = get_tool(action)

    if tool is None:
        return f"❌ No tool available: {action}"

    try:

        signature = inspect.signature(tool)

        parameters = list(signature.parameters.values())

        # --------------------------------------
        # Tool takes no arguments
        # --------------------------------------

        if len(parameters) == 0:
            return tool()

        # --------------------------------------
        # Tool expects one argument called target
        # --------------------------------------

        if len(parameters) == 1:

            parameter = parameters[0]

            if parameter.name == "target":
                return tool(target)

            # If target contains matching parameter
            if parameter.name in target:
                return tool(target[parameter.name])

            # Common parameter names
            for key in [
                "song",
                "query",
                "message",
                "contact",
                "app",
                "website",
                "folder",
                "network",
                "wifi"
            ]:

                if parameter.name == key and key in target:
                    return tool(target[key])

            # Last fallback
            return tool(target)

        # --------------------------------------
        # Multiple parameters
        # --------------------------------------

        kwargs = {}

        for parameter in parameters:

            if parameter.name in target:
                kwargs[parameter.name] = target[parameter.name]

        return tool(**kwargs)

    except Exception as e:

        return f"❌ Tool failed: {e}"


# ==========================================
# EXECUTE COMPLETE PLAN
# ==========================================

def execute_plan(tasks):

    results = []

    if not tasks:
        return results

    # Make sure tasks execute in correct order
    tasks = sorted(
        tasks,
        key=lambda x: x.get("step", 0)
    )

    for task in tasks:

        step = task.get("step")
        action = task.get("action")
        target = task.get("target", {})

        print()
        print("=" * 50)
        print(f"▶️ STEP {step}")
        print(f"🔧 ACTION: {action}")
        print(f"🎯 TARGET: {target}")
        print("=" * 50)

        result = execute(
            action,
            target
        )

        print(f"💻 RESULT: {result}")

        results.append({
            "step": step,
            "action": action,
            "target": target,
            "result": result
        })

    return results