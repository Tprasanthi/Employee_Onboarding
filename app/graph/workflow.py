from langgraph.graph import StateGraph
from state import OnboardingState
from app.agents.planner_agent import planner_node, it_agent, payroll_agent, compliance_agent, benefits_agent,sla_monitor, escalation_agent
workflow = StateGraph(OnboardingState)

workflow.add_node("planner", planner_node)
workflow.add_node("it", it_agent)
workflow.add_node("payroll", payroll_agent)
workflow.add_node("compliance", compliance_agent)
workflow.add_node("benefits", benefits_agent)
workflow.add_node("sla_monitor", sla_monitor)
workflow.add_node("escalation", escalation_agent)

workflow.set_entry_point("planner")

workflow.add_edge("planner", "it")
workflow.add_edge("planner", "payroll")
workflow.add_edge("planner", "compliance")
workflow.add_edge("planner", "benefits")

workflow.add_edge("it", "sla_monitor")
workflow.add_edge("payroll", "sla_monitor")
workflow.add_edge("compliance", "sla_monitor")
workflow.add_edge("benefits", "sla_monitor")

workflow.add_edge("sla_monitor", "escalation")

graph = workflow.compile()