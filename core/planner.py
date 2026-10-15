def validate_plan(plan):

    if not isinstance(plan, dict):
        return False

    tasks = plan.get("tasks")

    if not isinstance(tasks, list):
        return False

    for task in tasks:

        if "action" not in task:
            return False

        if "target" not in task:
            return False

    return True


def get_tasks(plan):

    if not validate_plan(plan):
        return []

    return sorted(
        plan["tasks"],
        key=lambda task: task.get("step", 0)
    )