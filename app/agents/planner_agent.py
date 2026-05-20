from datetime import datetime


def planner_agent(state):

    employee_type = state["employee_type"]

    if employee_type == "FTE":

        tasks = [
            "it",
            "payroll",
            "compliance",
            "benefits"
        ]

    elif employee_type == "contractor":

        tasks = [
            "it",
            "compliance"
        ]

    else:

        tasks = [
            "it",
            "compliance"
        ]

    task_map = {}

    for task in tasks:

        task_map[task] = {
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }

    state["tasks"] = task_map

    return state