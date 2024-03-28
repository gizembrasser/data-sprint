import requests
from bs4 import BeautifulSoup, SoupStrainer

def scrape_css(url, user_agent, timeout=10):
  """
  Fetch meta tags whose names contain 'verification' from the given URL.
  """
  try:
    headers = {"User-Agent": user_agent}
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()

    # Parse only the meta tags to improve performance
    parse_only = SoupStrainer("meta")
    soup = BeautifulSoup(response.text, "html.parser", parse_only=parse_only)

    used_classes = set()

    for elem in soup.select("[class]"):
      classes = elem["class"]
      used_classes.update(classes)

    return used_classes
  except Exception as e:
    print(f"Error scraping CSS classes from {url}: {e}")
    return set()


def compare_css(source_url, target_urls, user_agent):
    """
    Compare CSS classes from a base URL to CSS classes from a list of other URLs.
    Return URLs with 90% or more common classes.
    """
    source_css_classes = scrape_css(source_url, user_agent)

    matching_urls = []
    for target_url in target_urls:
        css_classes = scrape_css(target_url, user_agent)
        common_classes = source_css_classes.intersection(css_classes)

        # Calculate the percentage of common classes
        percentage_common = len(common_classes) / len(source_css_classes)

        if percentage_common >= 0.9:
          matching_urls.append(target_url)

    return matching_urls