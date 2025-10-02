import base64
import speech_recognition as sr
from utils import JSON_response_to_dictionary, text2audio, save_base64_image
from datetime import datetime
from ollama import chat
'''
    Interact with Misty through speech
'''
def talk_to_misty(misty):
    try:
        r = sr.Recognizer()
        r.dynamic_energy_threshold = False

        print("I am Misty. Happy to talk with you! ")
        while True:
            print("Start listening: press 'y' to record")
            start_listening = input()

            with sr.Microphone() as source:
                print("Say something!")
                if start_listening == 'y':
                    user_audio = r.listen(source, 15)

            try:
                user_input = r.recognize_whisper(user_audio, language="english")
                print("Whisper thinks you said " + user_input)
            except sr.UnknownValueError:
                print("Whisper could not understand audio")
                continue
            except sr.RequestError as e:
                print(f"Could not request results from Whisper; {e}")
                continue

            response = chat(model='llama3.2', messages=[
                {'role': 'user', 'content': user_input + " Please provide a concise answer in 30 words and be friendly."},
            ])
            response_text = response['message']['content']
            print("LLM response: " + response_text)

            audio_file = text2audio(response_text)

            ENCODING = 'utf-8'
            encode_string = base64.b64encode(open(audio_file, "rb").read())
            base64_string = encode_string.decode(ENCODING)

            save_audio_response = misty.save_audio(audio_file, data=base64_string, overwriteExisting=True, immediatelyApply=True)
            save_audio = JSON_response_to_dictionary(save_audio_response)
            print("Saving Audio Response: " + str(save_audio))

            try:
                play_audio_response = misty.play_audio(audio_file)
                print(play_audio_response)
                print(play_audio_response.status_code)
                print(play_audio_response.json())
            except Exception as e:
                print("Error playing audio:", e)

    except KeyboardInterrupt:
        pass

'''
    Misty takes a picture and save it
'''
def capture_image(misty):
    try:
        photo_name = "myphoto"
        photo_name = photo_name + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") # add timestamp to the photo name
        new_picture_response = misty.take_picture("true", photo_name, 800, 600, "true", "true")
        save_pic = JSON_response_to_dictionary(new_picture_response)
        saved_image_path = save_base64_image(save_pic["result"])
        return saved_image_path
    except KeyboardInterrupt:
        pass


