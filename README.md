# AWS Bedrock Access Troubleshooter

Tools to validate and troubleshoot AWS Bedrock access for Anthropic's Claude models. Created after observing that while Claude works via direct API and Google Vertex AI, AWS Bedrock access needs special configuration.

## Problem Statement

The same code should work across platforms where Claude models and inference endpoints are hosted:

```python
# Works ✓ - Direct Anthropic API
python hi_claude.py  # Uses claude-3-opus-20240229

# Works ✓ - Google Vertex AI
python hi_claude_vertexai.py  # Uses claude-3-sonnet@20240229

# Fails ✗ - AWS Bedrock
python hi_claude_bedrock.py  # Rate limit errors
```

## Claude API Access Options

### 1. Direct Anthropic API

- Documentation: [Anthropic API Getting Started](https://docs.anthropic.com/en/api/getting-started)
- Requires API key from Anthropic console
- Straightforward implementation

### 2. Google Vertex AI

- Documentation: [Claude on Vertex AI](https://docs.anthropic.com/en/api/claude-on-vertex-ai)
- Requires Google Cloud project setup
- Generally available through Google Cloud

### 3. Amazon Bedrock

- Documentation: [Claude on Amazon Bedrock](https://docs.anthropic.com/en/api/claude-on-amazon-bedrock)
- Requires specific AWS setup (focus of this troubleshooter)
- Complex permissions and regional access requirements

## Authentication Setup

### AWS Credentials via Granted (Recommended)

[Granted](https://www.granted.dev/) provides secure AWS credential management:

1. Install [Granted](https://docs.commonfate.io/granted/getting-started):

   ```bash
   # macOS
   brew install common-fate/granted/granted

   # Windows (PowerShell as Admin)
   Set-ExecutionPolicy Bypass -Scope Process -Force
   iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/common-fate/granted/main/install.ps1'))
   ```

2. Use `assume` command:

   ```bash
   assume
   # Select profile using arrows or type to filter
   # Sets AWS environment variables automatically

3. Set AWS environment variables

   If `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are not set by the assume command:

   ```bash
   # Check current AWS environment variables
   env|grep AWS_
   AWS_PROFILE=profile-name
   AWS_DEFAULT_REGION=us-east-1
   AWS_REGION=us-east-1
   ```

   You will need to assume the role (e.g. "rad-bedrock-role") that can access Anthropic Claude inference endpoints in AWS Bedrock:

   ```bash
   $ aws sts get-caller-identity --query "Account" --output text
   123456789012

   $ acct=$(aws sts get-caller-identity --query "Account" --output text)

   $ eval $(aws sts assume-role --role-arn arn:aws:iam::${acct}:role/rad-bedrock-role --role-session-name "bedrock-client" | jq -r '"export AWS_ACCESS_KEY_ID=" + .Credentials.AccessKeyId, "export AWS_SECRET_ACCESS_KEY=" + .Credentials.SecretAccessKey, "export AWS_SESSION_TOKEN=" + .Credentials.SessionToken')

   $ env|grep AWS_
   AWS_PROFILE=profile-name
   AWS_DEFAULT_REGION=us-east-1
   AWS_REGION=us-east-1
   AWS_SECRET_ACCESS_KEY=value-one
   AWS_ACCESS_KEY_ID=value-two
   AWS_SESSION_TOKEN=value-three

   $ python hi_claude_bedrock.py
   Response: Hello! It's nice to meet you. How can I assist you today?
   Model: claude-3-sonnet-20240229
   Tokens: 20
   ```

## Tools Provided

1. `aws_bedrock_troubleshooting.ipynb`: Main diagnostic notebook
   - Checks AWS credentials
   - Validates Bedrock access
   - Tests different regions
   - Checks quotas and limits

2. `clean_notebooks.py`: Utility to clean notebook outputs

   ```bash
   # Clean specific notebook
   python clean_notebooks.py notebook.ipynb

   # Clean all notebooks
   python clean_notebooks.py
   ```

## Setup

1. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

2. Configure git hook for clean notebooks:

   ```bash
   mkdir -p .git/hooks
   cp pre-commit .git/hooks/
   chmod +x .git/hooks/pre-commit
   ```

## Usage

1. Run the troubleshooting notebook
2. Follow diagnostic steps
3. Check region-specific quotas
4. Verify IAM permissions

## Requirements

- Python 3.11+
- AWS CLI configured
- Required packages in `requirements.txt`

## Security Note

Always clean notebook outputs before committing:

- Removes sensitive AWS account info
- Clears execution counts and outputs
- Pre-commit hook handles this automatically
