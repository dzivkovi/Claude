import boto3
import json
import time
from datetime import datetime


def check_quotas():
    quotas = boto3.client('service-quotas', region_name='us-east-1')
    try:
        # Check quotas in multiple regions
        regions = ['us-east-1', 'us-west-2', 'ap-northeast-1']

        for region in regions:
            print(f"\nQuotas in {region}:")
            quotas = boto3.client('service-quotas', region_name=region)
            response = quotas.list_service_quotas(ServiceCode='bedrock')

            for quota in response['Quotas']:
                if any(term.lower() in quota['QuotaName'].lower() for term in 
                      ['invoke', 'token', 'request', 'anthropic', 'claude']):
                    print(f"- {quota['QuotaName']}")
                    print(f"  Value: {quota['Value']}")
                    print(f"  Adjustable: {quota['Adjustable']}")
                    if quota['Value'] == 0:
                        print("  ⚠️ Zero quota!")

            # Also check bedrock directly for model-specific limits
            bedrock = boto3.client('bedrock', region_name=region)
            try:
                models = bedrock.list_foundation_models()
                print("\nModel-specific limits:")
                for model in models['modelSummaries']:
                    if 'claude' in model['modelId'].lower():
                        print(f"- {model['modelId']}")
                        print(f"  Types: {model.get('inferenceTypesSupported', [])}")
            except Exception as e:  # pylint: disable=broad-except
                print(f"Error checking models in {region}: {e}")
                
    except Exception as e:
        print(f"Error checking quotas: {e}")


def test_model(runtime, model_id, delay=30):
    print(f"\nTesting {model_id}...")
    try:
        response = runtime.invoke_model(
            modelId=model_id,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 256,
                "messages": [
                    {
                        "role": "user",
                        "content": "Say hello!"
                    }
                ]
            })
        )
        response_body = json.loads(response['body'].read())
        print(f"Response: {response_body['content'][0]['text']}")
        print(f"✓ Test successful!")
        return True
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error: {e}")
        print(f"Waiting {delay} seconds before next test...")
        time.sleep(delay)
        return False


def check_bedrock_access():
    print(f"\nTest started at: {datetime.now()}")
    print("-" * 50)

    # Check identity
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    print(f"\nRunning as: {identity['Arn']}")

    # Check quotas first
    check_quotas()

    # List models
    bedrock = boto3.client('bedrock', region_name='us-east-1')
    runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

    # Test models in order of likely success
    models_to_test = [
        "anthropic.claude-instant-v1",
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-sonnet-20240229-v1:0"
    ]

    for model_id in models_to_test:
        if test_model(runtime, model_id, delay=30):
            print("Successfully tested at least one model!")
            break

    print("\nTest completed!")


if __name__ == "__main__":
    check_bedrock_access()
