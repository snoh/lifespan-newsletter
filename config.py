"""
Configuration settings for the newsletter summary system
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

# RSS 피드 설정
RSS_FEEDS: List[Dict[str, str]] = [
    {
        "url": "https://feeds.npr.org/1126/rss.xml",
        "name": "NPR Mental Health",
        "category": "mental_health"
    },
    {
        "url": "https://www.sciencedaily.com/rss/mind_brain.xml", 
        "name": "ScienceDaily Mind & Brain",
        "category": "psychology"
    },
    {
        "url": "https://feeds.npr.org/1007/rss.xml",
        "name": "NPR Health",
        "category": "health"
    }
]

# 심리학 관련 키워드 필터링
PSYCHOLOGY_KEYWORDS: List[str] = [
    # 심리학 일반
    "psychology", "psychological", "psychologist", "psychotherapy", "therapy",
    "mental health", "mental illness", "depression", "anxiety", "stress",
    "cognitive", "behavioral", "behavior", "cognition", "memory", "learning",
    "emotion", "emotional", "mood", "personality", "intelligence", "iq",
    
    # 정신건강
    "mental disorder", "psychiatric", "psychiatry", "psychiatrist",
    "bipolar", "schizophrenia", "ptsd", "ocd", "adhd", "autism",
    "addiction", "substance abuse", "alcohol", "drug", "recovery",
    
    # 뇌과학
    "brain", "neuroscience", "neural", "neuron", "neurotransmitter",
    "dopamine", "serotonin", "endorphin", "cortisol", "oxytocin",
    
    # 발달심리학
    "child development", "adolescent", "teen", "youth", "aging",
    "elderly", "senior", "cognitive decline", "dementia", "alzheimer",
    
    # 사회심리학
    "social psychology", "group behavior", "conformity", "obedience",
    "prejudice", "discrimination", "stereotype", "attitude", "belief",
    
    # 임상심리학
    "clinical psychology", "diagnosis", "treatment", "intervention",
    "counseling", "counselor", "therapist", "psychoanalysis",
    
    # 연구 관련
    "study", "research", "experiment", "survey", "clinical trial",
    "meta-analysis", "systematic review", "longitudinal study"
]

# 제외할 키워드 (일반 뉴스 필터링)
EXCLUDE_KEYWORDS: List[str] = [
    "politics", "election", "president", "congress", "government",
    "economy", "business", "finance", "stock", "market", "trade",
    "war", "military", "weapon", "conflict", "violence", "crime",
    "sports", "football", "basketball", "baseball", "soccer",
    "entertainment", "movie", "music", "celebrity", "hollywood",
    "technology", "computer", "software", "hardware", "internet"
]

# OpenAI 설정
OPENAI_MODELS: Dict[str, str] = {
    "keyword_extraction": "gpt-3.5-turbo",
    "draft_summary": "gpt-4o-mini", 
    "refine_summary": "gpt-4o-mini"
}

TEMPERATURE_SETTINGS: Dict[str, float] = {
    "keyword_extraction": 0.3,
    "draft_summary": 0.4,
    "refine_summary": 0.2
}

# 텍스트 처리 설정
MAX_TEXT_LENGTH: int = 6000
MAX_RETRIES: int = 3
DEFAULT_ARTICLE_LIMIT: int = 3

# 파일 경로
SPEC_FILE: Path = Path("summary_spec.md")
LOG_FILE: Path = Path("summary.log")

# 환경 변수
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY") 