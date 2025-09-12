from rdflib import Graph
import os
from django.conf import settings

class OntologyService:
    def __init__(self):
        self.graph = None
        self.fish_species_mapping = {
            "bulath_hapaya": {"id": "wd:Q2249852", "vernacular": "Bulath Hapaya", "scientific": "Pethia nigrofasciata"},
            "dankuda_pethiya": {"id": "wd:Q28599176", "vernacular": "Dankuda Pethiya", "scientific": "Dawkinsia srilankensis"},
            "depulliya": {"id": "wd:Q1518816", "vernacular": "Depulliya", "scientific": "Pethia cumingii"},
            "halamal_dandiya": {"id": "wd:Q269931", "vernacular": "Halamal Dandiya", "scientific": "Rasboroides vaterifloris"},
            "lethiththaya": {"id": "wd:Q637598", "vernacular": "Lay titteya", "scientific": "Puntius titteya"},
            "pathirana_salaya": {"id": "wd:Q2917966", "vernacular": "Pathirana Salaya", "scientific": "Devario pathirana"},
            "thal_kossa": {"id": "wd:Q2703814", "vernacular": "Thal Kossa", "scientific": "Belontia signata"}
        }
        self._load_ontology()

    def _load_ontology(self):
        """Load the fish ontology from TTL file"""
        try:
            ontology_path = os.path.join(settings.BASE_DIR, 'fish_ontology.ttl')
            if os.path.exists(ontology_path):
                self.graph = Graph()
                self.graph.parse(ontology_path, format="turtle")
            else:
                print(f"Ontology file not found at {ontology_path}")
        except Exception as e:
            print(f"Error loading ontology: {e}")

    def query_ontology(self, user_query):
        """Query the ontology based on user input"""
        if not self.graph:
            return "I don't have access to the fish knowledge base at the moment."
        
        # Find which fish is being talked about
        found_fish = self._find_fish_in_query(user_query.lower())
        
        if not found_fish:
            fish_names = [info["vernacular"] for info in self.fish_species_mapping.values()]
            return f"I can only answer questions about the following fish: {', '.join(fish_names)}. Please ask about one of them."
        
        # Query the ontology
        return self._query_fish_information(found_fish, user_query)

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

    def _query_fish_information(self, fish_name, requested_info):
        """Query specific information about a fish species"""
        fish_info = self.fish_species_mapping.get(fish_name)
        if not fish_info:
            return f"I don't have information about {fish_name}."
        
        fish_id = fish_info["id"]
        fish_display_name = fish_info["vernacular"]
        
        # Check for comprehensive requests
        comprehensive_keywords = ["all details", "complete information", "everything about", "full details", "comprehensive", "all information"]
        is_comprehensive = any(keyword in requested_info.lower() for keyword in comprehensive_keywords)
        
        if is_comprehensive:
            return self._get_comprehensive_information(fish_id, fish_display_name)
        else:
            return self._get_specific_information(fish_id, fish_display_name, requested_info)

    def _get_comprehensive_information(self, fish_id, fish_display_name):
        """Get comprehensive information about a fish species"""
        sparql_prefix = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
            PREFIX iucn: <http://iucn.org/ontology/>
            PREFIX obo: <http://purl.obolibrary.org/obo/>
            PREFIX envo: <http://purl.obolibrary.org/obo/ENVO_>
            PREFIX wd: <http://www.wikidata.org/entity/>
        """
        
        query = f"""
            {sparql_prefix}
            SELECT ?property ?value ?label
            WHERE {{
                {fish_id} ?property ?value .
                OPTIONAL {{ ?value rdfs:label ?label }}
                FILTER(?property != rdf:type)
            }}
            ORDER BY ?property
        """
        
        results = self.graph.query(query)
        
        if not results:
            return f"I have no information about {fish_display_name}."
        
        # Format comprehensive response
        context = f"# Complete Information for {fish_display_name}\n\n"
        
        for row in results:
            prop_name = str(row.property).split('#')[-1].split('/')[-1]
            value = str(row.value)
            label = str(row.label) if row.label else ""
            
            # Clean up property name
            clean_prop_name = prop_name.replace("_", " ").lower()
            if clean_prop_name.startswith("ro"):
                clean_prop_name = clean_prop_name.replace("ro", "").strip()
            
            # Use label if available, otherwise use value
            display_value = label if label and label != "None" else value
            context += f"- **{clean_prop_name.title()}**: {display_value}\n"
        
        return context.strip()

    def _get_specific_information(self, fish_id, fish_display_name, requested_info):
        """Get specific information based on the request"""
        # Map keywords to ontology properties
        property_map = {
            "scientific name": ("dwc:scientificName", "Scientific name"),
            "habitat": ("obo:RO_0002451", "Habitat"),
            "description": ("rdfs:label", "Description"),
            "family": ("dwc:family", "Family"),
            "genus": ("dwc:genus", "Genus"),
            "conservation": ("iucn:threatStatus", "Conservation status"),
            "size": (":maxSizeCm", "Maximum size"),
            "appearance": (":bodyColor", "Appearance"),
            "body color": (":bodyColor", "Body color"),
            "body shape": (":bodyShape", "Body shape"),
            "location": (":specificLocations", "Locations"),
            "diet": ("obo:RO_0002228", "Diet"),
            "threats": ("obo:RO_0002234", "Threats")
        }
        
        # Find matching property
        query_type = None
        for keyword, (prop, label) in property_map.items():
            if keyword in requested_info.lower():
                query_type = prop
                break
        
        if not query_type:
            return self._get_comprehensive_information(fish_id, fish_display_name)
        
        # Query specific property
        sparql_prefix = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
            PREFIX iucn: <http://iucn.org/ontology/>
            PREFIX obo: <http://purl.obolibrary.org/obo/>
            PREFIX envo: <http://purl.obolibrary.org/obo/ENVO_>
            PREFIX wd: <http://www.wikidata.org/entity/>
        """
        
        query = f"""
            {sparql_prefix}
            SELECT ?value ?label
            WHERE {{
                {fish_id} {query_type} ?value .
                OPTIONAL {{ ?value rdfs:label ?label }}
            }}
        """
        
        results = self.graph.query(query)
        
        if not results:
            return f"I don't have specific information about that aspect of {fish_display_name}."
        
        context = f"Information about {fish_display_name}:\n"
        for row in results:
            value = str(row.value)
            label = str(row.label) if row.label else ""
            display_value = label if label and label != "None" else value
            context += f"- {display_value}\n"
        
        return context.strip()
