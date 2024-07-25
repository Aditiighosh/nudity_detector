# Nudity / gore / violence detection 

This repository contains a Streamlit application for detecting nudity, gore, violence, and weapons in uploaded images. The application utilizes the NudeNet and Sightengine APIs to perform content detection and display results to the user.

# Technologies Used
1. NudeNet
   
NudeNet is a pre-trained model for detecting nudity in images and videos. It is designed to be accurate and efficient, providing detailed information about the type and location of nudity detected in an image. NudeNet can classify different parts of the body and identify exposed areas that may be deemed inappropriate.

3. Sightengine
   
Sightengine is a powerful content moderation and image analysis API. It provides various models to detect different types of inappropriate content such as gore, violence, and weapons. The API is easy to use and integrates well with various programming languages. It is particularly useful for applications requiring real-time or automated content moderation.

# NudeNet library documentation
https://pypi.org/project/nudenet/#description

# Sightengine API documentation
https://sightengine.com/docs/getstarted

# Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.6 or higher
- Streamlit
- NudeNet
- Requests
- Pillow
- os

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/aditiighosh/nudity_detector.git
   cd nudity_detector
2. Run the Streamlit application:
   streamlit run app.py
   

# app.py
The main application file for Streamlit. It integrates functionalities from nude.py and gore.py to provide a unified interface for content detection.

# gore.py
Contains functions to detect gore and violence using the Sightengine API.

# nude.py
Contains functions to detect nudity using the NudeNet library.

# API Keys
Make sure to replace the placeholders with your actual API keys in gore.py and app.py files


