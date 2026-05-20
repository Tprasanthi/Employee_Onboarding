from datetime import datetime
import time

from app.services.dynamodb_service import save_state


def it_agent(state):

    """
    IT Provisioner Agent

    Responsibilities:
    - Laptop provisioning
    - Email account setup
    - VPN access
    - Slack/MS Teams access
    - Software access provisioning
    """

    print(
        f"\n💻 IT Agent started for "
        f"{state['employee_id']}"
    )

    # -----------------------------------------------------
    # CHECK IF IT TASK EXISTS
    # -----------------------------------------------------

    if "it" not in state["tasks"]:

        print(
            f"\nℹ️ IT task not required for "
            f"{state['employee_type']}"
        )

        return state

    # -----------------------------------------------------
    # SIMULATED SLA BREACH / DELAY
    # -----------------------------------------------------

    if state["employee_id"] == "EMP003":

        print(
            f"\n⏳ Simulating provisioning delay for "
            f"{state['employee_id']}"
        )

        time.sleep(5)

    # -----------------------------------------------------
    # PROVISION RESOURCES
    # -----------------------------------------------------

    provisioning_details = {

        "email_created": True,

        "vpn_access": True,

        "slack_access": True,

        "laptop_assigned": True,

        "software_access": [
            "Jira",
            "Confluence",
            "GitHub",
            "Slack"
        ],

        "provisioned_at": datetime.now().isoformat()
    }

    # -----------------------------------------------------
    # UPDATE TASK STATUS
    # -----------------------------------------------------

    state["tasks"]["it"]["status"] = "completed"

    state["tasks"]["it"]["details"] = provisioning_details

    # -----------------------------------------------------
    # SAVE STATE
    # -----------------------------------------------------

    save_state(state)

    print(
        f"\n✅ IT provisioning completed for "
        f"{state['employee_id']}"
    )

    return state