from django.core.management.base import BaseCommand
from chatbot.models import FishSpecies
from rdflib import Graph
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Populate fish species data from ontology'

    def handle(self, *args, **options):
        # Load the ontology
        ontology_path = os.path.join(settings.BASE_DIR, 'fish_ontology.ttl')
        if not os.path.exists(ontology_path):
            self.stdout.write(
                self.style.ERROR(f'Ontology file not found at {ontology_path}')
            )
            return

        g = Graph()
        g.parse(ontology_path, format="turtle")

        # Fish species data mapping
        fish_data = {
            "wd:Q2249852": {
                "scientific_name": "Pethia nigrofasciata",
                "vernacular_name": "Bulath Hapaya",
                "family": "Cyprinidae",
                "genus": "Pethia",
                "threat_status": "Vulnerable",
                "occurrence_status": "Endemic to Sri Lanka",
                "max_size_cm": 6.5,
                "body_shape": "Laterally compressed, deep body",
                "body_color": "Silver to golden base with black vertical bars",
                "description": "Bulath Hapaya (Pethia nigrofasciata) is a small, colorful freshwater fish endemic to Sri Lanka. This species is easily identified by its silver to golden base coloration with distinctive black vertical bars running along its body. Males are particularly striking during breeding season when they develop intense red coloration on their head and body.",
                "habitat_type": "Forest streams with clear, fast-flowing water",
                "water_conditions": "pH 6.0-6.5, temperature 22-26°C, well-oxygenated water",
                "specific_locations": "Kalu Ganga basin, Kelani Ganga basin, Mahaweli Ganga basin",
                "river_basins": "Kalu, Kelani, Mahaweli",
                "districts": "Kalutara, Colombo, Gampaha, Kegalle, Ratnapura, Kandy, Matale",
                "protected_areas": "Sinharaja Forest Reserve, Peak Wilderness Sanctuary, Knuckles Forest Reserve",
                "image_url": "https://example.com/images/bulath_hapaya.jpg"
            },
            "wd:Q28599176": {
                "scientific_name": "Dawkinsia srilankensis",
                "vernacular_name": "Dankuda Pethiya",
                "family": "Cyprinidae",
                "genus": "Dawkinsia",
                "threat_status": "Endangered",
                "occurrence_status": "Endemic to Sri Lanka",
                "max_size_cm": 8.0,
                "body_shape": "Elongate, laterally compressed body",
                "body_color": "Silver base with dark blotches and spots",
                "description": "Dankuda Pethiya (Dawkinsia srilankensis) is an endangered freshwater fish endemic to Sri Lanka, known for its distinctive blotched pattern and filamentous dorsal fin extensions. This species has a silver base coloration with dark blotches and spots scattered across its body.",
                "habitat_type": "Riverine habitats with moderate flow",
                "water_conditions": "pH 6.5-7.0, temperature 20-25°C, moderate flow",
                "specific_locations": "Mahaweli Ganga basin, Kalu Ganga basin, Gin Ganga basin",
                "river_basins": "Mahaweli, Kalu, Gin",
                "districts": "Kandy, Matale, Nuwara Eliya, Kalutara, Galle, Matara",
                "protected_areas": "Horton Plains National Park, Peak Wilderness Sanctuary, Sinharaja Forest Reserve",
                "image_url": "https://example.com/images/dankuda_pethiya.jpg"
            },
            "wd:Q1518816": {
                "scientific_name": "Pethia cumingii",
                "vernacular_name": "Depulliya",
                "family": "Cyprinidae",
                "genus": "Pethia",
                "threat_status": "Endangered",
                "occurrence_status": "Endemic to Sri Lanka",
                "max_size_cm": 5.5,
                "body_shape": "Laterally compressed, moderately deep body",
                "body_color": "Silver base with two distinct black spots",
                "description": "Depulliya (Pethia cumingii) is an endangered freshwater fish endemic to Sri Lanka, easily recognized by its two distinctive black spots on a silver base. This small fish typically grows to 5.5 cm and has a laterally compressed, moderately deep body.",
                "habitat_type": "Small forest streams and tributaries",
                "water_conditions": "pH 6.0-6.8, temperature 22-26°C, clear water",
                "specific_locations": "Kelani Ganga basin, Mahaweli Ganga basin, Kalu Ganga basin",
                "river_basins": "Kelani, Mahaweli, Kalu",
                "districts": "Colombo, Gampaha, Kegalle, Ratnapura, Kandy, Matale, Kalutara",
                "protected_areas": "Sinharaja Forest Reserve, Peak Wilderness Sanctuary, Knuckles Forest Reserve",
                "image_url": "https://example.com/images/depulliya.jpg"
            },
            "wd:Q269931": {
                "scientific_name": "Rasboroides vaterifloris",
                "vernacular_name": "Halamal Dandiya",
                "family": "Danionidae",
                "genus": "Rasboroides",
                "threat_status": "Endangered",
                "occurrence_status": "Endemic to Sri Lanka",
                "max_size_cm": 4.5,
                "body_shape": "Laterally compressed, deep body",
                "body_color": "Pearly silver with iridescent scales",
                "description": "Halamal Dandiya (Rasboroides vaterifloris) is an endangered freshwater fish endemic to Sri Lanka, renowned for its pearly appearance and distinctive iridescent scales. This beautiful fish has a laterally compressed, deep body with a silver base that shimmers with iridescent scales.",
                "habitat_type": "Small forest streams with sandy bottoms",
                "water_conditions": "pH 6.2-6.8, temperature 23-27°C, slow to moderate flow",
                "specific_locations": "Kalu Ganga basin, Bentota Ganga basin, Gin Ganga basin",
                "river_basins": "Kalu, Bentota, Gin",
                "districts": "Kalutara, Galle, Matara, Hambantota",
                "protected_areas": "Sinharaja Forest Reserve, Kanneliya Forest Reserve, Hiyare Forest Reserve",
                "image_url": "https://example.com/images/halamal_dandiya.jpg"
            },
            "wd:Q637598": {
                "scientific_name": "Puntius titteya",
                "vernacular_name": "Lethiththaya",
                "family": "Cyprinidae",
                "genus": "Puntius",
                "threat_status": "Vulnerable",
                "occurrence_status": "Endemic to Sri Lanka",
                "max_size_cm": 5.0,
                "body_shape": "Laterally compressed, moderately deep body",
                "body_color": "Silver base with cherry-red coloration in males",
                "description": "Lethiththaya (Puntius titteya), also known as the Cherry Barb, is a vulnerable freshwater fish endemic to Sri Lanka, famous for its brilliant cherry-red coloration in males. This species has a laterally compressed, moderately deep body with a silver base that transforms into stunning cherry-red coloration in males during breeding season.",
                "habitat_type": "Forest streams and small rivers",
                "water_conditions": "pH 6.0-6.5, temperature 22-26°C, clear, well-oxygenated water",
                "specific_locations": "Kelani Ganga basin, Nilwala Ganga basin, Kalu Ganga basin",
                "river_basins": "Kelani, Nilwala, Kalu",
                "districts": "Colombo, Gampaha, Kegalle, Ratnapura, Matara, Galle, Kalutara",
                "protected_areas": "Sinharaja Forest Reserve, Peak Wilderness Sanctuary, Kanneliya Forest Reserve",
                "image_url": "https://example.com/images/lethiththaya.jpg"
            },
            "wd:Q2917966": {
                "scientific_name": "Devario pathirana",
                "vernacular_name": "Pathirana Salaya",
                "family": "Danionidae",
                "genus": "Devario",
                "threat_status": "Endangered",
                "occurrence_status": "Critically endangered (in wild), Common (in captivity)",
                "max_size_cm": 7.0,
                "body_shape": "Elongate, laterally compressed body",
                "body_color": "Silver base with dark horizontal bars",
                "description": "Pathirana Salaya (Devario pathirana), also known as the Barred Danio, is an endangered freshwater fish endemic to Sri Lanka, distinguished by its horizontal barring pattern. This species has an elongate, laterally compressed body with a silver base and dark horizontal bars running across its body.",
                "habitat_type": "Forest streams with rocky substrates",
                "water_conditions": "pH 6.0-6.5, temperature 20-25°C, fast-flowing, well-oxygenated water",
                "specific_locations": "Kalu Ganga basin, Kelani Ganga basin, Mahaweli Ganga basin",
                "river_basins": "Kalu, Kelani, Mahaweli",
                "districts": "Kalutara, Colombo, Gampaha, Kegalle, Ratnapura, Kandy, Matale",
                "protected_areas": "Sinharaja Forest Reserve, Peak Wilderness Sanctuary, Knuckles Forest Reserve",
                "image_url": "https://example.com/images/pathirana_salaya.jpg"
            },
            "wd:Q2703814": {
                "scientific_name": "Belontia signata",
                "vernacular_name": "Thal Kossa",
                "family": "Osphronemidae",
                "genus": "Belontia",
                "threat_status": "Vulnerable",
                "occurrence_status": "Endemic to Sri Lanka",
                "max_size_cm": 12.0,
                "body_shape": "Laterally compressed, deep body",
                "body_color": "Brown to olive base with dark vertical bars",
                "description": "Thal Kossa (Belontia signata), also known as the Ceylonese Combtail, is a vulnerable freshwater fish endemic to Sri Lanka, distinguished by its comb-like caudal fin and filamentous extensions. This species has a laterally compressed, deep body with a brown to olive base coloration and dark vertical bars.",
                "habitat_type": "Slow-moving forest streams and pools",
                "water_conditions": "pH 6.0-6.8, temperature 22-28°C, slow flow, can tolerate low oxygen",
                "specific_locations": "Kalu Ganga basin, Kelani Ganga basin, Mahaweli Ganga basin",
                "river_basins": "Kalu, Kelani, Mahaweli",
                "districts": "Kalutara, Colombo, Gampaha, Kegalle, Ratnapura, Kandy, Matale",
                "protected_areas": "Sinharaja Forest Reserve, Peak Wilderness Sanctuary, Knuckles Forest Reserve",
                "image_url": "https://example.com/images/thal_kossa.jpg"
            }
        }

        # Create or update fish species
        created_count = 0
        updated_count = 0

        for fish_id, data in fish_data.items():
            fish_species, created = FishSpecies.objects.get_or_create(
                scientific_name=data["scientific_name"],
                defaults=data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {data["vernacular_name"]}')
                )
            else:
                # Update existing record
                for key, value in data.items():
                    setattr(fish_species, key, value)
                fish_species.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated: {data["vernacular_name"]}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {len(fish_data)} fish species. '
                f'Created: {created_count}, Updated: {updated_count}'
            )
        )
