from splitter import *
from llmclient import customLLMClient
from qdrant_client import QdrantClient, models # type: ignore
from qdrant_client.http import models as rest # type: ignore
from hashlib import sha256
from conf import *

class Indexer:
    def __init__(self, in_server:str, in_collection:str, in_llmclient:customLLMClient):
        self.server = in_server
        self.col = in_collection
        self.splitter = MySplit()
        self.llm_client = in_llmclient
        
        self.con = QdrantClient(url=self.server)
        
        if not self.con.collection_exists(self.col):
            self.con.create_collection(
                collection_name=self.col,
                # This size is dependent of the model used to generate the embeddings
                # you can check it by making a embedding request to the system
                # one of the parameters in the reply is the size
                vectors_config=models.VectorParams(size=EMBED_DIMESION_SIZE, distance=models.Distance.COSINE),
            )
    
    def index(self, data, metadata):
        """
            Index data 
        """

        # first we split the text
        # if its not already splitted
        if not isinstance(data, list):
            chunks = self.splitter.split_text(data)
            doc_hash = sha256(''.join(data).encode('utf-8')).hexdigest()
        else:
            chunks = data
            doc_hash = sha256(data.encode('utf-8')).hexdigest()

        metadata["doc_hash"] = doc_hash
        # add data hash and store it on metadata to avoid duplicate docs
        # TODO: make a query to the db and see if any doc has the same doc_hash

        # for each chunk we need to prepare the insertion
        # this depends highly on the vector db used
        points = list() 
        metalist = list()
        ids = list()
        i = 0
        for c in chunks:
            lmeta = metadata.copy()
            # you can generate a UUID as an ID for the chunk or just an integer 
            # and store it assoicated with the chunk hash to avoid duplicate chunks.
            lmeta["chunk_hash"] = sha256(c.encode('utf-8')).hexdigest()
            # because this vector db also does fulltext search we store the 
            # chunk data in it also, along with other metadata sent to us
            payload = {"payload": c, "metadata":lmeta}
            print(f"Using local embedding: {LOCAL_EMBEDDING}")
            if LOCAL_EMBEDDING is False:
                vectors = self.llm_client.do_embeddings(c, EMBED_MODEL)
                # the reply from the inference engine has more data but we don't care about it
                vectors = vectors["embeddings"][0]
                points.append(models.PointStruct(id=i,vector=vectors, payload=payload))
                i = i+1
            else:
                ids.append(id)
                metalist.append(payload)
                
        try:
            
            if LOCAL_EMBEDDING is True:
                # We are using local embedding from Qdrant for the sake of 
                # demo speed
                operation_info = self.con.add(collection_name=self.col, documents=chunks, ids=ids, metadata=metalist)
            else:
                # split pints into batches
                # 32 is usually a good size 
                for batch in [points[i : i + 32] for i in range(0, len(points), 32)]:
                    operation_info = self.con.upsert(collection_name=self.col, points=batch)
            return operation_info
        
        except Exception as e:
            print(f"Error adding points to vectordb. Message: {e}")
    
        return {"n_chunks": len(chunks)}