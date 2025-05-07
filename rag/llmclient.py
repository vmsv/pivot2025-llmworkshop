import requests
from prompts import *
from conf import *
import json
import httpx # type: ignore
import anyio # type: ignore

class customLLMClient:
    """
        An external client to use with rest interface enabled LLMS
    """

    def __init__(self, in_llm_url, in_debug:bool=False) -> None:

        self.url = in_llm_url.rstrip('/')
        self.endpoints = {"rag": f"{self.url}/api/chat", 
                          "ner": f"{self.url}/api/chat",
                          "embed": "http://ollama-embed-pivot2025:11433/api/embed"}
        self.debug = in_debug

    async def __async_embedding(self, data):
        """
            This code is not really used its just an example of async requests
            there will be out or order issues that need to be solved.
        """
        
        url = self.endpoints["embed"]
        
        async with httpx.AsyncClient() as client:
            return await client.post(url, json=data)

    def batch_emdeddings(self, data):
        """
            A stub for the async requests
        """
        tasks = list()
        for c in data:
            tasks.append(anyio.from_thread.run(self.__async_embedding, c))

        return tasks
    
    def do_embeddings(self, in_data:str, in_model:str=EMBED_MODEL) -> None:
        """
            Asks the inference engine to generate the embeddings
        """

        data = {"model": in_model, "input":in_data}
        print(data)
        if isinstance(in_data, str):
            response = requests.post(self.endpoints["embed"], json=data)
            if response.status_code == 200:
                try:
                    print(response.content)
                    data = json.loads(response.text)
                    return data
                except:
                    print("Error decoding embeddings")
                    return ""
        else:
            data_request = list(map(lambda X: {"model":in_model, "input": X}, in_data))
            data = self.batch_emdeddings(data_request)
            vectors = list()
            for v in data:
                if v.status_code == 200:
                    try:
                        vectors.append(json.loads(v.text)["data"][0]["embedding"])
                    except:
                        return None
            return vectors

    def do_rag(self, query:str, context:str) -> str:
        """
            Performs the RAG request based on the RAGPrompt
        """
        _sys = SystemMessageItem(context=context)
        _user = UserMessageItem(content=query)
        data = RAGPrompt(messages=[_sys, _user]).model_dump()
        
        print(f"DEBUG: Prompt ==> {data}")
        response = requests.post(self.endpoints["rag"], json=data)
        if response.status_code == 200:
            try:
                print(response.content)
                data = json.loads(response.text)
                return data
            except:
                print("Error decoding answer form LLM") 

    def do_ner(self, data: str) -> str:
        """
            Performs a NER request
        """
        p = NERPrompt(messages=[UserMessageItem(content=data)])
        
        response = requests.post(self.endpoints["ner"], json=p.model_dump())
        if self.debug:
            print(f"DEBUG: Prompt ==> {data}")

        if response.status_code == 200:
            try:
                data = json.loads(response.text)
                return data
            except:
                print("Error decoding answer form LLM")
        else:
            print(f"Inference engine replied with. Status code {response.status_code}")
            return None