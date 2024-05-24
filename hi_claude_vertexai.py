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

response = client.messages.create(
    model=MODEL,
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
)

# print(response)

if hasattr(response, 'choices'):    # OpenAI completion API returns a list of choices
    query_response = response.choices[0].message.content

elif hasattr(response, 'content'):  # Anthropic messaging API returns a content object
    query_response = response.content[0].text
else:
    query_response = None

llm_model = response.model if hasattr(response, 'model') else MODEL

input_tokens = response.usage.input_tokens if hasattr(response, 'usage') else 0
output_tokens = response.usage.input_tokens if hasattr(response, 'usage') else 0
economic_unit = input_tokens + output_tokens

print(f"Response: {query_response}")
print(f"Model: {llm_model}")
print(f"Input Tokens: {input_tokens}")
print(f"Output Tokens: {output_tokens}")
print(f"Tokens: {economic_unit}")
