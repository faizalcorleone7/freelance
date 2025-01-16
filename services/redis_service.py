import redis
import os
from sentence_transformers import SentenceTransformer

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_index_if_not_exists():
    try:
        redis_client.ft("doc_index").info()
    except:
        index_creation = """
        FT.CREATE doc_index
            ON HASH
            PREFIX 1 doc:
            SCHEMA
                content TEXT
                embedding VECTOR FLAT 384 DISTANCE_METRIC COSINE
        """
        redis_client.execute_command(index_creation)

def process_document(content: str, doc_id: str):
    try:
        embedding = model.encode(content)
        redis_client.hset(
            f"doc:{doc_id}",
            mapping={
                "content": content,
                "embedding": embedding.tobytes()
            }
        )
        return True
    except Exception as e:
        print(f"Error processing document {doc_id}: {str(e)}")
        return False

def search_documents(query: str, top_k: int):
    try:
        query_embedding = model.encode(query)
        search_query = f"""
        FT.SEARCH doc_index '*=>[KNN {top_k} @embedding $embedding AS score]'
        PARAMS 2 embedding {query_embedding.tobytes()} DIALECT 2
        """
        results = redis_client.execute_command(search_query)
        search_results = []
        for i in range(1, len(results), 2):
            doc_id = results[i]
            doc_data = results[i + 1]
            search_results.append({
                "document_id": doc_id,
                "similarity_score": float(doc_data[1]),
                "content": doc_data[3]
            })
        return search_results

    except Exception as e:
        raise Exception(f"Error searching documents: {str(e)}")
