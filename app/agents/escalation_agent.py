from datetime import datetime
from app.services.dynamodb_service import save_state


def escalation_agent(state):

    """
    Escalation Agent

    Responsibilities:
    - Detect long-running blockers
    - Trigger HR escalation
    - Notify stakeholders
    - Update escalation history
    """

    print(
        f"\n📢 Escalation Agent started for "
        f"{state['employee_id']}"
    )

    # -----------------------------------------------------
    # CHECK BLOCKERS
    # -----------------------------------------------------

    escalated_items = []

    for blocker in state["blockers"]:

        blocker_age = blocker.get("age_hours", 0)

        # Escalate if blocker persists > 48 hours
        if blocker_age > 48:

            escalation = {

                "employee_id": state["employee_id"],

                "blocker_type": blocker["type"],

                "details": blocker,

                "escalated_to": "HR Coordinator",

                "status": "ESCALATED",

                "escalated_at": datetime.now().isoformat()
            }

            escalated_items.append(escalation)

            print(
                f"\n🚨 Escalation Triggered -> "
                f"{state['employee_id']}"
            )

            print(
                f"Blocker Type: {blocker['type']}"
            )

    # -----------------------------------------------------
    # UPDATE STATE
    # -----------------------------------------------------

    if escalated_items:

        state["escalations"].extend(escalated_items)

    else:

        print(
            f"\n✅ No escalation required for "
            f"{state['employee_id']}"
        )

    # -----------------------------------------------------
    # SAVE STATE
    # -----------------------------------------------------

    save_state(state)

    return state