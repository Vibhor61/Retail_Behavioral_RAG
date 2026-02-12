import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
import os

df = pd.read_parquet("Data/Final_Table.parquet")

client = chromadb.PersistentClient(path="chroma_store")
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="jinaai/jina-embeddings-v2-base-en",trust_remote_code=True)
collection_semantic = client.get_or_create_collection(name = "Semantic_Embeddings",embedding_function = emb_fn)

collection_semantic.add(
    ids = df["product_id"].astype(str).tolist(),
    documents = df["Embeddings card"].astype(str).tolist()
)

collection_sops = client.get_or_create_collection(name = "SOPs_Embeddings",embedding_function = emb_fn)

def sops_emb(path="Data/SOPs/"):
    for filename in os.listdir(path):
        if filename.endswith(".md"):
            sop_id = filename.split('_')[0] 
            
            with open(os.path.join(path, filename), "r", encoding="utf-8") as f:
                content = f.read()
        
            collection_sops.add(
                ids = [sop_id],
                documents = [content]
            )
        
sops_emb()


