import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Path to folder containing .txt files
DOCUMENTS_FOLDER = "DSC20 Assignments"
TEST_QUERY = "Give me a really creative assignment for a final exam about recursion and inheritance"

# Load documents from .txt files
def load_documents(folder_path):
    documents = []
    file_paths = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                documents.append(file.read())
                file_paths.append(file_path)
    return documents, file_paths

# Generate embeddings using a SentenceTransformer model
def generate_embeddings(documents, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(documents, show_progress_bar=True)
    return embeddings, model

# Create FAISS index
def create_faiss_index(embeddings):
    embedding_dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dim)  # L2 similarity
    index.add(embeddings)
    return index

# Retrieve the most relevant documents
def retrieve_documents(query, model, index, documents, top_k=-1):
    if top_k < 0:
        top_k = len(documents)
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    return [(documents[i], distance) for i, distance in zip(indices[0], distances[0])]

# Main
if __name__ == "__main__":
    # Load documents
    documents, file_paths = load_documents(DOCUMENTS_FOLDER)
    print(f"Loaded {len(documents)} documents.")

    # Generate embeddings
    embeddings, model = generate_embeddings(documents)

    # Convert embeddings to FAISS index
    embeddings = np.array(embeddings).astype("float32")
    faiss_index = create_faiss_index(embeddings)
    print(faiss_index)

    # Example query
    query = TEST_QUERY
    results = retrieve_documents(query, model, faiss_index, documents, top_k=3)

    print("\nTop Results:")
    for i, (doc, dist) in enumerate(results):
        print(f"\nResult {i + 1} (Distance: {dist}):\n{doc[:200]}...")
