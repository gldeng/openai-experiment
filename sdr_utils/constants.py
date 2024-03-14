COLLECTION_NAME = 'samples'
DALLE_RESULT_FIELD_NAME = 'dalle_result'
LEONARDO_API_KEY_NAME = 'LEONARDO_API_KEY'
LEONARDO_RESULT_FIELD_NAME = 'leonardo_result'
DREAM_SHAPER_MODEL_ID = 'ac614f96-1082-45bf-be9d-757f2d31c174'
BASE_PROMPT = 'A simple 128x128 pixel art image of a sitting down full-body cat '
AS_IS_PREFIX = 'I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:'
SUB_OPTIMAL_IMAGE_DETECTION_PROMPT = '''Is any of the following statements true about the image?
It contains more than one cat.
It contains text.
It contains a human character.
It is overlaid with a grid.
It contains a color scale or palette.
There are many small items surrounding the main character.'''