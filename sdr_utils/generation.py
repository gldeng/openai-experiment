

from .constants import DALLE_RESULT_FIELD_NAME
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
