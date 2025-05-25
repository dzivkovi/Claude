import os
import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# MODEL = "claude-3-opus-20240229"
MODEL = "claude-opus-4-20250514"

prompt = "Generate a trivia question and an answer"
response = client.messages.create(
    model=MODEL,
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt}
    ]
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
