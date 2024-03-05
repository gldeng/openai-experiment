def run_reorg(prompt):
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
      model="gpt-4-turbo-preview",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "Reorganize the sentences: " + prompt},
          ],
        }
      ],
      max_tokens=500,
    )
    res = response.dict()
    return res['choices'][0]['message']['content']
