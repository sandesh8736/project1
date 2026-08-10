from huggingface_hub import InferenceClient
import os

api_key = os.getenv("HF_TOKEN")

client = InferenceClient(
    token=api_key
)


def answer_question(question, chunks, chunk_embeddings, model, k=3):

    top_chunks = find_top_k_chunks(
        question,
        chunks,
        chunk_embeddings,
        k=k
    )

    context_text = "\n\n".join(top_chunks)

    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the question using only the provided "
                    "document excerpts. "
                    "If the answer isn't in the excerpts, "
                    "say so honestly."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Excerpts:\n{context_text}\n\n"
                    f"Question: {question}"
                )
            }
        ]
    )

    return response.choices[0].message.content