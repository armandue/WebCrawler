import requests
import re
from urllib.parse import urlparse

HTML_INFO = "\nCount {count} --- Link: {link}\n\tDescription: {description}\n\tKeywords: {keywords}\n"

BASE_URL_FORMAT = "{scheme}://{netloc}"

A_TAG_REGEX = '<a\s+(?:[^>]*?\s+)?href="([^"]*)"'

INFO_REGEX = "<meta .*?name=[\"'](.*?)['\"].*?content=[\"'](.*?)['\"].*?>"


def get_html(url):
    try:
        html = requests.get(url)
    except Exception as e:
        print(e)
        return ""
    else:
        return html.content.decode('latin-1')


def get_links(url):
    html = get_html(url)
    parsed = urlparse(url)
    base = BASE_URL_FORMAT.format(scheme=parsed.scheme, netloc=parsed.netloc)
    links = re.findall(A_TAG_REGEX, html)
    for i, link in enumerate(links):
        if not urlparse(link).netloc:
            link_with_base = base + link
            links[i] = link_with_base
    return set(filter(lambda x: 'mailto' not in x, links))


def extract_info(url):
    html = get_html(url)
    meta = re.findall(INFO_REGEX, html)
    return dict(meta)


class PyCrawler(object):

    def __init__(self):
        self.visited = set()
        self.count = 0

    def crawl(self, url):
        for link in get_links(url):
            if link not in self.visited:
                # info = extract_info(link)
                self.count += 1
                # print(HTML_INFO.format(count=self.count,
                #                        link=link,
                #                        description=info.get('description'),
                #                        keywords=info.get('keywords')))
                self.visited.add(link)
                self.crawl(link)

    def start(self, starting_url):
        self.crawl(starting_url)


if __name__ == "__main__":
    crawler = PyCrawler()
    crawler.start("https://proxyorbit.com/")
    print("I am done with " + str(crawler.count) + " urls.")
