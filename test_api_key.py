import os
import openai
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")
print(f"API 키 길이: {len(api_key) if api_key else 0}")
print(f"API 키 시작: {api_key[:20] if api_key else 'None'}...")
print(f"API 키 끝: ...{api_key[-10:] if api_key else 'None'}")

# OpenAI 클라이언트 설정
client = openai.OpenAI(api_key=api_key)

try:
    # 간단한 테스트 요청
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello, this is a test message."}
        ],
        max_tokens=10
    )
    print("✅ API 키가 유효합니다!")
    print(f"응답: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ API 키 오류: {e}")
    print(f"오류 타입: {type(e).__name__}")
    
    # 더 자세한 오류 정보 출력
    if hasattr(e, 'response') and e.response:
        print(f"응답 상태 코드: {e.response.status_code}")
        print(f"응답 내용: {e.response.text}")
