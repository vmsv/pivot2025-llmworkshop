from pydantic import BaseModel, Field, model_serializer # type: ignore
from typing import List
"""
# Example RAG prompt
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
                              
You are a helpful assistant

{context}<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{question}<|eot_id|><|start_header_id|>assistant<|end_header_id|><|eot_id|>
                              
# Example NER prompt
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

you are a name entity recognition extractor. Provide the output in JSON format only
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{}<|eot_id|question><|start_header_id|>assistant<|end_header_id|><|eot_id|>
"""

class MessageItem(BaseModel):
    content: str = Field(default="", description="Content of the message item")

class SystemMessageItem(MessageItem):
    role: str = "system"
    instructions: str = Field(default="You are a helpfull assistant", description="Instructions to the system")
    context: str = Field(..., description="Context to be used")

    @model_serializer()
    def custom_serializer(self):
        return {"role": self.role, "content": '\n\n'.join([self.instructions, self.context])}

class UserMessageItem(MessageItem):
    role: str = "user"
    content: str = Field(..., description="Typically the question that needs to be made")

    @model_serializer()
    def custom_serializer(self):
        return {"role": self.role, "content": self.content}
    
class RAGPrompt(BaseModel):
    messages: List[SystemMessageItem|UserMessageItem]

    @model_serializer()
    def custom_serializer(self):
        o = list()
        for m in self.messages:
            o.append(m.model_dump())
        
        return {"model":"gemma3:4b","stream": False, "messages":o}
    
class NERPrompt(BaseModel):
    messages: List[UserMessageItem]

    @model_serializer()
    def custom_serializer(self):
        system_inst = SystemMessageItem(instructions="you are a name entity recognition extractor bot. Do not analise the content simply provide all the entities in JSON ingestable format", context="")
        o = list()
        o.append(system_inst.model_dump())
        for m in self.messages:
            o.append(m.model_dump())
        
        return {"model":"gemma3:4b","stream": False, "messages":o}