"""
Simple chatbot service that provides fish information without complex ontology queries
"""
from .models import FishSpecies

class SimpleChatbotService:
    def __init__(self):
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
            },
            "devario_pathirana": {
                "id": "http://www.freshwaterfish.org/ontology#Devario_pathirana",
                "scientific": "Devario pathirana",
                "vernacular": "pathirana saalaya",
                "common": "Barred Danio, Sri Lanka Barred Danio",
                "family": "Danionidae",
                "order": "Cypriniformes",
                "habitat": "Freshwater, prefers still pools over fast-flowing areas",
                "max_length": "6.0 cm SL",
                "iucn_status": "Endangered (EN)",
                "description": "Compressed body, dorsally greenish-brown, lighter laterally with metallic blue bars"
            },
            "dawkinsia_srilankensis": {
                "id": "http://www.freshwaterfish.org/ontology#Dawkinsia_srilankensis",
                "scientific": "Dawkinsia srilankensis",
                "vernacular": "Mal Pethiya",
                "common": "Sri Lanka Blotched Filamented Barb, Blotched Filamented Barb",
                "family": "Cyprinidae",
                "order": "Cypriniformes",
                "habitat": "Freshwater; benthopelagic; tropical. Prefers fast flowing streams",
                "max_length": "10.0 cm TL",
                "iucn_status": "Endangered (EN)",
                "description": "Slightly elongated body with terminal mouth, no barbels. Three distinct black blotches laterally"
            },
            "pethia_cumingii": {
                "id": "http://www.freshwaterfish.org/ontology#Pethia_cumingii",
                "scientific": "Pethia cumingii",
                "vernacular": "Kahavaral Depulliya /Potaya",
                "common": "Cuming's Barb, Two spot barb",
                "family": "Cyprinidae",
                "order": "Cypriniformes",
                "habitat": "Freshwater; benthopelagic. Clear, shallow, slow flowing, shaded streams",
                "max_length": "5.0 cm TL",
                "iucn_status": "Endangered (EN)",
                "description": "Laterally compressed body with two vertically elongated blotches"
            },
            "belontia_signata": {
                "id": "http://www.freshwaterfish.org/ontology#Belontia_signata",
                "scientific": "Belontia signata",
                "vernacular": "Thalkossa",
                "common": "Ceylonese Combtail",
                "family": "Osphronemidae",
                "order": "Anabantiformes",
                "habitat": "Freshwater, prefers slow-flowing, clear streams with sandy or rocky substrates",
                "max_length": "18.0 cm TL",
                "iucn_status": "Vulnerable (VU)",
                "description": "Compressed body with elongated, pointed dorsal and anal fins"
            },
            "pethia_nigrofasciata": {
                "id": "http://www.freshwaterfish.org/ontology#Pethia_nigrofasciata",
                "scientific": "Pethia nigrofasciata",
                "vernacular": "Bulath Hapaya / Manamaalaya",
                "common": "Sri Lanka Black Ruby Barb, Black Ruby Barb",
                "family": "Cyprinidae",
                "order": "Cypriniformes",
                "habitat": "Freshwater; benthopelagic. Clear waters with rocky and sandy substrata",
                "max_length": "6.0 cm TL",
                "iucn_status": "Vulnerable (VU)",
                "description": "Compressed body with three black vertical bands"
            }
        }

    def get_response(self, user_query):
        """Get chatbot response for user query"""
        try:
            # Find which fish is being talked about
            found_fish = self._find_fish_in_query(user_query.lower())
            
            if not found_fish:
                fish_names = [info["vernacular"] for info in self.fish_species_mapping.values()]
                return f"I can only answer questions about the following fish: {', '.join(fish_names)}. Please ask about one of them."
            
            # Get fish information from database
            return self._get_fish_information(found_fish, user_query)
                
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}"

    def _find_fish_in_query(self, query):
        """Find which fish species is mentioned in the query"""
        # Check for scientific names
        for key, info in self.fish_species_mapping.items():
            if info['scientific'].lower() in query:
                return key
        
        # Check for vernacular names (including partial matches)
        for key, info in self.fish_species_mapping.items():
            vernacular = info['vernacular'].lower()
            if vernacular in query or any(part in query for part in vernacular.split()):
                return key
        
        # Check for common names (including partial matches)
        for key, info in self.fish_species_mapping.items():
            common = info['common'].lower()
            if common in query or any(part in query for part in common.split(',')):
                return key
        
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
            if variation in query:
                return key
        
        return None

    def _get_fish_information(self, fish_name, user_query):
        """Get fish information from database"""
        try:
            # Try to get from database first
            fish_info = self.fish_species_mapping.get(fish_name)
            if not fish_info:
                return f"I don't have information about {fish_name}."
            
            vernacular_name = fish_info["vernacular"]
            scientific_name = fish_info["scientific"]
            
            # Try to get detailed info from database
            try:
                db_fish = FishSpecies.objects.get(vernacular_name=vernacular_name)
                return self._format_detailed_response(db_fish, user_query)
            except FishSpecies.DoesNotExist:
                # Fallback to basic info
                return self._format_basic_response(fish_info, user_query)
                
        except Exception as e:
            print(f"Error getting fish information: {e}")
            return f"I'm sorry, I couldn't retrieve information about {fish_name}."

    def _format_detailed_response(self, fish, user_query):
        """Format detailed response from database"""
        response = f"**{fish.vernacular_name}** ({fish.scientific_name})\n\n"
        
        # Always show basic info
        response += f"**Scientific Name**: {fish.scientific_name}\n"
        response += f"**Family**: {fish.family or 'Cyprinidae'}\n"
        response += f"**Conservation Status**: {fish.threat_status or 'Endemic to Sri Lanka'}\n\n"
        
        # Show specific information based on query
        if "habitat" in user_query.lower() or "where" in user_query.lower() or "live" in user_query.lower():
            response += f"**🌍 Habitat & Distribution**\n"
            if fish.habitat_type:
                response += f"• **Habitat Type**: {fish.habitat_type}\n"
            if fish.water_conditions:
                response += f"• **Water Conditions**: {fish.water_conditions}\n"
            if fish.specific_locations:
                response += f"• **River Basins**: {fish.specific_locations}\n"
            if fish.districts:
                response += f"• **Districts**: {fish.districts}\n"
            if fish.protected_areas:
                response += f"• **Protected Areas**: {fish.protected_areas}\n"
            response += "\n"
        
        if "size" in user_query.lower() or "length" in user_query.lower() or "appearance" in user_query.lower():
            response += f"**🔍 Physical Characteristics**\n"
            if fish.max_size_cm:
                response += f"• **Maximum Size**: {fish.max_size_cm} cm\n"
            if fish.body_color:
                response += f"• **Body Color**: {fish.body_color}\n"
            if fish.body_shape:
                response += f"• **Body Shape**: {fish.body_shape}\n"
            response += "\n"
        
        if "conservation" in user_query.lower() or "threat" in user_query.lower():
            response += f"**⚠️ Conservation**\n"
            response += f"• **Status**: {fish.threat_status or 'Endemic to Sri Lanka'}\n"
            response += f"• **Occurrence**: {fish.occurrence_status or 'Endemic to Sri Lanka'}\n"
            response += "\n"
        
        # Always include description
        if fish.description:
            response += f"**📝 Description**\n{fish.description}\n"
        else:
            response += f"**📝 Description**\n{fish.vernacular_name} is an endemic freshwater fish species of Sri Lanka.\n"
        
        return response

    def _format_basic_response(self, fish_info, user_query):
        """Format basic response when database is not available"""
        return f"""**{fish_info['vernacular']}** ({fish_info['scientific']})

This is one of the six endemic freshwater fish species of Sri Lanka.

- **Scientific Name**: {fish_info['scientific']}
- **Vernacular Name**: {fish_info['vernacular']}
- **Common Name**: {fish_info['common']}
- **Family**: {fish_info['family']}
- **Order**: {fish_info['order']}
- **Habitat**: {fish_info['habitat']}
- **Maximum Length**: {fish_info['max_length']}
- **IUCN Status**: {fish_info['iucn_status']}
- **Description**: {fish_info['description']}

For more detailed information, please ask specific questions about:
- Habitat and water conditions
- Conservation status and threats
- Physical appearance and size
- Distribution and locations"""
