import logging
import requests
import json
from constants import HEADERS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fixReactCode(code):
    logger.info('Fixing renderer file')
    payload = {
        "model": "gpt-4o",
        "response_format": {
            "type": "json_object"
        },
        "messages": [
            {
                "role": "system",
                "content": """
                    You are a web developer. Your role is to analyze react code and do small fixes to make the code functional for Next.js 14.
                    Follow this schema to return a JSON response: { code: <fixed code> }

                    Other rules to apply:
                    - Remember including `"use client";` at the top, as this is only UI.
                """
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Fix the following react code if there are errors."
                    },
                    {
                        "type": "text",
                        "text": code
                    }
                ]
            }
        ],
        "max_tokens": 2000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=HEADERS, json=payload)
    response.raise_for_status()

    response_json = response.json()
    logger.info(f'Received fixed React component from ChatGPT: {response_json}')

    # Extract the data from the JSON response
    fixed_code = json.loads(response_json['choices'][0]['message']['content'])["code"]
    
    return fixed_code
