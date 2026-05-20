from datetime import datetime
import random

from app.services.qdrant_service import retrieve_checklist
from app.services.dynamodb_service import save_state


def compliance_agent(state):

    """
    Compliance Collector Agent

    Responsibilities:
    - Validate onboarding documents
    - Verify compliance checklist
    - Detect missing documents
    - Raise blockers if documents missing

    Uses:
    - Qdrant RAG retrieval
    """

    print(
        f"\n📄 Compliance Agent started for "
        f"{state['employee_id']}"
    )

    # -----------------------------------------------------
    # CHECK IF COMPLIANCE TASK EXISTS
    # -----------------------------------------------------

    if "compliance" not in state["tasks"]:

        print(
            f"\nℹ️ Compliance not required for "
            f"{state['employee_type']}"
        )

        return state

    # -----------------------------------------------------
    # RETRIEVE REQUIRED DOCUMENTS
    # -----------------------------------------------------

    required_docs = retrieve_checklist(
        state["employee_type"]
    )

    print(
        f"\n📚 Required Documents: {required_docs}"
    )

    # -----------------------------------------------------
    # SIMULATE DOCUMENT UPLOADS
    # -----------------------------------------------------

    uploaded_docs = []

    for doc in required_docs:

        uploaded = random.choice([True, False])

        if uploaded:

            uploaded_docs.append(doc)

    # -----------------------------------------------------
    # FIND MISSING DOCUMENTS
    # -----------------------------------------------------

    missing_docs = list(
        set(required_docs) - set(uploaded_docs)
    )

    # -----------------------------------------------------
    # HANDLE BLOCKERS
    # -----------------------------------------------------

    if missing_docs:

        blocker = {

            "type": "missing_documents",

            "docs": missing_docs,

            "status": "BLOCKED",

            "age_hours": 50,

            "created_at": datetime.now().isoformat()
        }

        state["blockers"].append(blocker)

        state["tasks"]["compliance"]["status"] = "blocked"

        print(
            f"\n❌ Missing Documents for "
            f"{state['employee_id']}"
        )

        print(missing_docs)

    else:

        state["tasks"]["compliance"]["status"] = "completed"

        print(
            f"\n✅ Compliance completed for "
            f"{state['employee_id']}"
        )

    # -----------------------------------------------------
    # STORE DETAILS
    # -----------------------------------------------------

    state["tasks"]["compliance"]["details"] = {

        "required_documents": required_docs,

        "uploaded_documents": uploaded_docs,

        "missing_documents": missing_docs,

        "verified_at": datetime.now().isoformat()
    }

    # -----------------------------------------------------
    # SAVE STATE
    # -----------------------------------------------------

    save_state(state)

    return state