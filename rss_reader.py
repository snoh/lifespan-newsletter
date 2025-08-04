"""
RSS 피드 읽기 및 처리 기능
"""

import feedparser
import logging
import re
from typing import List, Dict
from datetime import datetime
from config import RSS_FEEDS, DEFAULT_ARTICLE_LIMIT, PSYCHOLOGY_KEYWORDS, EXCLUDE_KEYWORDS

logger = logging.getLogger(__name__)

class RSSReader:
    """RSS 피드 읽기 및 처리 클래스"""
    
    def __init__(self):
        """초기화"""
        self.feeds = RSS_FEEDS
        logger.info(f"RSSReader 초기화 완료 - {len(self.feeds)}개 피드 설정")
    
    def fetch_feed(self, feed_config: Dict) -> List[Dict]:
        """단일 RSS 피드에서 기사 가져오기"""
        try:
            url = feed_config["url"]
            name = feed_config["name"]
            category = feed_config["category"]
            
            logger.info(f"피드 읽기 시작: {name} ({url})")
            
            parsed = feedparser.parse(url)
            
            if parsed.bozo:
                logger.warning(f"피드 파싱 경고: {name} - {parsed.bozo_exception}")
            
            articles = []
            for entry in parsed.entries:
                # 기사 정보 추출
                article = {
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", ""),
                    "content": self._extract_content(entry),
                    "published": entry.get("published", ""),
                    "published_parsed": entry.get("published_parsed"),
                    "source": name,
                    "category": category,
                    "url": url
                }
                articles.append(article)
            
            logger.info(f"피드 읽기 완료: {name} - {len(articles)}개 기사")
            return articles
            
        except Exception as e:
            logger.error(f"피드 읽기 실패: {feed_config.get('name', 'Unknown')} - {e}")
            return []
    
    def _extract_content(self, entry) -> str:
        """기사 내용 추출 (여러 필드에서 시도)"""
        # 우선순위: content > summary > title
        if hasattr(entry, 'content') and entry.content:
            # content 필드가 있는 경우
            for content_item in entry.content:
                if content_item.get('type') == 'text/html':
                    return content_item.get('value', '')
        
        # summary 필드 사용
        if hasattr(entry, 'summary') and entry.summary:
            return entry.summary
        
        # title만 있는 경우
        return entry.get('title', '')
    
    def is_psychology_related(self, article: Dict) -> bool:
        """기사가 심리학 관련인지 판단"""
        # 제목과 내용을 합쳐서 검색
        text = f"{article.get('title', '')} {article.get('content', '')} {article.get('summary', '')}"
        text = text.lower()
        
        # 제외 키워드가 있으면 제외
        for exclude_word in EXCLUDE_KEYWORDS:
            if exclude_word.lower() in text:
                logger.debug(f"제외 키워드 '{exclude_word}' 발견: {article.get('title', '')[:50]}...")
                return False
        
        # 심리학 관련 키워드가 있으면 포함
        for psychology_word in PSYCHOLOGY_KEYWORDS:
            if psychology_word.lower() in text:
                logger.debug(f"심리학 키워드 '{psychology_word}' 발견: {article.get('title', '')[:50]}...")
                return True
        
        return False
    
    def filter_psychology_articles(self, articles: List[Dict]) -> List[Dict]:
        """심리학 관련 기사만 필터링"""
        filtered_articles = []
        
        for article in articles:
            if self.is_psychology_related(article):
                filtered_articles.append(article)
                # 유니코드 문자를 안전하게 처리
                title = article.get('title', '')[:60].encode('ascii', 'ignore').decode('ascii')
                logger.info(f"심리학 관련 기사 포함: {title}...")
            else:
                logger.debug(f"일반 기사 제외: {article.get('title', '')[:60]}...")
        
        logger.info(f"심리학 기사 필터링 완료: {len(filtered_articles)}개 (총 {len(articles)}개 중)")
        return filtered_articles
    
    def fetch_all_feeds(self, limit: int = DEFAULT_ARTICLE_LIMIT) -> List[Dict]:
        """모든 RSS 피드에서 기사 가져오기"""
        all_articles = []
        
        for feed_config in self.feeds:
            try:
                articles = self.fetch_feed(feed_config)
                all_articles.extend(articles)
            except Exception as e:
                logger.error(f"피드 처리 실패: {feed_config.get('name', 'Unknown')} - {e}")
                continue
        
        # 심리학 관련 기사만 필터링
        psychology_articles = self.filter_psychology_articles(all_articles)
        
        # 날짜순 정렬 (최신순)
        psychology_articles.sort(
            key=lambda x: x.get('published_parsed') or datetime.now().timetuple(),
            reverse=True
        )
        
        # 제한된 수만 반환
        result = psychology_articles[:limit]
        
        logger.info(f"전체 피드 처리 완료: {len(result)}개 심리학 기사 (총 {len(all_articles)}개 중)")
        return result
    
    def get_feed_info(self) -> List[Dict]:
        """피드 정보 반환"""
        return [
            {
                "name": feed["name"],
                "url": feed["url"],
                "category": feed["category"]
            }
            for feed in self.feeds
        ] 