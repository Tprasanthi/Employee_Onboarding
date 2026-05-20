from datetime import datetime
import uuid

from app.graph.workflow import graph


# ---------------------------------------------------------
# SYNTHETIC EMPLOYEES
# ---------------------------------------------------------

employees = [

    {
        "employee_id": "EMP001",
        "employee_name": "John",
        "employee_type": "FTE"
    },

    {
        "employee_id": "EMP002",
        "employee_name": "Alice",
        "employee_type": "FTE"
    },

    {
        "employee_id": "EMP003",
        "employee_name": "David",
        "employee_type": "contractor"
    },

    {
        "employee_id": "EMP004",
        "employee_name": "Sophia",
        "employee_type": "contractor"
    },

    {
        "employee_id": "EMP005",
        "employee_name": "Emma",
        "employee_type": "intern"
    }
]


# ---------------------------------------------------------
# EXECUTE WORKFLOW
# ---------------------------------------------------------

for emp in employees:

    print("\n====================================")
    print(f"STARTING WORKFLOW -> {emp['employee_id']}")
    print("====================================")

    initial_state = {

        "employee_id": emp["employee_id"],

        "workflow_id": str(uuid.uuid4()),

        "employee_name": emp["employee_name"],

        "employee_type": emp["employee_type"],

        "start_date": str(datetime.now().date()),

        "tasks": {},

        "blockers": [],

        "escalations": [],

        "sla_status": {},

        "completion_percentage": 0,

        "eta": "",

        "final_status": ""
    }

    try:

        result = graph.invoke(initial_state)

        print("\n✅ WORKFLOW COMPLETED")

        print("\nFINAL RESULT:")
        print(result)

    except Exception as e:

        print("\n❌ WORKFLOW FAILED")

        print(f"ERROR: {str(e)}")