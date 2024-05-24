#OPENAI_API_VERSION=2024-05-01-preview   
#OPENAI_API_VERSION=2024-02-01
OPENAI_API_VERSION=2023-05-15

curl -X POST "https://magmainc.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=$OPENAI_API_VERSION" \
-H "Content-Type: application/json" \
-H "api-key: $AZURE_OPENAI_API_KEY" \
-d '{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Once upon a time"}
  ],
  "max_tokens": 50,
  "temperature": 0.7,
  "top_p": 1.0,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0
}'
