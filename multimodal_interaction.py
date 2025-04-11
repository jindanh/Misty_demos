'''
    Integrating Misty with Llama3.2 and Gemma3 model
'''

from mistyPy.Robot import Robot
import base64
from gtts import gTTS       # text to speech 
from ollama import chat
from ollama import ChatResponse     # llm model responses
from ollama import generate
import speech_recognition as sr     # speech recognition
import threading
from utils import JSON_response_to_dictionary, text2audio, save_base64_image


'''
    Interact with Misty through speech
'''
def talk_to_misty():
    try:
        # obtain audio from the microphone
        r = sr.Recognizer()
        r.dynamic_energy_threshold = False

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
                    user_audio = r.listen(source, 15)

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
                'content': user_input+" Please provide a concise answer and be friendly.",     # To-do: explore prompts
            },
            ])
            response_text = response['message']['content']
            print("LLM response: "+response_text)
            
            audio_file = text2audio(response_text)

            ENCODING = 'utf-8'
            encode_string = base64.b64encode(open(audio_file, "rb").read())
            base64_string = encode_string.decode(ENCODING)

            save_audio_response = misty.save_audio(audio_file, data=base64_string, overwriteExisting=True, immediatelyApply=True)
            save_audio = JSON_response_to_dictionary(save_audio_response)
            print("Saving Audio Response: " + str(save_audio))

    except KeyboardInterrupt:
        pass



'''
    Misty takes a picture and save it
'''
def capture_image():
    try:
        # take a picture using Misty's camera
        new_picture_response = misty.take_picture("true","myphoto", 800, 600,"true","true")
        save_pic = JSON_response_to_dictionary(new_picture_response)
        saved_image_path = save_base64_image(save_pic["result"])

        return saved_image_path

    except KeyboardInterrupt:
        pass
        


if __name__ == "__main__":
    ip_address = "10.5.10.198"   # make sure your PC and misty are using the same network
    misty = Robot(ip_address)   # create an instance of a robot

    # take a picture and save it
    saved_image_path = capture_image()

    # use gemma3:4b multimodal model to understand the scene
    gemma3_prompt = "explain the image"     # To-do: explore prompts
    for response in generate('gemma3:4b', gemma3_prompt, images=[saved_image_path], stream=True):
        print(response['response'], end='', flush=True)
    

    # # obtain audio from the microphone
    # r = sr.Recognizer()
    # r.dynamic_energy_threshold = False

    # to-do: see if the threading is needed
    # talking_thread = threading.Thread(target=talk_to_misty)
    # camera_thread = threading.Thread(target=capture_image)

    # while True:
    #     user_input = input()
    #     if user_input == 's':
    #         talking_thread.start()
    #     elif user_input == 'p':
    #         camera_thread.start()
    #     elif user_input == 'q':
    #         break

    
    