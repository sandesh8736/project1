from services.postgres_rag import PostgreSQLRAG


rag = PostgreSQLRAG(

    postgres_password="YOUR_POSTGRES_PASSWORD",

    hf_token="YOUR_HUGGINGFACE_TOKEN"
)


question = input(
    "Ask a question: "
)


answer = rag.answer_question(
    question,
    k=3
)


print("\nAnswer:")
print(answer)
