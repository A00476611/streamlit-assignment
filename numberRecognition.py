import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# Load the trained model
model = load_model("digit_classifier_model.h5")

def preprocess_image(rgba_image):
    alpha_channel = rgba_image[:, :, 3]
    grayscale_image = Image.fromarray(alpha_channel)
    binary_image = grayscale_image.point(lambda x: 255 if x > 128 else 0, 'L')
    resized_image = binary_image.resize((28, 28))
    normalized_image = np.array(resized_image) / 255.0
    normalized_image = np.expand_dims(normalized_image, axis=-1)

    return normalized_image

def main():
    st.title("Number Recognition App")

    # Upload image
    uploaded_file = st.file_uploader("Upload PNG image with numbers", type=["png"])

    if uploaded_file is not None:
        image = np.array(Image.open(uploaded_file))
        preprocessed_image = preprocess_image(image)
        st.image(image, caption='Original Image', use_column_width=True)
        pil_image = Image.fromarray((preprocessed_image.squeeze() * 255).astype(np.uint8))
        prediction = model.predict(np.expand_dims(preprocessed_image, axis=0))
        predicted_number = np.argmax(prediction)
        st.write(f"Predicted Number: {predicted_number}")

if __name__ == "__main__":
    main()
