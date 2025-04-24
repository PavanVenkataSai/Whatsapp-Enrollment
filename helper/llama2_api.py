import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

# API_URL = "https://api-inference.huggingface.co/models/meta-lab/llama2"

# API_URL = "https://api-inference.huggingface.co/models/meta-lab/llama-2"

# API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat"
API_URL = "https://huggingface.co/meta-llama/Llama-2-7b-chat"
HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_TOKEN')}"}

def text_complition(prompt: str) -> dict:
    '''
    Call Llama 2 API for text completion

    Parameters:
        - prompt: user query (str)

    Returns:
        - dict
    '''
    try:
        data = {
            "inputs": f"Human: {prompt}\nAI:",
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.9,
                "top_p": 1,
                "presence_penalty": 0.6,
                "frequency_penalty": 0,
                "stop": ["Human:", "AI:"]
            }
        }
        response = requests.post(API_URL, headers=HEADERS, data=json.dumps(data)).json()
        print(response)
        return {
            'status': 1,
            'response': response['generated_text']
        }
    except:
        return {
            'status': 0,
            'response': 'KD'
        }