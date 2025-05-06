from sentence_transformers import SentenceTransformer

class Embedder():

    def __init__(self):
        self.model = SentenceTransformer("jinaai/jina-embeddings-v3", trust_remote_code=True, revision="main")


    def get_embed_for_index(self, data):
        task = "retrieval.passage"
        if isinstance(data, str):
            data = [data]
        embeddings = self.model.encode(
            data,
            ask=task,
            prompt_name=task,
        )
        return embeddings

    def get_embed_for_query(self, query):
        task = "retrieval.query"
        if isinstance(query, str):
            query = [query]
        embeddings = self.model.encode(query,
                                       ask=task,
                                       prompt_name=task)
        return embeddings
    
if __name__ == "__main__":
    emb = Embedder()
    try:
        import sys
        data = sys.argv[1]
        _e = emb.get_embed_for_index(data)
        print(_e)
        print("Done")
    except:
        print("You need to provide some text to be embedded")
