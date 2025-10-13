import re
from datetime import datetime

from app.scrape.twitter_web_scraper import scrape_twitter_web


def extract_twitter_handle(url: str) -> str:
    match = re.search(r"(?:https?://)?(?:www\.)?(?:x\.com|twitter\.com)/([A-Za-z0-9_]+)", url)
    return match.group(1) if match else None

def daily_newsletter_scrape(sources: list[str]):
    """Function to run daily for AI newsletter content"""

    # Define your newsletter sources
    ai_accounts = [
        "OpenAI", "AnthropicAI", "DeepMind", "huggingface",
        "ylecun", "karpathy", "jeremyphoward"
    ]

    ai_hashtags = [
        "#AI", "#MachineLearning", "#DeepLearning", "#LLM",
        "#GenerativeAI", "#ChatGPT", "#GPT4"
    ]

    # Combine accounts and hashtags
    all_targets = ai_accounts + ai_hashtags

    # Scrape data
    data = scrape_twitter_web(
        targets=all_targets,
        output_file=f"newsletter_data_{datetime.now().strftime('%Y%m%d')}.json",
        delay=2
    )

    return data