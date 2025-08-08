"""
HTML 형식으로 요약 결과를 내보내는 모듈
"""

import os
from datetime import datetime
from typing import List, Dict

class HTMLExporter:
    """HTML 형식으로 요약 결과를 내보내는 클래스"""
    
    def __init__(self):
        """초기화"""
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def export_summaries_to_html(self, summaries: List[Dict], filename: str = None) -> str:
        """요약 결과를 HTML 파일로 내보내기"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"newsletter_summary_{timestamp}.html"
        
        filepath = os.path.join(self.output_dir, filename)
        
        html_content = self._generate_html_content(summaries)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def _generate_html_content(self, summaries: List[Dict]) -> str:
        """HTML 콘텐츠 생성"""
        html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>심리학 뉴스레터 요약 - {datetime.now().strftime("%Y년 %m월 %d일")}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .summary-card {{
            margin: 20px;
            padding: 25px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            background: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .summary-title {{
            color: #2c3e50;
            font-size: 1.4em;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        .meta-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
        }}
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .meta-label {{
            font-weight: 600;
            color: #495057;
            min-width: 80px;
        }}
        .keywords {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 15px 0;
        }}
        .keyword {{
            background: #e3f2fd;
            color: #1976d2;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.9em;
            font-weight: 500;
        }}
        .images-section {{
            margin: 20px 0;
        }}
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 10px;
        }}
        .image-item {{
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
            background: white;
        }}
        .image-item img {{
            width: 100%;
            height: 150px;
            object-fit: cover;
        }}
        .image-caption {{
            padding: 10px;
            font-size: 0.9em;
            color: #666;
        }}
        .references-section {{
            margin: 20px 0;
        }}
        .reference-item {{
            margin: 10px 0;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }}
        .reference-link {{
            color: #007bff;
            text-decoration: none;
        }}
        .reference-link:hover {{
            text-decoration: underline;
        }}
        .summary-text {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            border-left: 4px solid #28a745;
            margin: 20px 0;
            font-size: 1.1em;
            line-height: 1.7;
        }}
        .tone-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: 600;
            margin-left: 10px;
        }}
        .tone-positive {{
            background: #d4edda;
            color: #155724;
        }}
        .tone-neutral {{
            background: #d1ecf1;
            color: #0c5460;
        }}
        .tone-negative {{
            background: #f8d7da;
            color: #721c24;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            border-top: 1px solid #eee;
        }}
        @media (max-width: 768px) {{
            .meta-info {{
                grid-template-columns: 1fr;
            }}
            .image-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 심리학 뉴스레터 요약</h1>
            <p>NPR & ScienceDaily 심리학 관련 뉴스 자동 요약</p>
            <p>생성일: {datetime.now().strftime("%Y년 %m월 %d일 %H:%M")}</p>
        </div>
"""
        
        for i, summary in enumerate(summaries, 1):
            html += self._generate_summary_card(summary, i)
        
        html += """
        <div class="footer">
            <p>🤖 AI 기반 자동 요약 시스템 | OpenAI GPT-4 활용</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def _generate_summary_card(self, summary: Dict, index: int) -> str:
        """개별 요약 카드 HTML 생성"""
        # 톤에 따른 CSS 클래스 결정
        summary_text = summary.get('summary', '')
        tone_class = 'tone-neutral'
        if '(Tone: Positive)' in summary_text:
            tone_class = 'tone-positive'
        elif '(Tone: Negative)' in summary_text:
            tone_class = 'tone-negative'
        
        # 톤 텍스트 추출
        tone_text = 'Neutral'
        if '(Tone: Positive)' in summary_text:
            tone_text = 'Positive'
        elif '(Tone: Negative)' in summary_text:
            tone_text = 'Negative'
        
        # 톤 마킹 제거
        clean_summary = summary_text.replace('(Tone: Positive)', '').replace('(Tone: Negative)', '').replace('(Tone: Neutral)', '').strip()
        
        html = f"""
        <div class="summary-card">
            <h2 class="summary-title">{index}. {summary.get('title', '제목 없음')}</h2>
            
            <div class="meta-info">
                <div class="meta-item">
                    <span class="meta-label">📰 출처:</span>
                    <span>{summary.get('source', 'N/A')}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">📅 발행일:</span>
                    <span>{summary.get('published', 'N/A')}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">🔗 링크:</span>
                    <a href="{summary.get('link', '#')}" target="_blank" class="reference-link">원문 보기</a>
                </div>
                {f'<div class="meta-item"><span class="meta-label">✍️ 저자:</span><span>{summary.get("author", "N/A")}</span></div>' if summary.get('author') else ''}
            </div>
            
            <div class="keywords">
                {''.join([f'<span class="keyword">{kw}</span>' for kw in summary.get('keywords', [])])}
            </div>
        """
        
        # 이미지 섹션
        images = summary.get('images', [])
        if images:
            html += f"""
            <div class="images-section">
                <h3>🖼️ 관련 이미지 ({len(images)}개)</h3>
                <div class="image-grid">
            """
            for img in images[:6]:  # 최대 6개만 표시
                html += f"""
                    <div class="image-item">
                        <img src="{img['url']}" alt="{img.get('alt', '이미지')}" onerror="this.style.display='none'">
                        <div class="image-caption">{img.get('alt', '이미지 설명 없음')}</div>
                    </div>
                """
            html += """
                </div>
            </div>
            """
        
        # 참고문헌 섹션
        references = summary.get('references', [])
        if references:
            html += f"""
            <div class="references-section">
                <h3>📚 참고문헌 ({len(references)}개)</h3>
            """
            for ref in references[:5]:  # 최대 5개만 표시
                html += f"""
                <div class="reference-item">
                    <div><strong>{ref.get('text', '참고문헌')}</strong></div>
                    <a href="{ref['url']}" target="_blank" class="reference-link">{ref['url']}</a>
                </div>
                """
            html += """
            </div>
            """
        
        # 요약 텍스트
        html += f"""
            <div class="summary-text">
                {clean_summary}
                <span class="tone-badge {tone_class}">{tone_text}</span>
            </div>
        </div>
        """
        
        return html 