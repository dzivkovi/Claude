# Claude Code AWS Bedrock Configuration

This guide covers switching Claude Code from Anthropic's SaaS API to your organization's AWS Bedrock environment, including model discovery, configuration, and troubleshooting.

## Prerequisites

Before configuring Claude Code for AWS Bedrock, ensure you have:

1. **AWS CLI configured** with appropriate credentials
2. **AWS Bedrock access** through your organization's AWS account
3. **Required IAM permissions** for Bedrock model access
4. **Claude Code installed** in your WSL/development environment

## Setup script for Claude 4/3.7 Sonnet models

```bash
#!/bin/bash
# Claude Code AWS Bedrock Configuration

# Enable Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export DISABLE_PROMPT_CACHING=1

# Required fast model (Claude Code dependency)
export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-3-5-haiku-20241022-v1:0'

# Choose your main model:
export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-20250514-v1:0'        # Recommended: Latest, best availability
# export ANTHROPIC_MODEL='us.anthropic.claude-3-7-sonnet-20250219-v1:0'   # Alternative: Extended thinking, may hit 429 limits

echo "✅ Claude Code configured for AWS Bedrock"
echo "🤖 Main model: $ANTHROPIC_MODEL"
```

### Finding Available Models

**Check your available Claude inference profiles:**

```bash
# List Claude models available in your account (cross-regional)
aws bedrock list-inference-profiles --region us-east-1 \
  --query 'inferenceProfileSummaries[?contains(inferenceProfileName, `Claude`)].{Name:inferenceProfileName, ID:inferenceProfileId}' \
  --output table
```

**Example output:**

```bash
---------------------------------------------------------------------------------------
|                                ListInferenceProfiles                                |
+-----------------------------------------------+-------------------------------------+
|                      ID                       |                Name                 |
+-----------------------------------------------+-------------------------------------+
|  us.anthropic.claude-3-sonnet-20240229-v1:0   |  US Anthropic Claude 3 Sonnet       |
|  us.anthropic.claude-3-opus-20240229-v1:0     |  US Anthropic Claude 3 Opus         |
|  us.anthropic.claude-3-haiku-20240307-v1:0    |  US Anthropic Claude 3 Haiku        |
|  us.anthropic.claude-3-5-sonnet-20240620-v1:0 |  US Anthropic Claude 3.5 Sonnet     |
|  us.anthropic.claude-3-5-haiku-20241022-v1:0  |  US Anthropic Claude 3.5 Haiku      |
|  us.anthropic.claude-3-5-sonnet-20241022-v2:0 |  US Anthropic Claude 3.5 Sonnet v2  |
|  us.anthropic.claude-3-7-sonnet-20250219-v1:0 |  US Anthropic Claude 3.7 Sonnet     |
|  us.anthropic.claude-sonnet-4-20250514-v1:0   |  US Claude Sonnet 4                 |
|  us.anthropic.claude-opus-4-20250514-v1:0     |  US Claude Opus 4                   |
+-----------------------------------------------+-------------------------------------+
```

**Switch models between sessions:**

```bash
# Change model and resume session
export ANTHROPIC_MODEL='us.anthropic.claude-3-7-sonnet-20250219-v1:0'
claude --continue

# Switch back to Claude 4
export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-20250514-v1:0' 
claude --continue
```

## Model Naming Conventions Across Platforms

Understanding model naming helps when transitioning between platforms:

| Platform | Example Model Name | Notes |
|----------|-------------------|-------|
| **Anthropic SaaS** | `claude-3-sonnet-20240229` | Simple date-based naming |
| **AWS Bedrock** | `anthropic.claude-3-sonnet-20240229-v1:0` | Includes provider prefix and version |
| **Google Vertex AI** | `claude-3-sonnet@20240229` | Uses @ symbol for versioning |
| **Azure OpenAI** | `claude-3-sonnet-deployment` | Custom deployment names |

**AWS Bedrock Inference Profile IDs** (recommended for cross-region availability):

- Use the `us.anthropic.*` prefix for inference profiles
- These automatically route across all US regions
- Better availability than region-specific model IDs

## Persistent Environment Configuration

Add to your `~/.bashrc` for permanent configuration:

```bash
# Tell Claude Code to use AWS Bedrock instead of Anthropic's SaaS API
export CLAUDE_CODE_USE_BEDROCK=1
# Disable prompt caching (unless you've enabled it with AWS)
export DISABLE_PROMPT_CACHING=1
# Main model - Claude Sonnet 4 (most advanced available to you)
export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-20250514-v1:0'
# Small/fast model - Claude 3.5 Haiku (required by Claude Code)
export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-3-5-haiku-20241022-v1:0'
```

Apply changes:

```bash
source ~/.bashrc
```

## Validating Configuration

### Check Claude Code Status

After configuration, verify Claude Code is using Bedrock:

```bash
claude
```

Then use the `/status` command:

```bash
> /status

Claude Code Status v1.0.3

Working Directory 
 L /mnt/c/Users/username/ws/LLMs/Claude

Account • /login
 L Login Method: API Key (/login managed key)
 L Organization: YourCompany
 L Email: your.email@company.com

Memory • /memory
 L project: CLAUDE.md

Model • /model
 L us.anthropic.claude-3-7-sonnet-20250219-v1:0
```

**Key indicators of successful Bedrock configuration:**

- Model shows the `us.anthropic.*` format (inference profile ID)
- No authentication errors when sending messages  
- Models respond successfully through Bedrock backend
- Note: Login Method still shows "API Key" even when using Bedrock

### Test Basic Functionality

```bash
# In Claude Code session
> hello world
```

Should receive a response confirming the model is working through Bedrock.

## Troubleshooting

### Common Issues and Solutions

**1. Authentication Errors**

```bash
# Verify AWS credentials
aws sts get-caller-identity

# Check Bedrock access
aws bedrock list-foundation-models --region us-east-1
```

**2. Model Not Found Errors**

```bash
# List available models in your account
aws bedrock list-inference-profiles --region us-east-1

# Verify model access permissions
aws bedrock get-inference-profile --inference-profile-identifier us.anthropic.claude-sonnet-4-20250514-v1:0
```

**3. Rate Limiting (429 Errors)**

- Claude 3.7 Sonnet often hits rate limits due to high demand
- Switch to Claude 4 Sonnet for better availability:

  ```bash
  export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-20250514-v1:0'
  ```

**4. Region Availability Issues**

- Use inference profiles (`us.anthropic.*`) instead of region-specific models
- Inference profiles automatically route to available regions

### Using Repository Diagnostic Tools

This repository includes specialized Bedrock troubleshooting tools:

```bash
# Clone and setup (if not already done)
git clone <repository-url>
cd Claude
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-bedrock.txt

# Run comprehensive diagnostics
python bedrock/check_bedrock_access.py
python bedrock/check_bedrock_quotas.py

# Test specific Claude models
python hi_claude_bedrock.py
python hi_claude_bedrock_streaming.py

# Interactive troubleshooting
jupyter notebook bedrock/aws_bedrock_troubleshooting.ipynb
```

## Performance Notes

- **Inference Profiles**: Provide better availability and performance than regional models
- **Streaming**: Use streaming responses for better perceived performance
- **Model Selection**: Claude 4 Sonnet currently has better availability than Claude 3.7 Sonnet
- **Caching**: Disabled for Bedrock to avoid compatibility issues

## Security Best Practices

- **Never commit AWS credentials** to version control
- **Use IAM roles** instead of long-term access keys when possible
- **Rotate credentials regularly** per your organization's policy
- **Use least-privilege permissions** for Bedrock access
- **Monitor usage** through AWS CloudTrail and billing alerts

## Notes

- Inference profiles route across all US regions automatically
- Models cannot be switched mid-session; use `--continue` with new ENV vars
- Claude 3.7 Sonnet experiences 429 errors due to high demand for extended thinking features
- Claude Sonnet 4 recommended for better availability and superior performance
- Requires AWS credentials: `aws configure`
