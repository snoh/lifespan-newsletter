#!/usr/bin/env python3
"""
템플릿 및 테마 테스트 스크립트
"""

from html_exporter import HTMLExporter
from datetime import datetime

def create_sample_data():
    """샘플 데이터 생성"""
    return [
        {
            'title': 'Why do some people\'s memories stay sharp as they age?',
            'source': 'NPR Health',
            'published': 'Fri, 08 Aug 2025 03:00:00 -0400',
            'link': 'https://www.npr.org/2025/08/08/nx-s1-5494697/aging-memory-alzheimers-dementia',
            'author': 'Regina G. Barber 외',
            'keywords': ['SuperAger', 'Brain', 'Northwestern', 'Memory', 'Aging'],
            'summary': 'Northwestern University 연구진은 80세 이후에도 예외적으로 뛰어난 기억력을 보유한 SuperAgers를 확인했습니다. 이들의 뇌 기능 저하는 평균보다 느리며, 50–60대 수준의 인지 성능을 보이는 사례가 보고되었습니다. 해당 연구(Alzheimer\'s & Dementia 게재)는 고령층 기억 보존 전략 개발에 시사점을 제공합니다. (Tone: Positive)',
            'images': [
                {
                    'url': 'https://prod-eks-static-assets.npr.org/chrome_svg/npr-logo-2025.svg',
                    'alt': 'NPR logo'
                }
            ],
            'references': [
                {
                    'text': 'Northwestern University Research',
                    'url': 'https://example.com/research'
                }
            ],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            'title': 'Johns Hopkins scientists grow a mini human brain that lights up and connects',
            'source': 'ScienceDaily — Mind & Brain',
            'published': 'Mon, 04 Aug 2025 23:58:21 EDT',
            'link': 'https://www.sciencedaily.com/releases/2025/08/250803233113.htm',
            'author': 'Johns Hopkins Team',
            'keywords': ['Organoid', 'Neural activity', 'Early brain dev.'],
            'summary': 'Hopkins 팀은 기본 혈관 구조와 전기적 신호를 보이는 멀티-리전 전뇌 오가노이드를 제시했습니다. 동물 모델의 한계를 보완하며, 자폐·정신분열 스펙트럼 등 초기 발달 연구 및 신약 테스트의 새로운 플랫폼이 될 수 있습니다. (Tone: Positive)',
            'images': [
                {
                    'url': 'https://www.sciencedaily.com/images/1920/multi-region-brain-organoid.webp',
                    'alt': 'Lab-grown brain organoid'
                }
            ],
            'references': [
                {
                    'text': 'JHU Research Paper',
                    'url': 'http://dx.doi.org/10.1002/advs.202503768'
                }
            ],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]

def test_themes():
    """다양한 테마로 HTML 생성 테스트"""
    exporter = HTMLExporter()
    sample_data = create_sample_data()
    
    themes = ['default', 'mint', 'amber']
    
    print("🎨 테마별 HTML 파일 생성 중...")
    
    for theme in themes:
        try:
            # 각 테마별 파일 생성
            filename = f"test_{theme}_theme.html"
            filepath = exporter.export_summaries_to_html(
                sample_data,
                filename=filename,
                theme=theme,
                title=f"🧠 심리학 뉴스레터 — {theme.title()} 테마",
                header_title=f"🧠 심리학 뉴스레터 ({theme.title()})"
            )
            print(f"✅ {theme.title()} 테마: {filepath}")
            
        except Exception as e:
            print(f"❌ {theme.title()} 테마 생성 실패: {e}")
    
    # docs 폴더에도 기본 테마로 생성
    try:
        docs_path = exporter.export_to_docs(
            sample_data,
            theme="default"
        )
        print(f"📄 GitHub Pages 업데이트: {docs_path}")
    except Exception as e:
        print(f"❌ GitHub Pages 업데이트 실패: {e}")

if __name__ == "__main__":
    test_themes()
