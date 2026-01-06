from langchain_huggingface import HuggingFaceEmbeddings
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# docs = ["Hello world"]

# # load embedding model
# embedding_model = get_embeddings()

# # generate embeddings
# vectors = embedding_model.embed_documents(docs)

# print(vectors)
