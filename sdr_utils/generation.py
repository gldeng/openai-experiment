

from .constants import DALLE_RESULT_FIELD_NAME, DREAM_SHAPER_MODEL_ID, LEONARDO_RESULT_FIELD_NAME
from .resizer import reduce_size


def download_image(image_url):
    import requests
    return requests.get(image_url).content

def convert_to_webp(image_bin):
    from io import BytesIO
    from PIL import Image
    with Image.open(BytesIO(image_bin)) as image:
        with BytesIO() as img_bytes:
            # Save the image to the BytesIO object, specifying the format if necessary
            image.save(img_bytes, format='WEBP')  # You can change 'PNG' to your desired format
            return img_bytes.getvalue()

def run_dalle(prompt):
    from openai import OpenAI
    client = OpenAI()
    response = client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      size="1024x1024",
      quality="standard",
      n=1,
    )

    return response.dict()

def run_one_sample(coll, sample_item):
    import base64
    doc = coll.find_one({'prompt': sample_item['prompt']}, {'_id': 0})
    if DALLE_RESULT_FIELD_NAME in doc:
        print("Existing: " + doc['prompt'])
        return
    dalle_result = run_dalle(sample_item['prompt'])
    url = dalle_result['data'][0]['url']
    print(url)
    image_bin = download_image(url)
    image_256 = reduce_size(image_bin, 4)
    result = {
        DALLE_RESULT_FIELD_NAME: dalle_result,
        'image': base64.b64encode(image_bin).decode('utf8'),
        'image256': base64.b64encode(image_256).decode('utf8'),
    }
    coll.update_one({'prompt': doc['prompt']}, {'$set': result})
    return result

def run_leonardo(prompt, image_file_path, api_key):
    import requests
    import json
    import time

    authorization = "Bearer %s" % api_key

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": authorization
    }

    # Get a presigned URL for uploading an image
    init_url = "https://cloud.leonardo.ai/api/rest/v1/init-image"

    payload = {"extension": "jpg"}
    response = requests.post(init_url, json=payload, headers=headers)
    print(f"initialization of URL for uploading is: {response.status_code}")

    # Upload image via presigned URL
    fields = json.loads(response.json()['uploadInitImage']['fields'])
    upload_url = response.json()['uploadInitImage']['url']

    # image_id is used for referencing to the image in the next step
    image_id = response.json()['uploadInitImage']['id']
    files = {'file': open(image_file_path, 'rb')}

    response = requests.post(upload_url, data=fields, files=files)
    print(f"initialization of source image: {response.status_code}")

    # Generate with an image prompt
    payload = {
        "height": 512,
        "modelId": DREAM_SHAPER_MODEL_ID, # Dream Shaper
        "prompt": prompt,
        "width": 512,
        "init_image_id": image_id, # Accepts an array of image IDs
        "seed": 163432960,
        "num_images": 1,
        "init_strength": 0.15,
        "guidance_scale": 7,
        "public": True,
        "promptMagic": False,
        "photoReal": False,
        "alchemy": False,
        "presetStyle": "LEONARDO",
        "negative_prompt": None
    }
    generation_url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    response = requests.post(generation_url, json=payload, headers=headers)
    print(f"image generation: {response.status_code}")

    # Wait for the generation to finish
    time.sleep(15)

    # Get the generation of images
    generation_id = response.json()['sdGenerationJob']['generationId']
    get_image_url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id
    response = requests.get(get_image_url, headers=headers)
    return response


def run_leonardo_next(prompt, base_image_id, api_key):
    import json
    import requests
    import time

    authorization = "Bearer %s" % api_key

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": authorization
    }

    # Generate with an image prompt
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"

    payload = {
        "height": 512,
        "modelId": DREAM_SHAPER_MODEL_ID,
        "prompt": prompt,
        "width": 512,
        "init_generation_image_id": base_image_id,
        "init_strength": 0.15,
        "seed": 163432960,
        "num_images": 1,
        "guidance_scale": 7,
        "public": True,
        "promptMagic": False,
        "photoReal": False,
        "alchemy": False,
        "presetStyle": "LEONARDO",
        "negative_prompt": None
    }
    response = requests.post(url, json=payload, headers=headers)

    print(f"image generation: {response.status_code}")

    # Wait for the generation to finish
    time.sleep(15)

    # Get the generation of images
    generation_id = response.json()['sdGenerationJob']['generationId']
    get_image_url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id
    response = requests.get(get_image_url, headers=headers)
    return response


def run_one_leonardo_sample(parent_doc, doc, sample_item, image_file_path, api_key):
    import base64
    if LEONARDO_RESULT_FIELD_NAME in doc:
        print("Existing: " + doc['prompt'])
        return {}
    leonardo_result = {}
    if parent_doc is None:
        prompt = 'Add a ' + doc['trait_args'][0]['value']
        # prompt = doc['prompt']
        leonardo_result = run_leonardo(prompt, image_file_path, api_key)
    else:
        image_id = parent_doc[LEONARDO_RESULT_FIELD_NAME]['generations_by_pk']['generated_images'][0]['id']
        parent_traits = set(x['name'] for x in parent_doc['trait_args'])
        prompt = 'Add a ' + ' and '.join([x['value'] for x in doc['trait_args'] if x['name'] not in parent_traits])
        leonardo_result = run_leonardo_next(sample_item['prompt'], image_id, api_key)
    url = leonardo_result.json()['generations_by_pk']['generated_images'][0]['url']
    print(url)
    image_bin = download_image(url)
    image_256 = reduce_size(image_bin, 4)
    result = {
        LEONARDO_RESULT_FIELD_NAME: leonardo_result.json(),
        'image': base64.b64encode(image_bin).decode('utf8'),
        'image256': base64.b64encode(image_256).decode('utf8'),
    }
    return result
