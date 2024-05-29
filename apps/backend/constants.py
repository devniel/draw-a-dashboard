import os

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Path to the Next.js renderer file
RENDERER_FILE_PATH = os.getenv('RENDERER_FILE_PATH')
RENDERER_TEMPLATE_FILE_PATH = os.getenv('RENDERER_TEMPLATE_FILE_PATH')
PORT_BACKEND = int(os.getenv('PORT_BACKEND', 5000))

# OpenAI API Headers
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}