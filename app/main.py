from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router


app = FastAPI(
    title="Autonomous Onboarding Orchestrator",
    description="Production-grade multi-agent onboarding orchestration platform",
    version="1.0.0"
)


# ---------------------------------------------------------
# CORS CONFIGURATION
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# REGISTER ROUTES
# ---------------------------------------------------------

app.include_router(router)


# ---------------------------------------------------------
# ROOT ENDPOINT
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "Autonomous Onboarding Orchestrator Running"
    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ---------------------------------------------------------
# METRICS ENDPOINT
# ---------------------------------------------------------

@app.get("/metrics")
def metrics():

    return {
        "service": "onboarding-orchestrator",

        "agents": [
            "planner_agent",
            "it_agent",
            "payroll_agent",
            "compliance_agent",
            "benefits_agent",
            "escalation_agent",
            "day30_agent"
        ],

        "version": "1.0.0"
    }