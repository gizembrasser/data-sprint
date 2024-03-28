import re

def validate_url(url):
    """
    Check if the given string is a valid URL.
    """
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https:// or ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,63}|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # Check if the string matches the URL pattern
    if re.match(url_pattern, url):
        return True
    else:
        return False


def validate_user_agent(user_agent):
    """
    Check if the provided string is a valid User-Agent.
    """
    if user_agent and any(keyword in user_agent.lower() for keyword in ['mozilla', 'chrome', 'safari', 'firefox']):
        return True
    else:
        return False