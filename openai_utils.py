import os
import base64
import requests
import ast
from openai import OpenAI

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def run_dalle(prompt):
    client = OpenAI()

    response = client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      size="1024x1024",
      quality="standard",
      n=1,
    )

    return response.dict()


def run_vision(base64_image):
    client = OpenAI()
    response = client.chat.completions.create(
      model="gpt-4-vision-preview",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "Describe the image"},
            {
              "type": "image_url",
              "image_url": {
                  "url": f"data:image/webp;base64,{base64_image}",
                  "detail": "low"
              },
            },
          ],
        }
      ],
      max_tokens=300,
    )
    return response.dict()


def craft_prompt(desc, variation):
    client = OpenAI()
    content = [
        'I have an image described as follows.',
        f'"{desc}"',
        'I want to create a variation of the pixel art image of 64x64 pixel grid.',
        'And try to maintain the original image as much as possible.',
        "Don't change the posture of the character.",
        variation,
        'Please create a prompt for this variation to be used in DALL-E 3?'
    ]
    # print(content)
    
    response_prompt = client.completions.create(
      model='gpt-3.5-turbo-instruct',
      prompt=' '.join(content),
        max_tokens=2000
    )
    prompt = response_prompt.choices[0].text.encode('utf8').decode('unicode_escape').strip()
    return response_prompt.dict()


# def craft_base_prompt():
#     client = OpenAI()
#     content = [
#         'I have an image described as follows.',
#         f'"{desc}"',
#         'I want to create a variation of the pixel art image of 128x128 pixel grid.',
#         'And try to maintain the original image as much as possible.',
#         variation,
#         'Please create a prompt for this variation to be used in DALL-E 3?'
#     ]
    
#     response_prompt = client.completions.create(
#       model='gpt-3.5-turbo-instruct',
#       prompt=' '.join(content),
#         max_tokens=2000
#     )
#     prompt = response_prompt.choices[0].text.encode('utf8').decode('unicode_escape').strip()
#     return prompt, response_prompt.id


def download_image(image_url):
    return requests.get(image_url).content


def create_variation(base64_image, variation):
    import base64
    vision_result = run_vision(base64_image)
    description = vision_result['choices'][0]['message']['content']
    craft_prompt_result= craft_prompt(description, variation)
    prompt = craft_prompt_result['choices'][0]['text'].strip()
    dalle_result = run_dalle(prompt)
    url = dalle_result['data'][0]['url']
    image_bin = download_image(url)
    return {
        'vision': vision_result,
        'craft_prompt': craft_prompt_result,
        'dalle': dalle_result,
        'image': base64.b64encode(image_bin).decode('utf8')
    }


def reduce_size(image_bin, ratio):
    import numpy as np
    from PIL import Image
    from io import BytesIO
    # Load your image
    img = Image.open(BytesIO(image_bin))
    img_array = np.array(img)
    new_size = tuple(map(lambda x: x // ratio, img.size))
    mid = ratio//2 - 1

    # Initialize an empty array for the reduced image
    reduced_img_array = np.empty((new_size[0], new_size[1], 3), dtype=np.uint8)  # Assuming a 3-channel RGB image

    # Loop over every 2x2 block and take the upper-left pixel
    for i in range(0, img.size[0], ratio):
        for j in range(0, img.size[1], ratio):
            reduced_img_array[i//ratio, j//ratio] = img_array[i + mid, j + mid]

    # Convert the reduced array back to an image
    reduced_img = Image.fromarray(reduced_img_array)

    with BytesIO() as img_bytes:
        # Save the image to the BytesIO object, specifying the format if necessary
        reduced_img.save(img_bytes, format='PNG')  # You can change 'PNG' to your desired format
        
        return img_bytes.getvalue()


def enlarge_size(image_bin, ratio):
    import numpy as np
    from PIL import Image
    from io import BytesIO
    # Load your image
    img = Image.open(BytesIO(image_bin))
    img_array = np.array(img)
    new_size = tuple(map(lambda x: x * ratio, img.size))

    enlarged_img_array = np.empty((new_size[0], new_size[1], 3), dtype=np.uint8)  # Assuming a 3-channel RGB image

    for i in range(0, img.size[0]):
        for j in range(0, img.size[1]):
            for k in range(0, ratio):
                for l in range(0, ratio):
                    enlarged_img_array[i*ratio+k, j*ratio+l] = img_array[i, j]

    enlarged_img = Image.fromarray(enlarged_img_array)

    with BytesIO() as img_bytes:
        # Save the image to the BytesIO object, specifying the format if necessary
        enlarged_img.save(img_bytes, format='PNG')  # You can change 'PNG' to your desired format
        
        return img_bytes.getvalue()
