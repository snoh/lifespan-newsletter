# Summary Specification

These guidelines define the quality standards the AI must follow when summarizing news articles, columns, or similar texts.  
They allow non-experts to verify that the output meets expectations.

- **Output format**: The final summary must be **a single paragraph consisting of exactly three sentences**.  
  Write it as one continuous paragraph with no line breaks.
- **Core content**: Include **exactly five keywords** that capture the article’s most important claims or facts.  
  These keywords are taken directly from the result of the `extract_keywords()` function.
- **Analytical note**: Append the article’s overall tone—**positive, neutral, or negative**—in parentheses at the end  
  of the summary, e.g., `(Tone: Neutral)`.
- **Audience**: The target readers are general audiences with no deep expertise in IT or psychology.  
  Minimize technical jargon and use easy-to-understand language.

If the AI satisfies the above criteria, its summaries can be easily checked and improved in future iterations.
