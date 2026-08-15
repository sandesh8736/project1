import os
from dotenv import load_dotenv

from huggingface_hub import InferenceClient
load_dotenv = load_dotenv()

# Get API key from environment variable
api_key = os.getenv("HF_TOKEN")

if not api_key:
    raise ValueError("HF_TOKEN environment variable is not set")


client = InferenceClient(
    api_key=api_key
)


def generate_answer(question, context):

    response = client.chat.completions.create(

        model="Qwen/Qwen2.5-7B-Instruct",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document question-answering assistant. "
                    "Answer the question using only the provided document context. "
                    "If the answer is not present in the context, "
                    "say that the answer is not available in the document."
                )
            },
            {
                "role": "user",
                "content": f"""
                Document Context:{context}
                Question:{question}
        
                Answer:
                """
            }
        ],

        max_tokens=500,
        temperature=0.2
    )

    return response.choices[0].message.content

if __name__ == "__main__":

    question = "What is the main topic of the document?"

    context = """
    Machine learning is a branch of artificial intelligence.
    It allows computers to learn patterns from data
    without being explicitly programmed for every task.
    """

    answer = generate_answer(
        question,
        context
    )

    print("\nAnswer:")
    print(answer)