import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# Load the trained model
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('brain_tumor_model.h5')
    return model

model = load_model()

# Define image dimensions and class names
IMG_WIDTH = 150
IMG_HEIGHT = 150
CLASS_NAMES = ['glioma', 'meningioma', 'notumor', 'pituitary'] # Ensure this matches your training order

st.title('Brain Tumor Detection App')
st.write('Upload an MRI image to predict if a tumor is present and its type.')

uploaded_file = st.file_uploader("Choose an MRI image...", type=["jpg", "jpeg", "png"]) # Allow multiple image types

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded MRI Image', use_column_width=True)
    st.write("")

    if st.button('Predict'):
        # Preprocess the image
        img_array = image.resize((IMG_WIDTH, IMG_HEIGHT))
        img_array = np.array(img_array)
        img_array = np.expand_dims(img_array, axis=0) # Add batch dimension
        img_array = img_array / 255.0 # Rescale image

        # Make prediction
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        predicted_class_index = np.argmax(score)
        predicted_class = CLASS_NAMES[predicted_class_index]
        confidence = np.max(score) * 100

        st.success(f"Prediction: This image most likely belongs to the **{predicted_class}** category with a **{confidence:.2f}%** confidence.")

        st.subheader("All Predictions:")
        for i, class_name in enumerate(CLASS_NAMES):
            st.write(f"- {class_name}: {score[i]*100:.2f}%")
