from .utils import get_soup
from .utils import now
from dateutil.parser import parse

def parse_page(url):
    """
    Argument
    --------
    url : str
        Web page url

    Returns
    -------
    json_object : dict
        JSON format web page contents
        It consists with
            title : article title
            time : article written time
            content : text with line separator \\n
            url : web page url
            scrap_time : scrapped time
    """
    try:
        if '/pub' in url:
            return parse_report(url)
        if '/blog/' in url:
            return parse_blog(url)
    except Exception as e:
        print(e)
        print('Parsing error from {}'.format(url))
        return None

def parse_report(url):
    def parse_author(soup):
        author = soup.find('p', class_='authors')
        if not author:
            return 'no author'
        return author.text

    def parse_title(soup):
        title = soup.find('h1', id='RANDTitleHeadingId')
        if not title:
            return ''
        return title.text

    def parse_date(soup):
        date = soup.find('meta',attrs={'name':"rand-date"})['content']
        if not date:
            return '20190306'
        return parse(date)

    def parse_content(soup):
        content = soup.find('div', class_= 'product-main')
        if not content:
            return ''
        return content.text

    def parse_publication_link(soup):
        for a in soup.select('a'):
            if '/content/dam/rand/' in a.attrs.get('href', ''):
                return a.attrs['href']
            if 'external' in a.attrs.get('class', ''):
                return 'external article'

    soup = get_soup(url)
    temp_content_url = parse_publication_link(soup)
    if '/content/dam/rand/' in temp_content_url:
        if 'https:' not in temp_content_url:
            content_url = 'https://www.rand.org' + temp_content_url
    else:
        content_url = temp_content_url
    return {
        'url': url,
        'title': parse_title(soup),
        'date': parse_date(soup),
        'author': parse_author(soup),
        'abstract': parse_content(soup),
        'content_url': content_url,
        'scraping_time': now()
    }

def parse_blog(url):
    def parse_author(soup):
        author = soup.find('p', class_='authors')
        if not author:
            return 'no name'
        return author.text

    def parse_title(soup):
        title = soup.find('h1', id='RANDTitleHeadingId')
        if not title:
            return ''
        return title.text

    def parse_date(soup):
        date = soup.find('p', class_= 'date')
        if not date:
            return '20190306'
        return parse(date.text)

    def parse_content(soup):
        content = soup.find('div', class_= 'body-text')
        if not content:
            return ''
        return content.text

    def parse_category(soup):
        blog_category = soup.find('p', class_='type')
        if not blog_category:
            return ''
        return blog_category.text

    soup = get_soup(url)

    return {
        'url': url,
        'title': parse_title(soup),
        'date': parse_date(soup),
        'author': parse_author(soup),
        'content': parse_content(soup),
        'blog_category': parse_category(soup),
        'scraping_time': now()
    }
