"""
HTML 형식으로 요약 결과를 내보내는 모듈 (Jinja2 템플릿 엔진 사용)
"""

import os
from datetime import datetime
from typing import List, Dict, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape


class HTMLExporter:
    """HTML 형식으로 요약 결과를 내보내는 클래스"""
    
    def __init__(self, template_dir: str = "docs/templates", output_dir: str = "output"):
        """초기화"""
        self.template_dir = template_dir
        self.output_dir = output_dir
        
        # 출력 디렉토리 생성
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Jinja2 환경 설정
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    def export_summaries_to_html(
        self, 
        summaries: List[Dict], 
        filename: str = None,
        template_name: str = "newsletter.html.j2",
        theme: str = "default",
        **template_vars
    ) -> str:
        """요약 결과를 HTML 파일로 내보내기"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"newsletter_summary_{timestamp}.html"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # 템플릿 데이터 준비
        template_data = self._prepare_template_data(summaries, theme, **template_vars)
        
        # 템플릿 렌더링
        html_content = self._render_template(template_name, template_data)
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def export_to_docs(
        self,
        summaries: List[Dict],
        filename: str = "index.html",
        template_name: str = "newsletter.html.j2",
        theme: str = "default",
        **template_vars
    ) -> str:
        """docs 폴더에 직접 내보내기 (GitHub Pages용)"""
        filepath = os.path.join("docs", filename)
        
        # 템플릿 데이터 준비
        template_data = self._prepare_template_data(summaries, theme, **template_vars)
        
        # 템플릿 렌더링
        html_content = self._render_template(template_name, template_data)
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def export_to_dist(
        self,
        summaries: List[Dict],
        filename: str = "index.html",
        template_name: str = "newsletter.html.j2",
        theme: str = "default",
        formspree_id: str = "",
        **template_vars
    ) -> str:
        """dist 폴더에 직접 내보내기 (GitHub Actions/Pages용)"""
        # dist 폴더 생성
        dist_dir = "dist"
        if not os.path.exists(dist_dir):
            os.makedirs(dist_dir, exist_ok=True)
            
        filepath = os.path.join(dist_dir, filename)
        
        # 템플릿 데이터 준비
        template_data = self._prepare_template_data(
            summaries, 
            theme, 
            formspree_id=formspree_id,
            **template_vars
        )
        
        # 템플릿 렌더링
        html_content = self._render_template(template_name, template_data)
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def _prepare_template_data(self, summaries: List[Dict], theme: str, **kwargs) -> Dict:
        """템플릿에 전달할 데이터 준비"""
        now = datetime.now()
        
        # 기본 템플릿 변수
        template_data = {
            'lang': 'ko',
            'title': '🧠 심리학 뉴스레터 요약 — 프리미엄 템플릿',
            'description': 'NPR & ScienceDaily 심리학 관련 뉴스 자동 요약 — 프리미엄 웹 템플릿',
            'header_title': '🧠 심리학 뉴스레터 요약',
            'header_subtitle': 'NPR & ScienceDaily 심리학 관련 뉴스 자동 요약',
            'generated_at': now.strftime("%Y년 %m월 %d일 %H:%M"),
            'current_year': now.year,
            'version': 'v1.0 • Premium',
            'theme': theme,
            'sources': ['NPR', 'ScienceDaily'],
            'articles': []
        }
        
        # 사용자 정의 변수 병합
        template_data.update(kwargs)
        
        # 요약 데이터를 템플릿 형식으로 변환
        template_data['articles'] = [self._convert_summary_to_article(summary) for summary in summaries]
        
        return template_data
    
    def _convert_summary_to_article(self, summary: Dict) -> Dict:
        """요약 데이터를 템플릿 article 형식으로 변환"""
        # 톤 분석
        summary_text = summary.get('summary', '')
        tone = 'neutral'
        if '(Tone: Positive)' in summary_text:
            tone = 'positive'
        elif '(Tone: Negative)' in summary_text:
            tone = 'negative'
        
        # 톤 마킹 제거
        clean_summary = (summary_text
                        .replace('(Tone: Positive)', '')
                        .replace('(Tone: Negative)', '')
                        .replace('(Tone: Neutral)', '')
                        .strip())
        
        # 요약을 불릿 포인트로 변환
        summary_bullets = self._convert_summary_to_bullets(clean_summary)
        

        
        # 참고문헌 데이터 변환
        references = []
        for ref in summary.get('references', []):
            references.append({
                'title': ref.get('text', '참고문헌'),
                'url': ref.get('url', ''),
                'link_text': '링크'
            })
        
        return {
            'title': summary.get('title', '제목 없음'),
            'subtitle': self._generate_subtitle(summary),
            'source': summary.get('source', ''),
            'published_date': summary.get('published', ''),
            'link': summary.get('link', ''),
            'author': self._clean_author(summary.get('author', '')),
            'keywords': summary.get('keywords', []),

            'references': references,
            'summary': clean_summary,
            'summary_bullets': summary_bullets,
            'tone': tone
        }
    
    def _generate_subtitle(self, summary: Dict) -> Optional[str]:
        """제목을 기반으로 한국어 부제목 생성"""
        title = summary.get('title', '').lower()
        
        # 간단한 키워드 매칭으로 부제목 생성
        if 'memory' in title or 'aging' in title:
            return "노화와 기억력 연구"
        elif 'brain' in title:
            return "뇌과학 연구 동향"
        elif 'gorilla' in title or 'social' in title:
            return "동물 행동학 연구"
        elif 'organoid' in title:
            return "오가노이드 기술 발전"
        else:
            return None
    
    def _clean_author(self, author: str) -> str:
        """저자 정보 정리"""
        if not author or author == 'N/A':
            return ''
        
        # 긴 저자 정보에서 핵심만 추출
        if len(author) > 50:
            # 첫 번째 저자만 추출하고 "외" 추가
            first_author = author.split(',')[0].split('By')[-1].strip()
            if first_author:
                return f"{first_author} 외"
        
        return author
    
    def _convert_summary_to_bullets(self, summary: str) -> List[str]:
        """요약 텍스트를 불릿 포인트로 변환"""
        if not summary:
            return []
        
        # 문장 단위로 분리
        sentences = summary.split('. ')
        bullets = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:  # 너무 짧은 문장 제외
                # 문장 끝의 마침표 제거
                if sentence.endswith('.'):
                    sentence = sentence[:-1]
                bullets.append(sentence)
        
        # 최대 5개까지만 표시
        return bullets[:5]
    
    def _render_template(self, template_name: str, data: Dict) -> str:
        """템플릿 렌더링"""
        try:
            template = self.env.get_template(template_name)
            return template.render(**data)
        except Exception as e:
            raise RuntimeError(f"템플릿 렌더링 실패: {e}")
    
    def get_available_themes(self) -> List[str]:
        """사용 가능한 테마 목록 반환"""
        return ['default', 'mint', 'amber']