import requests
import time
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup

BASE = "https://distill.pub"
USER_AGENT = "MyScraperBot/1.0 (+https://example.com/contact)"
HEADERS = {"User-Agent": USER_AGENT}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

def can_fetch(url, agent=USER_AGENT):
    robots_url = urljoin(BASE, "/robots.txt")
    rp = RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
    except Exception:
        # robots.txt missing or unreadable -> treat as "no rules"
        return True
    return rp.can_fetch(agent, url)

def fetch_page(url):
    if not can_fetch(url):
        print(f"Blocked by robots.txt: {url}")
        return None
    try:
        resp = SESSION.get(url, timeout=15)
        resp.raise_for_status()
        # be polite
        time.sleep(1.5)
        return resp.text
    except requests.HTTPError as e:
        print("HTTP error:", e)
    except requests.RequestException as e:
        print("Request error:", e)
    return None

def scrape_example(path="/"):
    url = urljoin(BASE, path)
    html = fetch_page(url)
    if not html:
        return
    soup = BeautifulSoup(html, "html.parser")
    # example: get all article links on front page (adjust selectors for the real page)
    for a in soup.select("a"):
        href = a.get("href")
        if not href:
            continue
        # normalize relative links
        full = urljoin(BASE, href)
        print(full, "-", a.get_text(strip=True))

if __name__ == "__main__":
    # Example usage: check robots and scrape homepage
    robots_txt_url = urljoin(BASE, "/robots.txt")
    r = SESSION.get(robots_txt_url)
    print("robots.txt status:", r.status_code)  # you saw 404 earlier
    scrape_example("/")
