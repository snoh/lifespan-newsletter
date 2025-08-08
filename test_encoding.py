from openai import OpenAI
from dotenv import load_dotenv
import os

# 환경 변수 불러오기
load_dotenv()

# API 키 확인 (config에서 가져오기)
from config import OPENAI_API_KEY
api_key = OPENAI_API_KEY

print("=== API 키 분석 ===")
print(f"API 키 길이: {len(api_key) if api_key else 0}")
print(f"API 키 시작: {api_key[:20] if api_key else 'None'}...")
print(f"API 키 끝: ...{api_key[-20:] if api_key else 'None'}")

# 각 문자 분석
print("\n=== 문자별 분석 ===")
if api_key:
    for i, char in enumerate(api_key):
        if not char.isascii():
            print(f"위치 {i}: '{char}' (ASCII 아님) - 유니코드: {ord(char)}")
        elif not char.isprintable():
            print(f"위치 {i}: '{char}' (출력 불가) - 유니코드: {ord(char)}")

# 인코딩 테스트
print("\n=== 인코딩 테스트 ===")
try:
    # UTF-8로 인코딩/디코딩 테스트
    encoded = api_key.encode('utf-8')
    decoded = encoded.decode('utf-8')
    print(f"UTF-8 인코딩 성공: {api_key == decoded}")
except Exception as e:
    print(f"UTF-8 인코딩 오류: {e}")

try:
    # ASCII로 인코딩/디코딩 테스트
    encoded = api_key.encode('ascii')
    decoded = encoded.decode('ascii')
    print(f"ASCII 인코딩 성공: {api_key == decoded}")
except Exception as e:
    print(f"ASCII 인코딩 오류: {e}")

# API 키 정리 (공백, 줄바꿈 등 제거)
cleaned_key = api_key.strip() if api_key else ""
print(f"\n정리된 키 길이: {len(cleaned_key)}")
print(f"원본 키와 동일: {api_key == cleaned_key}")

# 정리된 키로 테스트
print("\n=== 정리된 키로 테스트 ===")
try:
    client = OpenAI(api_key=cleaned_key)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello! Please respond with 'API key is working' if you can see this message."}
        ],
        max_tokens=50
    )
    
    print("✅ 정리된 API 키가 유효합니다!")
    print(f"응답: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ 정리된 API 키 오류: {e}")
