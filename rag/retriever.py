from splitter import *
from llmclient import customLLMClient
from qdrant_client import QdrantClient, models # type: ignore
from qdrant_client.http import models as rest # type: ignore
from hashlib import sha256
from conf import *


class CustomRetriever:
    
    def __init__(self, in_server, in_collection:str, in_llmclient:customLLMClient) -> None:
        self.server = in_server
        self.con = QdrantClient(url=self.server)
        self.col = in_collection
        self.llm_client = in_llmclient

    def get_context(self, in_question) -> tuple:
        """
            Builds the context
            in this case its just joining several chunks
        """
        # if we want to do a hybrid RAG then we can now search for data on other 
        # sources and either rerank it or just smash it all together
        nodes =self.fetch_vectors(in_question=in_question)
        ctx = list()
        metadata = list()
        for n in nodes:
            ctx.append(n.payload["payload"])
            metadata.append(n.payload["metadata"])

        return (''.join(ctx), metadata)

    def fetch_vectors(self, in_question) -> list:
        """
            This actually performs que query to the db
        """
        # first we generate embeddings for the question
        qvector = self.llm_client.do_embeddings(in_question)
        qvector = qvector["embeddings"][0]
        # now we query the database
        nodes = self.con.search(query_vector=qvector, collection_name=COLLECTION)
        return nodes