from mistyPy.Robot import Robot
import base64
from gtts import gTTS       # text to speech 
DEBUG_JSON_REQUESTS = False

def JSON_response_to_dictionary(response):
    API_Data = response.json()
    if DEBUG_JSON_REQUESTS:
        for key in API_Data:
            {print(key,":", API_Data[key])}
    return API_Data

if __name__ == "__main__":
    ip_address = "10.5.9.252"   # make sure your PC and misty are using the same network
    # Create an instance of a robot
    misty = Robot(ip_address)
    # Movement testing
    current_response = misty.move_arms(80, 20)
    print(current_response)
    print(current_response.status_code)
    print(current_response.json())

    current_response = misty.get_log_level()
    print(current_response)
    print(current_response.status_code)
    print(current_response.json())
    print(current_response.json()["result"])

    # Speak testing: text-to-audio
    text = "How are you doing today? I am happy to talk with you"
    language = 'en'
    speech = gTTS(text=text, lang=language, slow=False)
    file_name = "audio.mp3"
    speech.save(file_name) # GTTS says you can save as .wav but it lies, it's still a .mp3 object at heart, just a heads up
    
    ENCODING = 'utf-8'
    encode_string = base64.b64encode(open(file_name, "rb").read())
    base64_string = encode_string.decode(ENCODING)

    save_audio_response = misty.save_audio(file_name, data=base64_string, overwriteExisting=True, immediatelyApply=True)
    save_audio = JSON_response_to_dictionary(save_audio_response)
    print("Saving Audio Response: " + str(save_audio))