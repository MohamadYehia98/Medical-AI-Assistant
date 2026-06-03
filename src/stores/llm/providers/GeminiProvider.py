from ..LLMInterface import LLMinterface
from google import genai
import logging
from ..LLMEnum import GEMINIENUMS


class GeminiProvider(LLMinterface):

    def __init__(self, api_key: str, api_url: str = None,
                 default_input_max_char: int = 1000, 
                 default_output_max_char: int = 1000,
                 temperature: float = 0.1,):
        
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max = default_input_max_char
        self.default_output_max = default_output_max_char
        self.default_temp = temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = genai.Client(
            api_key=self.api_key
        )
        
        self.enums = GEMINIENUMS
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):

         self.embedding_model_id = model_id
         self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max].strip()

    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int = None,
                      temperature: float = None):
        
        if not self.client:
            self.logger.error(" OpenAI client was not set")
            return None 
        
        if not self.generation_model_id:
            self.logger.error("Generation model for OpenAI was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_output_max
        temperature = temperature if temperature else self.default_temp

        chat_history.append(
            self.construct_prompt(prompt = prompt, role = GEMINIENUMS.USER.value)
        )

        response = self.client.models.generate_content(
            model=self.generation_model_id,
            contents=chat_history,
            config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
            },
            
        )

        if not response or not response.text or len(response.text) == 0 :
            self.logger.error(" Error while generation with Gemini")
            return None
        
        return response.text


    def embeded_text(self, text: str, document_type: str = None):

        if not self.client:
            self.logger.error(" Gemini client was not set")
            return None 
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for Gemini was not set")
            return None
        
        response = self.client.models.embed_content(

            model = self.embedding_model_id,
            contents = text,
        )
        
        if not response or not response.data or not len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Error while embedding text with Gemini")
            return None
        
        return response.embeddings[0].values
    
    def construct_prompt(self, prompt: str, role: str):

        return {
            "role" : role,
            "parts": [{"text": self.process_text(prompt)}],
        }