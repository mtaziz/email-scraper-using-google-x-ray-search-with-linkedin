# -*- coding: utf-8 -*-
import scrapy

from ..items import GoogleSpiderItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request

from scrapy.conf import settings
import logging
from scrapy.utils.log import configure_logging
import sys
import time
from datetime import datetime
from pprint import pprint
# Regular Express
import re
from urlparse import urljoin


class GoogleDetailedSpider(CrawlSpider):
    # timestamp = datetime.now().strftime('%Y-%b-%d')
    timestamp = datetime.now().strftime('%Y-%b-%d_%H%M')
    customs_settings = {}
    # name = 'google_spider'
    name = 'namespider1'
    allowed_domains = ['google.com', 'linkedin.com']
    # Ignore the HTTP status code
    handle_httpstatus_list = [404, 302, 301, 429, 503]
    custom_settings = {
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_USER': '3e1257a319944e91b9f74c642c71e432',
        'CRALERA_PRESERVE_DELAY': True,
        'DOWNLOAD_DELAY': 15,
        'FEED_URI': "export/{0}_{1}.csv".format(name, timestamp)
    }

    """
        # NOTE
        #
        # 'https://www.google.com/search?q=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&oq=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&gs_l\'
        # =serp.3...5963.8711.0.9950.2.2.0.0.0.0.146.277.0j2.2.0....0...1.1.64.serp..0.0.0.bXd0pwkPwok
        # https://www.google.com/search?site=&source=hp&q=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&oq=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&gs_l=hp.3...970.970.0.1720.1.1.0.0.0.0.138.138.0j1.1.0....0...1.1.64.hp..0.0.0.rlmDAXb2pVo
        # https://www.google.com/search?num=50&safe=active&site=&source=hp&q=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&oq=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&gs_l=hp.3...2259.87379.0.88187.2.2.0.0.0.0.255.255.2-1.1.0....0...1.1.64.hp..1.0.0.Y2MYYNUsNro
        g_keyword_list = ['"Red blood cell" -jobs -topic site:linkedin.com']

        query_string = {'linkedin_site': 'linkedin.com', 'minus_topic':'-topic', 'minus_jobs': '-jobs', }

        # Google with 100 pages example
        # google_url = 'https://www.google.com/search?num=100&start=0&hl=en&q=site%3Alinkedin.com+"%40'
        q_number_of_results = 0
        q_string = {}
        q_colon = '%3A'
        q_google_base_url = 'https://www.google.com/search?num={0}&start=0&hl=en&q='.format()
        q_double_quote = '%22'
        q_space = '+'
        q_ignore_hyphen = '-'
        q_at_the_rate = '%40'
        q_ampersend = 'A%26'
        q_kewords = 'Red blood cell'
    """

    start_urls = ['https://www.google.com/search?site=&source=hp&q=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&oq=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&gs_l=hp.3...970.970.0.1720.1.1.0.0.0.0.138.138.0j1.1.0....0...1.1.64.hp..0.0.0.rlmDAXb2pVo']
    rules = (
        Rule(
            LinkExtractor(
                # allow=(),
                #
                restrict_xpaths=(
                    '//table[@id="nav"]//a[contains(@class, "fl")]',),
                # unique=True,
            ),
            callback='parse_name_and_linkedin_url',
            follow=True,
        ),
    )

    def parse_name_and_linkedin_url(self, response):

        item = GoogleSpiderItem()
        divs = response.xpath('//div[contains(@class, "srg")]/div[@class="g"]')
        for div in divs:
            item = GoogleSpiderItem()

            # LinkedIn URL
            item['s1_linkedin_url'] = div.xpath(
                './/div[@class="rc"]/h3/a/@href').extract_first()
            linkedin_url = item['s1_linkedin_url']
            if "/pulse/" in linkedin_url or "/learning/" in linkedin_url:
                item['s1_linkedin_url_with_valid_name'] = ''
            else:
                item['s1_linkedin_url_with_valid_name'] = linkedin_url

            # description
            item['s1_description'] = div.xpath(
                './/span[@class="st"]//text()').extract()

            # Name can be found in title data
            item['s1_title_name_data'] = div.xpath(
                './/div[@class="rc"]/h3/a/text()').extract_first()
            google_title = item['s1_title_name_data']
            company = re.search(r'(?<= at )(.*)', google_title)
            if company:
                item['s1_workat'] = company.group(0)
            else:
                item['s1_workat'] = ''
            address = re.search(r"\((.*?)\)", google_title)
            if address:
                item['s1_address'] = address.group(0)
            else:
                item['s1_address'] = ''

            # phd_data = 'Elena Kostova, PhD | Professioneel profiel - LinkedIn'
            phd_info = re.search(r'(\bPhD\b)|(Ph.D)', google_title)
            if phd_info:
                item['s1_phd_data'] = phd_info.group(0)
                # phd_info_list.append(phd)
            else:
                item['s1_phd_data'] = ''
                # phd_info_list.append(phd)

            title_clean = google_title\
                .replace(item['s1_address'], '')\
                .replace('at {0}'.format(company), '')\
                .replace('(', '').replace(')', '')\
                .replace('| Professional Profile - LinkedIn', '')\
                .replace(' | LinkedIn', '').replace(' on LinkedIn', '')\
                .replace('{}'.format(item['s1_phd_data']), '')
            title_clean = title_clean.split('|')[0]
            title_clean = title_clean.split(',')[0]

            item['s1_name_in_title'] = title_clean

            name_in_linkedin_url_split = item['s1_linkedin_url_with_valid_name'].rsplit(
                '-', 1)[0]
            name_in_linkedin_url_split = (
                ' '.join((name_in_linkedin_url_split.split('/in/')[-1].split('-')))).title()
            item['s1_name_in_linkedin_url'] = name_in_linkedin_url_split

            name_matched = re.search(
                item['s1_name_in_linkedin_url'], item['s1_name_in_title'], re.IGNORECASE)

            if name_matched:
                item['s1_name_in_title_and_linkedin_url'] = name_matched.group(
                    0)
                pprint("Name Found: \n {0} \n".format(name_matched))
            else:
                item['s1_name_in_title_and_linkedin_url'] = ''

            if not item['s1_name_in_title_and_linkedin_url']:
                name_string_in_title = item['s1_name_in_title']
                name_string_in_title = name_string_in_title.split(' ')
                d = re.findall(r"(?=(" + '|'.join(name_string_in_title) + r"))",
                               item['s1_name_in_linkedin_url'], re.IGNORECASE)
                item['s1_name_in_title_and_linkedin_url'] = ' '.join(
                    filter(None, d)).title()
            else:
                item['s1_name_in_title_and_linkedin_url'] = name_matched.group(
                    0)

            item['s1_source_gurl'] = response.url

            yield item
