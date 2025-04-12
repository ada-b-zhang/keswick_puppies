import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Load the model once
style_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

def load_image(path, size=(256, 256)):
    img = Image.open(path).convert("RGB").resize(size)
    img = np.array(img) / 255.0
    return tf.constant(img, dtype=tf.float32)[tf.newaxis, ...]

def stylize_image(content_path, style_img_pil, output_path):
    content_img = load_image(content_path)
    style_img_pil = style_img_pil.resize((256, 256)).convert("RGB")
    style_img = tf.constant(np.array(style_img_pil) / 255.0, dtype=tf.float32)[tf.newaxis, ...]

    stylized_img = style_model(content_img, style_img)[0]
    stylized_array = (stylized_img[0].numpy() * 255).astype(np.uint8)
    stylized_pil = Image.fromarray(stylized_array)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    stylized_pil.save(output_path)
    return output_path
