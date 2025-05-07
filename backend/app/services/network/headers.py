import requests


def get_http_headers(url):
    """
    Get the HTTP headers for a given URL.

    Args:
        url (str): The URL to get headers for.

    Returns:
        dict: A dictionary containing the URL, status code, headers, and any error encountered.
    """
    
    try:
        resp = requests.head(url, timeout=3)
        return {
            "url": url,
            "status_code": resp.status_code,
            "headers": dict(resp.headers),
            "error": None
        }
    except Exception as e:
        return {
            "url": url,
            "status_code": None,
            "headers": None,
            "error": str(e)
        }
