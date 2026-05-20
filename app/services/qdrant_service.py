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