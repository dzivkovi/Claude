# AWS Bedrock Access Troubleshooter

Tools to validate and troubleshoot AWS Bedrock access for Anthropic's Claude models. Created after observing that while Claude works via direct API and Google Vertex AI, AWS Bedrock access needs special configuration.

## Problem Statement

The same code works differently across platforms:

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

[Granted](https://docs.commonfate.io/granted/getting-started) provides secure AWS credential management:

1. Install Granted:

   ```bash
   # macOS
   brew install common-fate/granted/granted

   # Windows (PowerShell as Admin)
   Set-ExecutionPolicy Bypass -Scope Process -Force
   iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/common-fate/granted/main/install.ps1'))
   ```

2. Configure AWS profiles in `~/.aws/config`:

   ```ini
   [profile your-profile-name]
   region = us-east-1
   output = json
   ```

3. Use assume command:

   ```bash
   assume
   # Select profile using arrows or type to filter
   # Sets AWS environment variables automatically
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
