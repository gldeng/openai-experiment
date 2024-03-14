# openai-experiment

## Installation Guide

1. Install MongoDB and Anaconda

   a. Follow [this page](https://www.mongodb.com/docs/manual/installation/) to install MongoDB and [MongoDB Compass](https://www.mongodb.com/try/download/compass) (Optional if you want to check the data).

   b. Follow [this page](https://docs.anaconda.com/free/anaconda/install/index.html) to install Anaconda so that you have a proper Python environment.

1. Clone this repo
   ```
   git clone https://github.com/gldeng/openai-experiment.git
   ```

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
    export BASE_PROMPT="I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: A medium resolution pixel art image of a cat standing like a human with both feet visible on the ground, facing directly at the viewer,"
    export DB_NAME=cat_samples_0313_0004
    export SAMPLE_SIZE=100
    export TRAIT_DIR=traits
    ```
    **Notes: Please modify the API key and DB_NAME**
2. Generate a set of samples
    ```
    sdr sample $TRAIT_DIR -d $DB_NAME -p "$BASE_PROMPT" -n $SAMPLE_SIZE -r true
    ```
    **Notes: Remove `-r true` option if reorg of prompt is not required. Reorg means using GPT-4 to reorganize our prompt sentences.**
4. Generate images
    ```
    sdr generate -d $DB_NAME
    ```
5. Generate html
    ```
    sdr html -d $DB_NAME
    ```

If scripts are changed, you need to uninstall the package first and reinstall it.
```
pip uninstall sdr-utils
pip install -e .
```