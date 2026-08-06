from huggingface_hub import InferenceClient
import os

client = InferenceClient(
    provider="auto",  # lets HF pick a provider that's currently serving this model for free
    api_key=os.environ.get("HF_TOKEN"),
)

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",  # check huggingface.co/models for current availability if this errors
    messages=[
        {"role": "user", "content": "Say hello and tell me one fun fact about the number 7."}
    ]
)

print(response.choices[0].message.content)
