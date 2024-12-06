import os
from dotenv import load_dotenv
from anthropic import AnthropicBedrock

load_dotenv()

ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "anthropic.claude-3-sonnet-20240307-v1:0")


def print_styled_stream(chunk_text: str, chunk_number: int = None):
    """
    Print streaming chunks with visual indicators and proper multi-line handling
    Uses a simple dot animation to show activity without disrupting text
    """
    # Print the indicator at the start of response only
    if chunk_number == 1:
        print("\n█ ", end="", flush=True)

    # Handle newlines specially
    if "\n" in chunk_text:
        lines = chunk_text.split("\n")
        for i, line in enumerate(lines):
            if line:
                if i > 0:  # For lines after a newline
                    print("\n█ " + line, end="", flush=True)
                else:  # For text before the first newline
                    print(line, end="", flush=True)
    else:
        print(chunk_text, end="", flush=True)


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
    print("\n🔷 Question:", message_content)

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
        print("🔶 Response:", end="")
        for chunk in stream:
            if chunk.type == "content_block_delta":
                chunk_text = chunk.delta.text
                full_response += chunk_text
                chunk_count += 1
                print_styled_stream(chunk_text, chunk_count)

        print("\n\n" + "━" * 50)  # Using box drawing characters for a cleaner look
        print("📝 Complete Response:")
        print("━" * 50)
        print(full_response)
        print("━" * 50)
        print(f"ℹ️ Received {chunk_count} chunks")

except Exception as e:  # pylint: disable=broad-except
    print(f"\n❌ Error occurred: {str(e)}")
