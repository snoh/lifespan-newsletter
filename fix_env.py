#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

def clear_environment_cache():
    """환경변수 캐시를 클리어합니다."""
    # Python 환경변수 캐시 클리어
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    print("🔄 환경변수 캐시 클리어 완료")

def read_api_key_from_env():
    """환경변수에서 API 키를 읽어옵니다."""
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print(f"📖 .env 파일에서 API 키 읽기 성공")
            print(f"📏 API 키 길이: {len(api_key)}")
            return api_key
        else:
            print("❌ .env 파일에서 API 키를 찾을 수 없습니다.")
            print("💡 .env 파일에 OPENAI_API_KEY=your-api-key-here를 추가하세요.")
            return None
    except Exception as e:
        print(f"❌ .env 파일 읽기 오류: {e}")
        return None

def verify_api_key():
    """API 키가 올바르게 설정되었는지 확인합니다."""
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)  # override=True로 기존 환경변수 덮어쓰기
        
        loaded_key = os.getenv('OPENAI_API_KEY')
        if loaded_key:
            print("✅ API 키가 올바르게 로드되었습니다!")
            print(f"🔑 로드된 키 시작: {loaded_key[:20]}...")
            print(f"🔑 로드된 키 끝: {loaded_key[-20:]}...")
            return True
        else:
            print("❌ API 키 로드 실패")
            return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def test_openai_connection():
    """OpenAI API 연결을 테스트합니다."""
    try:
        import openai
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # 간단한 테스트 요청
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        
        print("✅ OpenAI API 연결 성공!")
        return True
    except Exception as e:
        print(f"❌ OpenAI API 연결 실패: {e}")
        return False

def main():
    """메인 함수"""
    print("🚀 API 키 설정 및 테스트 시작")
    print("=" * 50)
    
    # 1. 환경변수 캐시 클리어
    clear_environment_cache()
    
    # 2. .env 파일에서 API 키 읽기
    api_key = read_api_key_from_env()
    if not api_key:
        print("❌ API 키를 읽을 수 없습니다.")
        print("💡 .env 파일에 OPENAI_API_KEY=your-api-key-here를 추가하세요.")
        return
    
    # 3. API 키 확인
    if verify_api_key():
        # 4. OpenAI 연결 테스트
        if test_openai_connection():
            print("\n🎉 모든 설정이 완료되었습니다!")
            print("이제 main.py를 실행할 수 있습니다.")
        else:
            print("\n⚠️ API 키가 유효하지 않습니다.")
            print("새로운 API 키를 발급받아 주세요.")
    else:
        print("\n❌ API 키 설정에 실패했습니다.")

if __name__ == "__main__":
    main() 