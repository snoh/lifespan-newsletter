"""
Core summarization functionality
"""

import re
import logging
from typing import List, Dict, Optional
import openai
from datetime import datetime

from config import (
    OPENAI_MODELS, 
    TEMPERATURE_SETTINGS, 
    MAX_TEXT_LENGTH, 
    MAX_RETRIES,
    SPEC_FILE
)
from prompts import KEYWORD_PROMPT, DRAFT_PROMPT, REFINE_PROMPT

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('summary.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ArticleSummarizer:
    """뉴스 기사 요약을 담당하는 클래스"""
    
    def __init__(self, api_key: str):
        """초기화"""
        if not api_key:
            raise ValueError("OpenAI API 키가 필요합니다")
        
        # OpenAI 클라이언트 초기화 (최신 API)
        self.client = openai.OpenAI(api_key=api_key)
        self.spec_text = SPEC_FILE.read_text(encoding="utf-8") if SPEC_FILE.exists() else ""
        logger.info("ArticleSummarizer 초기화 완료")
    
    def extract_keywords(self, text: str) -> List[str]:
        """기사에서 5개의 핵심 키워드를 추출"""
        try:
            logger.info("키워드 추출 시작")
            
            # 텍스트 길이 제한
            truncated_text = text[:MAX_TEXT_LENGTH]
            
            response = self.client.chat.completions.create(
                model=OPENAI_MODELS["keyword_extraction"],
                messages=[{"role": "user", "content": KEYWORD_PROMPT.format(article=truncated_text)}],
                temperature=TEMPERATURE_SETTINGS["keyword_extraction"],
            )
            
            content = response.choices[0].message.content
            keywords = [kw.strip() for kw in re.split(r"[,\n]", content) if kw.strip()]
            
            # 정확히 5개 키워드 반환
            result = keywords[:5]
            if len(result) < 5:
                logger.warning(f"키워드가 5개 미만입니다: {len(result)}개")
            
            logger.info(f"키워드 추출 완료: {result}")
            return result
            
        except Exception as e:
            logger.error(f"키워드 추출 실패: {e}")
            raise
    
    def draft_summary(self, keywords: List[str], text: str) -> str:
        """5문장 초안 요약 생성"""
        try:
            logger.info("초안 요약 생성 시작")
            
            truncated_text = text[:MAX_TEXT_LENGTH]
            
            response = self.client.chat.completions.create(
                model=OPENAI_MODELS["draft_summary"],
                messages=[{
                    "role": "user", 
                    "content": DRAFT_PROMPT.format(
                        keywords=", ".join(keywords), 
                        article=truncated_text
                    )
                }],
                temperature=TEMPERATURE_SETTINGS["draft_summary"],
            )
            
            draft = response.choices[0].message.content.strip()
            logger.info("초안 요약 생성 완료")
            return draft
            
        except Exception as e:
            logger.error(f"초안 요약 생성 실패: {e}")
            raise
    
    def refine_summary(self, draft: str) -> str:
        """3문장 최종 요약으로 정제"""
        try:
            logger.info("요약 정제 시작")
            
            for attempt in range(MAX_RETRIES):
                logger.info(f"정제 시도 {attempt + 1}/{MAX_RETRIES}")
                
                response = self.client.chat.completions.create(
                    model=OPENAI_MODELS["refine_summary"],
                    messages=[{
                        "role": "user", 
                        "content": REFINE_PROMPT.format(draft=draft, spec=self.spec_text)
                    }],
                    temperature=TEMPERATURE_SETTINGS["refine_summary"],
                )
                
                final = response.choices[0].message.content.strip()
                
                # 품질 검증
                if self._validate_summary(final):
                    logger.info("요약 정제 완료")
                    return final
                else:
                    logger.warning(f"시도 {attempt + 1}: 요약 품질 검증 실패")
            
            logger.warning("최대 재시도 횟수 도달, 마지막 결과 반환")
            return final
            
        except Exception as e:
            logger.error(f"요약 정제 실패: {e}")
            raise
    
    def _validate_summary(self, summary: str) -> bool:
        """요약 품질 검증"""
        # 문장 수 확인 (3문장)
        sentence_count = summary.count('.')
        if sentence_count > 3:
            return False
        
        # 톤 마킹 확인
        if "(Tone:" not in summary:
            return False
        
        # 키워드 수 확인 (대략적으로)
        if summary.count(',') < 3:  # 키워드가 적어도 4개 이상 있어야 함
            return False
        
        return True
    
    def summarize_article(self, title: str, content: str, source: str = "RSS") -> Dict:
        """기사 요약 전체 파이프라인"""
        try:
            logger.info(f"기사 요약 시작: {title[:50]}...")
            
            # 1단계: 키워드 추출
            keywords = self.extract_keywords(content)
            
            # 2단계: 초안 요약
            draft = self.draft_summary(keywords, content)
            
            # 3단계: 최종 요약
            final_summary = self.refine_summary(draft)
            
            result = {
                "title": title,
                "keywords": keywords,
                "summary": final_summary,
                "source": source,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"기사 요약 완료: {title[:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"기사 요약 실패: {title[:50]}... - {e}")
            raise 