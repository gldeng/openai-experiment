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
    export DB_NAME=cat_samples_progressive_0305_5
    ```
2. Generate a sample
    ```
    sdr sample-progressive xibo\'s-6-traits.json -d $DB_NAME
    ```
3. Generate images
    ```
    sdr generate -d $DB_NAME
    ```
4. Generate html
    ```
    sdr html -d $DB_NAME
    ```
