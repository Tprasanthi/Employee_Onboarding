from datetime import datetime


def sla_monitor(state):

    status = {}

    for task_name, task_data in state["tasks"].items():

        created = datetime.fromisoformat(
            task_data["created_at"]
        )

        elapsed = (
            datetime.now() - created
        ).total_seconds() / 3600

        if elapsed > 24:
            status[task_name] = "BREACHED"

        else:
            status[task_name] = "OK"

    state["sla_status"] = status

    return state