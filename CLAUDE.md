# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an AWS Bedrock access troubleshooter and multi-platform Claude API testing repository. It provides tools to validate and troubleshoot access to Anthropic's Claude models across three platforms:

1. **Direct Anthropic API** - Standard implementation using `anthropic` client
2. **Google Vertex AI** - Using `AnthropicVertex` client  
3. **AWS Bedrock** - Using `AnthropicBedrock` client (primary focus)

## Common Commands

### Environment Setup
```bash
# Install main dependencies
pip install -r requirements.txt

# Install minimal Bedrock-only dependencies
pip install -r requirements-bedrock.txt
```

### Running Tests
```bash
# Test direct Anthropic API
python hi_claude.py

# Test Google Vertex AI (requires PROJECT_ID and REGION env vars)
python hi_claude_vertexai.py

# Test AWS Bedrock (requires AWS credentials)
python hi_claude_bedrock.py

# Test Bedrock streaming
python hi_claude_bedrock_streaming.py

# Run comprehensive Bedrock diagnostics
python bedrock/check_bedrock_access.py
python bedrock/check_bedrock_quotas.py
```

### Notebook Management
```bash
# Clean all notebook outputs (removes sensitive data)
python clean_notebooks.py

# Clean specific notebook
python clean_notebooks.py bedrock/aws_bedrock_troubleshooting.ipynb
```

## Architecture

### Core Components

- **Client Examples**: `hi_claude*.py` files demonstrate identical functionality across different Claude hosting platforms
- **Bedrock Diagnostics**: `bedrock/` directory contains specialized tools for AWS Bedrock troubleshooting
- **Response Extraction**: Common `extract_response_details()` function in `hi_claude_bedrock.py` handles response parsing across different API formats
- **Notebook Utilities**: `clean_notebooks.py` provides secure notebook output cleaning for git commits

### Authentication Patterns

Each platform uses different authentication:
- **Anthropic**: `ANTHROPIC_API_KEY` environment variable
- **Vertex AI**: Google Cloud credentials + `PROJECT_ID`/`REGION` env vars  
- **Bedrock**: AWS credentials via standard AWS credential chain or explicit env vars (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`)

### Model Naming Conventions

Models use different naming patterns across platforms:
- **Anthropic**: `claude-3-opus-20240229`
- **Vertex AI**: `claude-3-sonnet@20240229` 
- **Bedrock**: `anthropic.claude-3-sonnet-20240229-v1:0`

## Development Notes

### AWS Bedrock Specifics
- Requires specific IAM role assumptions (see README for "rad-bedrock-role" example)
- Region-specific model availability varies
- Complex permission requirements often cause issues
- Use diagnostic notebooks for systematic troubleshooting

### Security Practices
- Always clean notebook outputs before committing (use `clean_notebooks.py`)
- Never commit AWS credentials or sensitive account information
- Environment variables used for all API keys and configuration

### Testing Strategy
- Cross-platform compatibility testing using identical prompts
- Token counting validation across different response formats
- Region and quota validation for Bedrock deployments