from openai import OpenAI
from dotenv import load_dotenv
import os

# 환경 변수 불러오기
load_dotenv()

from config import OPENAI_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY
)

# GPT 요청
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print("🧠 요약 결과:", response.choices[0].message.content)

