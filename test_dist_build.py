#!/usr/bin/env python3
"""
dist/ 빌드 시스템 테스트
"""

from html_exporter import HTMLExporter
from datetime import datetime
import os

def test_dist_build():
    """dist 폴더 빌드 테스트"""
    # 샘플 데이터
    sample_data = [
        {
            'title': 'Test Article with Formspree Modal',
            'source': 'Test Source',
            'published': 'Test Date',
            'link': 'https://example.com',
            'author': 'Test Author',
            'keywords': ['Test', 'Sample', 'Demo'],
            'summary': 'This is a test article to verify the new dist build system with Formspree modal integration. (Tone: Positive)',
            'images': [
                {
                    'url': 'https://via.placeholder.com/400x200/7c89ff/ffffff?text=Test+Image',
                    'alt': 'Test image'
                }
            ],
            'references': [
                {
                    'text': 'Test Reference',
                    'url': 'https://example.com/ref'
                }
            ],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]
    
    # HTMLExporter로 dist 빌드 테스트
    exporter = HTMLExporter()
    
    print("🏗️  dist/ 빌드 시스템 테스트 시작...")
    
    # Formspree ID 환경변수에서 읽기
    formspree_id = os.getenv("FORMSPREE_ID", "")
    print(f"📧 Formspree ID: {formspree_id}")
    
    # dist 폴더에 빌드
    filepath = exporter.export_to_dist(
        sample_data,
        theme="default",
        formspree_id=formspree_id,
        title="🧠 테스트 뉴스레터 — Formspree 모달 포함",
        header_title="🧠 테스트 뉴스레터",
        header_subtitle="Formspree 구독 모달 테스트"
    )
    
    print(f"✅ dist 빌드 완료: {filepath}")
    
    # 다른 테마들도 테스트
    themes = ['mint', 'amber']
    for theme in themes:
        theme_filepath = exporter.export_to_dist(
            sample_data,
            filename=f"test_{theme}.html",
            theme=theme,
            formspree_id=formspree_id
        )
        print(f"✅ {theme.title()} 테마: {theme_filepath}")
    
    print("\n🎉 모든 테스트 완료!")
    print("📁 생성된 파일들:")
    print("   - dist/index.html (기본 테마 + Formspree 모달)")
    print("   - dist/test_mint.html (Mint 테마)")
    print("   - dist/test_amber.html (Amber 테마)")
    print("   - dist/assets/og-default.png (OG 이미지)")

if __name__ == "__main__":
    test_dist_build()
