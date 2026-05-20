from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AWS_REGION = os.getenv("AWS_REGION")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")
QDRANT_URL = os.getenv("QDRANT_URL")