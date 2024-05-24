import os
from dotenv import load_dotenv
from anthropic import AnthropicBedrock

load_dotenv()


client = AnthropicBedrock(
    # Authenticate by either providing the keys below or use the default AWS credential providers, such as
    # using ~/.aws/credentials or the "AWS_SECRET_ACCESS_KEY" and "AWS_ACCESS_KEY_ID" environment variables.
    aws_access_key=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    # Temporary credentials can be used with aws_session_token.
    # Read more at https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html.
    # aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
    # aws_region changes the aws region to which the request is made. By default, we read AWS_REGION,
    # and if that's not present, we default to us-east-1. Note that we do not read ~/.aws/config for the region.
    aws_region="us-east-1",
)

response = client.messages.create(
    model="anthropic.claude-3-sonnet-20240229-v1:0",  # "anthropic.claude-3-haiku-20240307-v1:0",
    max_tokens=256,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude"
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
