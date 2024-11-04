import boto3
import json
import time
from datetime import datetime
def check_bedrock_access():
    print(f"\nTest started at: {datetime.now()}")
    print("-" * 50)

    # 1. First check identity
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    print("\nRunning as:")
    print(f"User ARN: {identity['Arn']}")

    # 2. List available models
    bedrock = boto3.client('bedrock', region_name='us-west-2')
    runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

    print("\nChecking available models...")
    try:
        models = bedrock.list_foundation_models()
        for model in models['modelSummaries']:
            if 'claude' in model['modelId'].lower():
                print(f"Found: {model['modelId']} - {model.get('inferenceTypesSupported', [])}")
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error listing models: {e}")

    # 3. Try a simple inference
    print("\nTesting inference with Claude Instant...")
    try:
        response = runtime.invoke_model(
            modelId="anthropic.claude-instant-v1",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 256,
                "messages": [
                    {
                        "role": "user",
                        "content": "Say hello and confirm you're working!"
                    }
                ]
            })
        )
        response_body = json.loads(response['body'].read())
        print(f"Response: {response_body['content'][0]['text']}")
        print("✓ Inference test successful!")
    except Exception as e:
        print(f"Error with inference: {e}")

    # 4. Try Claude 3 Sonnet
    print("\nTesting Claude 3 Sonnet...")
    try:
        response = runtime.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 256,
                "messages": [
                    {
                        "role": "user",
                        "content": "Say hello and confirm you're Claude 3!"
                    }
                ]
            })
        )
        response_body = json.loads(response['body'].read())
        print(f"Response: {response_body['content'][0]['text']}")
        print("✓ Claude 3 test successful!")
    except Exception as e:
        print(f"Error with Claude 3: {e}")

    print("\nTest completed!")


if __name__ == "__main__":
    check_bedrock_access()
