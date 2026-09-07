import os
from huggingface_hub import InferenceClient


token = os.getenv("HF_TOKEN")

if not token:
    raise ValueError("HF_TOKEN is not set")


client = InferenceClient(
    provider="featherless-ai",
    api_key=token
)


response = client.chat.completions.create(
    model="microsoft/Phi-3-mini-4k-instruct",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "What is RAG?"
        }
    ],
    max_tokens=150
)


print("\nAnswer:")
print(response.choices[0].message.content)