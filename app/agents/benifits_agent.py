from datetime import datetime
from app.services.dynamodb_service import save_state


def benefits_agent(state):

    """
    Benefits Advisor Agent

    Responsibilities:
    - Insurance enrollment
    - Wellness plan onboarding
    - Leave policy guidance
    - Benefits package setup
    """

    print(
        f"\n🏥 Benefits Agent started for "
        f"{state['employee_id']}"
    )

    # -----------------------------------------------------
    # CHECK IF BENEFITS TASK EXISTS
    # -----------------------------------------------------

    if "benefits" not in state["tasks"]:

        print(
            f"\nℹ️ Benefits not required for "
            f"{state['employee_type']}"
        )

        return state

    # -----------------------------------------------------
    # SIMULATE BENEFITS PROCESSING
    # -----------------------------------------------------

    benefits_summary = {

        "insurance_plan": "Premium Health Plan",

        "leave_policy_shared": True,

        "wellness_program_enabled": True,

        "benefits_orientation_completed": True,

        "processed_at": datetime.now().isoformat()
    }

    # -----------------------------------------------------
    # UPDATE TASK STATUS
    # -----------------------------------------------------

    state["tasks"]["benefits"]["status"] = "completed"

    state["tasks"]["benefits"]["details"] = benefits_summary

    # -----------------------------------------------------
    # SAVE STATE
    # -----------------------------------------------------

    save_state(state)

    print(
        f"\n✅ Benefits completed for "
        f"{state['employee_id']}"
    )

    return state