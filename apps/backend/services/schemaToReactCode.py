import logging
import requests
import json
from constants import HEADERS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def schemaToReactCode(component_name, component_properties):
    logger.info(f'Extracted component schema for {component_name}: {component_properties}')

    prompt = f"""
        Follow this schema to return a JSON response: 
        ```
        {{ 
            {component_name}: {{
                code: <component code without imports, should be a string>, 
                imports: <imports required for the component, should be a string> 
            }} 
        }}
        
        Convert the following {component_name} component schema to Material-UI React code,
        return the component code without wrappers and required imports separately:
        {component_properties}
    """

    payload = {
        "model": "gpt-4o",
        "response_format": {
            "type": "json_object"
        },
        "messages": [
            {
                "role": "system",
                "content": "You are an AI assistant specialized in converting component schemas to Material-UI React components. Return JSON."
            },
            {
                "role": "user",
                "content": [
                {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "max_tokens": 2000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=HEADERS, json=payload)
    response.raise_for_status()

    response_json = response.json()
    logger.info(f'Received Material-UI React component from ChatGPT: {response_json}')

    # Extract the data from the JSON response
    component_data = json.loads(response_json['choices'][0]['message']['content'])[component_name]
    
    return component_data
    