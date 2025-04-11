# Misty_demos

**Package Requirements**  
- Misty Python SDK:  https://github.com/MistyCommunity/Python-SDK/tree/main  
- Google Text-to-speech (gTTS): https://pypi.org/project/gTTS/  

**Demo: Integrating Misty with LLM models**  
Ollama: https://github.com/ollama/ollama  - This package allows you to run LLMs on your Mac/Windows/Linux  
`pip install ollama`  

Example: `misty_llama.py`


**Demo: Misty Multimodal Interaction**  
Implemented Functions: 
- Speech: Users can talk to Misty and Misty processes the input and respond verbally using a language model (e.g. Llama3.2)   
- Vision: Misty takes a picture and use a language model (e.g. Gemma3:4b) to interpret and describe the scene   

Example: `multimodal_interaction.py`