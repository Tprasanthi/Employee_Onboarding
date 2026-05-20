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