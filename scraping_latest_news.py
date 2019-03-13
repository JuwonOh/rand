import argparse
import json
import os
import re
from rand_scraper import yield_latest_report
from rand_scraper import yield_latest_blog
from rand_scraper import download

def report_save(json_obj, directory):
    url = json_obj['url']
    title = [p for p in url.split('/') if p][-1]
    category = [p for p in url.split('/') if p][3]
    dt = json_obj['date']
    name = '{}-{}-{}_{}_{}'.format(dt.year, dt.month, dt.day, category, re.sub("[\/:*?\<>|]","", title[:50]))
    filepath = '{}/{}.json'.format(directory, name)
    with open(filepath, 'w', encoding='utf-8') as fp:
        json.dump(json_obj, fp, indent=2, ensure_ascii=False, sort_keys=True, default=str)

def blog_save(json_obj, directory):
    url = json_obj['url']
    title = [p for p in url.split('/') if p][-1]
    category = [p for p in url.split('/') if p][2]
    dt = json_obj['date']
    name = '{}-{}-{}_{}_{}'.format(dt.year, dt.month, dt.day, category, re.sub("[\/:*?\<>|]","", title[:50]))
    filepath = '{}/{}.json'.format(directory, name)
    with open(filepath, 'w', encoding='utf-8') as fp:
        json.dump(json_obj, fp, indent=2, ensure_ascii=False, sort_keys=True, default=str)

def scraping_reserch(begin_date, max_num, sleep, directory, verbose):

    n_exceptions = 0
# research category
    for i, json_obj in enumerate(yield_latest_report(begin_date, max_num, sleep)):
        try:
            if '/pubs/' in json_obj['url']:
                report_save(json_obj, directory)
                if 'https:' in json_obj['content_url']:
                    filename = re.sub("[\/:*?\<>|]","", json_obj['content_url'].split('/')[-1])
                    download_path = '{}/{}'.format(directory, filename)
                    download(json_obj['content_url'], download_path)
            if '/blog/' in json_obj['url']:
                blog_save(json_obj, directory)
        except Exception as e:
            n_exceptions += 1
            print(e)
            continue

        if verbose:
            title = json_obj['title']
            time = json_obj['date']
            print('[{} / {}] ({}) {}'.format(i+1, max_num, time, title))

    if n_exceptions > 0:
        print('Exist %d report exceptions' % n_exceptions)

def scraping_article(begin_date, max_num, sleep, directory, verbose):

    n_exceptions = 0
# article category
    for i, json_obj in enumerate(yield_latest_blog(begin_date, max_num, sleep)):
        try:
            blog_save(json_obj, directory)
        except Exception as e:
            n_exceptions += 1
            print(e)
            continue
        if verbose:
            title = json_obj['title']
            time = json_obj['date']
            print('[{} / {}] ({}) {}'.format(i+1, max_num, time, title))

    if n_exceptions > 0:
        print('Exist %d article exceptions' % n_exceptions)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--begin_date', type=str, default='2018-07-01', help='datetime YYYY-mm-dd')
    parser.add_argument('--directory', type=str, default='./output', help='Output directory')
    parser.add_argument('--max_num', type=int, default=1000, help='Maximum number of news to be scraped')
    parser.add_argument('--sleep', type=float, default=1.0, help='Sleep time for each news')
    parser.add_argument('--verbose', dest='VERBOSE', action='store_true')

    args = parser.parse_args()
    begin_date = args.begin_date
    directory = args.directory
    max_num = args.max_num
    sleep = args.sleep
    VERBOSE = args.VERBOSE

    # check output directory
    if not os.path.exists(directory):
        os.makedirs(directory)

    scraping_reserch(begin_date, max_num, sleep, directory, VERBOSE)
    scraping_article(begin_date, max_num, sleep, directory, VERBOSE)

if __name__ == '__main__':
    main()
