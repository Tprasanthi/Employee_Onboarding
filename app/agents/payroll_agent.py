from datetime import datetime
import time

from app.services.dynamodb_service import save_state


def payroll_agent(state):

    """
    Payroll Enroller Agent

    Responsibilities:
    - Payroll enrollment
    - Tax setup
    - Bank account verification
    - Salary structure configuration
    """

    print(
        f"\n💰 Payroll Agent started for "
        f"{state['employee_id']}"
    )

    # -----------------------------------------------------
    # CHECK IF PAYROLL TASK EXISTS
    # -----------------------------------------------------

    if "payroll" not in state["tasks"]:

        print(
            f"\nℹ️ Payroll not required for "
            f"{state['employee_type']}"
        )

        return state

    # -----------------------------------------------------
    # SIMULATE SLA DELAY
    # -----------------------------------------------------

    if state["employee_id"] == "EMP005":

        print(
            f"\n⏳ Simulating payroll delay for "
            f"{state['employee_id']}"
        )

        time.sleep(5)

    # -----------------------------------------------------
    # PROCESS PAYROLL SETUP
    # -----------------------------------------------------

    payroll_details = {

        "bank_account_verified": True,

        "tax_information_completed": True,

        "salary_structure_created": True,

        "payroll_id": f"PAY-{state['employee_id']}",

        "currency": "USD",

        "processed_at": datetime.now().isoformat()
    }

    # -----------------------------------------------------
    # UPDATE TASK STATUS
    # -----------------------------------------------------

    state["tasks"]["payroll"]["status"] = "completed"

    state["tasks"]["payroll"]["details"] = payroll_details

    # -----------------------------------------------------
    # SAVE STATE
    # -----------------------------------------------------

    save_state(state)

    print(
        f"\n✅ Payroll setup completed for "
        f"{state['employee_id']}"
    )

    return state