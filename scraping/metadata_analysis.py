import requests
from bs4 import BeautifulSoup, SoupStrainer


def scrape_tags(url, user_agent, timeout=10):
  """
  Fetch meta tags whose names contain 'verification' from the given URL.
  """
  try:
    # Set a User-Agent and timeout for the HTTP request
    headers = {"User-Agent": user_agent}
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()

    # Parse only the meta tags to improve performance
    parse_only = SoupStrainer("meta")
    soup = BeautifulSoup(response.text, "html.parser", parse_only=parse_only)

    # Find all meta tags with 'name' attribute containing 'verification'
    verification_tags = soup.find_all("meta", attrs={"name": lambda x: x and "verification" in x.lower()})
    # Extract 'content' attribute
    if verification_tags:
      return {tag['name']: tag.get('content', '') for tag in verification_tags if tag.has_attr('content')}
    else:
      return {}
  except Exception as e:
    print(f"Error fetching verification tags from {url}: {e}")
    return {}


def compare_tags(source_url, target_urls, user_agent):
    """
    Compare verification meta tags between a source URL and a list of target URLs.
    """
    source_tag = scrape_tags(source_url, user_agent)
    all_matches = []

    for target_url in target_urls:
      target_tag = scrape_tags(target_url, user_agent)

      # Check for matches with each dictionary in target_tags list
      matches = {name: content for name, content in target_tag.items() if name in source_tag and source_tag[name] == content}

      if matches:
          all_matches.append((target_url, matches))
    
    return all_matches

