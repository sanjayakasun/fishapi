import os
import openai
from dotenv import load_dotenv
from .ontology_service import OntologyService

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")
    # Set default API key if .env loading fails
    os.environ.setdefault('DEEPSEEK_API_KEY', 'sk-e27dc948ee3545d5ab92fbafdf55b171')

class ChatbotService:
    def __init__(self):
        self.ontology_service = OntologyService()
        
        # Initialize DeepSeek client
        try:
            self.client = openai.OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com"
            )
        except Exception as e:
            print(f"Failed to initialize DeepSeek client: {e}")
            self.client = None

    def get_response(self, user_query):
        """Get chatbot response for user query"""
        try:
            # Query the ontology for relevant information
            context = self.ontology_service.query_ontology(user_query)
            
            if not context or "I have no information" in context:
                return "I don't have information about that fish species. Please ask about one of the Sri Lankan endemic fish species I know about."
            
            # Get LLM response
            if self.client:
                response = self._get_llm_response(user_query, context)
                return response
            else:
                return context
                
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}"

    def get_fish_information(self, fish_name):
        """Get basic information about a fish species for classification results"""
        try:
            # Map class names to vernacular names
            class_to_vernacular = {
                "Bulath_hapaya": "Bulath Hapaya",
                "Dankuda_pethiya": "Dankuda Pethiya", 
                "Depulliya": "Depulliya",
                "Halamal_dandiya": "Halamal Dandiya",
                "Lethiththaya": "Lethiththaya",
                "Pathirana_salaya": "Pathirana Salaya",
                "Thal_kossa": "Thal Kossa"
            }
            
            vernacular_name = class_to_vernacular.get(fish_name, fish_name)
            query = f"Tell me about {vernacular_name}"
            
            # Get basic information
            context = self.ontology_service.query_ontology(query)
            
            if context and "I have no information" not in context:
                # Return a brief summary for classification results
                return {
                    "name": vernacular_name,
                    "description": context[:200] + "..." if len(context) > 200 else context,
                    "full_info_available": True
                }
            else:
                return {
                    "name": vernacular_name,
                    "description": f"This appears to be a {vernacular_name}, but I don't have detailed information available.",
                    "full_info_available": False
                }
                
        except Exception as e:
            return {
                "name": fish_name,
                "description": f"Information about {fish_name} is not available at the moment.",
                "full_info_available": False
            }

    def _get_llm_response(self, user_query, context):
        """Get response from DeepSeek LLM"""
        try:
            system_prompt = """
            You are a specialized chatbot about endemic fish species of Sri Lanka.
            Your knowledge is strictly limited to the information provided in the 'CONTEXT' section.
            DO NOT use any external knowledge or make up information.
            Answer the user's question clearly and concisely based ONLY on the provided context.
            If the context does not contain the answer, say "I do not have that specific information in my knowledge base."
            Be helpful and provide detailed information when available.
            """
            
            completion = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"CONTEXT:\n---\n{context}\n---\n\nUSER QUESTION: {user_query}"}
                ],
                max_tokens=500,
                temperature=0.2
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            print(f"Error getting LLM response: {e}")
            return context
