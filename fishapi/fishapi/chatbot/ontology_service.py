from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS, Namespace
import os
from django.conf import settings

class OntologyService:
    def __init__(self):
        self.graph = None
        self.fish_species_mapping = {}
        self._load_ontology()

    def _load_ontology(self):
        """Load the fish ontology from OWL file"""
        try:
            ontology_path = os.path.join(settings.BASE_DIR, 'fish6species(1).owl')
            if os.path.exists(ontology_path):
                self.graph = Graph()
                self.graph.parse(ontology_path, format="xml")
                print(f"OWL Ontology loaded successfully from {ontology_path}")
                self._extract_fish_data()
            else:
                print(f"OWL file not found at {ontology_path}")
                self._create_fallback_data()
        except Exception as e:
            print(f"Error loading OWL ontology: {e}")
            self._create_fallback_data()

    def _extract_fish_data(self):
        """Extract fish data from the OWL ontology"""
        if not self.graph:
            return
        
        # Define namespaces
        fish_ns = Namespace("http://www.freshwaterfish.org/ontology#")
        
        # Query for all fish species
        query = """
        SELECT ?fish ?scientificName ?commonName ?sinhalaName ?family ?order ?habitat ?maxLength ?iucnStatus ?description
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
                "description": description
            }
        
        print(f"Extracted {len(self.fish_species_mapping)} fish species from OWL ontology")
    
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

    def query_ontology(self, user_query):
        """Query the ontology based on user input"""
        if not self.graph:
            return self._get_fallback_response(user_query)
        
        found_fish = self._find_fish_in_query(user_query.lower())
        
        if not found_fish:
            fish_names = [info["vernacular"] for info in self.fish_species_mapping.values()]
            return f"I can only answer questions about the following fish: {', '.join(fish_names)}. Please ask about one of them."
        
        try:
            return self._query_fish_information(found_fish, user_query)
        except Exception as e:
            print(f"Error querying ontology: {e}")
            return self._get_fallback_response(user_query, found_fish)
    
    def _get_fallback_response(self, user_query, found_fish=None):
        """Provide fallback response when ontology fails"""
        if found_fish and found_fish in self.fish_species_mapping:
            fish_info = self.fish_species_mapping[found_fish]
            return f"""**{fish_info['vernacular']}** ({fish_info['scientific']})
            
            This is one of the six endemic freshwater fish species of Sri Lanka. Here's what I know:

            - **Scientific Name**: {fish_info['scientific']}
            - **Vernacular Name**: {fish_info['vernacular']}
            - **Common Name**: {fish_info['common']}
            - **Family**: {fish_info['family']}
            - **Order**: {fish_info['order']}
            - **Habitat**: {fish_info['habitat']}
            - **Maximum Length**: {fish_info['max_length']}
            - **IUCN Status**: {fish_info['iucn_status']}
            - **Description**: {fish_info['description']}

            For more detailed information about this species, please check our database or ask specific questions about its habitat, conservation status, or physical characteristics."""
        
        return "I can help you learn about Sri Lankan endemic freshwater fish species. Please ask about a specific fish or ask me to list all available species."

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

    def _query_fish_information(self, fish_name, requested_info):
        """Queries the RDF graph to get information about a fish."""
        if fish_name not in self.fish_species_mapping:
            return f"Fish species '{fish_name}' not found in the ontology."
        
        fish_info = self.fish_species_mapping[fish_name]
        
        # Get additional details from the OWL file
        additional_info = self._get_additional_fish_details(fish_name)
        
        response = f"""**{fish_info['vernacular']}** ({fish_info['scientific']})
        
        **Scientific Name**: {fish_info['scientific']}
        **Vernacular Name**: {fish_info['vernacular']}
        **Common Name**: {fish_info['common']}
        **Family**: {fish_info['family']}
        **Order**: {fish_info['order']}
        **Habitat**: {fish_info['habitat']}
        **Maximum Length**: {fish_info['max_length']}
        **IUCN Status**: {fish_info['iucn_status']}
        
        **Description**: {fish_info['description']}"""
        
        if additional_info:
            response += f"\n\n**Additional Information**:\n{additional_info}"
        
        return response

    def _get_additional_fish_details(self, fish_name):
        """Get additional details from the OWL file for a specific fish"""
        if not self.graph:
            return ""
        
        try:
            # Define namespaces
            fish_ns = Namespace("http://www.freshwaterfish.org/ontology#")
            
            # Find the fish URI
            fish_uri = None
            for key, info in self.fish_species_mapping.items():
                if key == fish_name:
                    fish_uri = URIRef(info['id'])
                    break
            
            if not fish_uri:
                return ""
            
            # Query for additional properties
            query = """
            SELECT ?property ?value
            WHERE {
                ?fish ?property ?value .
                FILTER(?fish = ?fish_uri)
                FILTER(?property != fish:ScientificName)
                FILTER(?property != fish:CommonName)
                FILTER(?property != fish:SinhalaName)
                FILTER(?property != fish:Family)
                FILTER(?property != fish:Order)
                FILTER(?property != fish:Habitat)
                FILTER(?property != fish:MaximumLengthCm)
                FILTER(?property != fish:IUCNStatus)
                FILTER(?property != fish:MorphologyDescription)
            }
            """
            
            # Replace the placeholder with actual fish URI
            query = query.replace("?fish_uri", f"<{fish_uri}>")
            
            results = self.graph.query(query)
            
            additional_details = []
            for row in results:
                property_name = str(row.property).split('#')[-1] if '#' in str(row.property) else str(row.property)
                value = str(row.value)
                additional_details.append(f"• **{property_name}**: {value}")
            
            return "\n".join(additional_details) if additional_details else ""
            
        except Exception as e:
            print(f"Error getting additional details: {e}")
            return ""

    def get_fish_information(self, fish_name):
        """Get basic information about a fish species for classification results"""
        found_fish = self._find_fish_in_query(fish_name.lower())
        
        if found_fish and found_fish in self.fish_species_mapping:
            fish_info = self.fish_species_mapping[found_fish]
            return {
                "scientific_name": fish_info['scientific'],
                "vernacular_name": fish_info['vernacular'],
                "common_name": fish_info['common'],
                "family": fish_info['family'],
                "iucn_status": fish_info['iucn_status'],
                "description": fish_info['description']
            }
        
        return None
