from openai import OpenAI
from dotenv import load_dotenv
import os

# 환경 변수 강제로 다시 로드
os.environ.clear()
load_dotenv()

# API 키 확인
api_key = os.getenv("OPENAI_API_KEY")
print(f"API 키 길이: {len(api_key) if api_key else 0}")
print(f"API 키 시작: {api_key[:20] if api_key else 'None'}...")

try:
    client = OpenAI(api_key=api_key)
    
    # 간단한 테스트 요청
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello! Please respond with 'API key is working' if you can see this message."}
        ],
        max_tokens=50
    )
    
    print("✅ API 키가 유효합니다!")
    print(f"응답: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ API 키 오류: {e}")
