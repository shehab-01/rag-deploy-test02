import requests
import time
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
openai = OpenAI(api_key=api_key)


def send_request(prompt, system_instruction):
    print("sending to api helper...")
    url = "http://localhost:8080/predict"
    data = {
        "model_name": "llama",  # or "mixtral"
        "messages": [{"role": "system", "content": system_instruction}, {"role": "user", "content": prompt}],
        "max_new_tokens": 500,
    }
    start_time = time.time()
    response = requests.post(url, json=data)

    total_time = time.time() - start_time
    # print(response.json())
    # print(total_time)
    return response.json()


def send_open_api(system_instruction, prompt):
    print("OPEN API..")
    response = openai.chat.completions.create(
        model=MODEL, messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def send_open_api_stream(system_instruction, prompt):
    print("OPEN API streaming...")
    stream = openai.chat.completions.create(
        model=MODEL, max_tokens=500, messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": prompt}], stream=True
    )
    return stream
