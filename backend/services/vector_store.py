import chromadb

client = chromadb.PersistentClient(path="./vector_store")
collection = client.get_or_create_collection(name="documents")


def clear_old_embeddings():

    count = collection.count()

    if count > 0:

        results = collection.get()

        ids = results["ids"]

        collection.delete(ids=ids)

        print("Old embeddings cleared")

    else:

        print("ChromaDB is already empty")


def store_embeddings(chunks, embeddings):

    clear_old_embeddings()

    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )

    print("New embeddings stored successfully")


print("Collection:", collection.name)
print("Number of embeddings:", collection.count())
