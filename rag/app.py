from fastapi import FastAPI, Request, File, UploadFile # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from pydantic import BaseModel, Field # type: ignore
import time
from pdf_loader import *
import uvicorn # type: ignore
from indexer import Indexer
from qdrant_client import QdrantClient # type: ignore
from prompts import *
from llmclient import *
from conf import *
import secrets
import re
import sys
from retriever import *

#qdrantcon = QdrantClient(url=QDRANT_URL)

# WEB API
llm_client = customLLMClient(LLM_EXTERNAL_URL)
indexer = Indexer(in_collection=COLLECTION, in_server=VECTORDB, in_llmclient=llm_client)

# Create a class for the input data
class InputData(BaseModel):
    text: str
    metadata: dict
    options: dict

class InputQuery(BaseModel):
    query: str
    debug: bool = Field(default=False, description="Defines if debug should be set for the chain steps")
    options: dict

app = FastAPI()

@app.post("/api/v1/upload/file")
async def create_upload_file(file: UploadFile = File(...), request: Request=None):
    """
        Just simple way to upload a file
    """
    random_file_name = secrets.token_hex(24)
    random_file_path = "/tmp/" + random_file_name
    data = file.file.read()    
    try:
        with open(random_file_path, "wb") as fp:
            fp.write(data)
    except Exception as e:
        print("Error writing file")
        return JSONResponse({"result": "ko", "message":"Unable to save file"})
    
    return JSONResponse({"result": "ok", "message":"File uploaded", "details": {"filename":random_file_name}})

@app.post("/api/v1/index/document", response_class=JSONResponse)
def indexdoc(in_data: InputData, request: Request=None):
    """
        Document indexer
        First the doc must be uploaded
    """
    start_time = time.time()
    # Get the prompt from the input data
    file_name = in_data.text
    metadata = in_data.metadata
    options = in_data.options
    
    try:
        if options["type"] == 'file':
            # just make sure there is no path traversal
            if bool(re.search(r'^[a-z0-9]*$', file_name)) is False:
                return JSONResponse({"result":"ko", "msg":"Error on data", "time":time.time()-start_time, "details":{}})

            file_content = loadPdf(in_file="/tmp/"+file_name).get_text()
            result = indexer.index(file_content, metadata=metadata)

    except KeyError as e:
        return JSONResponse({"result":"ko", "msg":"Index type was not defined", "time":time.time()-start_time, "details":{e}})

    return JSONResponse({"result":"ok", "msg": "Doc was indexeed", "time": time.time() - start_time})

@app.post("/api/v1/ner", response_class=JSONResponse)
async def ner(in_data: InputQuery, request: Request=None):
    """
        Ner query endpoint
    """
    start_time = time.time()
    output = dict()
    output["reply"] = dict()
    output["request"] = in_data.model_dump()
    output["notes"] = list()

    llm_client = customLLMClient(LLM_EXTERNAL_URL)
    output["LLM_external"] = True
    output["LLM_url"] = LLM_EXTERNAL_URL
    
    ner_data = llm_client.do_ner(in_data.query)
    try:
        data = ner_data["choices"][0]["message"]["content"]
    except TypeError:
        pass
    
    output["reply"] = {"answer": data, "nodes": [], "iocs": []}
    output["timetook"] = time.time() - start_time
    return JSONResponse(output)

@app.post("/api/v1/embed", response_class=JSONResponse)
async def embed(in_data: InputQuery, request: Request=None):
    """
        embed query endpoint
    """
    start_time = time.time()
    output = dict()
    output["reply"] = dict()
    output["request"] = in_data.model_dump()
    output["configuration"] = {"LLM_external": True, "LLM_url": LLM_EXTERNAL_URL}
    
    
    embeddings_data = llm_client.do_embeddings(in_data=in_data.query, model=EMBED_MODEL)
    try:
        data = embeddings_data["data"][0]["embedding"]
    except TypeError:
        pass

    output["reply"] = {"embeddings": data, "size": len(data)}
    output["timetook"] = time.time() - start_time
    return JSONResponse(output)

@app.post("/api/v1/query", response_class=JSONResponse)
async def query(request: Request, in_data: InputQuery):
    """
        Regular query endpoint
    """
    start_time = time.time()
    output = dict()
    output["reply"] = dict()
    output["request"] = in_data.model_dump()
    output["configuration"] = {"LLM_external": True, "LLM_url": LLM_EXTERNAL_URL, "Local_embedding": LOCAL_EMBEDDING}
    used_chunks = list()
    iocs = list()

    output["request_type"] = "llm"
    
   
    meta = dict()
    llm_client = customLLMClient(LLM_EXTERNAL_URL)
    retriever = CustomRetriever(in_server=VECTORDB, in_collection=COLLECTION, in_llmclient=llm_client)
    nodes = list()
    print(f"Sending query to LLM")
    (context, nodes) = retriever.get_context(in_data.query)
    print(f"Context: {context}\n\n\n Nodes: {nodes}")
    rag_data = llm_client.do_rag(query=in_data.query, context=context)

    for n in nodes:
        try:
            del n["vector"]
            del n["order_value"]
            del n["version"]
        except KeyError:
            pass
        

    output["reply"] = {"answer": rag_data, "nodes": nodes }
    output["timetook"] = time.time() - start_time
    return JSONResponse(output)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")