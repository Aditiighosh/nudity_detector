import requests
import json

# Parameters for the API request
params = {
    'models': 'weapon,gore-2.0,violence',
    'api_user': '1059340949',  # Replace with your actual API user ID
    'api_secret': 'rpuE4donxjTCnJFrcNfjviqhp4NDramZ'  # Replace with your actual API secret
}

# Path to the image you want to check
image_path = '/Users/aditighosh/Desktop/nude_detector/nudes/nude.jpeg'

try:
    # Make the API request
    with open(image_path, 'rb') as image_file:
        files = {'media': image_file}
        response = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)
    
    # Check for HTTP errors
    response.raise_for_status()
    
    # Parse the response
    output = response.json()  # Using .json() directly for parsing
    
    # Print the full output for debugging
    print("API Response:", json.dumps(output, indent=4))
    
    # Check the response status
    if output['status'] == 'success':
        gore_prob = output['gore']['prob']
        gore_classes = output['gore']['classes']
        
        # Display if there is gore or not based on probability
        if gore_prob > 0.5:  # You can adjust the threshold as needed
            print("The image contains gore.")
        else:
            print("The image does not contain gore.")
        
        # Display the detailed gore classes and their probabilities
        print("Detailed Gore Probabilities:")
        for gore_class, prob in gore_classes.items():
            print(f"{gore_class}: {prob}")
    else:
        print("Failed to process the image. Please check the API request and try again.")
except Exception as e:
    print(f"An error occurred: {e}")

# Check violence information
violence_prob = output['violence']['prob']
violence_classes = output['violence']['classes']

# Display if there is violence or not based on probability
if violence_prob > 0.5:  # You can adjust the threshold as needed
    print("The image contains violence.")
else:
    print("The image does not contain violence.")

# Display the detailed violence classes and their probabilities
print("Detailed Violence Probabilities:")
for violence_class, prob in violence_classes.items():
    print(f"{violence_class}: {prob}")
# Check weapon information
weapon_classes = output['weapon']['classes']

# Display if there is any detected weapon based on probability
weapon_detected = False
for weapon_class, prob in weapon_classes.items():
    if prob > 0.5:  # Adjust the threshold if needed
        weapon_detected = True
        break

if weapon_detected:
    print("The image contains weapons.")
else:
    print("The image does not contain weapons.")

# Display the detailed weapon classes and their probabilities
print("Detailed Weapon Probabilities:")
for weapon_class, prob in weapon_classes.items():
    print(f"{weapon_class}: {prob}")

