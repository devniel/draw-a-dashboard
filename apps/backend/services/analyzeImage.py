import logging
import requests
from constants import HEADERS
from utils.utils import extract_json_content

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyzeImage(base64_image):
    logger.info('Sending image to OpenAI API')
    payload = {
        "model": "gpt-4o",
        "response_format": {
            "type": "json_object"
        },
        "messages": [
            {
                "role": "system",
                "content": """
                You are a web developer. Your role is to receive images, such as drawings or mockups, of user interfaces for web dashboards. Your task is to analyze these images to understand the design and layout, identify the used components and reply with a declarative schema of the input translated into a dashboard.

                Follow this schema to return a JSON response: 
                ```    
                    { 
                        components: [
                            {
                                type: <component name>,
                                id: <uuid>
                                properties: <component properties>
                            }
                        ]
                    }
                ```

                Follow this rules to create the schema:
                - <component name> should be the name of a valid MaterialUI React component.
                - <uuid> a generated uniqued id.
                - <component properties> should be a key, value json of the component properties and values 
                  based on the component API and MUI documentation. Don't use library-related properties
                  such as `children`.
                - Ignore the content if there is a sub-component inside the component.
                """
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image? Return the detected components in the image, in a JSON format."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 2000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=HEADERS, json=payload)
    response.raise_for_status()

    response_json = response.json()
    logger.info(f'Received response from OpenAI API: {response_json}')

    # Extract JSON content
    message_content = response_json.get('choices', [])[0].get('message', {}).get('content', '')
    schema_json = extract_json_content(message_content)
    
    if schema_json is None:
        logger.error('Failed to extract JSON from the response')
        raise ValueError('Failed to extract JSON from the response')
    
    return schema_json
