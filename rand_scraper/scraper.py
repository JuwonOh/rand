import re
import time
from datetime import datetime
from .parser import parse_page
from .utils import get_soup
from .utils import blog_dateformat
from .utils import user_dateformat
from .utils import report_dateformat
from .utils import strf_to_datetime

def is_matched(url):
    for pattern in patterns:
        if pattern.match(url):
            return True
    return False

patterns = [
    re.compile('https://www.rand.org/blog/[\w]+'),
    re.compile('https://www.rand.org/pubs/[\w]+'),
    re.compile('/blog/[\w]+')
    ]
url_report = 'https://www.rand.org/pubs.html?page={}'

def yield_latest_report(begin_date, max_num=10, sleep=1.0):
    """
    Artuments
    ---------
    begin_date : str
        eg. 2018-01-01
    max_num : int
        Maximum number of news to be scraped
    sleep : float
        Sleep time. Default 1.0 sec

    It yields
    ---------
    news : json object
    """

    # prepare parameters
    d_begin = strf_to_datetime(begin_date, user_dateformat)
    end_page = 72
    n_news = 0
    outdate = False

    for page in range(1, end_page+1):

        # check number of scraped news
        if n_news >= max_num or outdate:
            break

        # get urls
        links_all= []
        url = url_report.format(page)
        soup = get_soup(url)
        sub_links =soup.find_all('div', class_='text')
        links = [i.find('h3').find('a')['href'] for i in sub_links]
        links_all += links
        links_all = [url for url in links_all if is_matched(url)]

        # scrap
        for url in links_all:

            news_json = parse_page(url)

            # check date
            if '/pub' in url:
                d_news = strf_to_datetime(news_json['date'], report_dateformat)
            elif 'blog' in url:
                d_news = strf_to_datetime(news_json['date'], blog_dateformat)

            if d_begin > d_news:
                outdate = True
                print('Stop scrapping. {} / {} article was scrapped'.format(n_news, max_num))
                print('The oldest article has been created after {}'.format(begin_date))
                break
            # yield
            yield news_json

            # check number of scraped news
            n_news += 1
            if n_news >= max_num:
                break
            time.sleep(sleep)

def get_report_urls(begin_page=0, end_page=3, verbose=True):
    """
    Arguments
    ---------
    begin_page : int
        Default is 1
    end_page : int
        Default is 3
    verbose : Boolean
        If True, print current status

    Returns
    -------
    links_all : list of str
        List of urls
    """

    links_all = []
    for page in range(begin_page, end_page+1):
        url = url_report.format(page)
        soup = get_soup(url)
        sub_links = soup.find_all('div', class_='text')
        links = [i.find('h3').find('a')['href'] for i in sub_links]
        links_all += links
        links_all = [url for url in links_all if is_matched(url)]

    return links_all

blog_urls = 'https://www.rand.org/blog/{}/{}.html'

def yield_latest_blog(begin_date, max_num=10, sleep=1.0):
    """
    Artuments
    ---------
    begin_date : str
        eg. 2018-01-01
    page_number : print
         if you want more page, you increase page number
    max_num : int
        Maximum number of news to be scraped
    sleep : float
        Sleep time. Default 1.0 sec

    It yields
    ---------
    news : json object
    """

    # prepare parameters
    d_begin = strf_to_datetime(begin_date, user_dateformat)
    end_page = 72
    n_news = 0
    outdate = False

    for year in (2019, 2018):

        # check number of scraped news
        if n_news >= max_num or outdate:
            break

        # get urls
        links_all =[]
        links = []
        for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            url = blog_urls.format(year, month)
            soup = get_soup(url)
            sub_links = soup.find_all('div', class_='text')
            links = [i.find('h3').find('a')['href'] for i in sub_links]
            links_all += links
            links = [url for url in links_all if is_matched(url)]

        # scrap
        links_all = ['https://www.rand.org' + url for url in links if 'https:' not in url]
        links = list(reversed(links_all))
        for url in links:
            news_json = parse_page(url)

            # check date
            if '/pub' in url:
                d_news = strf_to_datetime(news_json['date'], report_dateformat)
            elif '/blog/' in url:
                d_news = strf_to_datetime(news_json['date'], blog_dateformat)

            if d_begin > d_news:
                outdate = True
                print('Stop scrapping. {} / {} article was scrapped'.format(n_news, max_num))
                print('The oldest article has been created after {}'.format(begin_date))
                break

            # yield
            yield news_json

            # check number of scraped news
            n_news += 1
            if n_news >= max_num:
                break
            time.sleep(sleep)

def get_blog_urls(verbose=True):
    """
    Arguments
    ---------
    begin_page : int
        Default is 1
    end_page : int
        Default is 3
    verbose : Boolean
        If True, print current status

    Returns
    -------
    links_all : list of str
        List of urls
    """

    links_all = []
    links = []

    for year in (2018,2019):
        for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            url = blog_urls.format(year, month)
            soup = get_soup(url)
            sub_links = soup.find_all('div', class_='text')
            links = [i.find('h3').find('a')['href'] for i in sub_links]
            links_all += links
            links = [url for url in links_all if is_matched(url)]

    links_all = ['https://www.rand.org' + url for url in links if 'https:' not in url]
    links = list(reversed(links_all))
    return links
