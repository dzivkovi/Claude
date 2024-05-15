import os
from dotenv import load_dotenv
from anthropic import AnthropicVertex

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION", "us-central1")
MODEL = os.getenv("MODEL", "claude-3-sonnet@20240229")

# Where the model is running. e.g. us-central1 or europe-west4 for haiku


# Debugging prints to verify environment variables
print(f"PROJECT_ID: {PROJECT_ID}")
print(f"REGION: {REGION}")
print(f"MODEL: {MODEL}")

client = AnthropicVertex(region=REGION, project_id=PROJECT_ID)

# pylint: disable=E1129:not-context-manager
with client.messages.stream(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Send me a recipe for banana bread.",
        }
    ],
    model=MODEL,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
