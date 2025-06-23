from rest_framework.decorators import api_view
from rest_framework.response import Response
from keras.models import load_model
from PIL import Image
import numpy as np
import tensorflow as tf
import cv2
import io
import os
import uuid
from django.core.files.storage import default_storage
from django.conf import settings
import time

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'best_fish_classifier.h5')
model = load_model(model_path)

# Class labels
class_names = [
    "Bulath_hapaya", "Dankuda_pethiya", "Depulliya",
    "Halamal_dandiya", "Lethiththaya", "Pathirana_salaya", "Thal_kossa"
]

def normalize(x):
    """Normalize an array to the [0, 1] range"""
    return (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-10)

def generate_gradcam_overlay(img_array, model, pred_class):
    original_img = img_array.copy()
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    img_tensor = tf.convert_to_tensor(img_array, dtype=tf.float32)

    with tf.GradientTape() as tape:
        tape.watch(img_tensor)
        predictions = model(img_tensor)
        target_score = predictions[:, pred_class]

    grads = tape.gradient(target_score, img_tensor)

    grad_mag = tf.reduce_max(tf.abs(grads), axis=-1)[0].numpy()
    guided_grads = tf.cast(grads > 0, tf.float32) * grads
    guided_mag = tf.reduce_sum(guided_grads, axis=-1)[0].numpy()
    grad_input = grads * img_tensor
    grad_input_mag = tf.reduce_sum(tf.abs(grad_input), axis=-1)[0].numpy()

    composite_heatmap = (normalize(grad_mag) + normalize(guided_mag) + normalize(grad_input_mag)) / 3
    composite_heatmap = cv2.GaussianBlur(composite_heatmap, (5, 5), 0)
    composite_heatmap = normalize(composite_heatmap)

    heatmap_colored = cv2.applyColorMap(np.uint8(255 * composite_heatmap), cv2.COLORMAP_JET)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)

    superimposed = cv2.addWeighted(original_img.astype('uint8'), 0.6, heatmap_colored, 0.4, 0)

    return superimposed

@api_view(['POST'])
def predict_image(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=400)

    image_file = request.FILES['image']
    img = Image.open(image_file).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img)

    # Predict
    img_tensor = np.expand_dims(img_array / 255.0, axis=0)
    predictions = model.predict(img_tensor)[0]
    class_index = int(np.argmax(predictions))
    confidence = float(np.max(predictions))
    class_name = class_names[class_index]

    # Generate heatmap overlay
    overlay_img = generate_gradcam_overlay(img_array, model, class_index)

    # Save overlay image to disk
    filename = f"overlay_{uuid.uuid4().hex}.png"
    overlay_path = os.path.join(settings.MEDIA_ROOT, filename)
    cv2.imwrite(overlay_path, overlay_img)

    # Ensure file is written before returning
    for _ in range(10):  # wait max 2 seconds
        if os.path.exists(overlay_path):
            break
        time.sleep(0.2)

    time.sleep(0.3)
    # Return prediction with relative path to image
    return Response({
        "prediction": class_name,
        "confidence": round(confidence, 3),
        "heatmap_image": f"/media/{filename}"
    })
