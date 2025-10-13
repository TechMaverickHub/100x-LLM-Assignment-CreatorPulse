import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime
from urllib.parse import urljoin, quote
import logging


class TwitterWebScraper:
    def __init__(self, delay=2):
        """
        Initialize Twitter web scraper

        Args:
            delay: Delay between requests in seconds
        """
        self.session = requests.Session()
        self.delay = delay

        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _make_request(self, url, max_retries=3):
        """
        Make HTTP request with retry logic

        Args:
            url: URL to request
            max_retries: Maximum number of retries

        Returns:
            requests.Response or None
        """
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=10)

                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    self.logger.warning(f"Rate limited. Waiting {self.delay * 2} seconds...")
                    time.sleep(self.delay * 2)
                else:
                    self.logger.warning(f"HTTP {response.status_code} for {url}")

            except requests.RequestException as e:
                self.logger.error(f"Request failed (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(self.delay)

        return None

    def _extract_tweet_data(self, tweet_element):
        """
        Extract data from a tweet element

        Args:
            tweet_element: BeautifulSoup element containing tweet

        Returns:
            dict: Tweet data
        """
        tweet_data = {
            'id': None,
            'text': '',
            'author': '',
            'created_at': None,
            'media_attachments': [],
            'metrics': {
                'likes': 0,
                'retweets': 0,
                'replies': 0
            },
            'url': ''
        }

        try:
            # Extract tweet text
            text_elements = tweet_element.find_all(['span', 'div'],
                                                   class_=re.compile(r'.*tweet.*text.*|.*text.*content.*', re.I))
            if text_elements:
                tweet_data['text'] = ' '.join(
                    [elem.get_text(strip=True) for elem in text_elements if elem.get_text(strip=True)])

            # Extract author information
            author_elements = tweet_element.find_all(['span', 'div'],
                                                     class_=re.compile(r'.*username.*|.*handle.*|.*author.*', re.I))
            if author_elements:
                author_text = author_elements[0].get_text(strip=True)
                if author_text.startswith('@'):
                    tweet_data['author'] = author_text[1:]
                else:
                    tweet_data['author'] = author_text

            # Extract media attachments (images, videos)
            media_elements = tweet_element.find_all(['img', 'video'], src=True)
            for media in media_elements:
                if 'profile' not in media.get('src', '').lower():  # Skip profile images
                    media_info = {
                        'type': 'image' if media.name == 'img' else 'video',
                        'url': media.get('src'),
                        'alt': media.get('alt', '')
                    }
                    tweet_data['media_attachments'].append(media_info)

            # Extract metrics (likes, retweets, replies)
            metric_elements = tweet_element.find_all(['span', 'div'],
                                                     class_=re.compile(r'.*metric.*|.*count.*|.*stat.*', re.I))
            for elem in metric_elements:
                text = elem.get_text(strip=True)
                if text.isdigit():
                    # This is a simple heuristic - in real scraping you'd need more sophisticated logic
                    if 'like' in str(elem.get('class', [])).lower():
                        tweet_data['metrics']['likes'] = int(text)
                    elif 'retweet' in str(elem.get('class', [])).lower():
                        tweet_data['metrics']['retweets'] = int(text)
                    elif 'reply' in str(elem.get('class', [])).lower():
                        tweet_data['metrics']['replies'] = int(text)

        except Exception as e:
            self.logger.error(f"Error extracting tweet data: {str(e)}")

        return tweet_data

    def get_user_tweets(self, username, count=10):
        """
        Scrape tweets from a user's profile

        Args:
            username: Twitter handle (without @)
            count: Number of tweets to attempt to scrape

        Returns:
            list: List of tweet data dictionaries
        """
        self.logger.info(f"Scraping tweets from @{username}")

        url = f"https://twitter.com/{username}"
        response = self._make_request(url)

        if not response:
            self.logger.error(f"Failed to fetch profile page for @{username}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')

        # Check if account is private/protected
        private_indicators = soup.find_all(text=re.compile(r'protected|private|suspended', re.I))
        if private_indicators:
            self.logger.warning(f"Account @{username} appears to be private/protected or suspended")
            return []

        # Look for tweet elements using common Twitter CSS patterns
        # Note: These selectors are based on common patterns and may need updates
        tweet_selectors = [
            '[data-testid="tweet"]',
            'article[role="article"]',
            '.tweet',
            '[class*="tweet"]'
        ]

        tweets = []
        for selector in tweet_selectors:
            tweet_elements = soup.select(selector)
            if tweet_elements:
                self.logger.info(f"Found {len(tweet_elements)} tweet elements using selector: {selector}")
                break
        else:
            # Fallback: look for any elements that might contain tweets
            tweet_elements = soup.find_all(['article', 'div'],
                                           class_=re.compile(r'.*tweet.*|.*post.*', re.I))
            self.logger.info(f"Using fallback selector, found {len(tweet_elements)} elements")

        # Extract data from tweet elements
        for i, tweet_element in enumerate(tweet_elements[:count]):
            tweet_data = self._extract_tweet_data(tweet_element)
            if tweet_data['text']:  # Only add tweets with actual text content
                tweet_data['author'] = username  # Ensure author is set
                tweet_data['url'] = f"https://twitter.com/{username}"
                tweets.append(tweet_data)

        self.logger.info(f"Successfully extracted {len(tweets)} tweets from @{username}")
        time.sleep(self.delay)

        return tweets

    def search_tweets_by_hashtag(self, hashtag, count=10):
        """
        Search tweets by hashtag

        Args:
            hashtag: Hashtag to search (with or without #)
            count: Number of tweets to attempt to scrape

        Returns:
            list: List of tweet data dictionaries
        """
        # Ensure hashtag starts with #
        if not hashtag.startswith('#'):
            hashtag = f"#{hashtag}"

        self.logger.info(f"Scraping tweets for hashtag {hashtag}")

        # URL encode the hashtag for the search
        encoded_hashtag = quote(hashtag)
        url = f"https://twitter.com/search?q={encoded_hashtag}&src=typed_query&f=live"

        response = self._make_request(url)

        if not response:
            self.logger.error(f"Failed to fetch search results for {hashtag}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for tweet elements in search results
        tweet_selectors = [
            '[data-testid="tweet"]',
            'article[role="article"]',
            '.tweet',
            '[class*="tweet"]'
        ]

        tweets = []
        for selector in tweet_selectors:
            tweet_elements = soup.select(selector)
            if tweet_elements:
                self.logger.info(f"Found {len(tweet_elements)} tweet elements for {hashtag}")
                break
        else:
            # Fallback
            tweet_elements = soup.find_all(['article', 'div'],
                                           class_=re.compile(r'.*tweet.*|.*post.*', re.I))
            self.logger.info(f"Using fallback selector for {hashtag}, found {len(tweet_elements)} elements")

        # Extract data from tweet elements
        for i, tweet_element in enumerate(tweet_elements[:count]):
            tweet_data = self._extract_tweet_data(tweet_element)
            if tweet_data['text'] and hashtag.lower() in tweet_data['text'].lower():
                tweet_data['hashtag_searched'] = hashtag
                tweets.append(tweet_data)

        self.logger.info(f"Successfully extracted {len(tweets)} tweets for hashtag {hashtag}")
        time.sleep(self.delay)

        return tweets

    def save_to_json(self, data, filename):
        """
        Save scraped data to JSON file

        Args:
            data: Data to save
            filename: Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Data saved to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving to JSON: {str(e)}")


# Main scraping function
def scrape_twitter_web(targets, output_file="twitter_web_data.json", delay=2):
    """
    Main function to scrape Twitter using web scraping

    Args:
        targets: List of usernames and/or hashtags
        output_file: Output JSON filename
        delay: Delay between requests
    """
    scraper = TwitterWebScraper(delay=delay)
    all_data = {
        'scraped_at': datetime.now().isoformat(),
        'method': 'web_scraping',
        'users': {},
        'hashtags': {}
    }

    for target in targets:
        if target.startswith('#'):
            # It's a hashtag
            hashtag_data = scraper.search_tweets_by_hashtag(target, count=10)
            all_data['hashtags'][target] = hashtag_data
            print(f"Scraped {len(hashtag_data)} tweets for hashtag {target}")
        else:
            # It's a username
            user_data = scraper.get_user_tweets(target, count=10)
            all_data['users'][target] = user_data
            print(f"Scraped {len(user_data)} tweets for user @{target}")

    scraper.save_to_json(all_data, output_file)
    return all_data

# Usage example:
# scrape_twitter_web(["elonmusk", "#AI", "OpenAI"])
