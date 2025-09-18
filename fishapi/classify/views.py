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
model_path = os.path.join(os.path.dirname(__file__), 'best_finetuned_stage2.keras')
model = load_model(model_path)

# Class labels
class_names = [
    "Bulath_hapaya", "Dankuda_pethiya", "Depulliya",
    "Halamal_dandiya", "Lethiththaya", "Pathirana_salaya", "Thal_kossa"
]

# ================================
# GradCAM Utilities
# ================================
def make_gradcam_heatmap(img_array, model, layer_name, pred_index=None):
    """Generate a GradCAM heatmap for the specified layer and prediction index."""
    target_layer = model.get_layer(layer_name)

    # Feature extractor
    feature_model = tf.keras.Model(inputs=model.inputs, outputs=target_layer.output)

    # Classifier model (layers after target layer)
    classifier_input = tf.keras.Input(shape=target_layer.output.shape[1:])
    x = classifier_input
    all_layers = model.layers
    target_layer_idx = all_layers.index(target_layer)
    for layer in all_layers[target_layer_idx + 1:]:
        try:
            x = layer(x)
        except Exception:
            continue
    classifier_model = tf.keras.Model(inputs=classifier_input, outputs=x)

    # Gradient calculation
    with tf.GradientTape() as tape:
        features = feature_model(img_array)
        tape.watch(features)
        preds = classifier_model(features)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, features)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    weights = tf.reshape(pooled_grads, (1, 1, features.shape[-1]))
    features = features[0]
    cam = tf.reduce_sum(features * weights, axis=-1)

    # Normalize
    cam = tf.maximum(cam, 0)
    cam = cam / (tf.reduce_max(cam) + tf.keras.backend.epsilon())
    return cam.numpy()


def create_feature_images(img_path, heatmap, threshold=0.5):
    """Generate original, heatmap, outlines, and overlay images."""
    original_img = cv2.imread(img_path)
    if original_img is None:
        original_img = np.array(Image.open(img_path).convert("RGB"))
        original_img = cv2.cvtColor(original_img, cv2.COLOR_RGB2BGR)

    # Resize heatmap
    heatmap_resized = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
    heatmap_colored = np.uint8(255 * heatmap_resized)
    heatmap_colored = cv2.applyColorMap(heatmap_colored, cv2.COLORMAP_JET)

    # Contours
    _, binary_mask = cv2.threshold(
        np.uint8(255 * heatmap_resized), int(255 * threshold), 255, cv2.THRESH_BINARY
    )
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    outline_img = np.zeros_like(original_img)
    cv2.drawContours(outline_img, contours, -1, (0, 255, 0), 3)

    # Overlay outlines
    result_img = cv2.addWeighted(original_img, 1.0, outline_img, 1.0, 0)

    # Final combined (heatmap + outlines)
    superimposed_img = cv2.addWeighted(result_img, 0.7, heatmap_colored, 0.3, 0)

    return original_img, heatmap_colored, outline_img, superimposed_img


# ================================
# API: Predict Image
# ================================
@api_view(['POST'])
def predict_image(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=400)

    # Load & preprocess
    image_file = request.FILES['image']
    img = Image.open(image_file).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img)

    # Save original image
    temp_filename = f"input_{uuid.uuid4().hex}.png"
    img_path = os.path.join(settings.MEDIA_ROOT, temp_filename)
    cv2.imwrite(img_path, cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR))

    # Prediction
    img_tensor = np.expand_dims(img_array / 255.0, axis=0)
    predictions = model.predict(img_tensor)[0]
    class_index = int(np.argmax(predictions))
    confidence = float(np.max(predictions))
    class_name = class_names[class_index]

    # Quick heatmap for overlay
    heatmap = make_gradcam_heatmap(img_tensor, model, "conv2d_5", class_index)
    heatmap_resized = cv2.resize(heatmap, (224, 224))
    heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(
        img_array.astype("uint8"), 0.6,
        cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB),
        0.4, 0
    )

    # Save overlay
    overlay_filename = f"overlay_{uuid.uuid4().hex}.png"
    overlay_path = os.path.join(settings.MEDIA_ROOT, overlay_filename)
    cv2.imwrite(overlay_path, cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))

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
        "heatmap_image": f"/media/{overlay_filename}"
    })


# ================================
# API: Explore More (all 4 images)
# ================================
@api_view(['POST'])
def explore_more(request):
    img_path = request.data.get("image_path")
    if not img_path:
        return Response({"error": "No image path provided"}, status=400)

    # Resolve file path
    full_path = os.path.join(settings.MEDIA_ROOT, os.path.basename(img_path))
    if not os.path.exists(full_path):
        return Response({"error": "Image not found"}, status=404)

    # Prepare
    img = Image.open(full_path).resize((224, 224))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

    predictions = model.predict(img_array)[0]
    class_index = int(np.argmax(predictions))

    # GradCAM
    heatmap = make_gradcam_heatmap(img_array, model, "conv2d_5", class_index)
    original_img, heatmap_img, outline_img, superimposed_img = create_feature_images(full_path, heatmap)

    # Save all
    paths = {}
    for label, arr in [
        ("original", original_img),
        ("heatmap", heatmap_img),
        ("outlines", outline_img),
        ("combined", superimposed_img)
    ]:
        fname = f"{label}_{uuid.uuid4().hex}.png"
        outpath = os.path.join(settings.MEDIA_ROOT, fname)
        cv2.imwrite(outpath, arr)
        paths[label] = f"/media/{fname}"

    return Response(paths)