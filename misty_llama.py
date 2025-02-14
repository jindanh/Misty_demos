'''
    Integrating Misty with Llama3.2 model
'''

from mistyPy.Robot import Robot
import base64
from gtts import gTTS       # text to speech 
from ollama import chat
from ollama import ChatResponse     # llm model responses
import speech_recognition as sr     # speech recognition
DEBUG_JSON_REQUESTS = False

def JSON_response_to_dictionary(response):
    API_Data = response.json()
    if DEBUG_JSON_REQUESTS:
        for key in API_Data:
            {print(key,":", API_Data[key])}
    return API_Data


def LLMtext2audio(llm_text, language='en'):
    speech = gTTS(text=llm_text, lang=language, slow=False)
    file_name = "audio.mp3"
    speech.save(file_name) # GTTS says you can save as .wav but it lies, it's still a .mp3 object at heart, just a heads up
    return file_name

if __name__ == "__main__":
    ip_address = "10.5.9.252"   # make sure your PC and misty are using the same network
    # Create an instance of a robot
    misty = Robot(ip_address)

    # obtain audio from the microphone
    r = sr.Recognizer()

    try:
        print("I am Misty. Happy to talk with you! ")
        while True:

            # ### option 1: interact with Misty through typing                  - uncomment it to use
            # print("Please type whatever you want to share with me.")
            # user_input = input()


            ### option 2: interact with Misty through speech 
            print("Start listening: press 'y' to record")       # press 'y' if you want the program to detect your speech
            start_listening = input()

            with sr.Microphone() as source:     # listen user speech 
                print("Say something!")
                if start_listening == 'y':
                    user_audio = r.listen(source, 5)

            # recognize speech using whisper
            try:
                user_input = r.recognize_whisper(user_audio, language="english")
                print("Whisper thinks you said " + user_input)     # To-do: let user check if the speech recognition is correct
            except sr.UnknownValueError:
                print("Whisper could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Whisper; {e}")
            
            # Generating responses with Llama3.2 3B model 
            response: ChatResponse = chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': user_input+" Please provide a one-sentence answer and be friendly.",     # To-do: explore prompts
            },
            ])
            response_text = response['message']['content']
            # language = 'en'
            # speech = gTTS(text=response_text, lang=language, slow=False)
            # file_name = "audio.mp3"
            # speech.save(file_name) # GTTS says you can save as .wav but it lies, it's still a .mp3 object at heart, just a heads up
            
            audio_file = LLMtext2audio(response_text)

            ENCODING = 'utf-8'
            encode_string = base64.b64encode(open(audio_file, "rb").read())
            base64_string = encode_string.decode(ENCODING)

            save_audio_response = misty.save_audio(audio_file, data=base64_string, overwriteExisting=True, immediatelyApply=True)
            save_audio = JSON_response_to_dictionary(save_audio_response)
            print("Saving Audio Response: " + str(save_audio))

    except KeyboardInterrupt:
        pass
    