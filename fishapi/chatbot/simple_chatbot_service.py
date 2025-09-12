"""
Simple chatbot service that provides fish information without complex ontology queries
"""
from .models import FishSpecies

class SimpleChatbotService:
    def __init__(self):
        self.fish_species_mapping = {
            "bulath_hapaya": {"id": "wd:Q2249852", "vernacular": "Bulath Hapaya", "scientific": "Pethia nigrofasciata"},
            "dankuda_pethiya": {"id": "wd:Q28599176", "vernacular": "Dankuda Pethiya", "scientific": "Dawkinsia srilankensis"},
            "depulliya": {"id": "wd:Q1518816", "vernacular": "Depulliya", "scientific": "Pethia cumingii"},
            "halamal_dandiya": {"id": "wd:Q269931", "vernacular": "Halamal Dandiya", "scientific": "Rasboroides vaterifloris"},
            "lethiththaya": {"id": "wd:Q637598", "vernacular": "Lethiththaya", "scientific": "Puntius titteya"},
            "pathirana_salaya": {"id": "wd:Q2917966", "vernacular": "Pathirana Salaya", "scientific": "Devario pathirana"},
            "thal_kossa": {"id": "wd:Q2703814", "vernacular": "Thal Kossa", "scientific": "Belontia signata"}
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
        for fish_key, fish_info in self.fish_species_mapping.items():
            # Check for various forms of the fish name
            fish_variations = [
                fish_key,
                fish_key.replace('_', ' '),
                fish_info["vernacular"].lower(),
                fish_info["scientific"].lower()
            ]
            
            # Add common alternative names
            if fish_key == "lethiththaya":
                fish_variations.extend(["lethiththaya", "lay titteya", "cherry barb"])
            elif fish_key == "bulath_hapaya":
                fish_variations.extend(["bulath hapaya", "black ruby barb", "purplehead barb"])
            elif fish_key == "dankuda_pethiya":
                fish_variations.extend(["dankuda pethiya", "blotched filamented barb"])
            elif fish_key == "depulliya":
                fish_variations.extend(["depulliya", "two-spot barb", "cuming's barb"])
            elif fish_key == "halamal_dandiya":
                fish_variations.extend(["halamal dandiya", "pearly rasbora", "fire rasbora"])
            elif fish_key == "pathirana_salaya":
                fish_variations.extend(["pathirana salaya", "barred danio"])
            elif fish_key == "thal_kossa":
                fish_variations.extend(["thal kossa", "ceylonese combtail"])
            
            for variation in fish_variations:
                if variation in query:
                    return fish_key
        
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

This is one of the seven endemic freshwater fish species of Sri Lanka.

- **Scientific Name**: {fish_info['scientific']}
- **Vernacular Name**: {fish_info['vernacular']}
- **Status**: Endemic to Sri Lanka

For more detailed information, please ask specific questions about:
- Habitat and water conditions
- Conservation status and threats
- Physical appearance and size
- Distribution and locations"""
