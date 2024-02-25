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

    image_url = response.data[0].url
    return image_url, response.data[0].revised_prompt


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
    return response.choices[0].message.content, response.id


def craft_prompt(desc, variation):
    client = OpenAI()
    content = [
        'I have an image described as follows.',
        f'"{desc}"',
        'I want to create a variation of the pixel art image of 128x128 pixel grid.',
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
    return prompt, response_prompt.id


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
    description, vision_session_id = run_vision(base64_image)
    prompt, craft_prompt_session_id = craft_prompt(description, variation)
    url, dalle_revised_prompt = run_dalle(prompt)
    image_bin = download_image(url)
    return {
        'description': description,
        'visionSessionId': vision_session_id,
        'newPrompt': prompt,
        'craftPromptSessionId': craft_prompt_session_id,
        'dalleRevisedPrompt': dalle_revised_prompt,
        'url': url,
        'image': base64.b64encode(image_bin).decode('utf8')
    }
