"""
뉴스레터 요약 시스템 - 메인 실행 파일
"""

import sys
import logging
from typing import List, Dict
from dotenv import load_dotenv

from config import OPENAI_API_KEY, DEFAULT_ARTICLE_LIMIT
from rss_reader import RSSReader
from summarizer import ArticleSummarizer
from content_extractor import ContentExtractor
from html_exporter import HTMLExporter

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsletterSummarySystem:
    """뉴스레터 요약 시스템 메인 클래스"""
    
    def __init__(self):
        """시스템 초기화"""
        self.api_key = OPENAI_API_KEY
        if not self.api_key:
            raise ValueError(
                "OpenAI API 키가 설정되지 않았습니다.\n"
                ".env 파일에 OPENAI_API_KEY=your-api-key-here를 추가하세요."
            )
        
        self.rss_reader = RSSReader()
        self.summarizer = ArticleSummarizer(self.api_key)
        self.content_extractor = ContentExtractor()
        self.html_exporter = HTMLExporter()
        
        logger.info("뉴스레터 요약 시스템 초기화 완료")
    
    def run(self, limit: int = DEFAULT_ARTICLE_LIMIT) -> List[Dict]:
        """메인 실행 함수"""
        try:
            logger.info(f"뉴스레터 요약 시작 (기사 수: {limit})")
            
            # 1단계: RSS 피드에서 기사 수집
            articles = self.rss_reader.fetch_all_feeds(limit)
            
            if not articles:
                logger.warning("수집된 기사가 없습니다")
                return []
            
            # 2단계: 각 기사 요약
            summaries = []
            for idx, article in enumerate(articles, 1):
                try:
                    logger.info(f"\n[{idx}/{len(articles)}] 기사 처리: {article['title'][:50]}...")
                    
                    # 기사 내용 준비
                    content = article.get('content') or article.get('summary') or article.get('title', '')
                    
                    # 요약 생성
                    summary_result = self.summarizer.summarize_article(
                        title=article['title'],
                        content=content,
                        source=article['source']
                    )
                    
                    # 이미지와 참고문헌 추출
                    article_url = article.get('link', '')
                    if article_url:
                        logger.info(f"콘텐츠 메타데이터 추출 시작: {article_url}")
                        metadata = self.content_extractor.extract_content_metadata(article_url)
                        
                        # 추가 정보 추가
                        summary_result.update({
                            'link': article_url,
                            'published': article.get('published', ''),
                            'category': article.get('category', ''),
                            'images': metadata.get('images', []),
                            'references': metadata.get('references', []),
                            'author': metadata.get('author', ''),
                            'description': metadata.get('description', '')
                        })
                    else:
                        # URL이 없는 경우 기본 정보만 추가
                        summary_result.update({
                            'link': '',
                            'published': article.get('published', ''),
                            'category': article.get('category', ''),
                            'images': [],
                            'references': [],
                            'author': '',
                            'description': ''
                        })
                    
                    summaries.append(summary_result)
                    
                    # 결과 출력
                    self._print_summary(idx, summary_result)
                    
                except Exception as e:
                    logger.error(f"기사 요약 실패: {article.get('title', 'Unknown')} - {e}")
                    continue
            
            logger.info(f"뉴스레터 요약 완료: {len(summaries)}개 기사 처리됨")
            
            # HTML 파일로 내보내기
            if summaries:
                try:
                    html_filepath = self.html_exporter.export_summaries_to_html(summaries)
                    logger.info(f"HTML 파일 생성 완료: {html_filepath}")
                    print(f"\n🌐 HTML 파일이 생성되었습니다: {html_filepath}")
                    print("   브라우저에서 열어서 이미지와 함께 확인하세요!")
                except Exception as e:
                    logger.error(f"HTML 파일 생성 실패: {e}")
            
            return summaries
            
        except Exception as e:
            logger.error(f"시스템 실행 실패: {e}")
            raise
    
    def _print_summary(self, idx: int, summary: Dict):
        """요약 결과 출력"""
        print(f"\n{'='*60}")
        print(f"[{idx}] {summary['title']}")
        print(f"{'='*60}")
        print(f"📰 출처: {summary['source']}")
        print(f"🔗 링크: {summary['link']}")
        print(f"📅 발행일: {summary.get('published', 'N/A')}")
        if summary.get('author'):
            print(f"✍️  저자: {summary['author']}")
        print(f"🏷️  키워드: {', '.join(summary['keywords'])}")
        
        # 이미지 정보 출력
        images = summary.get('images', [])
        if images:
            print(f"\n🖼️  이미지 ({len(images)}개):")
            for i, img in enumerate(images[:3], 1):  # 최대 3개만 표시
                print(f"  {i}. {img['url']}")
                if img.get('alt'):
                    print(f"     설명: {img['alt']}")
            if len(images) > 3:
                print(f"     ... 외 {len(images) - 3}개 더")
        
        # 참고문헌 정보 출력
        references = summary.get('references', [])
        if references:
            print(f"\n📚 참고문헌 ({len(references)}개):")
            for i, ref in enumerate(references[:3], 1):  # 최대 3개만 표시
                print(f"  {i}. {ref['text']}")
                print(f"     링크: {ref['url']}")
            if len(references) > 3:
                print(f"     ... 외 {len(references) - 3}개 더")
        
        print(f"\n📝 요약:")
        print(f"{summary['summary']}")
        print(f"\n⏰ 처리시간: {summary['timestamp']}")
        print(f"{'='*60}")
    
    def show_feed_info(self):
        """피드 정보 출력"""
        feeds = self.rss_reader.get_feed_info()
        print("\n📡 설정된 RSS 피드:")
        for i, feed in enumerate(feeds, 1):
            print(f"  {i}. {feed['name']} ({feed['category']})")
            print(f"     URL: {feed['url']}")
        print()

def main():
    """메인 실행 함수"""
    try:
        # 명령행 인수 처리
        limit = DEFAULT_ARTICLE_LIMIT
        if len(sys.argv) > 1:
            try:
                limit = int(sys.argv[1])
            except ValueError:
                print("사용법: python main.py [기사수]")
                print("예시: python main.py 5")
                return
        
        # 시스템 실행
        system = NewsletterSummarySystem()
        
        # 피드 정보 출력
        system.show_feed_info()
        
        # 요약 실행
        summaries = system.run(limit)
        
        if summaries:
            print(f"\n✅ 총 {len(summaries)}개 기사 요약 완료!")
        else:
            print("\n❌ 요약할 기사가 없습니다.")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  사용자에 의해 중단되었습니다.")
    except Exception as e:
        logger.error(f"프로그램 실행 실패: {e}")
        print(f"\n❌ 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main() 