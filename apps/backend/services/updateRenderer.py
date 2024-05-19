import logging
from services import fixReactCode
from constants import RENDERER_FILE_PATH, RENDERER_TEMPLATE_FILE_PATH

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def updateRenderer(material_ui_imports, material_ui_components):
    try:
        with open(RENDERER_TEMPLATE_FILE_PATH, 'r') as file:
            content = file.read()

        updated_content = content.replace('{IMPORTS}', material_ui_imports)
        updated_content = updated_content.replace('{COMPONENTS}', material_ui_components)

        fixed_content = fixReactCode(updated_content)
        
        with open(RENDERER_FILE_PATH, 'w') as file:
            file.write(fixed_content)

        logger.info('Successfully updated the renderer file')
    except Exception as e:
        logger.error(f'Error updating the renderer file: {e}')
        raise
