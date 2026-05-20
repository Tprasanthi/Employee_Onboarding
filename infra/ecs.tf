resource "aws_ecs_cluster" "onboarding_cluster" {

  name = "onboarding-agent-cluster"
}

resource "aws_ecs_task_definition" "onboarding_task" {

  family                   = "onboarding-agent-task"

  network_mode             = "awsvpc"

  requires_compatibilities = ["FARGATE"]

  cpu    = "512"

  memory = "1024"

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([

    {
      name  = "onboarding-agent"

      image = "onboarding-agent:latest"

      essential = true

      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "onboarding_service" {

  name            = "onboarding-agent-service"

  cluster         = aws_ecs_cluster.onboarding_cluster.id

  task_definition = aws_ecs_task_definition.onboarding_task.arn

  desired_count = 1

  launch_type = "FARGATE"

  network_configuration {

    subnets = [
      "subnet-xxxxxxxx"
    ]

    assign_public_ip = true

    security_groups = [
      "sg-xxxxxxxx"
    ]
  }
}