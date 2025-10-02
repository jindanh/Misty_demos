'''
    Multi-Turn Conversation with Misty
    
    Author: Jindan Huang
    
    This script enables interactive speech conversation with Misty:
    1. Press 'y' to start listening to your voice for each turn
    2. Speak to Misty (your speech is converted to text using Whisper)
    3. Misty processes your input with Llama3.2 language model
    4. Misty responds verbally using gTTS and plays the audio
    
    Outputs:
    - Audio files saved to: audio/ (with timestamps)
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
from robot_utils import talk_to_misty


if __name__ == "__main__":
    ip_address = "10.5.10.198"   # make sure your PC and misty are using the same network
    misty = Robot(ip_address)   # create an instance of a robot
    
    # interact with Misty through speech
    talk_to_misty(misty)
