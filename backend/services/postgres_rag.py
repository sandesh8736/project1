import os
from dotenv import load_dotenv
from services.database.postgres_retriever import PostgreSQLRetriever
from huggingface_hub import InferenceClient

load_dotenv()
class PostgreSQLRAG:

    def __init__(self, postgres_password, hf_token):

        # Retriever
        self.retriever = PostgreSQLRetriever(password="Documind@123")

        # Hugging Face client
        hf_token = os.getenv("HF_TOKEN")

        if not hf_token:
            raise ValueError(
                "HF_TOKEN is not configured. "
                "Add it to .env or export it in the terminal."
            )

        self.client = InferenceClient(provider="featherless-ai",
          api_key=hf_token)

         # LLM
        self.model = "microsoft/Phi-3-mini-4k-instruct"

    # Ask question
 
    def answer_question(self,question,k=3,document_id=None):

    # Retrieve relevant chunks
        results = self.retriever.retrieve(question,k=k,document_id=document_id)

    # No results
         
        if not results:

            return {"answer": "I could not find relevant information in the documents.", "sources": []}

        # Build context
 
        context_parts = []

        sources = []

        for result in results:

            chunk_text = result["content"]
            document_id = result["document_id"]
            title = result["title"]
            page_id = result["page_id"]
            page_number = result.get("page_number")
            distance = result["distance"]

            context_parts.append(
                f"""
Document: {title}
Page Number: {page_number}

{chunk_text}
"""
            )

        sources.append({
            "document_id": document_id,
            "title": title,
            "page_number": page_number,
            "distance": distance
        })

        context = "\n\n".join(context_parts)

         # Prompt
        messages = [

            {
                "role": "system",

                "content": """
You are Documind AI.

Answer the user's question using only the provided document context.

If the answer is not present in the context, honestly say that the answer
was not found in the provided documents.

Do not invent information.
"""
            },

            {
                "role": "user",
                "content": f"""
Document Context:{context}
Question:{question}
"""
            }

        ]
         # Call LLM
        response = self.client.chat.completions.create(model=self.model,messages=messages,max_tokens=500,temperature=0.2)

        # Return answer
        answer = response.choices[0].message.content

        return {
            "answer": answer,
            "sources": sources
        }