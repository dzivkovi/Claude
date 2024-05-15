import os
import anthropic

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

prompt = "Generate a trivia question and an answer"
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    system="You are a trivia champion.",  # System instruction at top-level
    messages = [
     {"role": "user", "content": prompt}
    ]
)
print(message.content)
