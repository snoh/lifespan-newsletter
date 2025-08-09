# 🧠 심리학 뉴스레터 자동 생성 시스템

AI를 활용한 자동 뉴스레터 요약 시스템입니다. RSS 피드에서 기사를 수집하고 OpenAI GPT를 사용하여 3단계 파이프라인으로 요약을 생성합니다.

## 🚀 주요 기능

- **RSS 피드 자동 수집**: NPR, ScienceDaily 등 심리학/정신건강 관련 뉴스
- **3단계 요약 파이프라인**: 키워드 추출 → 초안 요약 → 최종 정제
- **프리미엄 웹 템플릿**: Jinja2 기반 반응형 디자인 (3가지 테마)
- **구독 기능**: Formspree 기반 백엔드 없는 이메일 구독
- **자동 배포**: GitHub Actions + Pages 자동 배포
- **구조화된 로깅**: structlog 기반 JSON 로깅
- **코드 품질**: 타입 힌트, 린팅, pre-commit hooks

## 🌐 배포 URL

- **라이브 사이트**: https://snoh.github.io/lifespan-newsletter/
- **자동 업데이트**: 매일 09:00 KST

## 📋 요구사항

- Python 3.9+
- OpenAI API 키
- Formspree 계정 (구독 기능 사용 시)
- 인터넷 연결

## 🛠️ 설치

1. **저장소 클론**
```bash
git clone https://github.com/snoh/lifespan-newsletter.git
cd lifespan-newsletter
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
pip install structlog  # 추가 의존성
```

4. **환경 변수 설정**
`.env` 파일을 생성하고 다음 내용을 추가하세요:

```bash
# 필수: OpenAI API 키
OPENAI_API_KEY=your-openai-api-key-here

# 선택: Formspree 구독 기능
FORMSPREE_ID=your_formspree_form_id
```

## 🔧 사용법

### 수동 빌드 (로컬)
```bash
python main.py
# 결과: dist/index.html
```

### 기사 수 제한
```bash
python main.py 5  # 최대 5개 기사만 처리
```

### 테마별 테스트
```bash
python test_templates.py  # 3가지 테마로 HTML 생성
```

## 🚀 배포 (자동)

- **GitHub Actions + Pages 사용**
- **스케줄**: 매일 09:00 KST 자동 빌드/배포
- **수동 배포**: main 브랜치로 push 또는 Actions의 `workflow_dispatch`

### 배포 설정
1. GitHub 리포지토리 **Settings → Pages → Source: GitHub Actions**로 설정
2. **Settings → Secrets → Actions**에서 환경변수 추가:
   - `OPENAI_API_KEY`: OpenAI API 키
   - `FORMSPREE_ID`: Formspree 폼 ID (선택)

## 📧 구독 설정 (백엔드 없이)

1. [Formspree](https://formspree.io/) 계정 생성
2. 새 폼 생성 후 폼 ID 복사
3. `.env`에 `FORMSPREE_ID` 설정
4. 페이지 우하단 구독 버튼(FAB) 클릭 → 모달에서 이메일 제출

## 📁 프로젝트 구조

```
lifespan-newsletter/
├── main.py                      # 메인 실행 파일
├── config.py                    # 설정 관리 (타입 힌트 포함)
├── html_exporter.py             # Jinja2 기반 HTML 생성
├── logger_config.py             # 구조화된 로깅 설정
├── rss_reader.py                # RSS 피드 수집
├── summarizer.py                # 3단계 요약 파이프라인
├── content_extractor.py         # 콘텐츠 메타데이터 추출
├── test_templates.py            # 테마 테스트 스크립트
├── docs/
│   ├── templates/
│   │   └── newsletter.html.j2   # Jinja2 템플릿
│   └── index.html               # GitHub Pages 출력
├── dist/                        # 빌드 산출물
│   ├── index.html
│   └── assets/
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions 워크플로우
├── requirements.txt             # 운영 의존성
├── requirements-dev.txt         # 개발 의존성
├── pyproject.toml              # 린팅 설정
├── .pre-commit-config.yaml     # pre-commit hooks
└── .env                        # 환경변수 (사용자 생성)
```

## 🎨 테마 시스템

3가지 내장 테마 지원:
- **Default**: 기본 보라색 그라데이션
- **Mint**: 청록색 테마
- **Amber**: 주황색 테마

```python
# 테마별 빌드
exporter.export_to_dist(summaries, theme="mint")
```

## 📊 출력 파일

- `dist/index.html`: 메인 뉴스레터 페이지
- `dist/assets/`: 정적 리소스 (OG 이미지 등)
- `summary.log`: 상세 JSON 로그 파일
- `output/`: 테스트용 HTML 파일들

## 🔍 로깅

구조화된 로깅으로 디버깅과 모니터링 지원:
- 콘솔: 컬러 출력
- 파일: JSON 형식 (`summary.log`)
- 컨텍스트: 기사 ID, 처리 단계, 에러 정보

## 🛠️ 개발

### 코드 품질 도구
```bash
# 개발 의존성 설치
pip install -r requirements-dev.txt

# 린팅 및 포맷팅
ruff check .
black .
mypy .

# pre-commit hooks 설치
pre-commit install
```

### 체크리스트
- [ ] `.env`에 `OPENAI_API_KEY` 및 `FORMSPREE_ID` 입력  
- [ ] `python main.py` 실행 → `dist/index.html` 생성 확인  
- [ ] 리포 **Settings → Pages → Source=GitHub Actions**  
- [ ] `main`에 푸시 → Actions 성공 → 공개 URL 접속  
- [ ] 모달에서 이메일 제출 시 Formspree 대시보드에서 수신 확인

## 📸 스크린샷

![Newsletter Screenshot](docs/screenshot.png)

## 🤝 기여

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🙋‍♂️ 지원

문제가 발생하거나 질문이 있으시면 [Issues](https://github.com/snoh/lifespan-newsletter/issues)를 통해 문의해주세요.