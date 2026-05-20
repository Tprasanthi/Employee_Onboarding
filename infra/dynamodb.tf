provider "aws" {
  region = "us-east-1"
}

resource "aws_dynamodb_table" "onboarding_workflows" {

  name         = "onboarding_workflows"

  billing_mode = "PAY_PER_REQUEST"

  hash_key = "employee_id"

  range_key = "workflow_id"

  attribute {
    name = "employee_id"
    type = "S"
  }

  attribute {
    name = "workflow_id"
    type = "S"
  }

  attribute {
    name = "final_status"
    type = "S"
  }

  global_secondary_index {

    name = "status-index"

    hash_key = "final_status"

    projection_type = "ALL"
  }

  tags = {
    Environment = "dev"
    Project     = "onboarding-agent"
  }
}