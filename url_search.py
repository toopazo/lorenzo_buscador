
import argparse
import requests
from bs4 import BeautifulSoup


def search_inside_baseurl(scrapy_log, baseurl, patterns, outfile):
    """
    Search for all the url that are a strict subset of baseurl and that also
    contain the given patterns

    :param scrapy_log: Log produced by 'scrapy crawl' command
    :param baseurl: Base url
    :param patterns: Patterns that all url need to satisfy
    :param outfile: Output file to save all the resulting url
    """

    url_arr = get_url_from_scrapy_log(scrapy_log, baseurl)

    unique_urls = []
    for url in url_arr:
        print('--------')
        print(f'url {url}')
        rel_urls = find_links_using_bs4(url, patterns)
        for suburl in rel_urls:
            unique_urls.append(f"{baseurl}{suburl}")

    unique_urls = set(unique_urls)
    fd = open(outfile, 'w')
    for elem in unique_urls:
        fd.write(f'{elem}\n')
    fd.close()


def get_url_from_scrapy_log(scrapy_log, url):
    fd = open(scrapy_log, 'r')
    lines = fd.readlines()

    pattern = f"[scrapy.core.engine] DEBUG: Crawled (200) <GET {url}"
    target_urls = []
    for line in lines:
        if pattern in line:
            # print(f'[search_in_spider_log] match {line}')

            # Extract target url from line
            turl = line
            split_str = "> (referer:"
            sarr = turl.split(split_str)
            turl = sarr[0]
            split_str = "<GET "
            sarr = turl.split(split_str)
            turl = sarr[1]
            print(f'[search_in_spider_log] target url {turl}')
            target_urls.append(turl)

    # Filter repeated urls
    print(f'[search_in_spider_log] len target urls {len(target_urls)}')
    target_urls = set(target_urls)
    print(f'[search_in_spider_log] len target urls {len(target_urls)}')
    # print(f'[search_in_spider_log] target urls {turls}')
    return target_urls


def find_links_using_bs4(url, patterns):
    # url = 'https://www.geeksforgeeks.org/'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    rel_urls = []
    for link in soup.find_all('a'):
        link = link.get('href')
        # link = f'{url}/{link}'
        # print(f"link: {link}")
        all_good = True
        for pattern in patterns:
            if pattern in link:
                pass
            else:
                all_good = False
        if all_good:
            print(f"link: {link}")
            rel_urls.append(f'{link}')

    return rel_urls


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Arguments for search_inside_url')
    parser.add_argument('--baseurl', action='store', required=True,
                        help='url bajo la que buscar')
    parser.add_argument('--scrapy_log', action='store', required=True,
                        help='Log de scrapy')
    parser.add_argument('--patterns', action='store', nargs='+', required=True,
                        help='Lista de patrones para filtrar')
    parser.add_argument('--outfile', action='store', required=True,
                        help='Archivo de las url subconjunto de baseurl')

    args = parser.parse_args()
    print(f'baseurl {args.baseurl}')
    print(f'scrapy_log {args.scrapy_log}')
    print(f'patterns {args.patterns}')
    print(f'outfile {args.outfile}')

    # www.corplascondes.cl/contenidos/transparencia/ley_de_transparencia/
    search_inside_baseurl(
        args.scrapy_log, args.baseurl, args.patterns, args.outfile)

    # python url_search.py \
    # --baseurl https://www.corplascondes.cl/contenidos/transparencia/ley_de_transparencia/ \
    # --scrapy_log scrapy_crawler/scrapy_crawler/spiders/corplascondes.log \
    # --patterns 2019 .pdf --outfile output_2019_pdf.txt

