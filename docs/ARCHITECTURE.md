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