from sentence_transformers import SentenceTransformer


class MultimodalEmbeddings:

    def __init__(
        self,
        model_name="all-MiniLM-L6-v2",
        local_files_only=True,
    ):

        self.model_name = model_name
        self.local_files_only = local_files_only

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            self.model_name,
            local_files_only=self.local_files_only,
        )

        print("Embedding model loaded.")

    def generate_embeddings(self, chunks):

        if not chunks:
            return []

        texts = []

        for chunk in chunks:

            texts.append(
                chunk["content"]
            )

        print(
            f"Creating embeddings for "
            f"{len(texts)} chunks..."
        )

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )

        print(
            "Embedding generation complete."
        )

        print(
            "Number of embeddings:",
            len(embeddings)
        )

        print(
            "Embedding dimension:",
            embeddings.shape[1]
        )

        return embeddings
