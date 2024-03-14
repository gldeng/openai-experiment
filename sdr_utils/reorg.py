from .constants import AS_IS_PREFIX, DALLE_RESULT_FIELD_NAME
from openai import OpenAI

def run_reorg(prompt):
    client = OpenAI()
    response = client.chat.completions.create(
      model="gpt-4-turbo-preview",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "Re-write the sentences but don't add more details: " + prompt},
          ],
        }
      ],
      max_tokens=500,
    )
    res = response.dict()
    return res['choices'][0]['message']['content']


def run_vision(base64_image):
    client = OpenAI()
    response = client.chat.completions.create(
      model="gpt-4-vision-preview",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "Does the image contain text?"},
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


def check_text(coll, doc):
    doc = coll.find_one({'prompt': doc['prompt']}, {'_id': 0})
    if 'check_text' in doc:
        print("Existing: " + doc['prompt'])
        return
    result = run_vision(doc['image256'])
    return result['choices'][0]['message']['content'].startswith('Yes')


def reorg_prompt(coll, doc):
    doc = coll.find_one({'prompt': doc['prompt']}, {'_id': 0})
    if 'reorg' in doc:
        print("Existing: " + doc['prompt'])
        return
    check_text = run_vision(doc['image256'])
    reorg_obj = {
        'check_text': check_text,
    }
    has_text = check_text['choices'][0]['message']['content'].startswith('Yes')
    if has_text:
      reorged_prompt = run_reorg(doc[DALLE_RESULT_FIELD_NAME]['data'][0]['revised_prompt'])
      reorg_obj['prompt'] = AS_IS_PREFIX + reorged_prompt
    coll.update_one({'prompt': doc['prompt']}, {'$set': {'reorg': reorg_obj}})
