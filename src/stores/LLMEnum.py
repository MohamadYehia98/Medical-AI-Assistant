from enum import Enum

class LLEnum(Enum):
    
    OPENAI = "OPENAI"
    COHERE = "COHERE"

class OpenAIEnum(Enum):

   SYSTEM = "system"
   USER = "user"
   ASSISTENT = "assistant"