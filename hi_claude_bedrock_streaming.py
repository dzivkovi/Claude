import os
from typing import Any
from dotenv import load_dotenv
from anthropic import AnthropicBedrock

load_dotenv()

ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "anthropic.claude-3-sonnet-20240307-v1:0")


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

try:
    message_content = "Who is president of Canada?"

    # Create message and get streaming response
    with client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": message_content
        }],
        stream=True
    ) as stream:
        full_response = ""

        # Process the streaming response
        for chunk in stream:
            if chunk.type == "content_block_delta":
                chunk_text = chunk.delta.text
                full_response += chunk_text
                print("\n", chunk_text, end='', flush=True)

        print("\n\nFull response accumulated:")
        print(full_response)

except Exception as e:  # pylint: disable=broad-except
    print(f"Error occurred: {str(e)}")
