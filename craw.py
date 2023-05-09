import multiprocessing
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import requests
import colorama
import argparse




colorama.init()
note = colorama.Fore.CYAN
name = colorama.Fore.GREEN

requests.packages.urllib3.disable_warnings()



class MultiThreadedCrawler:

    def __init__(self, seed_url):
        self.seed_url = seed_url
        self.root_url = '{}://{}'.format(urlparse(self.seed_url).scheme,
                                        urlparse(self.seed_url).netloc)
        self.domain = urlparse(self.root_url ).netloc
        self.pool = ThreadPoolExecutor(max_workers=5)
        self.scraped_pages = set([])
        self.crawl_queue = Queue()
        self.crawl_queue.put(self.seed_url)

    def do_request(self, url):
        try:

            with requests.get(url, verify=False, timeout=(3, 30)) as res:
                return res
        except requests.RequestException:
            return

    def parse_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        Anchor_Tags = soup.find_all('a')
        for a_tag in  Anchor_Tags:
            href = a_tag.get("href")
            if href == "" or href is None:
                continue
            href = urljoin(self.root_url, href)
            if self.domain in href:
                if href not in self.scraped_pages:
                    self.crawl_queue.put(href)


        Link_Tag = soup.find_all("link")
        for link_tag in Link_Tag:
            href = link_tag.get("href")
            if href == "" or href is None:
                continue
            href = urljoin(self.root_url, href)
            if self.domain in href:
                if href not in self.scraped_pages:
                    self.crawl_queue.put(href)

        # Find all <script src=>
        scripts = soup.find_all("script")
        for src in [link['src'] for link in scripts if 'src' in link.attrs]:
            if src == "" or src is None:
                continue
            src = urljoin(self.root_url, src)
            if self.domain in src:
                if src not in self.scraped_pages:
                    self.crawl_queue.put(src)
        
        # Find all <src=>
        for src_tag in soup.find_all("src"):
            src = src_tag.get("src")
            if src == "" or src is None:
                continue
            src = urljoin(self.root_url, src)
            if self.domain in src:
                if src not in self.scraped_pages:
                    self.crawl_queue.put(src)

        # Find all <img src=>
        for img_tag in soup.find_all("img"):
            src = img_tag.get("src")
            if src == "" or src is None:
                continue
            src = urljoin(self.root_url, src)
            if self.domain in src:
                if src not in self.scraped_pages:
                    self.crawl_queue.put(src)

        # Find all <video src=>
        for video_tag in soup.find_all("video"):
            src = video_tag.get("src")
            if src == "" or src is None:
                continue
            src = urljoin(self.root_url, src)
            if self.domain in src:
                if src not in self.scraped_pages:
                    self.crawl_queue.put(src)

        # Find all <track src=>
        for track_tag in soup.find_all("track"):
            src = track_tag.get("src")
            if src == "" or src is None:
                continue
            src = urljoin(self.root_url, src)
            if self.domain in src:
                if src not in self.scraped_pages:
                    self.crawl_queue.put(src)

        # Find all  <audio src=>
        for audio_tag in soup.find_all("audio"):
            src = audio_tag.get("src")
            if src == "" or src is None:
                continue
            src = urljoin(self.root_url, src)
            if self.domain in src:
                if src not in self.scraped_pages:
                    self.crawl_queue.put(src)

        # Find all  <embed src=>
        for embed_tag in soup.find_all("embed"):
            src = embed_tag.get("src")
            if src == "" or src is None:
                continue
            src = urljoin(self.root_url, src)
            if self.domain in src:
                if src not in self.scraped_pages:
                    self.crawl_queue.put(src)

        # Find all  <iframe src=>
        for iframe_tag in soup.find_all("iframe"):
            src = iframe_tag.get("src")
            if src == "" or src is None:
                continue
            src = urljoin(self.root_url, src)
            if self.domain in src:
                if src not in self.scraped_pages:
                    self.crawl_queue.put(src)

        # Find all <button onclick="">
        buttons = [btn['onclick']
                for btn in soup.find_all('button') if 'onclick' in btn.attrs]
        for onclick in buttons:
            d = re.search(r"='.*'|=\".*\"", onclick).group()
            b = urljoin(url, d.split("=")[1].replace("'", "").replace('"', ""))
            if self.domain in b:
                if b not in self.scraped_pages:
                    self.crawl_queue.put(b)



    def post_scrape_callback(self, res):
        result = res.result()
        if result and result.status_code < 400:
            self.parse_links(result.text)


    def run_web_crawler(self):
        while True:
            try:
                target_url = self.crawl_queue.get(timeout=3)
                if target_url not in self.scraped_pages:
                    print(target_url)
                    self.current_scraping_url = "{}".format(target_url)
                    self.scraped_pages.add(target_url)
                    job = self.pool.submit(self.do_request, target_url)
                    job.add_done_callback(self.post_scrape_callback)

            except Empty:
                return
            except Exception as e:
                print(e)
                continue

    def info(self):
        print()
        print(f'{note}[*] URL is: ', self.seed_url)
        print(f'{note}[*] Number of Crawled Urls : {len(self.scraped_pages)}')
        print(f'{name}[#] Coded By Muhammad Ehab - @_muhamd_ehab_')


def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-u", "--url", help="Target URL (e.g. http://testphp.vulnweb.com)",required=True)
    return argparser.parse_args()

def main():
    args = parse_args()
    start = MultiThreadedCrawler(args.url)
    start.run_web_crawler()
    start.info()

if __name__ == "__main__":
    main()
            