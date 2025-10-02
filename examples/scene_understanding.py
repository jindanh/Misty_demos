'''
    Misty Scene Understanding Demo
    
    Author: Jindan Huang
    
    This script demonstrates Misty's computer vision capabilities:
    1. Takes a photo using Misty's camera
    2. Uses Gemma3:4b multimodal model to analyze and describe the scene
    3. Converts the description to speech using gTTS
    4. Plays the audio on Misty so she can "tell" you what she sees
    
    Outputs:
    - Photos saved to: images/misty_photos/
    - Audio files saved to: audio/
'''

import sys
import os
# add parent directory to path so we can import mistyPy and other modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)  # insert at beginning of path

from mistyPy.Robot import Robot
import base64
from gtts import gTTS       # text to speech 
from ollama import chat
from ollama import ChatResponse     # llm model responses
from ollama import generate
import speech_recognition as sr     # speech recognition
import threading
from utils import JSON_response_to_dictionary, text2audio, save_base64_image
from robot_utils import capture_image



if __name__ == "__main__":
    ip_address = "10.5.10.198"   # make sure your PC and misty are using the same network
    misty = Robot(ip_address)   # create an instance of a robot

    # take a picture and save it
    saved_image_path = capture_image(misty)

    # use gemma3:4b multimodal model to understand the scene
    gemma3_prompt = "explain the image within 20 words."     # To-do: explore prompts
    llm_output = ""
    for response in generate('gemma3:4b', gemma3_prompt, images=[saved_image_path], stream=True):
        chunk = response['response']
        llm_output += chunk
        print(chunk, end='', flush=True)

    # convert LLM response to audio and play on Misty
    audio_file = text2audio(llm_output)

    ENCODING = 'utf-8'
    encode_string = base64.b64encode(open(audio_file, "rb").read())
    base64_string = encode_string.decode(ENCODING)

    save_audio_response = misty.save_audio(audio_file, data=base64_string, overwriteExisting=True, immediatelyApply=True)
    save_audio = JSON_response_to_dictionary(save_audio_response)
    print("\nSaving Audio Response: " + str(save_audio))

    try:
        play_audio_response = misty.play_audio(audio_file)
        print(play_audio_response)
        print(play_audio_response.status_code)
        print(play_audio_response.json())
    except Exception as e:
        print("Error playing audio:", e)
    