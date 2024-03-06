# openai-experiment

## Installation Guide

1. **Navigate to the Project Directory**: Use the command line to navigate into the cloned project directory. For example:
    ```
    cd openai-experiment
    ```

2. **Install**: 
    ```
    pip install -e .
    ```

## Usage
After install follow these steps to use it.

1. Set an environment variable for the db name and one for OPENAI
    ```
    export OPENAI_API_KEY=<Paste-The-API-Key-Here>
    export BASE_PROMPT="A simple 128x128 pixel art image of a cartoonish cat with cartoonish head "
    export EXTRA_DESC="The cat in the image appears to be sitting upright with its front paws placed forward and down, almost between its hind paws. The tail is visible to the side, curving slightly towards the front. Its head is facing forward, giving the impression of looking directly at the viewer."
    export DB_NAME=cat_samples_progressive_0305_5
    ```
2. Set environment variables for Leonardo.ai if you are planning to generate images with Leonardo.ai
    ```
    export LEONARDO_API_KEY=<Paste-Leonardo.ai-API-Key-Here>
    ```
3. Generate a sample
    ```
    sdr sample-progressive xibo\'s-6-traits.json -d $DB_NAME -p "$BASE_PROMPT" -e "$EXTRA_DESC" -R "$NO_REORG"
    ```
4. Generate images
    ```
    # For Dalle
    sdr generate -d $DB_NAME
    # For Leonardo.ai
    sdr leonardo -d $DB_NAME "$SOURCE_IMAGE_FILE_PATH"
    ```
5. Generate html
    ```
    sdr html -d $DB_NAME
    ```
