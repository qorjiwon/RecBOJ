import re

def extract_user_id_from_url(url):
    pattern = r'user_id=([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def extract_problem_id_from_url(url):
    pattern = r'problem_id=([0-9]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None
