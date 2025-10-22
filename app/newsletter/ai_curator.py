import json
from typing import List

from dotenv import load_dotenv
from groq import Groq
import os

from app.sample.sample_utils import style_examples_loader

load_dotenv()


# def curate_newsletter(articles: list, user_topics: list):
#     """Use Groq LLM to curate and summarize articles"""
#
#     client = Groq(api_key=os.getenv("GROQ_API_KEY"))
#
#     # Combine articles into context
#     context = "\n\n".join([
#         f"Source: {a['source']}\n{a['content']}"
#         for a in articles
#     ])
#
#     prompt = f"""You are an AI newsletter curator. Based on these articles about {', '.join(user_topics)}, create:
#
# 1. A catchy subject line
# 2. A 3-paragraph summary of the most important developments
# 3. One key learning point
# 4. One action item the reader can do today
#
# Articles:
# {context}
#
# Format your response as:
# SUBJECT: [subject line]
# SUMMARY: [3 paragraphs]
# LEARNING: [key point]
# ACTION: [one specific task]
# """
#
#     response = client.chat.completions.create(
#         model="openai/gpt-oss-20b",
#         messages=[{"role": "user", "content": prompt}],
#     )
#
#     return response.choices[0].message.content


# def curate_newsletter(articles: list, user_topics: list, top_trends: list):
#     """Use Groq LLM to curate and summarize articles with Trends to Watch"""
#
#     client = Groq(api_key=os.getenv("GROQ_API_KEY"))
#
#     # Combine articles into context
#     context = "\n\n".join([
#         f"Source: {a['source']}\n{a['content']}"
#         for a in articles
#     ])
#
#     # Pass all trends to the LLM
#     trends_context = "\n\n".join([
#         f"Title: {t['title']}\nSummary: {t['summary']}\nLink: {t['link']}"
#         for t in top_trends
#     ])
#
#     prompt = f"""You are an AI newsletter curator. Based on these articles about {', '.join(user_topics)}, create:
#
# 1. A catchy subject line
# 2. A 3-paragraph summary of the most important developments
# 3. One key learning point
# 4. One action item the reader can do today
# 5. A 'Trends to Watch' block: From the list of trends below, select the top 3 most relevant to the user topics. For each, provide a short explainer and a link.
#
# Articles:
# {context}
#
# All Trends:
# {trends_context}
#
# Format your response exactly as:
# SUBJECT: [subject line]
# SUMMARY: [3 paragraphs]
# LEARNING: [key point]
# ACTION: [one specific task]
# TRENDS TO WATCH:
# 1. [Title + short explainer + link]
# 2. [Title + short explainer + link]
# 3. [Title + short explainer + link]
# """
#
#     response = client.chat.completions.create(
#         model="openai/gpt-oss-20b",
#         messages=[{"role": "user", "content": prompt}],
#     )
#
#     return response.choices[0].message.content

def summarize_text(text: str, max_words: int = 40) -> str:
    """Simple truncation-based summarizer to reduce token usage."""
    words = text.split()
    return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")

def curate_newsletter(
    articles: List[dict],
    user_topics: List[str],
    top_trends: List[dict],
    max_articles: int = 3,
    max_trends: int = 3,
    user_id: int = None
) -> dict:
    """Curate a newsletter as structured JSON using Groq LLM, token-safe version"""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Load writing style examples
    style_examples = style_examples_loader(user_id)
    style_prompt = "\n\n".join([
        f"=== EXAMPLE STYLE {i + 1} ===\n{ex}\n"
        for i, ex in enumerate(style_examples)
    ])
    style_prompt += "\n===\nWrite the following newsletter in a similar voice and tone.\n"

    # Sort or filter articles by relevance to user_topics (simple keyword match)
    def relevance_score(article):
        content = article.get("content", "") + " " + article.get("title", "")
        return sum(content.lower().count(topic.lower()) for topic in user_topics)

    top_articles = sorted(articles, key=relevance_score, reverse=True)[:max_articles]

    # Prepare article context
    articles_context = "\n\n".join([
        f"Title: {a.get('title','')}\nSummary: {summarize_text(a.get('content',''))}\nSource: {a.get('source','')}\nLink: {a.get('link','')}"
        for a in top_articles
    ])

    # Prepare trends context
    trends_context = "\n\n".join([
        f"Title: {t.get('title','')}\nSummary: {summarize_text(t.get('summary',''), max_words=30)}\nLink: {t.get('link','')}"
        for t in top_trends[:max_trends]
    ])

    prompt = f"""
{style_prompt}
You are an AI newsletter curator. Based on the following user topics: {', '.join(user_topics)}, create a newsletter as **valid JSON** with these sections:

1. "intro": a contextual overview paragraph of the week's developments.
2. "curated_links": list of 3 articles most relevant to the user topics. Each item must be an object with:
   - "title" (string)
   - "summary" (short blurb string)
   - "source" (string)
   - "link" (URL string)
3. "summaries": list of objects per topic. Each item must have:
   - "topic" (string)
   - "blurb" (short summary string)
4. "commentary": one overall editorial paragraph (string)
5. "trends": list of top 3 trends most relevant to user topics. Each item must have:
   - "title" (string)
   - "explainer" (short paragraph string)
   - "link" (URL string)

**Important instructions for JSON robustness**:
- Use **double quotes** for all keys and strings.
- Return **only the JSON**, do not add extra text or explanations.
- Example structure:
{{
    "intro": "string",
    "curated_links": [
        {{"title": "string", "summary": "string", "source": "string", "link": "string"}}
    ],
    "summaries": [
        {{"topic": "string", "blurb": "string"}}
    ],
    "commentary": "string",
    "trends": [
        {{"title": "string", "explainer": "string", "link": "string"}}
    ]
}}

Articles:
{articles_context}

All Trends:
{trends_context}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.choices[0].message.content.strip()

    try:
        newsletter_json = json.loads(content)
    except json.JSONDecodeError:
        # fallback if JSON fails
        newsletter_json = {"raw_text": content}

    return newsletter_json