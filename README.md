# 뉴스레터 요약 시스템

AI를 활용한 자동 뉴스레터 요약 시스템입니다. RSS 피드에서 기사를 수집하고 OpenAI GPT를 사용하여 3단계 파이프라인으로 요약을 생성합니다.

## 🚀 주요 기능

- **RSS 피드 자동 수집**: NPR, ScienceDaily 등 심리학/정신건강 관련 뉴스
- **3단계 요약 파이프라인**: 키워드 추출 → 초안 요약 → 최종 정제
- **품질 보장**: 정확히 3문장, 5개 키워드, 톤 마킹 포함
- **체계적 로깅**: 상세한 처리 과정 기록
- **모듈화된 구조**: 유지보수와 확장이 용이

## 📋 요구사항

- Python 3.8+
- OpenAI API 키
- 인터넷 연결

## 🛠️ 설치

1. **저장소 클론**
```bash
git clone <repository-url>
cd newsletter_summary
```

2. **가상환경 생성 및 활성화**
```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

3. **의존성 설치**
```bash
pip install -r requirements.txt
```

4. **환경 변수 설정**
`.env` 파일을 생성하고 OpenAI API 키를 추가:
```
OPENAI_API_KEY=your-api-key-here
```

## 🎯 사용법

### 기본 실행
```bash
python main.py
```

### 특정 수의 기사 요약
```bash
python main.py 5
```

### 기존 스크립트 실행
```bash
python newsletter_summary.py
```

## 📁 프로젝트 구조

```
newsletter_summary/
├── main.py              # 메인 실행 파일 (개선된 버전)
├── newsletter_summary.py # 기존 스크립트
├── config.py            # 설정 관리
├── prompts.py           # 프롬프트 템플릿
├── summarizer.py        # 요약 핵심 기능
├── rss_reader.py        # RSS 피드 읽기
├── summary_spec.md      # 요약 명세서
├── requirements.txt     # 의존성 목록
├── README.md           # 프로젝트 설명
└── .env                # 환경 변수 (사용자 생성)
```

## 🔧 설정

### RSS 피드 추가
`config.py`에서 `RSS_FEEDS` 리스트에 새로운 피드를 추가:

```python
RSS_FEEDS = [
    {
        "url": "https://feeds.npr.org/1126/rss.xml",
        "name": "NPR Mental Health",
        "category": "mental_health"
    },
    # 새 피드 추가
    {
        "url": "your-rss-feed-url",
        "name": "Your Feed Name",
        "category": "your_category"
    }
]
```

### OpenAI 모델 변경
`config.py`에서 모델 설정을 수정:

```python
OPENAI_MODELS = {
    "keyword_extraction": "gpt-3.5-turbo",
    "draft_summary": "gpt-4o-mini",
    "refine_summary": "gpt-4o-mini"
}
```

## 📊 요약 품질 기준

요약은 다음 기준을 따라야 합니다:

- **형식**: 정확히 3문장의 단일 단락
- **키워드**: 정확히 5개의 핵심 키워드 포함
- **톤**: 긍정/중립/부정 톤 마킹
- **대상**: IT/심리학 전문지식이 없는 일반 독자
- **언어**: 쉬운 용어 사용, 전문 용어 최소화

## 📝 로그

시스템 실행 시 다음 로그 파일이 생성됩니다:
- `summary.log`: 상세한 처리 과정 기록

## 🐛 문제 해결

### API 키 오류
```
❌ OPENAI_API_KEY is not set!
```
- `.env` 파일에 올바른 API 키가 설정되어 있는지 확인

### 피드 읽기 실패
- 인터넷 연결 상태 확인
- RSS 피드 URL이 유효한지 확인
- `summary.log`에서 상세 오류 확인

### 요약 품질 문제
- `summary_spec.md` 파일이 올바른 위치에 있는지 확인
- OpenAI API 할당량 확인

## 🔄 개선 사항

### 기존 버전 대비 개선점
1. **모듈화**: 기능별로 파일 분리
2. **에러 처리**: 더 견고한 예외 처리
3. **설정 관리**: 하드코딩된 값들을 설정 파일로 분리
4. **로깅**: 체계적인 로깅 시스템
5. **코드 품질**: 타입 힌트, 문서화 개선

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다! 