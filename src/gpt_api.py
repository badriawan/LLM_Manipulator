from openai import OpenAI
import os
import ast
import static_text

skripsi_key = os.environ.get('SKRIPSI_KEY')

client = OpenAI(api_key=skripsi_key)

def gpt_request(messages):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.5,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response

def speechtotext(path):
    audio_file = open(path, "rb")
    translation = client.audio.translations.create(
        model="whisper-1",
        file=audio_file
    )
    return translation.text

def first_handle(input_text):
    messages = [
        {
            "role": "system",
            "content": static_text.fh  # Assuming static_text.fh is a string
        },
        {
            "role": "user",
            "content": input_text
        }
    ]

    response_0 = gpt_request(messages).choices[0].message.content
    response = ast.literal_eval(response_0)
    return response

def target_function(input_text, action_detail):
    messages = [
        {
            "role": "system",
            "content": static_text.ts  # Assuming static_text.ts is a string
        },
        {
            "role": "user",
            "content": f"Text:{action_detail}, Information: {input_text}"
        }
    ]
    response_0 = gpt_request(messages).choices[0].message.content
    response = ast.literal_eval(response_0)
    return response

def trajectory_function(input_text):
    messages = [
        {
            "role": "system",
            "content": static_text.tg  # Assuming static_text.tg is a string
        },
        {
            "role": "user",
            "content": input_text
        }
    ]
    response_0 = gpt_request(messages).choices[0].message.content
    response = ast.literal_eval(response_0)
    response = [(x, -y) for x, y in response]
    return response
