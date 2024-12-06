import os
import sys
from typing import Any
from dotenv import load_dotenv
from anthropic import AnthropicBedrock

load_dotenv()

ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "anthropic.claude-3-sonnet-20240307-v1:0")


def print_streaming_chunk(chunk_text: str, chunk_number: int = None):
    """
    Print streaming chunks in a visually pleasing way.
    Option 1: Simple continuous printing (most common approach)
    """
    print(chunk_text, end="", flush=True)


def print_streaming_chunk_debug(chunk_text: str, chunk_number: int = None):
    """
    Option 2: Debug version with chunk information
    Useful when you need to see exact chunk boundaries
    """
    print(f"[Chunk {chunk_number:3d}] '{chunk_text}'")


def print_streaming_chunk_progress(chunk_text: str, chunk_number: int = None):
    """
    Option 3: Progress indicator version
    Shows a spinning cursor while receiving chunks
    """
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    sys.stdout.write(f"\r{spinner[chunk_number % len(spinner)]} {chunk_text}")
    sys.stdout.flush()


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
    print("\nQuestion:", message_content)
    print("\nResponse:", end=" ")

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
        chunk_count = 0

        # Process the streaming response
        for chunk in stream:
            if chunk.type == "content_block_delta":
                chunk_text = chunk.delta.text
                full_response += chunk_text
                chunk_count += 1

                # Choose one of these printing methods:
                print_streaming_chunk(chunk_text)  # Option 1: Simple continuous
                # print_streaming_chunk_debug(chunk_text, chunk_count)  # Option 2: Debug view
                # print_streaming_chunk_progress(chunk_text, chunk_count)  # Option 3: Progress indicator

        print("\n\n" + "="*50)
        print("Full accumulated response:")
        print("="*50)
        print(full_response)
        print("="*50)
        print(f"Total chunks received: {chunk_count}")

except Exception as e:  # pylint: disable=broad-except
    print(f"\nError occurred: {str(e)}")
