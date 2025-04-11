import os
import base64
from gtts import gTTS       # text to speech 

'''
    Convert a json response to a dictionary
    - response is the response from the API
    - DEBUG_JSON_REQUESTS is a boolean to print the json response
    - returns the json response as a dictionary
'''
def JSON_response_to_dictionary(response, DEBUG_JSON_REQUESTS=False):
    API_Data = response.json()
    if DEBUG_JSON_REQUESTS:
        for key in API_Data:
            {print(key,":", API_Data[key])}
    return API_Data


'''
    Save a base64 image to the images directory
    - response_data is the response from the take_picture function, json format
    - output_dir is the directory to save the image to
    - returns the filepath of the saved image
'''
def save_base64_image(response_data, output_dir="images/misty_photos"):
    # Create images directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get the base64 string and filename from the response
    base64_string = response_data["base64"]
    filename = response_data["name"]
    
    # Decode the base64 string to binary data
    image_data = base64.b64decode(base64_string)
    
    # Save the image
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "wb") as f:
        f.write(image_data)
    
    return filepath


'''
    Convert text to audio
    - llm_text is the text to convert to audio
    - language is the language of the audio
    - returns the filepath of the saved audio
'''
def text2audio(llm_text, language='en', file_name="audio.mp3"):
    speech = gTTS(text=llm_text, lang=language, slow=False)
    speech.save(file_name) # GTTS says you can save as .wav but it lies, it's still a .mp3 object at heart, just a heads up
    return file_name