import streamlit as st
from dotenv import load_dotenv
import os
from nudenet import NudeDetector
import requests
from io import BytesIO
from PIL import Image

# Load environment variables from .env file
load_dotenv()
SIGHTENGINE_USER_ID = os.getenv('SIGHTENGINE_USER_ID')
SIGHTENGINE_API_SECRET = os.getenv('SIGHTENGINE_API_SECRET')

# Function to set background color to red (optional)
def set_red_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: red;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply the background color (optional)
set_red_background()  # Uncomment if you want a red background

# Custom HTML with inline CSS for the title
custom_text = """
<div style="
    color: white;
    background-color: maroon;
    padding: 10px;
    border-radius: 5px;
    font-family: 'Arial Black', Gadget, sans-serif;
    font-size: 20px;
    text-align: center;
">
    Nudity, Gore, and Violence Detection
</div>
"""

st.markdown(custom_text, unsafe_allow_html=True)

# Initialize the NudeDetector once
try:
    detector = NudeDetector()
except Exception as e:
    st.error(f"Error initializing NudeDetector: {e}")
    st.stop()

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
        is_censored = any(
            det['class'] in unsafe_classes and det['score'] > 0.4 for det in detections
        )
        return {"nudity": {"safe": not is_censored, "unsafe": is_censored}}
    except Exception as e:
        st.error(f"Error in nudity detection: {e}")
        return {"nudity": {"safe": False, "unsafe": False}}

def detect_gore_violence(image_data):
    params = {
        'models': 'weapon,gore-2.0,violence',
        'api_user': SIGHTENGINE_USER_ID,
        'api_secret': SIGHTENGINE_API_SECRET
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
    # Inject custom CSS for styling
    # Inject custom CSS for styling
    st.markdown("""
        <style>
        /* Custom label styling */
        .custom-file-uploader-label {
            color: white; /* Set text color to white */
            font-size: 24px; /* Adjust font size as needed */
            font-family: 'Arial Black', Gadget, sans-serif; /* Choose your desired font */
            margin-bottom: 10px; /* Add spacing below the label */
            text-align: center; /* Center the label text */
        }

        /* Center the uploader and shift it upwards */
        .uploader-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: -50px; /* Negative margin to shift upwards */
        }

        /* Customize the file uploader button */
        div.stFileUploader > label {
            background-color: #4CAF50; /* Button background color */
            color: white; /* Button text color */
            padding: 10px 20px; /* Button padding */
            border-radius: 5px; /* Rounded corners */
            cursor: pointer; /* Pointer cursor on hover */
            font-size: 16px; /* Button text size */
            font-family: Arial, sans-serif; /* Button font */
            transition: background-color 0.3s ease; /* Smooth transition */
            margin-top: 10px; /* Additional spacing if needed */
        }

        /* Change button color on hover */
        div.stFileUploader > label:hover {
            background-color: #45a049;
        }

        /* Optional: Adjust other elements if necessary */
        </style>
        """, unsafe_allow_html=True)

    # Create a container to center the elements
    with st.container():
        st.markdown('<div class="uploader-container">', unsafe_allow_html=True)

        # Add the custom styled label
        st.markdown('<div class="custom-file-uploader-label">Upload Photo</div>', unsafe_allow_html=True)

        # Add the file uploader with the default label hidden
        uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility='hidden')


        if uploaded_file is not None:
            try:
                # Open the image using PIL
                image = Image.open(uploaded_file)
                
                # Display the uploaded image
                st.image(image, caption='Uploaded Image.', use_column_width=True)

                # Convert image to BytesIO for in-memory processing
                image_data = BytesIO()
                image.save(image_data, format="JPEG")
                image_data.seek(0)

                # Detect nudity
                st.write("### Detecting Nudity...")
                nudity_result = detect_nudity(image_data)
                
                if nudity_result["nudity"]["unsafe"]:
                    st.error("⚠️ The image contains nudity.")
                else:
                    st.success("✅ The image does not contain nudity.")
                
                # Reset image_data pointer to the start for reuse
                image_data.seek(0)
                
                # Detect gore and violence
                st.write("### Detecting Gore and Violence...")
                gore_violence_result = detect_gore_violence(image_data)
                
                if gore_violence_result.get('status') == 'success':
                    # Gore Detection
                    gore_prob = gore_violence_result.get('gore', {}).get('prob', 0)
                    if gore_prob > 0.5:
                        st.error("⚠️ The image contains gore.")
                    else:
                        st.success("✅ The image does not contain gore.")
                    
                    # Violence Detection
                    violence_prob = gore_violence_result.get('violence', {}).get('prob', 0)
                    if violence_prob > 0.5:
                        st.error("⚠️ The image contains violence.")
                    else:
                        st.success("✅ The image does not contain violence.")
                    
                    # Weapon Detection
                    weapon_classes = gore_violence_result.get('weapon', {}).get('classes', {})
                    weapon_detected = any(prob > 0.5 for prob in weapon_classes.values())
                    if weapon_detected:
                        st.error("⚠️ The image contains weapons.")
                    else:
                        st.success("✅ The image does not contain weapons.")
                else:
                    st.error("❌ Failed to process the image. Please check the API request and try again.")

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
