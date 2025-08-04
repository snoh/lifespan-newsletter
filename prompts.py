"""
Prompt templates for the newsletter summary system
"""

import textwrap

# 키워드 추출 프롬프트
KEYWORD_PROMPT = textwrap.dedent("""\
SYSTEM: You are an expert analyst who extracts only the 5 most important keywords from articles.

USER:
Extract only the 5 most important keywords from the article below and return them separated by commas.
Focus on keywords that capture the main claims, facts, or concepts.

=== Article ===
{article}
=== End ===

Return only the keywords, separated by commas.
""")

# 초안 요약 프롬프트
DRAFT_PROMPT = textwrap.dedent("""\
SYSTEM: You are a skilled journalist who writes clear, engaging summaries for general audiences.

USER:
Write a 5-sentence draft summary of the article below. 
- Use all 5 provided keywords naturally in the text
- Write in simple, easy-to-understand language
- Avoid technical jargon
- Target readers with no deep expertise in the subject

Keywords: {keywords}

Article:
{article}

Write a coherent 5-sentence summary.
""")

# 요약 정제 프롬프트
REFINE_PROMPT = textwrap.dedent("""\
SYSTEM: You are an editorial desk that strictly follows the summary specification.

Summary Specification:
{spec}

USER:
Compress the draft summary below into exactly 3 sentences in 1 continuous paragraph.
Requirements:
- Maintain all 5 keywords from the original
- Write as one paragraph with no line breaks
- Include exactly 5 keywords that capture the article's most important claims or facts
- Append the article's overall tone (positive, neutral, or negative) in parentheses at the end
- Use easy-to-understand language for general audiences

Draft Summary:
{draft}

Return the refined 3-sentence summary with tone marking.
""") 