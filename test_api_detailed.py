from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

# 환경 변수 불러오기
load_dotenv()

# API 키 확인 (config에서 가져오기)
from config import OPENAI_API_KEY
api_key = OPENAI_API_KEY

print("=== API 키 상세 분석 ===")
print(f"API 키 길이: {len(api_key) if api_key else 0}")
print(f"API 키 시작: {api_key[:20] if api_key else 'None'}...")
print(f"API 키 끝: ...{api_key[-20:] if api_key else 'None'}")

# API 키 형식 확인
if api_key:
    print(f"\n=== API 키 형식 확인 ===")
    print(f"sk-로 시작: {api_key.startswith('sk-')}")
    print(f"sk-proj-로 시작: {api_key.startswith('sk-proj-')}")
    print(f"올바른 길이 (164자): {len(api_key) == 164}")
    
    # 특수문자 확인
    special_chars = [char for char in api_key if not char.isalnum() and char not in '-_']
    if special_chars:
        print(f"특수문자 발견: {special_chars}")
    else:
        print("특수문자 없음 (정상)")

# 직접 HTTP 요청으로 테스트
print(f"\n=== 직접 HTTP 요청 테스트 ===")
try:
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'user', 'content': 'Hello!'}
        ],
        'max_tokens': 50
    }
    
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=data,
        timeout=10
    )
    
    print(f"HTTP 상태 코드: {response.status_code}")
    print(f"응답 헤더: {dict(response.headers)}")
    
    if response.status_code == 200:
        print("✅ HTTP 요청 성공!")
        result = response.json()
        print(f"응답: {result['choices'][0]['message']['content']}")
    else:
        print(f"❌ HTTP 요청 실패: {response.status_code}")
        print(f"오류 내용: {response.text}")
        
except Exception as e:
    print(f"❌ HTTP 요청 오류: {e}")

# OpenAI 클라이언트로 다시 테스트
print(f"\n=== OpenAI 클라이언트 테스트 ===")
try:
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello!"}
        ],
        max_tokens=50
    )
    
    print("✅ OpenAI 클라이언트 성공!")
    print(f"응답: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ OpenAI 클라이언트 오류: {e}")
