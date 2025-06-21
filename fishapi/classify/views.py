from rest_framework.decorators import api_view
from rest_framework.response import Response
from keras.models import load_model
from PIL import Image
import numpy as np
import io
import os

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'best_fish_classifier.h5')
model = load_model(model_path)

# Your class names
class_names = [
    "Bulath_hapaya", "Dankuda_pethiya", "Depulliya",
    "Halamal_dandiya", "Lethiththaya", "Pathirana_salaya", "Thal_kossa"
]

@api_view(['POST'])
def predict_image(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=400)

    image_file = request.FILES['image']
    img = Image.open(image_file).convert("RGB")
    img = img.resize((224, 224))  # adjust based on model input
    img_array = np.array(img) / 255.0
    img_tensor = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_tensor)[0]
    class_index = int(np.argmax(predictions))
    confidence = float(np.max(predictions))

    return Response({
        "prediction": class_names[class_index],
        "confidence": round(confidence, 3)
    })
