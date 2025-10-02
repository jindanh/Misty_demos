# Misty_demos

 




### Multi-modal Human-Robot Interaction Demos 
#### Implemented Functions 
**Multi-turn Conversation**: Users can talk to Misty and Misty processes the input and respond verbally using a language model (e.g. Llama3.2)    

Example:  
```bash
python examples/multi_turn_conversation.py
```

**Scene Understanding**: Misty takes a picture and use a language model (e.g. Gemma3:4b) to interpret and describe the scene   

Example:  
```bash
python examples/scene_understanding.py
```

### Package Requirements
- Misty Python SDK:  https://github.com/MistyCommunity/Python-SDK/tree/main  
- Google Text-to-speech (gTTS): https://pypi.org/project/gTTS/ 
- Ollama: https://github.com/ollama/ollama  (this package allows you to run LLMs on your Mac/Windows/Linux)  

Examples of using Ollama with Misty:  
- Text/voice interaction: `misty_llama.py`

#### Install dependencies

Using a virtual environment or conda environment is recommended to keep dependencies isolated.

1) Create and activate conda environment
```bash
conda create -n misty python=3.9 -y
conda activate misty
```

2) Install all dependencies
```bash
pip install mistyPy
pip install -r requirements.txt
```

#### Quickstart: Run the basic connection test

1) Configure your Misty IP
- Open `connection_testing.py` and set the `ip_address` variable to your robot's IP (ensure your computer and Misty are on the same network).

2) Run

```bash
python connection_testing.py
```

3) What to expect
- Arms move (movement test)
- An audio.mp3 is generated locally and sent to Misty; you should hear it speak
- A photo is taken;

Output locations
- Photos: `images/misty_photos/` 
- Audio files: `audio/`

Troubleshooting
- If you don't hear speech, verify speakers on Misty and that `gTTS` saved `audio.mp3` successfully.
- If you cannot connect, recheck the IP address and that both devices share the same network.