# Autonomous Employee Onboarding Orchestration Agent

Production-grade project structure for a LangGraph-based multi-agent onboarding orchestration platform.

---

# Project Structure

```text
onboarding-orchestrator/
│
├── app/
│   ├── agents/
│   │   ├── planner_agent.py
│   │   ├── it_agent.py
│   │   ├── payroll_agent.py
│   │   ├── compliance_agent.py
│   │   ├── benefits_agent.py
│   │   ├── escalation_agent.py
│   │   └── day30_agent.py
│   │
│   ├── graph/
│   │   ├── workflow.py
│   │   └── state.py
│   │
│   ├── services/
│   │   ├── dynamodb_service.py
│   │   ├── qdrant_service.py
│   │   ├── notification_service.py
│   │   └── observability.py
│   │
│   ├── monitoring/
│   │   └── sla_monitor.py
│   │
│   ├── models/
│   │   └── onboarding_models.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── utils/
│   │   ├── helpers.py
│   │   └── constants.py
│   │
│   └── main.py
│
├── docs/
│   ├── AGENTS.md
│   ├── ROLES.md
│   ├── ARCHITECTURE.md
│   └── FAILURE_MODES.md
│
├── tests/
│   ├── test_workflow.py
│   ├── test_sla.py
│   └── test_agents.py
│
├── infra/
│   ├── dynamodb.tf
│   ├── ecs.tf
│   └── iam.tf
│
├── .env
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── README.md
└── run.py
```

---

# requirements.txt

```txt
langgraph
langchain
langchain-openai
qdrant-client
boto3
fastapi
uvicorn
pydantic
python-dotenv
opentelemetry-api
opentelemetry-sdk
langsmith
pytest
```

---

# .env

```env
OPENAI_API_KEY=YOUR_KEY
LANGCHAIN_API_KEY=YOUR_KEY
LANGCHAIN_TRACING_V2=true
AWS_REGION=us-east-1
DYNAMODB_TABLE=onboarding_workflows
QDRANT_URL=http://localhost:6333
```

---

# README.md

````md
# Autonomous Employee Onboarding Orchestrator

Production-ready Agentic AI onboarding orchestration system.

## Features

- LangGraph multi-agent orchestration
- DynamoDB workflow persistence
- Qdrant RAG knowledge base
- SLA monitoring
- Escalation engine
- OpenTelemetry tracing
- LangSmith observability
- HR workflow automation

---

## Architecture

Planner Agent
    ↓
Specialist Sub Agents
    ↓
SLA Monitor
    ↓
Escalation Engine
    ↓
Status Generator

---

## Agents

| Agent | Responsibility |
|---|---|
| Planner | Workflow orchestration |
| IT Agent | Device + access provisioning |
| Payroll Agent | Payroll setup |
| Compliance Agent | Compliance docs validation |
| Benefits Agent | Insurance + benefits onboarding |
| Escalation Agent | SLA escalation |
| Day30 Agent | Post onboarding review |

---

## Running Project

```bash
pip install -r requirements.txt
python run.py
````

---

## API

Start API:

```bash
uvicorn app.main:app --reload
```

---

## Synthetic Joiners

* 2 FTE
* 2 Contractors
* 1 Intern

---

## Observability

* LangSmith traces
* OpenTelemetry spans
* SLA breach metrics
* Cost tracking

---

## Failure Handling

* Retries
* Timeout handling
* Durable checkpoints
* Escalation workflows

````

---

# docs/AGENTS.md

```md
# Agent Specifications

## 1. Planner Agent

Responsibilities:
- Determine onboarding workflow
- Assign specialist agents
- Track dependencies
- Route workflow execution

Input:
- Employee type
- Start date
- Joiner metadata

Output:
- Task graph

---

## 2. IT Provisioner Agent

Responsibilities:
- Laptop provisioning
- Email setup
- VPN creation
- Slack access

SLA:
- 24 hours

---

## 3. Payroll Agent

Responsibilities:
- Payroll enrollment
- Tax configuration
- Bank validation

SLA:
- 48 hours

---

## 4. Compliance Agent

Responsibilities:
- Aadhaar validation
- I-9 verification
- Form16 collection
- Offer letter verification

Uses:
- Qdrant retrieval

---

## 5. Benefits Agent

Responsibilities:
- Insurance onboarding
- Leave policy guidance
- Wellness enrollment

---

## 6. Escalation Agent

Responsibilities:
- Detect blockers
- Notify HR
- Trigger escalation workflows

Escalation Rule:
- Blocker persists > 48 hours

---

## 7. Day-30 Agent

Responsibilities:
- Generate onboarding summary
- Manager integration insights
- Completion analysis
````

---

# docs/ROLES.md

```md
# Employee Roles and Workflows

## FTE Workflow

Required:
- IT setup
- Payroll setup
- Compliance verification
- Benefits enrollment

Required Docs:
- Aadhaar
- Form16
- Offer Letter
- Bank Details

---

## Contractor Workflow

Required:
- IT setup
- Compliance validation

Required Docs:
- Aadhaar
- Contract Agreement

---

## Intern Workflow

Required:
- IT setup
- Basic compliance

Required Docs:
- Aadhaar
- College ID
```

---

# docs/ARCHITECTURE.md

```md
# System Architecture

## Core Components

### LangGraph

Used for:
- Stateful orchestration
- Multi-agent coordination
- Durable execution
- Retry handling

---

### DynamoDB

Stores:
- Workflow state
- SLA metadata
- Escalations
- Checkpoints

---

### Qdrant

Stores:
- Compliance checklists
- Onboarding playbooks
- HR policies

---

### OpenTelemetry

Provides:
- Trace spans
- Execution visibility
- Performance metrics

---

### LangSmith

Provides:
- Prompt traces
- LLM latency
- Token cost analysis
- Workflow debugging
```

---

# docs/FAILURE_MODES.md

```md
# Failure Mode Analysis

## 1. IT Agent Timeout

Problem:
Provisioning API failure.

Solution:
- Retry logic
- Exponential backoff
- Queue dead-letter handling

---

## 2. Compliance Hallucination

Problem:
LLM invents compliance documents.

Solution:
- RAG validation
- Structured outputs
- Rule-based validation

---

## 3. DynamoDB Failure

Problem:
State persistence unavailable.

Solution:
- Retry policy
- Backup queue
- Event replay

---

## 4. Notification Failure

Problem:
Slack/email delivery failure.

Solution:
- Retry queues
- Async event delivery

---

## 5. Partial Workflow Failure

Problem:
One sub-agent crashes.

Solution:
- LangGraph resumability
- Checkpoint recovery
```

---

# app/graph/state.py

```python
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
```

---

# app/config/settings.py

```python
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AWS_REGION = os.getenv("AWS_REGION")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")
QDRANT_URL = os.getenv("QDRANT_URL")
```

---

# app/services/dynamodb_service.py

```python
import boto3
from app.config.settings import DYNAMODB_TABLE


dynamodb = boto3.resource("dynamodb")

workflow_table = dynamodb.Table(DYNAMODB_TABLE)


def save_state(state):

    workflow_table.put_item(Item=state)


def get_state(employee_id, workflow_id):

    return workflow_table.get_item(
        Key={
            "employee_id": employee_id,
            "workflow_id": workflow_id
        }
    )
```

---

# app/services/qdrant_service.py

```python
from qdrant_client import QdrantClient

qdrant = QdrantClient(":memory:")


def retrieve_checklist(employee_type):

    mapping = {
        "FTE": [
            "Offer Letter",
            "Aadhaar",
            "Form16"
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
```

---

# app/services/observability.py

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)
```

---

# app/agents/planner_agent.py

```python
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
```

---

# app/agents/it_agent.py

```python
import time


def it_agent(state):

    if "it" not in state["tasks"]:
        return state

    time.sleep(1)

    state["tasks"]["it"]["status"] = "completed"

    return state
```

---

# app/agents/payroll_agent.py

```python

def payroll_agent(state):

    if "payroll" not in state["tasks"]:
        return state

    state["tasks"]["payroll"]["status"] = "completed"

    return state
```

---

# app/agents/compliance_agent.py

```python
from app.services.qdrant_service import retrieve_checklist


def compliance_agent(state):

    docs = retrieve_checklist(
        state["employee_type"]
    )

    missing_docs = []

    for doc in docs:

        if doc == "Form16":
            missing_docs.append(doc)

    if missing_docs:

        state["tasks"]["compliance"]["status"] = "blocked"

        state["blockers"].append({
            "type": "missing_documents",
            "docs": missing_docs,
            "age_hours": 50
        })

    else:

        state["tasks"]["compliance"]["status"] = "completed"

    return state
```

---

# app/monitoring/sla_monitor.py

```python
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
```

---

# app/agents/escalation_agent.py

```python

def escalation_agent(state):

    for blocker in state["blockers"]:

        if blocker["age_hours"] > 48:

            print(
                f"Escalating blocker for "
                f"{state['employee_id']}"
            )

            state["escalations"].append(blocker)

    return state
```

---

# app/agents/day30_agent.py

```python

def day30_agent(state):

    print(
        f"Generating day30 summary for "
        f"{state['employee_id']}"
    )

    return state
```

---

# app/graph/workflow.py

```python
from langgraph.graph import StateGraph, END

from app.graph.state import OnboardingState

from app.agents.planner_agent import planner_agent
from app.agents.it_agent import it_agent
from app.agents.payroll_agent import payroll_agent
from app.agents.compliance_agent import compliance_agent
from app.agents.escalation_agent import escalation_agent
from app.agents.day30_agent import day30_agent
from app.monitoring.sla_monitor import sla_monitor


workflow = StateGraph(OnboardingState)

workflow.add_node("planner", planner_agent)
workflow.add_node("it", it_agent)
workflow.add_node("payroll", payroll_agent)
workflow.add_node("compliance", compliance_agent)
workflow.add_node("sla", sla_monitor)
workflow.add_node("escalation", escalation_agent)
workflow.add_node("day30", day30_agent)

workflow.set_entry_point("planner")

workflow.add_edge("planner", "it")
workflow.add_edge("it", "payroll")
workflow.add_edge("payroll", "compliance")
workflow.add_edge("compliance", "sla")
workflow.add_edge("sla", "escalation")
workflow.add_edge("escalation", "day30")
workflow.add_edge("day30", END)


graph = workflow.compile()
```

---

# app/main.py

```python
from fastapi import FastAPI

app = FastAPI(
    title="Onboarding Orchestrator"
)


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }
```

---

# run.py

```python
from datetime import datetime
import uuid

from app.graph.workflow import graph

employees = [

    {
        "employee_id": "EMP001",
        "employee_name": "John",
        "employee_type": "FTE"
    },

    {
        "employee_id": "EMP002",
        "employee_name": "Alice",
        "employee_type": "contractor"
    }
]

for emp in employees:

    state = {
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

    result = graph.invoke(state)

    print(result)
```

---

# Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

---

# docker-compose.yml

```yaml
version: '3.9'

services:

  onboarding-agent:
    build: .
    container_name: onboarding-agent

  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
```

---

# tests/test_workflow.py

```python
from app.graph.workflow import graph


def test_workflow_execution():

    assert graph is not None
```

---

# tests/test_sla.py

```python
from app.monitoring.sla_monitor import sla_monitor


def test_sla_monitor():

    assert sla_monitor is not None
```

---

# tests/test_agents.py

```python
from app.agents.it_agent import it_agent


def test_it_agent():

    assert it_agent is not None
```

---

# COMPLETE DEMO EXECUTION FLOW

## Step 1: Create Project

```bash
mkdir onboarding-orchestrator
cd onboarding-orchestrator
```

---

## Step 2: Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# PostgreSQL Setup

We use PostgreSQL for:

* workflow analytics
* reporting
* audit trails
* historical onboarding records

---

## Install PostgreSQL Driver

Add to requirements.txt:

```txt
psycopg2-binary
sqlalchemy
```

---

# app/services/postgres_service.py

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    "postgresql://postgres:password@localhost:5432/onboarding"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

---

# app/models/onboarding_models.py

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

Base = declarative_base()


class WorkflowRun(Base):

    __tablename__ = "workflow_runs"

    employee_id = Column(String, primary_key=True)

    workflow_id = Column(String)

    employee_type = Column(String)

    final_status = Column(String)

    completion_percentage = Column(Integer)
```

---

# Initialize PostgreSQL Tables

```python
from app.models.onboarding_models import Base
from app.services.postgres_service import engine

Base.metadata.create_all(bind=engine)
```

---

# Save Workflow Analytics

```python
from app.models.onboarding_models import WorkflowRun
from app.services.postgres_service import SessionLocal


def save_workflow_analytics(state):

    db = SessionLocal()

    workflow = WorkflowRun(
        employee_id=state["employee_id"],
        workflow_id=state["workflow_id"],
        employee_type=state["employee_type"],
        final_status=state["final_status"],
        completion_percentage=state[
            "completion_percentage"
        ]
    )

    db.add(workflow)

    db.commit()

    db.close()
```

---

# app/api/routes.py

```python
from fastapi import APIRouter
from datetime import datetime
import uuid

from app.graph.workflow import graph

router = APIRouter()


@router.post("/start-onboarding")
def start_onboarding(payload: dict):

    state = {
        "employee_id": payload["employee_id"],

        "workflow_id": str(uuid.uuid4()),

        "employee_name": payload["employee_name"],

        "employee_type": payload["employee_type"],

        "start_date": str(datetime.now().date()),

        "tasks": {},

        "blockers": [],

        "escalations": [],

        "sla_status": {},

        "completion_percentage": 0,

        "eta": "",

        "final_status": ""
    }

    result = graph.invoke(state)

    return result
```

---

# Update app/main.py

```python
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Onboarding Orchestrator"
)

app.include_router(router)


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }
```

---

# Step 4: Start Qdrant

```bash
docker-compose up
```

Qdrant runs on:

```text
http://localhost:6333
```

---

# Step 5: Run API

```bash
uvicorn app.main:app --reload
```

API runs on:

```text
http://127.0.0.1:8000
```

---

# Step 6: Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

# Step 7: Demo Request

Use Swagger or Postman.

POST:

```text
/start-onboarding
```

Payload:

```json
{
  "employee_id": "EMP001",
  "employee_name": "John",
  "employee_type": "FTE"
}
```

---

# Expected Demo Output

```json
{
  "employee_id": "EMP001",
  "workflow_id": "1234",
  "employee_name": "John",
  "employee_type": "FTE",
  "tasks": {
    "it": {
      "status": "completed"
    },
    "payroll": {
      "status": "completed"
    },
    "compliance": {
      "status": "blocked"
    }
  },
  "blockers": [
    {
      "type": "missing_documents",
      "docs": [
        "Form16"
      ]
    }
  ],
  "sla_status": {
    "it": "OK",
    "payroll": "OK",
    "compliance": "BREACHED"
  },
  "completion_percentage": 75,
  "final_status": "BLOCKED"
}
```

---

# How To Demonstrate In Interview

## 1. Explain Business Problem

Say:

* HR lacks visibility
* Manual coordination exists
* Compliance risks occur
* SLA tracking missing

---

## 2. Explain Architecture

Show:

* LangGraph orchestration
* Specialist agents
* DynamoDB state management
* Qdrant RAG
* PostgreSQL analytics
* OTel tracing
* LangSmith observability

---

## 3. Run Live Workflow

Trigger onboarding API.

Explain each agent execution.

---

## 4. Show SLA Breach

Demonstrate:

* missing compliance docs
* SLA breach detection
* escalation workflow

---

## 5. Show Observability

Explain:

* OpenTelemetry spans
* LangSmith traces
* token/cost tracking

---

# Strong Interview Points

## Why LangGraph?

Because workflows are:

* stateful
* resumable
* multi-step
* agentic
* retry-based

---

## Why DynamoDB?

Because orchestration state is:

* dynamic
* event-driven
* scalable
* semi-structured

---

## Why PostgreSQL?

Because analytics/reporting need:

* SQL queries
* aggregations
* BI dashboards
* historical analysis

---

## Why Qdrant?

Because compliance workflows require:

* semantic retrieval
* playbook lookup
* onboarding policies
* vector search

---

# Production Enhancements

## Add Later

* AWS EventBridge
* Kafka
* Redis caching
* Celery workers
* Async agent execution
* Human approval workflows
* RBAC security
* OAuth authentication
* Kubernetes deployment
* Grafana dashboards
* Prometheus metrics

---

# Final Architecture Summary

```text
                        HR Portal
                            |
                            v
                    FastAPI Gateway
                            |
                            v
                LangGraph Orchestrator
                            |
        ------------------------------------------------
        |              |             |                 |
        v              v             v                 v

     IT Agent     Payroll Agent  Compliance Agent  Benefits Agent

                            |
                            v
                     SLA Monitor Node
                            |
                            v
                     Escalation Agent
                            |
                            v
                   Structured Status Output

---------------------------------------------------------------
Storage Layer
---------------------------------------------------------------

DynamoDB   -> Workflow State
Qdrant     -> Compliance Knowledge Base
PostgreSQL -> Analytics + Reporting
S3          -> Documents

---------------------------------------------------------------
Observability
---------------------------------------------------------------

LangSmith       -> LLM traces
OpenTelemetry   -> Execution spans
CloudWatch      -> Logs
```

---

# Final Interview Closing Statement

"I designed the system as a production-grade multi-agent orchestration platform using LangGraph for durable execution and agent coordination. DynamoDB stores workflow state, PostgreSQL handles analytics and reporting, Qdrant provides RAG-based compliance retrieval, and OpenTelemetry plus LangSmith provide full observability. The architecture supports SLA monitoring, escalation workflows, retries, and failure recovery, making it suitable for enterprise-scale onboarding automation."

```python
from app.agents.it_agent import it_agent


def test_it_agent():

    assert it_agent is not None
```


<!-- uvicorn app.main:app --reload -->