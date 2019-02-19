from .utils import get_soup
from .utils import now

def parse_page(url):
    if '/pub' in url:
        return parse_report(url)
    if '/blog/' in url:
        return parse_blog(url)
    return None

def parse_report(url):
    def parse_author(soup):
        author = soup.find('p', class_='authors').text
        if not author:
            return ''
        return author

    def parse_title(soup):
        title = soup.find('h1', id='RANDTitleHeadingId').text
        if not title:
            return ''
        return title

    def parse_date(soup):
        date = soup.find('meta',attrs={'name':"rand-date"})['content']
        if not date:
            return ''
        return date

    def parse_content(soup):
        content = soup.find('div', class_= 'product-main').text
        if not content:
            return ''
        return content

    def parse_publication_link(soup):
        for a in soup.select('a'):
            if '/content/dam/rand/' in a.attrs.get('href', ''):
                return a.attrs['href']
            if 'doi.org' in a.attrs.get('href', ''):
                return 'external article'

    soup = get_soup(url)
    temp_content_url = parse_publication_link(soup)
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
        'content_url': content_url
    }

def parse_blog(url):
    def parse_author(soup):
        author = soup.find('p', class_='authors').text
        if not author:
            return 'no name'
        return author

    def parse_title(soup):
        title = soup.find('h1', id='RANDTitleHeadingId').text
        if not title:
            return ''
        return title

    def parse_date(soup):
        date = soup.find('p', class_= 'date')
        if not date:
            return ''
        return date.text

    def parse_content(soup):
        content = soup.find('div', class_= 'body-text').text
        if not content:
            return ''
        return content

    def parse_category(soup):
        blog_category = soup.find('p', class_='type').text
        if not blog_category:
            return ''
        return blog_category

    soup = get_soup(url)

    return {
        'url': url,
        'title': parse_title(soup),
        'date': parse_date(soup),
        'author': parse_author(soup),
        'content': parse_content(soup),
        'blog_category': parse_category(soup)
    }
