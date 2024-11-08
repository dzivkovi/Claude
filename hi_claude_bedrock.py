import os
from typing import Any
from dotenv import load_dotenv
from anthropic import AnthropicBedrock

load_dotenv()

# Also try
# "anthropic.claude-3-haiku-20240307-v1:0"
# "anthropic.claude-3-5-sonnet-20241022-v2:0"
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "anthropic.claude-3-sonnet-20240229-v1:0")

def extract_response_details(llm_response: Any, client_name: str) -> tuple:
    """
    Extracts the response details from the LLM API response object.
    """
    if client_name == 'azure' or client_name == 'azure_openai' or client_name == 'openai':
        query_response = llm_response.choices[0].message.content.strip() if hasattr(llm_response, 'choices') else None
        llm_model = llm_response.model if hasattr(llm_response, 'model') else 'Unknown'
        economic_unit = llm_response.usage.total_tokens if hasattr(llm_response, 'usage') else 0
    elif client_name == 'anthropic' or client_name == 'claude' or client_name == 'bedrock':
        query_response = llm_response.content[0].text if hasattr(llm_response, 'content') else None
        llm_model = llm_response.model if hasattr(llm_response, 'model') else 'Unknown'
        if hasattr(llm_response, 'usage'):
            economic_unit = llm_response.usage.input_tokens + llm_response.usage.input_tokens
        else:
            economic_unit = 0
    else:
        query_response = llm_model = 'Unknown'
        economic_unit = 0
    return query_response, llm_model, economic_unit


client = AnthropicBedrock(
    # Authenticate by either providing the keys below or use the default AWS credential providers, such as
    # using ~/.aws/credentials or the "AWS_SECRET_ACCESS_KEY" and "AWS_ACCESS_KEY_ID" environment variables.
    aws_access_key=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    # Temporary credentials can be used with aws_session_token.
    # Read more at https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html.
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    # aws_region changes the aws region to which the request is made. By default, we read AWS_REGION,
    # and if that's not present, we default to us-east-1. Note that we do not read ~/.aws/config for the region.
    aws_region="us-east-1",
)

response = client.messages.create(
    model=ANTHROPIC_MODEL,
    max_tokens=256,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude"
        }
    ],
)

# print(response)

query_response, llm_model, economic_unit = extract_response_details(response, "anthropic")

print(f"Response: {query_response}")
print(f"Model: {llm_model}")
print(f"Tokens: {economic_unit}")
