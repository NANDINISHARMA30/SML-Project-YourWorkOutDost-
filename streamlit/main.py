#Streamlit web application to interact with a pre-trained gym equipment recognition model
import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image


# Tensorflow Model Prediction
def model_prediction(test_image):
    # Load model
    model = tf.keras.models.load_model("model.h5")
    
    # Preprocess the input image
    image = Image.open(test_image).resize((128, 128))  # Resize to match the model's input size
    input_arr = np.array(image) / 255.0  # Normalize to [0, 1]
    input_arr = np.expand_dims(input_arr, axis=0)  # Convert single image to batch format

    # Make predictions
    predictions = model.predict(input_arr)
    return np.argmax(predictions)  # Return the index of the maximum element


# Sidebar
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About Project", "Prediction"])

# Main Page
if app_mode == "Home":
    st.header("GYM EQUIPMENT RECOGNITION SYSTEM")
    image_path = "home.jpg"
    st.image(image_path)

# About Project
elif app_mode == "About Project":
    st.header("About Project")
    st.subheader("About Dataset")
    st.text("This dataset contains images of the following gym equipment:")
    st.code("Dumbbells, Barbell, Treadmill, Bench Press, Punching Bag, etc.")
    st.subheader("Content")
    st.text("This dataset contains folders for training images.")

# Prediction Page
elif app_mode == "Prediction":
    st.header("Model Prediction")
    
    # Upload test image
    test_image = st.file_uploader("Choose an Image:", type=["jpg", "jpeg", "png"])
    
    if test_image is not None:
        # Show the uploaded image
        st.image(test_image, use_column_width=True, caption="Uploaded Image")
        
        # Predict button
        if st.button("Predict"):
            st.snow()
            st.write("Our Prediction:")
            
            # Make predictions using the model
            result_index = model_prediction(test_image)
            
            # Reading Labels
            with open("label.txt", "r") as f:
                label = [line.strip() for line in f.readlines()]
            
            # Display the result
            st.success(f"Model is Predicting it's a: **{label[result_index]}**")    