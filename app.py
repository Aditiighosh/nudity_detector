import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
SIGHTENGINE_USER_ID = os.getenv('SIGHTENGINE_USER_ID')
SIGHTENGINE_API_SECRET = os.getenv('SIGHTENGINE_API_SECRET')
try:
    from nudenet import NudeDetector
except ImportError as e:
    st.error(f"ImportError: {e}")
import requests
from io import BytesIO
from PIL import Image

# Initialize the NudeDetector once
detector = NudeDetector()

def detect_nudity(image_data):
    try:
        # Convert image_data to bytes
        image_bytes = image_data.read()
        detections = detector.detect(image_bytes)
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
        return {"nudity": {"safe": not is_censored, "unsafe": is_censored}}
    except Exception as e:
        st.error(f"Error in nudity detection: {e}")
        return {"nudity": {"safe": False, "unsafe": False}}

def detect_gore_violence(image_data):
    params = {
        'models': 'weapon,gore-2.0,violence',
        'api_user': os.getenv('SIGHTENGINE_USER_ID'),
        'api_secret': os.getenv('SIGHTENGINE_API_SECRET')
    }
    
    try:
        # Convert image_data to bytes
        image_bytes = image_data.read()
        files = {'media': ('image.jpg', image_bytes, 'image/jpeg')}
        response = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)
        
        response.raise_for_status()
        output = response.json()
        return output
    except Exception as e:
        st.error(f"Error in gore/violence detection: {e}")
        return {"status": "error"}


def main():
    st.title("Nudity, Gore, and Violence Detection")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Convert image to BytesIO for in-memory processing
        image_data = BytesIO()
        image.save(image_data, format="JPEG")
        image_data.seek(0)
        
        # Detect nudity
        st.write("Detecting nudity...")
        nudity_result = detect_nudity(image_data)
        
        if nudity_result["nudity"]["unsafe"]:
            st.error("The image contains nudity.")
        else:
            st.success("The image does not contain nudity.")
        
        # Reset image_data pointer to the start for reuse
        image_data.seek(0)
        
        # Detect gore and violence
        st.write("Detecting gore and violence...")
        gore_violence_result = detect_gore_violence(image_data)
        
        if gore_violence_result['status'] == 'success':
            gore_prob = gore_violence_result['gore']['prob']
            violence_prob = gore_violence_result['violence']['prob']
            weapon_detected = any(prob > 0.5 for prob in gore_violence_result['weapon']['classes'].values())
            
            if gore_prob > 0.5:
                st.error("The image contains gore.")
            else:
                st.success("The image does not contain gore.")
            
            if violence_prob > 0.5:
                st.error("The image contains violence.")
            else:
                st.success("The image does not contain violence.")
            
            if weapon_detected:
                st.error("The image contains weapons.")
            else:
                st.success("The image does not contain weapons.")
        else:
            st.error("Failed to process the image. Please check the API request and try again.")

if __name__ == "__main__":
    main()
