"""
Autonomous Employee Onboarding Orchestration Agent
==================================================

Tech Stack:
- LangGraph
- LangChain
- Qdrant
- DynamoDB
- OpenTelemetry
- LangSmith

This is a simplified but production-style implementation
for interview/demo purposes.

---------------------------------------------------------
INSTALL
---------------------------------------------------------

pip install langgraph langchain qdrant-client boto3 \
openai opentelemetry-sdk

---------------------------------------------------------
ENV VARIABLES
---------------------------------------------------------

export OPENAI_API_KEY=xxx
export LANGCHAIN_API_KEY=xxx
export LANGCHAIN_TRACING_V2=true
export AWS_REGION=us-east-1

---------------------------------------------------------
AWS DynamoDB TABLES
---------------------------------------------------------

1. onboarding_workflows
2. onboarding_checkpoints

Partition Key: employee_id
Sort Key: workflow_id

---------------------------------------------------------
"""

from typing import TypedDict, Dict, List
from datetime import datetime, timedelta
import random
import time
import uuid
import boto3

from langgraph.graph import StateGraph, END
from qdrant_client import QdrantClient

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter


# =========================================================
# OPEN TELEMETRY SETUP
# =========================================================

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)


# =========================================================
# DYNAMODB SETUP
# =========================================================

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

workflow_table = dynamodb.Table("onboarding_workflows")


# =========================================================
# QDRANT SETUP
# =========================================================

qdrant = QdrantClient(":memory:")

# In production:
# qdrant = QdrantClient(
#     url="http://localhost:6333"
# )


# =========================================================
# WORKFLOW STATE
# =========================================================

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


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def save_workflow_state(state):

    workflow_table.put_item(Item=state)


def calculate_completion(state):

    total = len(state["tasks"])

    completed = 0

    for task_name, task_data in state["tasks"].items():

        if task_data["status"] == "completed":
            completed += 1

    percentage = int((completed / total) * 100)

    state["completion_percentage"] = percentage

    return state


def send_escalation(employee_id, blocker):

    print(
        f"\n🚨 ESCALATION SENT -> "
        f"{employee_id} | blocker={blocker}"
    )


# =========================================================
# QDRANT RETRIEVAL
# =========================================================

def get_required_documents(employee_type):

    mapping = {
        "FTE": [
            "Offer Letter",
            "Aadhaar",
            "Form16",
            "Bank Details"
        ],

        "contractor": [
            "Contract Agreement",
            "Aadhaar"
        ],

        "intern": [
            "College ID",
            "Aadhaar"
        ]
    }

    return mapping.get(employee_type, [])


# =========================================================
# PLANNER NODE
# =========================================================

def planner_node(state: OnboardingState):

    with tracer.start_as_current_span("planner_node"):

        employee_type = state["employee_type"]

        tasks = {}

        if employee_type == "FTE":

            tasks = {
                "it": {
                    "status": "pending",
                    "sla_hours": 24,
                    "created_at": datetime.now().isoformat()
                },

                "payroll": {
                    "status": "pending",
                    "sla_hours": 48,
                    "created_at": datetime.now().isoformat()
                },

                "compliance": {
                    "status": "pending",
                    "sla_hours": 24,
                    "created_at": datetime.now().isoformat()
                },

                "benefits": {
                    "status": "pending",
                    "sla_hours": 72,
                    "created_at": datetime.now().isoformat()
                }
            }

        elif employee_type == "contractor":

            tasks = {
                "it": {
                    "status": "pending",
                    "sla_hours": 24,
                    "created_at": datetime.now().isoformat()
                },

                "compliance": {
                    "status": "pending",
                    "sla_hours": 24,
                    "created_at": datetime.now().isoformat()
                }
            }

        elif employee_type == "intern":

            tasks = {
                "it": {
                    "status": "pending",
                    "sla_hours": 24,
                    "created_at": datetime.now().isoformat()
                },

                "compliance": {
                    "status": "pending",
                    "sla_hours": 24,
                    "created_at": datetime.now().isoformat()
                }
            }

        state["tasks"] = tasks

        print(
            f"\n🧠 Planner created tasks for "
            f"{state['employee_id']}"
        )

        save_workflow_state(state)

        return state


# =========================================================
# IT AGENT
# =========================================================

def it_agent(state: OnboardingState):

    with tracer.start_as_current_span("it_agent"):

        if "it" not in state["tasks"]:
            return state

        print(f"\n💻 IT Agent running for {state['employee_id']}")

        # Simulated delay for EMP003
        if state["employee_id"] == "EMP003":
            time.sleep(5)

        state["tasks"]["it"]["status"] = "completed"

        save_workflow_state(state)

        return state


# =========================================================
# PAYROLL AGENT
# =========================================================

def payroll_agent(state: OnboardingState):

    with tracer.start_as_current_span("payroll_agent"):

        if "payroll" not in state["tasks"]:
            return state

        print(f"\n💰 Payroll Agent running for {state['employee_id']}")

        # Simulated SLA breach
        if state["employee_id"] == "EMP005":
            time.sleep(5)

        state["tasks"]["payroll"]["status"] = "completed"

        save_workflow_state(state)

        return state


# =========================================================
# COMPLIANCE AGENT
# =========================================================

def compliance_agent(state: OnboardingState):

    with tracer.start_as_current_span("compliance_agent"):

        if "compliance" not in state["tasks"]:
            return state

        print(
            f"\n📄 Compliance Agent running for "
            f"{state['employee_id']}"
        )

        required_docs = get_required_documents(
            state["employee_type"]
        )

        uploaded_docs = []

        # Simulate missing docs
        for doc in required_docs:

            if random.choice([True, False]):
                uploaded_docs.append(doc)

        missing_docs = list(
            set(required_docs) - set(uploaded_docs)
        )

        if missing_docs:

            blocker = {
                "type": "missing_documents",
                "docs": missing_docs,
                "age_hours": 50
            }

            state["blockers"].append(blocker)

            state["tasks"]["compliance"]["status"] = "blocked"

            print(
                f"\n❌ Missing documents for "
                f"{state['employee_id']} -> {missing_docs}"
            )

        else:

            state["tasks"]["compliance"]["status"] = "completed"

        save_workflow_state(state)

        return state


# =========================================================
# BENEFITS AGENT
# =========================================================

def benefits_agent(state: OnboardingState):

    with tracer.start_as_current_span("benefits_agent"):

        if "benefits" not in state["tasks"]:
            return state

        print(
            f"\n🏥 Benefits Agent running for "
            f"{state['employee_id']}"
        )

        state["tasks"]["benefits"]["status"] = "completed"

        save_workflow_state(state)

        return state


# =========================================================
# SLA MONITOR
# =========================================================

def sla_monitor(state: OnboardingState):

    with tracer.start_as_current_span("sla_monitor"):

        print(
            f"\n⏰ SLA Monitor running for "
            f"{state['employee_id']}"
        )

        now = datetime.now()

        sla_status = {}

        for task_name, task_data in state["tasks"].items():

            created_time = datetime.fromisoformat(
                task_data["created_at"]
            )

            elapsed_hours = (
                now - created_time
            ).total_seconds() / 3600

            if (
                elapsed_hours > task_data["sla_hours"]
                and task_data["status"] != "completed"
            ):

                sla_status[task_name] = "BREACHED"

                print(
                    f"\n🚨 SLA BREACH -> "
                    f"{state['employee_id']} | "
                    f"{task_name}"
                )

            else:
                sla_status[task_name] = "OK"

        state["sla_status"] = sla_status

        save_workflow_state(state)

        return state


# =========================================================
# ESCALATION AGENT
# =========================================================

def escalation_agent(state: OnboardingState):

    with tracer.start_as_current_span("escalation_agent"):

        print(
            f"\n📢 Escalation Agent running for "
            f"{state['employee_id']}"
        )

        for blocker in state["blockers"]:

            if blocker["age_hours"] > 48:

                send_escalation(
                    state["employee_id"],
                    blocker
                )

                state["escalations"].append(blocker)

        save_workflow_state(state)

        return state


# =========================================================
# STATUS GENERATOR
# =========================================================

def status_generator(state: OnboardingState):

    with tracer.start_as_current_span("status_generator"):

        state = calculate_completion(state)

        if len(state["blockers"]) > 0:
            state["final_status"] = "BLOCKED"

        elif state["completion_percentage"] == 100:
            state["final_status"] = "COMPLETED"

        else:
            state["final_status"] = "IN_PROGRESS"

        state["eta"] = (
            datetime.now() + timedelta(days=1)
        ).strftime("%Y-%m-%d")

        print("\n===================================")
        print("FINAL STATUS")
        print("===================================")

        print(state)

        save_workflow_state(state)

        return state


# =========================================================
# DAY-30 CHECKIN AGENT
# =========================================================

def day30_checkin_agent(state):

    with tracer.start_as_current_span("day30_checkin_agent"):

        summary = f"""
        Employee: {state['employee_name']}

        Completion: {state['completion_percentage']}%

        Status: {state['final_status']}

        Recommendations:
        - Assign mentor
        - Schedule team connect
        - Complete remaining compliance tasks
        """

        print("\n📅 DAY-30 MANAGER SUMMARY")
        print(summary)

        return state


# =========================================================
# LANGGRAPH WORKFLOW
# =========================================================

workflow = StateGraph(OnboardingState)

workflow.add_node("planner", planner_node)

workflow.add_node("it_agent", it_agent)

workflow.add_node("payroll_agent", payroll_agent)

workflow.add_node("compliance_agent", compliance_agent)

workflow.add_node("benefits_agent", benefits_agent)

workflow.add_node("sla_monitor", sla_monitor)

workflow.add_node("escalation_agent", escalation_agent)

workflow.add_node("status_generator", status_generator)

workflow.add_node("day30_agent", day30_checkin_agent)

workflow.set_entry_point("planner")

# Main Flow

workflow.add_edge("planner", "it_agent")

workflow.add_edge("it_agent", "payroll_agent")

workflow.add_edge("payroll_agent", "compliance_agent")

workflow.add_edge("compliance_agent", "benefits_agent")

workflow.add_edge("benefits_agent", "sla_monitor")

workflow.add_edge("sla_monitor", "escalation_agent")

workflow.add_edge("escalation_agent", "status_generator")

workflow.add_edge("status_generator", "day30_agent")

workflow.add_edge("day30_agent", END)

graph = workflow.compile()


# =========================================================
# SYNTHETIC EMPLOYEES
# =========================================================

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


# =========================================================
# EXECUTION
# =========================================================

for emp in employees:

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

    print("\n\n===================================")
    print(f"STARTING WORKFLOW -> {emp['employee_id']}")
    print("===================================")

    result = graph.invoke(initial_state)

    print("\n✅ WORKFLOW COMPLETED")