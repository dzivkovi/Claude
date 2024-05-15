import os
from dotenv import load_dotenv
from anthropic import AnthropicVertex

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION", "us-central1")
# Where the model is running. e.g. us-central1 or europe-west4 for haiku
MODEL = os.getenv("MODEL", "claude-3-sonnet@20240229")
# "claude-3-sonnet@20240229", "claude-3-haiku@20240307", "claude-3-opus@20240229"

# Debugging prints to verify environment variables
print(f"PROJECT_ID: {PROJECT_ID}")
print(f"REGION: {REGION}")
print(f"MODEL: {MODEL}")

client = AnthropicVertex(region=REGION, project_id=PROJECT_ID)

message = client.messages.create(
    model=MODEL,
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
)
print(message)
