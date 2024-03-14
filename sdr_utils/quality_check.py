from openai import OpenAI

prompt = '''Is any of the following statements true about the image? (No repetition of the questions, just give me an array of json true/false values.)
It is overlaid with a grid.
It contains a color scale or palette.
There are many small items surrounding the main character.'''

def detect_bad(base64_image):
    client = OpenAI()

    response = client.chat.completions.create(
      model="gpt-4-vision-preview",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": prompt},
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
