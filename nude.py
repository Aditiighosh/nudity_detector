from nudenet import NudeDetector
import streamlit as st
from PIL import Image
import os

# Initialize the NudeDetector
detector = NudeDetector()

# Set up the Streamlit interface
st.title("Image Nudity Detection")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary directory
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Display the uploaded image
    # image = Image.open(uploaded_file)
    #st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Detect nudity in the uploaded image
    detections = detector.detect(file_path)
    
    # Print detections to understand the structure
    #st.write("Detections:", detections)
    
    # Define unsafe classes
    unsafe_classes = [
        "BUTTOCKS_EXPOSED",
        "FEMALE_GENITALIA_EXPOSED",
        "MALE_BREAST_EXPOSED",
        "ANUS_EXPOSED",
        "MALE_GENITALIA_EXPOSED",
        "FEMALE_BREAST_EXPOSED"
    ]
    
    # Check if any detection is unsafe
    is_censored = any(det['class'] in unsafe_classes and det['score'] > 0.4 for det in detections)
    
    # Display the result
    if is_censored:
        st.error("The image contains censored content.")
    else:
        st.success("The image is safe.")
    

