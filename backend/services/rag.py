from services.retriver import retrieve_chunks
from services.llm import generate_answer


def answer_question(question, k=3):

    # 1. Retrieve relevant chunks from ChromaDB
    results = retrieve_chunks(question,k=k)

    # 2. Get documents from ChromaDB result
    chunks = results["documents"][0]

    # 3. Combine retrieved chunks
   # context = "\n\n".join(documents)



    # 4. Send context + question to LLM
    answer = generate_answer(question,chunks)

    return answer

"""if __name__ == "__main__":

    question = input("Ask a question: ")

    answer = answer_question(question)

    print("\nAnswer:")
    print(answer)"""