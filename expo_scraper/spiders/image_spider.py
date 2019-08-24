import scrapy
import re
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from expo_scraper.items import ExpoScraperItem

class ImageSpider(scrapy.Spider):
    name = "images"

    
    downloaded_image_urls = set()
    visited_links = set()
    visited_stylesheets = set()

    # allowed_domains = ["exponea.com"]
    start_urls = [
            'https://exponea.com/'
    ]

    def resolve_image_url(self, image_url, response):
        self.downloaded_image_urls.add(image_url)
        return ExpoScraperItem(image_urls=[image_url], from_page=response.url)

    def parse(self, response):
        body = Selector(text=response.body)

        images_to_download = [img_url for img_url in body.css('img::attr(src)').getall() if self.has_image_extension(img_url) and not img_url in self.downloaded_image_urls]
        for image_url in images_to_download:
            yield self.resolve_image_url(image_url, response)

        stylesheets = [css_url for css_url in body.css('link[rel=stylesheet]::attr(href)').getall() if not css_url in self.visited_stylesheets]
        for stylesheet in stylesheets:
            self.visited_stylesheets.add(stylesheet)
            yield response.follow(stylesheet, self.parse_stylesheet)

        link_extractor = LinkExtractor(canonicalize=True, allow_domains=["exponea.com"])

        next_links = [link.url for link in link_extractor.extract_links(response) if not link.url in self.visited_links]
        self.log(f'Following {len(next_links)} links')
        self.log(f'Already scraped ({len(self.visited_links)}) links')
        for link in next_links:
            self.visited_links.add(link)
            yield response.follow(link, self.parse) 

    def parse_stylesheet(self, response):
        self.log(f'Crawling Stylesheet ({response.url})')
        css_text = response.text

        link_search = re.findall('url\((.*?)\)', css_text, re.IGNORECASE)
        for match in link_search:
            if str.startswith(match, '('):
                link = match[1:-1]
            else :
                link = match

            if not link.lower().startswith('http'):
                link = response.urljoin(link)
            
            if link.lower().endswith('.css') and not link in self.visited_stylesheets:
                self.log(f'Found Stylesheet url ({link})')
                self.visited_stylesheets.add(link)
                yield response.follow(link, self.parse_stylesheet) 

            if self.has_image_extension(link) and not link in self.downloaded_image_urls:
                self.log(f'Found Image in stylesheet url ({link})')
                yield self.resolve_image_url(link, response)
            
    def has_image_extension(self, file_name):
        lower_file_name = file_name.lower()
        return lower_file_name.endswith('.png') \
            or lower_file_name.endswith('.jpg') \
            or lower_file_name.endswith('.gif') \


        