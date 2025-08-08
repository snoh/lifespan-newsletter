"""
newsletter_summary.py  (debug build)
------------------------------------
- NPR·ScienceDaily Psychology RSS Auto Collection
- 3-stage Summary Pipeline + Detailed Logs
"""

import os, feedparser, openai, pathlib, re, textwrap
from datetime import datetime as dt
from dotenv import load_dotenv

# ---------- Environment ----------
load_dotenv()  # Load environment variables from .env file

# OpenAI 클라이언트 초기화 (최신 API)
# client는 함수 내에서 필요할 때 생성

FEEDS = [
    "https://feeds.npr.org/1126/rss.xml",                # NPR Mental Health
    "https://www.sciencedaily.com/rss/mind_brain.xml",   # ScienceDaily Mind & Brain
    "https://feeds.npr.org/1007/rss.xml",                # NPR Health
]

# 심리학 관련 키워드
PSYCHOLOGY_KEYWORDS = [
    "psychology", "psychological", "psychologist", "psychotherapy", "therapy",
    "mental health", "mental illness", "depression", "anxiety", "stress",
    "cognitive", "behavioral", "behavior", "cognition", "memory", "learning",
    "emotion", "emotional", "mood", "personality", "intelligence", "iq",
    "mental disorder", "psychiatric", "psychiatry", "psychiatrist",
    "bipolar", "schizophrenia", "ptsd", "ocd", "adhd", "autism",
    "addiction", "substance abuse", "alcohol", "drug", "recovery",
    "brain", "neuroscience", "neural", "neuron", "neurotransmitter",
    "dopamine", "serotonin", "endorphin", "cortisol", "oxytocin",
    "child development", "adolescent", "teen", "youth", "aging",
    "elderly", "senior", "cognitive decline", "dementia", "alzheimer",
    "social psychology", "group behavior", "conformity", "obedience",
    "prejudice", "discrimination", "stereotype", "attitude", "belief",
    "clinical psychology", "diagnosis", "treatment", "intervention",
    "counseling", "counselor", "therapist", "psychoanalysis",
    "study", "research", "experiment", "survey", "clinical trial",
    "meta-analysis", "systematic review", "longitudinal study"
]

# 제외할 키워드
EXCLUDE_KEYWORDS = [
    "politics", "election", "president", "congress", "government",
    "economy", "business", "finance", "stock", "market", "trade",
    "war", "military", "weapon", "conflict", "violence", "crime",
    "sports", "football", "basketball", "baseball", "soccer",
    "entertainment", "movie", "music", "celebrity", "hollywood",
    "technology", "computer", "software", "hardware", "internet"
]

SPEC_TEXT = pathlib.Path("summary_spec.md").read_text(encoding="utf-8")

# ---------- Prompts ----------
KW_PROMPT = textwrap.dedent("""\
SYSTEM: Analyst who extracts only 5 core keywords.

USER:
Extract only the 5 most important keywords from the article below and return them separated by commas.
=== Article ===
{article}
=== End ===
""")

DRAFT_PROMPT = textwrap.dedent("""\
SYSTEM: Journalist who summarizes in a way that readers can easily understand.

USER:
- Use all 5 keywords
- Write a 5-sentence draft summary
Keywords: {keywords}
Article:
{article}
""")

REFINE_PROMPT = textwrap.dedent("""\
SYSTEM: Editorial desk that strictly follows the summary specification.

Summary Specification:
{spec}

USER:
Compress the above draft into 3 sentences in 1 paragraph and maintain 5 keywords.
Mark (Tone: Positive/Neutral/Negative) at the end.
Draft:
{draft}
""")

# ---------- Functions ----------
def is_psychology_related(entry) -> bool:
    """기사가 심리학 관련인지 판단"""
    text = f"{entry.get('title', '')} {entry.get('summary', '')}"
    text = text.lower()
    
    # 제외 키워드가 있으면 제외
    for exclude_word in EXCLUDE_KEYWORDS:
        if exclude_word.lower() in text:
            return False
    
    # 심리학 관련 키워드가 있으면 포함
    for psychology_word in PSYCHOLOGY_KEYWORDS:
        if psychology_word.lower() in text:
            return True
    
    return False

def extract_keywords(text: str) -> list[str]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": KW_PROMPT.format(article=text[:6000])}],
        temperature=0.3,
    )
    kws = [k.strip() for k in re.split(r"[,\n]", resp.choices[0].message.content) if k.strip()]
    return kws[:5]

def draft_summary(kws: list[str], text: str) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": DRAFT_PROMPT.format(keywords=", ".join(kws), article=text[:6000])}],
        temperature=0.4,
    )
    return resp.choices[0].message.content.strip()

def refine_summary(draft: str) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    for _ in range(3):
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": REFINE_PROMPT.format(draft=draft, spec=SPEC_TEXT)}],
            temperature=0.2,
        )
        final = resp.choices[0].message.content.strip()
        if final.count(".") <= 3 and "(Tone:" in final:
            return final
    return final  # Return after maximum retries

def summarize(entry):
    text = entry.get("summary", "") or entry.get("title", "")
    print(f"🔍  [{entry.get('source', 'RSS')}] {entry.title}")
    kws = extract_keywords(text)
    draft = draft_summary(kws, text)
    final = refine_summary(draft)
    return {"title": entry.title, "url": entry.link, "keywords": kws, "summary": final,
    "source": entry.get("source", "RSS"),}

# ---------- Main ----------
def run(limit=3):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY is not set!")
        print("Add the following to your .env file:")
        print("OPENAI_API_KEY=your-api-key-here")
        return
    print("== Starting: ", api_key[:10], "...")
    print("🎯 심리학 관련 뉴스만 필터링합니다...")
    
    items = []
    for url in FEEDS:
        print(f"\n📥  Reading RSS → {url}")
        parsed = feedparser.parse(url)
        print(f"   ↳ Collected {len(parsed.entries)} articles")
        
        # 심리학 관련 기사만 필터링
        psychology_articles = [entry for entry in parsed.entries if is_psychology_related(entry)]
        print(f"   🧠 심리학 관련: {len(psychology_articles)}개")
        
        items += psychology_articles[:3]
    
    items = sorted(items, key=lambda e: e.get("published_parsed", dt.now().timetuple()), reverse=True)[:limit]

    for idx, e in enumerate(items, 1):
        try:
            r = summarize(e)
            print(f"\n=== [{idx}] {r['title']} ===")
            print("Keywords :", ", ".join(r['keywords']))
            print(r['summary'])
        except Exception as ex:
            print(f"⚠️  Failed to summarize {e.title} → {ex}")

if __name__ == "__main__":
    run(3)