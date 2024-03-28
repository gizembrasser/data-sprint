# -*- coding: utf-8 -*-

import pandas as pd

content = pd.read_excel("Output - Op-eds Russia Today (1).xlsx")
content = content[content["Irrelevant sites"].isnull()]
content["Domain"] = "https://" + content["Domain"]
content.head()

SEARCHED_URL = "https://www.rt.com"
RESULT_DOMAINS = content["Domain"].unique().tolist()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"



import requests
from bs4 import BeautifulSoup, SoupStrainer

def fetch_verification_tags(url, timeout=10):
  """
  Fetch meta tags whose names contain 'verification' from the given URL.
  """
  try:
    # Set a User-Agent and timeout for the HTTP request
    headers = {"User-Agent": USER_AGENT}
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



def compare_tags(source_url, target_urls, df):
    """
    Compare verification meta tags between a source URL and a list of target URLs.
    """
    source_tag = fetch_verification_tags(source_url)

    for target_url in target_urls:
      target_tag = fetch_verification_tags(target_url)

      # Check for matches with each dictionary in target_tags list
      matches = {name: content for name, content in target_tag.items() if name in source_tag and source_tag[name] == content}

      if matches:
        for name, content in matches.items():
          print(f"Matching metatags: {target_url}")
        # Update the 'Mirror / Reposter?' column
        df.loc[df["Domain"] == target_url, "Mirror / Reposter?"] = "Mirror"
      else:
        df.loc[df["Domain"] == target_url, "Mirror / Reposter?"] = ""

"""## CSS class analysis

Other metadata identifiers are the CSS classes for the websites. Similairly designed websites will share CSS classes. We will scrape all the unique CSS classes from RT.com.
"""

def scrape_css(url, timeout=10):
  try:
    headers = {"User-Agent": USER_AGENT}
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

"""Compare the unique CSS classes from the source URL to the ones from the dataset. If 90% of the classes match, return the URL for the mirror website."""

def compare_css(source_url, target_urls):
    """
    Compare CSS classes from a base URL to CSS classes from a list of other URLs.
    Return URLs with 90% or more common classes.
    """
    source_css_classes = scrape_css(source_url)

    matching_urls = []
    for url in target_urls:
        css_classes = scrape_css(url)
        common_classes = source_css_classes.intersection(css_classes)

        # Calculate the percentage of common classes
        percentage_common = len(common_classes) / len(source_css_classes)

        if percentage_common >= 0.9:
          matching_urls.append(url)

    return matching_urls

"""## Conclusion

First we will compare the Verification IDs. Print the matching tags and update the DataFrame when a site is classified as a mirror to RT.com. Some sites may still result in errors, so check those manually.
"""

rt_tags = fetch_verification_tags(SEARCHED_URL)
matching_tags = compare_tags(SEARCHED_URL, RESULT_DOMAINS, content)
print(matching_tags)

"""Compare CSS classes from all the unique domains to RT.com. Are the results the same as the matches that came up when comparing the Verification IDs?"""

rt_classes = scrape_css(SEARCHED_URL)
matching_css = compare_css(SEARCHED_URL, RESULT_DOMAINS)
print(matching_css)

"""Which sites are exact mirrors to RT.com, and what location are they based in?"""

filtered_content = content[content["Mirror / Reposter?"] == "Mirror"] # Filter rows with non null values
unique_mirrors = filtered_content["Domain"].unique().tolist() # Extract those values of the 'Domain' column

for domain in unique_mirrors:
  rows = filtered_content[filtered_content["Domain"] == domain]
  locations = rows["Location"].tolist()
  print(f"Domain: {domain}")
  print(f"Locations: {locations}")

"""Save the resulting DataFrame to an Excel file"""

content.to_excel("Output - Op-eds Russia Today (1).xlsx")