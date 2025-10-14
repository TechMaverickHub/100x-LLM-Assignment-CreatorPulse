import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone


def get_article_content_safe(url):
    """Safely get article content with error handling"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, verify=False, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Try to extract main content with comprehensive selectors
        content_selectors = [
            # News site specific selectors
            '.article-body p',
            '.story-body p',
            '.article-content p',
            '.post-content p',
            '.entry-content p',
            '.content p',
            '.story p',
            '.article p',
            'article p',
            'main p',
            '.main p',
            # Generic selectors
            'p'
        ]

        for selector in content_selectors:
            paragraphs = soup.select(selector)
            if paragraphs:
                content_parts = []
                for p in paragraphs[:5]:  # First 5 paragraphs for better context
                    text = p.get_text(strip=True)
                    if len(text) > 50:  # Longer minimum for better content
                        content_parts.append(text)

                if content_parts and len(' '.join(content_parts)) > 200:
                    return ' '.join(content_parts)

        # Try to get content from meta description as fallback
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc = meta_desc.get('content').strip()
            if len(desc) > 100:
                return desc

        # Final fallback: get all text and clean it
        text = soup.get_text()
        if len(text) > 100:
            # Clean up the text
            lines = text.split('\n')
            clean_lines = [line.strip() for line in lines if len(line.strip()) > 50]
            if clean_lines:
                return ' '.join(clean_lines[:3])  # First 3 substantial lines

    except Exception as e:
        print(f"     ⚠️ Error getting content from {url}: {e}")

    return ""

def scrape_api_source(url, headers):
    """Scrape from API source (like Hacker News)"""
    articles = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if 'hits' in data:
            for hit in data['hits'][:5]:
                title = hit.get('title', '')
                url = hit.get('url', '')
                points = hit.get('points', 0)
                created_at = hit.get('created_at', '')

                # if title and url and points > 5:  # Only articles with some engagement
                if title and url:
                    # Get content from the article
                    content = get_article_content_safe(url)

                    if content:
                        articles.append({
                            'source': url,
                            'title': title,
                            'content': content[:1500],
                            'published': created_at
                        })
                        print(f"   ✅ Found: {title[:50]}...")

    except Exception as e:
        print(f"   ⚠️ API scraping error: {e}")

    return articles


def scrape_reddit_source(url, headers):
    """Scrape from Reddit source"""
    articles = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if 'data' in data and 'children' in data['data']:
            for post in data['data']['children'][:5]:
                post_data = post.get('data', {})
                title = post_data.get('title', '')
                url = post_data.get('url', '')
                score = post_data.get('score', 0)
                selftext = post_data.get('selftext', '')

                if title and url and score > 10:  # Only posts with some engagement
                    # Try to get real content from the external URL
                    if selftext and len(selftext) > 100:
                        content = selftext
                    else:
                        # Fetch content from the external article URL
                        content = get_article_content_safe(url)
                        if not content or len(content) < 100:
                            content = f"Recent news: {title}. This article discusses important developments in the field."

                    articles.append({
                        'source': url,
                        'title': title,
                        'content': content[:1500],
                        'published': None
                    })
                    print(f"   ✅ Found: {title[:50]}...")

    except Exception as e:
        print(f"   ⚠️ Reddit scraping error: {e}")

    return articles


def scrape_arxiv_source(url, headers):
    """Scrape from ArXiv source"""
    articles = []


    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse XML response
        from xml.etree import ElementTree as ET
        root = ET.fromstring(response.content)

        # ArXiv namespace
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        for entry in root.findall('atom:entry', ns)[:5]:
            title_elem = entry.find('atom:title', ns)
            summary_elem = entry.find('atom:summary', ns)
            link_elem = entry.find('atom:link[@type="text/html"]', ns)

            if title_elem is not None and summary_elem is not None:
                title = title_elem.text.strip()
                summary = summary_elem.text.strip()
                url = link_elem.get('href') if link_elem is not None else ''

                articles.append({
                    'source': url,
                    'title': title,
                    'content': summary[:1500],
                    'published': None
                })
                print(f"   ✅ Found: {title[:50]}...")

    except Exception as e:
        print(f"   ⚠️ ArXiv scraping error: {e}")

    return articles

def scrape_rss_source(url):
    """
    Scrape articles from an RSS feed (e.g. 404media.co/rss)
    Returns a list of dicts with: source, title, content, published
    """

    articles = []
    seen_links = set()
    now = datetime.now(timezone.utc)

    try:
        feed = feedparser.parse(url)
        print(f"🔍 Found {len(feed.entries)} items in {url}")

        for entry in feed.entries:
            link = entry.get("link")
            title = entry.get("title", "").strip()

            # Deduplicate
            if not link or link in seen_links:
                continue
            seen_links.add(link)

            # Parse published date (RSS may vary)
            published_parsed = None
            if "published_parsed" in entry and entry.published_parsed:
                published_parsed = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            elif "updated_parsed" in entry and entry.updated_parsed:
                published_parsed = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
            else:
                published_parsed = now  # fallback if missing

            # Filter: only last 7 days
            if (now - published_parsed) > timedelta(days=7):
                continue

            # Fetch full article content (your existing helper)
            content = get_article_content_safe(link)

            # Skip empty content
            if not content:
                continue

            articles.append({
                "source": link,
                "title": title,
                "content": content[:1500],
                "published": published_parsed.isoformat()
            })

            print(f"   ✅ Collected: {title[:70]}")

    except Exception as e:
        print(f"⚠️ RSS scraping error for {url}: {e}")

    print(f"📰 Total collected: {len(articles)}")
    return articles
