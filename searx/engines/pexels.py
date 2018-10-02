"""
 Pexels

 @website     https://www.pexels.com
 @provide-api no

 @using-api   no
 @results     HTML
 @stable      no
 @parse       url, img_src, thumbnail_src
"""

from searx.url_utils import urlencode, quote, urljoin
from lxml import html

url = 'https://www.pexels.com'
search_url = url + '/search/{query}?format=html&'
paging = True
categories = ['images']
timeout = 5.0


def request(query, params):
    params['url'] = search_url.format(query=quote(query)) + urlencode({'page': params['pageno']})
    print(params['url'])
    return params


def response(resp):
    results = []

    dom = html.fromstring(resp.text)
    for photo in dom.xpath('//article[@class="photo-item"]'):
        link = photo.xpath('.//a[@class="js-photo-link"]')[0]
        thumbnail = link.xpath('.//img[@class="photo-item__img"]')[0]
        download_link = photo.xpath('.//a[@download]')[0]
        results.append({'template': 'images.html',
                        'url': urljoin(url, link.attrib.get('href')),
                        'thumbnail_src': urljoin(url, thumbnail.attrib.get('src')),
                        'img_src': urljoin(url, download_link.attrib.get('href')),
                        'title': '',
                        'content': ''})

    return results
