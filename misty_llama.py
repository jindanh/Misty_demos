'''
    Integrating Misty with Llama3.2 model
'''

from mistyPy.Robot import Robot
import base64
from gtts import gTTS       # text to speech 
from ollama import chat
from ollama import ChatResponse     # llm model responses
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

    try:
        while True:
            print("I am Misty. Please type anything you want to talk to me: ")
            user_input = input()                # To-do: add speech recognition
            
            # Generating responses with Llama3.2 3B model 
            response: ChatResponse = chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': user_input+" Please provide a one-sentence answer.",     # To-do: explore prompts
            },
            ])
            response_text = response['message']['content']
            language = 'en'
            speech = gTTS(text=response_text, lang=language, slow=False)
            file_name = "audio.mp3"
            speech.save(file_name) # GTTS says you can save as .wav but it lies, it's still a .mp3 object at heart, just a heads up
            
            ENCODING = 'utf-8'
            encode_string = base64.b64encode(open(file_name, "rb").read())
            base64_string = encode_string.decode(ENCODING)

            save_audio_response = misty.save_audio(file_name, data=base64_string, overwriteExisting=True, immediatelyApply=True)
            save_audio = JSON_response_to_dictionary(save_audio_response)
            print("Saving Audio Response: " + str(save_audio))

    except KeyboardInterrupt:
        pass
    