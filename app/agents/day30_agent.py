from datetime import datetime
from app.services.dynamodb_service import save_state


def day30_agent(state):

    """
    Day-30 Check-In Agent

    Responsibilities:
    - Analyze onboarding completion
    - Generate manager summary
    - Identify pending items
    - Suggest next actions
    """

    print(
        f"\n📅 Day-30 Agent started for "
        f"{state['employee_id']}"
    )

    # -----------------------------------------------------
    # CALCULATE PENDING TASKS
    # -----------------------------------------------------

    pending_tasks = []

    for task_name, task_data in state["tasks"].items():

        if task_data["status"] != "completed":

            pending_tasks.append(task_name)

    # -----------------------------------------------------
    # GENERATE MANAGER SUMMARY
    # -----------------------------------------------------

    summary = {

        "employee_id": state["employee_id"],

        "employee_name": state["employee_name"],

        "employee_type": state["employee_type"],

        "completion_percentage": state[
            "completion_percentage"
        ],

        "final_status": state["final_status"],

        "pending_tasks": pending_tasks,

        "blockers": state["blockers"],

        "recommendations": [
            "Assign onboarding buddy",
            "Schedule team introduction",
            "Conduct feedback session"
        ],

        "generated_at": datetime.now().isoformat()
    }

    # -----------------------------------------------------
    # SAVE DAY-30 SUMMARY
    # -----------------------------------------------------

    state["day30_summary"] = summary

    save_state(state)

    # -----------------------------------------------------
    # LOG OUTPUT
    # -----------------------------------------------------

    print("\n====================================")
    print("DAY-30 SUMMARY")
    print("====================================")

    print(summary)

    print(
        f"\n✅ Day-30 summary generated for "
        f"{state['employee_id']}"
    )

    return state