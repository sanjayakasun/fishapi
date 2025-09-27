# Fish Classification API with Chatbot Integration

This project integrates a fish classification model with an intelligent chatbot that can provide detailed information about Sri Lankan endemic freshwater fish species.

## Features

### 🐠 Fish Classification

- **Deep Learning Model**: Uses a trained CNN model to classify fish species from images
- **7 Species Support**: Bulath Hapaya, Dankuda Pethiya, Depulliya, Halamal Dandiya, Lethiththaya, Pathirana Salaya, Thal Kossa
- **Heatmap Visualization**: Generates GradCAM heatmaps to show which parts of the image influenced the prediction
- **Confidence Scores**: Provides confidence levels for predictions

### 🤖 Intelligent Chatbot

- **Ontology-Based Knowledge**: Uses RDF/OWL ontology for structured fish information
- **DeepSeek AI Integration**: Powered by DeepSeek API for natural language responses
- **Comprehensive Information**: Provides details about habitat, conservation status, morphology, and more
- **Interactive Web Interface**: Beautiful, responsive chat interface

### 🔗 Integrated Experience

- **Unified API**: Classification results include chatbot-generated fish information
- **Session Management**: Maintains chat history across interactions
- **Real-time Responses**: Fast, intelligent responses to user queries

## Project Structure

```
fishapi/
├── fishapi/                    # Django project settings
│   ├── settings.py
│   └── urls.py
├── classify/                   # Fish classification app
│   ├── views.py               # Classification API endpoints
│   ├── urls.py
│   └── best_fish_classifier.h5 # Trained model
├── chatbot/                   # Chatbot app
│   ├── models.py              # Database models
│   ├── views.py               # Chatbot API endpoints
│   ├── chatbot_service.py     # Core chatbot logic
│   ├── ontology_service.py    # RDF ontology queries
│   ├── templates/             # Web interface
│   └── management/commands/    # Database population
├── fish_ontology.ttl          # RDF ontology file
├── requirements.txt           # Dependencies
└── .env                       # Environment variables
```

## Installation

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**:
   Create a `.env` file with:

   ```
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   ```

3. **Run Migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Populate Database**:

   ```bash
   python manage.py populate_fish_species
   ```

5. **Start Server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Classification API

- **POST** `/predict/` - Classify fish from image
  - Input: Image file
  - Output: Prediction, confidence, heatmap, fish info

### Chatbot API

- **POST** `/chatbot/api/chat/` - Chat with the bot

  - Input: Message and session ID
  - Output: Bot response

- **GET** `/chatbot/api/species/` - List all fish species
- **GET** `/chatbot/api/species/{id}/` - Get species details

### Web Interface

- **GET** `/chatbot/chat/` - Interactive chat interface

## Usage Examples

### 1. Fish Classification

```python
import requests

# Upload image for classification
with open('fish_image.jpg', 'rb') as f:
    response = requests.post('http://localhost:8000/predict/', files={'image': f})
    result = response.json()

print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']}")
print(f"Fish Info: {result['fish_info']['description']}")
```

### 2. Chatbot Interaction

```python
import requests

# Chat with the bot
response = requests.post('http://localhost:8000/chatbot/api/chat/', json={
    "message": "Tell me about Bulath Hapaya",
    "session_id": "my_session"
})

result = response.json()
print(f"Bot: {result['response']}")
```

### 3. Web Interface

Visit `http://localhost:8000/chatbot/chat/` in your browser for the interactive chat interface.

## Fish Species Information

The system provides comprehensive information about 7 Sri Lankan endemic fish species:

1. **Bulath Hapaya** (Pethia nigrofasciata) - Vulnerable
2. **Dankuda Pethiya** (Dawkinsia srilankensis) - Endangered
3. **Depulliya** (Pethia cumingii) - Endangered
4. **Halamal Dandiya** (Rasboroides vaterifloris) - Endangered
5. **Lethiththaya** (Puntius titteya) - Vulnerable
6. **Pathirana Salaya** (Devario pathirana) - Endangered
7. **Thal Kossa** (Belontia signata) - Vulnerable

Each species includes:

- Scientific and vernacular names
- Conservation status
- Physical characteristics
- Habitat information
- Distribution data
- Conservation notes

## Technical Details

### Classification Model

- **Architecture**: Convolutional Neural Network
- **Input Size**: 224x224x3 RGB images
- **Output**: 7-class softmax predictions
- **Visualization**: GradCAM heatmaps for interpretability

### Chatbot Architecture

- **Knowledge Base**: RDF/OWL ontology with SPARQL queries
- **Language Model**: DeepSeek API for natural language generation
- **Database**: SQLite with Django ORM
- **Frontend**: HTML/CSS/JavaScript with responsive design

### Ontology Structure

The RDF ontology includes:

- Taxonomic information (scientific names, families, genera)
- Conservation data (IUCN status, threats)
- Physical characteristics (size, color, morphology)
- Habitat information (water conditions, locations)
- Distribution data (river basins, districts, protected areas)

## Testing

Run the integration test:

```bash
python test_integration.py
```

This will test:

- Species API endpoints
- Chatbot functionality
- Classification with dummy images

## Configuration

### Environment Variables

- `DEEPSEEK_API_KEY`: Your DeepSeek API key for chatbot responses

### Django Settings

- `DEBUG`: Set to `True` for development
- `ALLOWED_HOSTS`: Configure for your deployment
- `CORS_ALLOW_ALL_ORIGINS`: Set to `True` for development

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure proper `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Set up proper static file serving
5. Configure environment variables securely
6. Use HTTPS for API endpoints

## Troubleshooting

### Common Issues

1. **Model Loading Errors**: Ensure the model file exists and is compatible
2. **API Key Issues**: Check your DeepSeek API key in the .env file
3. **Ontology Loading**: Verify the fish_ontology.ttl file is in the correct location
4. **Database Errors**: Run migrations and populate the database

### Logs

Check the Django console output for detailed error messages and warnings.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and research purposes. Please ensure you have proper licenses for any commercial use of the fish classification model or API services.

## Acknowledgments

- Fish classification model trained on Sri Lankan endemic fish dataset
- RDF ontology based on scientific literature and conservation data
- DeepSeek API for natural language processing
- Django framework for web application development
