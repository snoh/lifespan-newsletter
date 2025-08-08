"""
웹 콘텐츠에서 이미지와 참고문헌 링크를 추출하는 모듈
"""

import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional
import re

logger = logging.getLogger(__name__)

class ContentExtractor:
    """웹 콘텐츠에서 이미지와 참고문헌을 추출하는 클래스"""
    
    def __init__(self):
        """초기화"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_images_from_url(self, url: str) -> List[Dict]:
        """URL에서 이미지를 추출"""
        try:
            logger.info(f"이미지 추출 시작: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            images = []
            
            # 이미지 태그 찾기
            img_tags = soup.find_all('img')
            
            for img in img_tags:
                src = img.get('src') or img.get('data-src')
                if src:
                    # 상대 URL을 절대 URL로 변환
                    absolute_url = urljoin(url, src)
                    
                    # 이미지 정보 수집
                    image_info = {
                        'url': absolute_url,
                        'alt': img.get('alt', ''),
                        'title': img.get('title', ''),
                        'width': img.get('width'),
                        'height': img.get('height')
                    }
                    
                    # 유효한 이미지 URL인지 확인
                    if self._is_valid_image_url(absolute_url):
                        images.append(image_info)
                        logger.debug(f"이미지 발견: {absolute_url}")
            
            logger.info(f"이미지 추출 완료: {len(images)}개")
            return images
            
        except Exception as e:
            logger.error(f"이미지 추출 실패: {url} - {e}")
            return []
    
    def extract_references_from_url(self, url: str) -> List[Dict]:
        """URL에서 참고문헌 링크를 추출"""
        try:
            logger.info(f"참고문헌 추출 시작: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            references = []
            
            # 참고문헌 관련 키워드
            reference_keywords = [
                'reference', 'bibliography', 'citation', 'source', 'study',
                'research', 'paper', 'article', 'publication', 'journal'
            ]
            
            # 링크 태그 찾기
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link.get('href')
                text = link.get_text(strip=True).lower()
                
                # 참고문헌 관련 링크인지 확인
                if self._is_reference_link(href, text, reference_keywords):
                    absolute_url = urljoin(url, href)
                    
                    reference_info = {
                        'url': absolute_url,
                        'text': link.get_text(strip=True),
                        'title': link.get('title', '')
                    }
                    
                    references.append(reference_info)
                    logger.debug(f"참고문헌 발견: {absolute_url}")
            
            logger.info(f"참고문헌 추출 완료: {len(references)}개")
            return references
            
        except Exception as e:
            logger.error(f"참고문헌 추출 실패: {url} - {e}")
            return []
    
    def _is_valid_image_url(self, url: str) -> bool:
        """유효한 이미지 URL인지 확인"""
        if not url:
            return False
        
        # 이미지 파일 확장자 확인
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
        parsed_url = urlparse(url)
        
        # 확장자 확인
        path = parsed_url.path.lower()
        if any(path.endswith(ext) for ext in image_extensions):
            return True
        
        # URL에 이미지 관련 키워드가 있는지 확인
        image_keywords = ['image', 'img', 'photo', 'picture', 'graphic']
        if any(keyword in url.lower() for keyword in image_keywords):
            return True
        
        return False
    
    def _is_reference_link(self, href: str, text: str, keywords: List[str]) -> bool:
        """참고문헌 링크인지 확인"""
        if not href:
            return False
        
        # URL에 참고문헌 키워드가 있는지 확인
        href_lower = href.lower()
        if any(keyword in href_lower for keyword in keywords):
            return True
        
        # 링크 텍스트에 참고문헌 키워드가 있는지 확인
        if any(keyword in text for keyword in keywords):
            return True
        
        # 학술 관련 도메인 확인
        academic_domains = [
            'doi.org', 'pubmed.ncbi.nlm.nih.gov', 'scholar.google.com',
            'researchgate.net', 'academia.edu', 'arxiv.org', 'biorxiv.org',
            'nature.com', 'science.org', 'cell.com', 'thelancet.com'
        ]
        
        parsed_url = urlparse(href)
        if any(domain in parsed_url.netloc.lower() for domain in academic_domains):
            return True
        
        return False
    
    def extract_content_metadata(self, url: str) -> Dict:
        """URL에서 콘텐츠 메타데이터 추출"""
        try:
            logger.info(f"메타데이터 추출 시작: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            metadata = {
                'title': '',
                'description': '',
                'author': '',
                'published_date': '',
                'images': [],
                'references': []
            }
            
            # 제목 추출
            title_tag = soup.find('title')
            if title_tag:
                metadata['title'] = title_tag.get_text(strip=True)
            
            # 메타 태그에서 설명 추출
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                metadata['description'] = meta_desc.get('content', '')
            
            # 저자 정보 추출
            author_selectors = [
                'meta[name="author"]',
                'meta[property="article:author"]',
                '.author',
                '[class*="author"]',
                '[class*="byline"]'
            ]
            
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem:
                    metadata['author'] = author_elem.get_text(strip=True)
                    break
            
            # 발행일 추출
            date_selectors = [
                'meta[property="article:published_time"]',
                'meta[name="date"]',
                'time',
                '[class*="date"]',
                '[class*="published"]'
            ]
            
            for selector in date_selectors:
                date_elem = soup.select_one(selector)
                if date_elem:
                    metadata['published_date'] = date_elem.get_text(strip=True)
                    break
            
            # 이미지와 참고문헌 추출
            metadata['images'] = self.extract_images_from_url(url)
            metadata['references'] = self.extract_references_from_url(url)
            
            logger.info(f"메타데이터 추출 완료: {url}")
            return metadata
            
        except Exception as e:
            logger.error(f"메타데이터 추출 실패: {url} - {e}")
            return {
                'title': '',
                'description': '',
                'author': '',
                'published_date': '',
                'images': [],
                'references': []
            } 