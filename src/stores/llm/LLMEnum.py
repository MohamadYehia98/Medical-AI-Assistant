from enum import Enum

class LLEnum(Enum):
    
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    GEMINI = "GEMINI"

class OpenAIEnum(Enum):

   SYSTEM = "system"
   USER = "user"
   ASSISTENT = "assistant"

class CoHereEnum(Enum):

    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTENT = "CHATBOT"

    DOCUMENT = "search_document"
    QUERY = "search_query"

class GEMINIENUMS(Enum):

   SYSTEM = "system"
   USER = "user"
   ASSISTENT = "assistant"

class DocumentTypeEnum(Enum):

    DOCUMENT = "documnet"
    QUERY = "query"
