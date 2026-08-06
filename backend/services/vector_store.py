import chromadb

client = chromadb.PersistentClient(path="./vector_store")

collection = client.get_or_create_collection(name="documents")

def store_embeddings(chunks,embeddings):

    ids = []

    for i in range (len(chunks)):
        ids.append(str(i))

    collection.add(
        ids = ids,
        documents = chunks,
        embeddings = embeddings.tolist()
    )

    print("Stored Successfully") 
