"""
RAG (Retrieval-Augmented Generation) Service for Fish Ontology
Combines OWL ontology retrieval with DeepSeek LLM generation
"""
import os
import openai
from dotenv import load_dotenv
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS, Namespace
from django.conf import settings
import json
import re

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")
    os.environ.setdefault('DEEPSEEK_API_KEY', 'sk-e27dc948ee3545d5ab92fbafdf55b171')

class RAGService:
    def __init__(self):
        self.client = None
        self.graph = None
        self.fish_species_mapping = {}
        self._initialize_deepseek()
        self._load_ontology()
        self._extract_fish_data()

    def _initialize_deepseek(self):
        """Initialize DeepSeek API client"""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if api_key:
            try:
                self.client = openai.OpenAI(
                    api_key=api_key,
                    base_url="https://api.deepseek.com"
                )
                print("DeepSeek API client initialized successfully")
            except Exception as e:
                print(f"Failed to initialize DeepSeek client: {e}")
        else:
            print("DEEPSEEK_API_KEY not found in environment variables")

    def _load_ontology(self):
        """Load the fish ontology from OWL file"""
        try:
            ontology_path = os.path.join(settings.BASE_DIR, 'fish6species(1).owl')
            if os.path.exists(ontology_path):
                self.graph = Graph()
                self.graph.parse(ontology_path, format="xml")
                print(f"OWL Ontology loaded successfully from {ontology_path}")
            else:
                print(f"OWL file not found at {ontology_path}")
                self._create_fallback_data()
        except Exception as e:
            print(f"Error loading OWL ontology: {e}")
            self._create_fallback_data()

    def _extract_fish_data(self):
        """Extract comprehensive fish data from the OWL ontology"""
        if not self.graph:
            return
        
        # Define namespaces
        fish_ns = Namespace("http://www.freshwaterfish.org/ontology#")
        
        # Enhanced query for comprehensive data extraction
        query = """
        SELECT ?fish ?scientificName ?commonName ?sinhalaName ?family ?order ?habitat ?maxLength ?iucnStatus ?description ?morphology ?ecology ?diet ?reproduction ?distribution ?specificLocation ?statusNotes ?authority ?etymology ?colourVariants ?temperatureRange ?phRange ?dhRange ?latitude ?region ?countries ?threatToHumans ?fisheriesValue ?aquariumGroupSize ?aquariumTankSize ?hatching ?freeSwimming ?maturity ?commonLength ?subfamily
        WHERE {
            ?fish rdf:type fish:FishSpecies .
            ?fish fish:ScientificName ?scientificName .
            ?fish fish:CommonName ?commonName .
            ?fish fish:SinhalaName ?sinhalaName .
            ?fish fish:Family ?family .
            ?fish fish:Order ?order .
            ?fish fish:Habitat ?habitat .
            ?fish fish:MaximumLengthCm ?maxLength .
            ?fish fish:IUCNStatus ?iucnStatus .
            ?fish fish:MorphologyDescription ?description .
            OPTIONAL { ?fish fish:MorphologyDescription ?morphology }
            OPTIONAL { ?fish fish:EcologyBehavior ?ecology }
            OPTIONAL { ?fish fish:Diet ?diet }
            OPTIONAL { ?fish fish:Reproduction ?reproduction }
            OPTIONAL { ?fish fish:Distribution ?distribution }
            OPTIONAL { ?fish fish:SpecificLocation ?specificLocation }
            OPTIONAL { ?fish fish:StatusNotes ?statusNotes }
            OPTIONAL { ?fish fish:Authority ?authority }
            OPTIONAL { ?fish fish:Etymology ?etymology }
            OPTIONAL { ?fish fish:ColourMorphsVariants ?colourVariants }
            OPTIONAL { ?fish fish:TemperatureRange ?temperatureRange }
            OPTIONAL { ?fish fish:PHRange ?phRange }
            OPTIONAL { ?fish fish:DHRange ?dhRange }
            OPTIONAL { ?fish fish:Latitude ?latitude }
            OPTIONAL { ?fish fish:Region ?region }
            OPTIONAL { ?fish fish:Countries ?countries }
            OPTIONAL { ?fish fish:ThreatToHumans ?threatToHumans }
            OPTIONAL { ?fish fish:FisheriesValue ?fisheriesValue }
            OPTIONAL { ?fish fish:AquariumGroupSize ?aquariumGroupSize }
            OPTIONAL { ?fish fish:AquariumMinimumTankSizeCm ?aquariumTankSize }
            OPTIONAL { ?fish fish:Hatching ?hatching }
            OPTIONAL { ?fish fish:FreeSwimmingAfter ?freeSwimming }
            OPTIONAL { ?fish fish:Maturity ?maturity }
            OPTIONAL { ?fish fish:CommonLengthCm ?commonLength }
            OPTIONAL { ?fish fish:Subfamily ?subfamily }
        }
        """
        
        results = self.graph.query(query)
        
        for row in results:
            fish_uri = str(row.fish)
            scientific_name = str(row.scientificName)
            common_name = str(row.commonName)
            sinhala_name = str(row.sinhalaName)
            family = str(row.family)
            order = str(row.order)
            habitat = str(row.habitat)
            max_length = str(row.maxLength)
            iucn_status = str(row.iucnStatus)
            description = str(row.description)
            
            # Create a key for mapping
            key = scientific_name.lower().replace(' ', '_')
            
            self.fish_species_mapping[key] = {
                "id": fish_uri,
                "scientific": scientific_name,
                "vernacular": sinhala_name,
                "common": common_name,
                "family": family,
                "order": order,
                "habitat": habitat,
                "max_length": max_length,
                "iucn_status": iucn_status,
                "description": description,
                "morphology": str(row.morphology) if row.morphology else "",
                "ecology": str(row.ecology) if row.ecology else "",
                "diet": str(row.diet) if row.diet else "",
                "reproduction": str(row.reproduction) if row.reproduction else "",
                "distribution": str(row.distribution) if row.distribution else "",
                "specific_location": str(row.specificLocation) if row.specificLocation else "",
                "status_notes": str(row.statusNotes) if row.statusNotes else "",
                "authority": str(row.authority) if row.authority else "",
                "etymology": str(row.etymology) if row.etymology else "",
                "colour_variants": str(row.colourVariants) if row.colourVariants else "",
                "temperature_range": str(row.temperatureRange) if row.temperatureRange else "",
                "ph_range": str(row.phRange) if row.phRange else "",
                "dh_range": str(row.dhRange) if row.dhRange else "",
                "latitude": str(row.latitude) if row.latitude else "",
                "region": str(row.region) if row.region else "",
                "countries": str(row.countries) if row.countries else "",
                "threat_to_humans": str(row.threatToHumans) if row.threatToHumans else "",
                "fisheries_value": str(row.fisheriesValue) if row.fisheriesValue else "",
                "aquarium_group_size": str(row.aquariumGroupSize) if row.aquariumGroupSize else "",
                "aquarium_tank_size": str(row.aquariumTankSize) if row.aquariumTankSize else "",
                "hatching": str(row.hatching) if row.hatching else "",
                "free_swimming": str(row.freeSwimming) if row.freeSwimming else "",
                "maturity": str(row.maturity) if row.maturity else "",
                "common_length": str(row.commonLength) if row.commonLength else "",
                "subfamily": str(row.subfamily) if row.subfamily else ""
            }
        
        print(f"Extracted comprehensive data for {len(self.fish_species_mapping)} fish species from OWL ontology")

    def _create_fallback_data(self):
        """Create fallback data when OWL loading fails"""
        print("Creating fallback data...")
        self.fish_species_mapping = {
            "puntius_titteya": {
                "id": "http://www.freshwaterfish.org/ontology#Puntius_titteya",
                "scientific": "Puntius titteya",
                "vernacular": "le titteya",
                "common": "cherry barb",
                "family": "Cyprinidae",
                "order": "Cypriniformes",
                "habitat": "Freshwater, prefers still pools over fast-flowing areas",
                "max_length": "5.0 cm TL",
                "iucn_status": "Vulnerable (VU)",
                "description": "Cherry Barb has an elongated body with a pair of maxillary barbels"
            }
        }

    def get_response(self, user_query):
        """Main RAG method: Retrieve relevant information and generate response"""
        try:
            # Step 1: Retrieve relevant information from ontology
            retrieved_info = self._retrieve_information(user_query)
            
            # Step 2: Generate response using DeepSeek with retrieved context
            response = self._generate_response(user_query, retrieved_info)
            
            return response
            
        except Exception as e:
            print(f"Error in RAG service: {e}")
            return f"I'm sorry, I encountered an error while processing your query: {str(e)}"

    def _retrieve_information(self, user_query):
        """Retrieve relevant information from the ontology based on user query"""
        query_lower = user_query.lower()
        
        # Find relevant fish species
        relevant_fish = self._find_relevant_fish(query_lower)
        
        # Extract specific information based on query intent
        retrieved_data = {
            "relevant_fish": relevant_fish,
            "query_intent": self._analyze_query_intent(query_lower),
            "context": self._build_context(relevant_fish, query_lower)
        }
        
        return retrieved_data

    def _find_relevant_fish(self, query):
        """Find fish species relevant to the query"""
        relevant_fish = []
        
        # Check for scientific names
        for key, info in self.fish_species_mapping.items():
            if info['scientific'].lower() in query:
                relevant_fish.append((key, info, "scientific"))
        
        # Check for vernacular names
        for key, info in self.fish_species_mapping.items():
            vernacular = info['vernacular'].lower()
            if vernacular in query or any(part in query for part in vernacular.split()):
                relevant_fish.append((key, info, "vernacular"))
        
        # Check for common names
        for key, info in self.fish_species_mapping.items():
            common = info['common'].lower()
            if common in query or any(part in query for part in common.split(',')):
                relevant_fish.append((key, info, "common"))
        
        # Check for specific known variations
        variations = {
            "bulath hapaya": "pethia_nigrofasciata",
            "bulath": "pethia_nigrofasciata",
            "hapaya": "pethia_nigrofasciata",
            "depulliya": "pethia_cumingii",
            "two spot": "pethia_cumingii",
            "cuming": "pethia_cumingii",
            "cherry barb": "puntius_titteya",
            "titteya": "puntius_titteya",
            "barred danio": "devario_pathirana",
            "pathirana": "devario_pathirana",
            "combtail": "belontia_signata",
            "thal kossa": "belontia_signata",
            "thalkossa": "belontia_signata",
            "blotched": "dawkinsia_srilankensis",
            "filamented": "dawkinsia_srilankensis",
            "mal pethiya": "dawkinsia_srilankensis"
        }
        
        for variation, key in variations.items():
            if variation in query and key in self.fish_species_mapping:
                relevant_fish.append((key, self.fish_species_mapping[key], "variation"))
        
        return relevant_fish

    def _analyze_query_intent(self, query):
        """Analyze what type of information the user is asking for"""
        intent_keywords = {
            "habitat": ["habitat", "where", "live", "environment", "water", "stream", "river"],
            "conservation": ["conservation", "threat", "endangered", "vulnerable", "status", "iucn"],
            "appearance": ["appearance", "look", "color", "size", "morphology", "shape", "body"],
            "behavior": ["behavior", "behaviour", "ecology", "feeding", "diet", "reproduction"],
            "distribution": ["distribution", "location", "found", "range", "basin", "district"],
            "aquarium": ["aquarium", "tank", "captive", "breeding", "care", "maintenance"],
            "general": ["tell me", "about", "information", "what is", "describe"]
        }
        
        for intent, keywords in intent_keywords.items():
            if any(keyword in query for keyword in keywords):
                return intent
        
        return "general"

    def _build_context(self, relevant_fish, query):
        """Build comprehensive context from relevant fish data"""
        if not relevant_fish:
            return "No specific fish species mentioned in the query."
        
        context_parts = []
        
        for fish_key, fish_info, match_type in relevant_fish:
            fish_context = f"""
Fish Species: {fish_info['vernacular']} ({fish_info['scientific']})
Common Name: {fish_info['common']}
Family: {fish_info['family']}
Order: {fish_info['order']}
IUCN Status: {fish_info['iucn_status']}
Maximum Length: {fish_info['max_length']}
Habitat: {fish_info['habitat']}
Description: {fish_info['description']}
"""
            
            # Add specific information based on query intent
            if fish_info.get('morphology'):
                fish_context += f"Morphology: {fish_info['morphology']}\n"
            if fish_info.get('ecology'):
                fish_context += f"Ecology & Behavior: {fish_info['ecology']}\n"
            if fish_info.get('diet'):
                fish_context += f"Diet: {fish_info['diet']}\n"
            if fish_info.get('distribution'):
                fish_context += f"Distribution: {fish_info['distribution']}\n"
            if fish_info.get('specific_location'):
                fish_context += f"Specific Locations: {fish_info['specific_location']}\n"
            if fish_info.get('status_notes'):
                fish_context += f"Conservation Notes: {fish_info['status_notes']}\n"
            if fish_info.get('colour_variants'):
                fish_context += f"Color Variants: {fish_info['colour_variants']}\n"
            if fish_info.get('temperature_range'):
                fish_context += f"Temperature Range: {fish_info['temperature_range']}\n"
            if fish_info.get('ph_range'):
                fish_context += f"pH Range: {fish_info['ph_range']}\n"
            if fish_info.get('aquarium_group_size'):
                fish_context += f"Aquarium Group Size: {fish_info['aquarium_group_size']}\n"
            if fish_info.get('aquarium_tank_size'):
                fish_context += f"Aquarium Tank Size: {fish_info['aquarium_tank_size']}\n"
            
            context_parts.append(fish_context)
        
        return "\n".join(context_parts)

    def _generate_response(self, user_query, retrieved_data):
        """Generate response using DeepSeek LLM with retrieved context"""
        if not self.client:
            return self._fallback_response(user_query, retrieved_data)
        
        try:
            # Build system prompt
            system_prompt = """You are an expert ichthyologist specializing in Sri Lankan endemic freshwater fish species. 
            You have access to comprehensive information about 6 endemic fish species from an OWL ontology.
            
            IMPORTANT INSTRUCTIONS:
            1. Keep responses CONCISE and DIRECT - answer only what was asked
            2. Avoid lengthy introductions or overviews unless specifically requested
            3. For simple greetings like "hi", give a brief welcome and ask what they want to know
            4. For specific questions, provide focused answers without extra background information
            5. Use bullet points and clear formatting for easy reading
            6. Be conversational but brief
            
            Examples:
            - "hi" → "Hello! What would you like to know about Sri Lankan fish?"
            - "habitat of bulath hapaya" → Direct habitat information only
            - "girlfriend of bulath hapaya" → Explain it's the female of the species, no extra details
            
            Always base your responses on the provided context data."""
            
            # Build user prompt with context
            user_prompt = f"""
            Context Information:
            {retrieved_data['context']}
            
            User Query: {user_query}
            
            Provide a CONCISE response that directly answers the user's question. 
            - Keep it brief and to the point
            - Use bullet points for easy reading
            - Only include information relevant to the specific question asked
            - Avoid lengthy introductions or extra background information
            """
            
            # Call DeepSeek API
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error calling DeepSeek API: {e}")
            return self._fallback_response(user_query, retrieved_data)

    def _fallback_response(self, user_query, retrieved_data):
        """Fallback response when DeepSeek API is not available"""
        if not retrieved_data['relevant_fish']:
            return "Hello! What would you like to know about Sri Lankan fish?"
        
        # Build response from retrieved data
        response_parts = []
        
        for fish_key, fish_info, match_type in retrieved_data['relevant_fish']:
            response = f"""**{fish_info['vernacular']}** ({fish_info['scientific']})

**Scientific Name**: {fish_info['scientific']}
**Vernacular Name**: {fish_info['vernacular']}
**Common Name**: {fish_info['common']}
**Family**: {fish_info['family']}
**Order**: {fish_info['order']}
**IUCN Status**: {fish_info['iucn_status']}
**Maximum Length**: {fish_info['max_length']}
**Habitat**: {fish_info['habitat']}

**Description**: {fish_info['description']}"""
            
            # Add specific information based on query intent
            intent = retrieved_data['query_intent']
            
            if intent == "habitat" and fish_info.get('specific_location'):
                response += f"\n\n**Specific Locations**: {fish_info['specific_location']}"
            if intent == "conservation" and fish_info.get('status_notes'):
                response += f"\n\n**Conservation Notes**: {fish_info['status_notes']}"
            if intent == "appearance" and fish_info.get('morphology'):
                response += f"\n\n**Morphology**: {fish_info['morphology']}"
            if intent == "behavior" and fish_info.get('ecology'):
                response += f"\n\n**Ecology & Behavior**: {fish_info['ecology']}"
            if intent == "aquarium" and fish_info.get('aquarium_group_size'):
                response += f"\n\n**Aquarium Care**: Group size: {fish_info['aquarium_group_size']}"
                if fish_info.get('aquarium_tank_size'):
                    response += f", Minimum tank size: {fish_info['aquarium_tank_size']}"
            
            response_parts.append(response)
        
        return "\n\n".join(response_parts)

    def get_fish_information(self, fish_name):
        """Get basic information about a fish species for classification results"""
        found_fish = self._find_relevant_fish(fish_name.lower())
        
        if found_fish:
            fish_key, fish_info, match_type = found_fish[0]
            return {
                "scientific_name": fish_info['scientific'],
                "vernacular_name": fish_info['vernacular'],
                "common_name": fish_info['common'],
                "family": fish_info['family'],
                "iucn_status": fish_info['iucn_status'],
                "description": fish_info['description']
            }
        
        return None
