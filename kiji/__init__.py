from kiji.article import Article
import requests


def from_url(url: str, params=None, **kwargs) -> Article:
    response = requests.get(url, params=params, **kwargs)
    return from_html(response.text)


def from_file(filename: str) -> Article:
    with open(filename) as f:
        return from_html(f.read())


def from_html(html_input: str) -> Article:
    return Article(html_input)
