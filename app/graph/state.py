from typing import TypedDict, Dict, List


class OnboardingState(TypedDict):

    employee_id: str
    workflow_id: str

    employee_name: str
    employee_type: str

    start_date: str

    tasks: Dict

    blockers: List

    escalations: List

    sla_status: Dict

    completion_percentage: int

    eta: str

    final_status: str