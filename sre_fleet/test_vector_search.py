from langchain_google_vertexai import VectorSearchVectorStore, VertexAIEmbeddings

# Initialize text-embedding configuration mapping
# Using text-embedding-004 as used during index generation
embeddings = VertexAIEmbeddings(model_name="text-embedding-004")

# Directly mount the managed collection
vector_store = VectorSearchVectorStore(
    project_id="ide-exp",
    region="us-central1",
    collection_id="8693488796127199232",
    embeddings=embeddings,
    api_version="v2" # Forces Vector Search 2.0 behaviors
)

try:
    # Search content natively without manual vector generation lines
    print("Searching for 'OOM'...")
    results = vector_store.similarity_search("OOM", k=3)
    if results:
        print(f"Found {len(results)} results.")
        print(f"Top result content: {results[0].page_content}")
    else:
        print("No results found.")
except Exception as e:
    print(f"Error during search: {e}")
