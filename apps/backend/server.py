import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.utils import encodeImage
from services import analyzeImage, schemaToReactCode, updateRenderer
from constants import PORT_BACKEND

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/toDashboard', methods=['POST'])
def to_dashboard():
    logger.info('Received request for /toDashboard endpoint')

    if 'image' not in request.files:
        logger.error('No image provided in the request')
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']

    try:
        # Read the image file as bytes
        image_bytes = image.read()
        base64_image = encodeImage(image_bytes)

        analyze_response = analyzeImage(base64_image)
        components = analyze_response["components"]  # Extract the root properties (components)
        logger.info(f'Extracted components: {components}')

        material_ui_imports = ""
        material_ui_components = ""

        for component in components:
            component_data = schemaToReactCode(component["type"], component["properties"])
            material_ui_imports += component_data["imports"] + "\n\n"
            material_ui_components += component_data["code"] + "\n\n"

        # Update the renderer file with the generated Material-UI code
        updateRenderer(material_ui_imports, material_ui_components)

        return jsonify({'status': 'success'})
        
    except Exception as e:
        logger.error(f'Error processing the image: {e}')
        return jsonify({'error': 'Failed to process the image'}), 500

if __name__ == '__main__':
    logger.info(f'Starting backend server on port {PORT_BACKEND}')
    app.run(host='0.0.0.0', port=PORT_BACKEND)