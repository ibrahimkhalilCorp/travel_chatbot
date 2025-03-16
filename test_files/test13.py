import chromadb

# Initialize a ChromaDB client (persistent or in-memory)
chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Persistent storage
# chroma_client = chromadb.Client()  # For in-memory storage

# Create or load a collection (like a table for vectors)
collection = chroma_client.get_or_create_collection(name="name_data")


def add_name_embedding(name, embedding):
    """
    Store a name and its vector embedding.
    """
    collection.add(
        ids=[name],  # Unique identifier
        embeddings=[embedding]  # Vector representation
    )


def search_name_embedding(query_embedding, top_k=1):
    """
    Search for the closest matching name based on the vector.
    """
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results


# Example Usage:
if __name__ == "__main__":
    sample_embedding = [0.1, 0.2, 0.3, 0.4]  # Replace with real embedding data
    add_name_embedding("Ibrahim", sample_embedding)

    search_results = search_name_embedding(sample_embedding)
    print(search_results)
