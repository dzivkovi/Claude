import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from anthropic import AnthropicBedrock
import time
from datetime import datetime

load_dotenv()


class BedrockConfig:
    """Configuration for Bedrock client"""
    MODELS = {
        # US West (Oregon) options
        "claude-3.5-sonnet-v2-west": {
            "id": "anthropic.claude-3-5-sonnet-20241022-v2:0",
            "region": "us-west-2",
            "type": "ON_DEMAND"
        },
        "claude-3-sonnet-west": {
            "id": "anthropic.claude-3-sonnet-20240229-v1:0",
            "region": "us-west-2",
            "type": "ON_DEMAND"
        },
        # Tokyo options (higher quotas)
        "claude-3.5-sonnet-tokyo": {
            "id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
            "region": "ap-northeast-1",
            "type": "ON_DEMAND"
        },
        "claude-3-haiku-tokyo": {
            "id": "anthropic.claude-3-haiku-20240307-v1:0",
            "region": "ap-northeast-1",
            "type": "ON_DEMAND"
        }
    }

    DEFAULT_MODEL = "claude-3-sonnet-west"
    MAX_RETRIES = 3
    BASE_DELAY = 5
    DEFAULT_MAX_TOKENS = 256


def extract_response_details(llm_response: Any, client_name: str = "anthropic") -> tuple:
    """
    Extracts the response details from the LLM API response object.
    """
    query_response = llm_response.content[0].text if hasattr(llm_response, 'content') else None
    llm_model = llm_response.model if hasattr(llm_response, 'model') else 'Unknown'
    if hasattr(llm_response, 'usage'):
        economic_unit = llm_response.usage.input_tokens + llm_response.usage.output_tokens
    else:
        economic_unit = 0
    return query_response, llm_model, economic_unit


class BedrockClient:
    def __init__(self, model_name: Optional[str] = None, region: Optional[str] = None):
        """
        Initialize Bedrock client with configurable model and region.

        Args:
            model_name: Name of the model from BedrockConfig.MODELS
            region: AWS region (if None, uses the model's default region)
        """
        self.model_name = model_name or BedrockConfig.DEFAULT_MODEL
        if self.model_name not in BedrockConfig.MODELS:
            raise ValueError(f"Model {model_name} not found in configuration")

        self.model_config = BedrockConfig.MODELS[self.model_name]
        self.region = region or self.model_config['region']

        self.client = self._initialize_client()

    def _initialize_client(self) -> AnthropicBedrock:
        """Initialize the Bedrock client with retry logic"""
        return AnthropicBedrock(
            aws_access_key=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            aws_region=self.region
        )

    def send_message(   # type: ignore
        self,
        message: str,
        max_tokens: Optional[int] = None,
        max_retries: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Send a message to the model with retry logic and error handling.

        Args:
            message: The message to send
            max_tokens: Maximum tokens for response
            max_retries: Maximum number of retry attempts
        """
        max_retries = max_retries or BedrockConfig.MAX_RETRIES
        max_tokens = max_tokens or BedrockConfig.DEFAULT_MAX_TOKENS

        for attempt in range(max_retries):
            try:
                response = self.client.messages.create(
                    model=self.model_config["id"],
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": message}],
                )

                query_response, llm_model, economic_unit = extract_response_details(
                    response
                )

                return {
                    "response": query_response,
                    "model": llm_model,
                    "tokens": economic_unit,
                    "timestamp": datetime.now().isoformat(),
                }

            except Exception as e:  # pylint: disable=broad-except
                wait_time = (2**attempt) * BedrockConfig.BASE_DELAY
                print(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")

                if attempt == max_retries - 1:
                    raise Exception(
                        f"Failed after {max_retries} attempts. Last error: {str(e)}"
                    )

                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)


def list_available_models():
    """List all available models and their configurations"""
    print("\nAvailable Models:")
    print("-" * 50)
    for name, config in BedrockConfig.MODELS.items():
        print(f"Model: {name}")
        print(f"  ID: {config['id']}")
        print(f"  Region: {config['region']}")
        print(f"  Type: {config['type']}")
        print("-" * 50)


if __name__ == "__main__":
    try:
        list_available_models()
        
        # Try different models in sequence to debug access
        models_to_try = [
            "claude-3.5-sonnet-v2-west",  # Try Oregon first
            "claude-3-sonnet-west",       # Fallback to Claude 3 in Oregon
            "claude-3.5-sonnet-tokyo",    # Try Tokyo if US West fails
            "claude-3-haiku-tokyo"        # Fastest model in Tokyo as last resort
        ]     
   
        for model_name in models_to_try:
            print(f"\nTrying model: {model_name}")
            try:
                client = BedrockClient(model_name=model_name)
                result = client.send_message(
                    "Hello, Claude",
                    max_tokens=256
                )
                print(f"Success with {model_name}!")
                print(f"Response: {result['response']}")
                break
            except Exception as e:
                print(f"Failed with {model_name}: {str(e)}")
                time.sleep(5)  # Wait before trying next model
                continue

    except Exception as e:
        print(f"Error: {str(e)}")
