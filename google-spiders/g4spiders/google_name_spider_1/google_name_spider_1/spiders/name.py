# -*- coding: utf-8 -*-
import scrapy
from ..items import GoogleSpiderItem
from ..items import GoogleDetailedSpiderItem
# from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy.selector import Selector
# from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from scrapy.conf import settings
from scrapy.utils.log import configure_logging
import logging
import sys
import time
from datetime import datetime
import re
from urlparse import urljoin
import csv
from pprint import pprint
from urlparse import urlparse


# Google search results information#############################################
# 1.1 No of google results in a single page
GS_RESULTS_NUM = 100

# 1.2 at which page it should start off
GS_RESULTS_START = 0

# 1.3
# :param - how many results should be returned by a search
GS_RESULTS_STEP = 100

# 1.4
GS_RESULTS_PAGES_NUM = 20

# 2.1
GS_QUERY_WORDS = 'Red blood cell'

# 2.2
GS_DOUBLE_QUOTE = '"'

# 2.3
GS_OPERATOR_SITE = 'site'

# 2.4
GS_LINKEDIN_DOMAIN_NAME = 'linkedin.com'

# 2.5
GS_EXCLUDING_SIGN = '-'

# 2.6
GS_EXCLUDED_WORD_1 = 'topic'

# 2.7
GS_EXCLUDED_WORD_2 = 'jobs'

GS_OPERATOR_SPACE = ' '


# Google search resturns then number of results/entries in a single pages
gGs_results_number = GS_RESULTS_NUM
if GS_RESULTS_NUM:
    GS_RESULTS_NUM = gGs_results_number
elif gGs_results_number == '':
    GS_RESULTS_NUM = 10
else:
    GS_RESULTS_NUM = 10

# Google search results starting at 0
gGs_results_start = GS_RESULTS_START
if gGs_results_start == 0:
    GS_RESULTS_START = gGs_results_start
else:
    GS_RESULTS_START = 0
###############################################################################


####################Google Queries operators conditions########################
# if search kewords not provided, it returns empty
gs_query_string = GS_QUERY_WORDS
if gs_query_string:
    GS_QUERY_WORDS = gs_query_string
else:
    GS_QUERY_WORDS = ''

# google search operator such as site or inurl or intext if not supplied, it returns empty
# google search operator ( i.e., 'site', 'inurl', 'intext', 'intitle')
gs_site_operator = GS_OPERATOR_SITE
if 'site' in gs_site_operator:
    GS_OPERATOR_SITE = 'site'
elif 'intitle' in gs_site_operator:
    GS_OPERATOR_SITE = 'intitle'
elif 'intext' in gs_site_operator:
    GS_OPERATOR_SITE = 'intext'
elif 'inurl' in gs_site_operator:
    GS_OPERATOR_SITE = 'inurl'
else:
    GS_OPERATOR_SITE = ''

# Google site search "domain name"
gs_site_domain = GS_LINKEDIN_DOMAIN_NAME
if gs_site_domain:
    GS_LINKEDIN_DOMAIN_NAME = gs_site_domain
else:
    GS_LINKEDIN_DOMAIN_NAME = ''

# If GS_DOUBLE_QUOTE not provided, it is assigned to 'Empty'
gs_double_quote = GS_DOUBLE_QUOTE
if gs_double_quote:
    GS_DOUBLE_QUOTE = '%22'
else:
    GS_DOUBLE_QUOTE = ''

# Google excluding sign
gs_excluding_sign = GS_EXCLUDING_SIGN
if gs_excluding_sign:
    GS_EXCLUDING_SIGN = gs_excluding_sign
else:
    GS_EXCLUDING_SIGN = ''

# word exclusion 1
gs_excluded_word_1 = GS_EXCLUDED_WORD_1
if gs_excluded_word_1:
    GS_EXCLUDED_WORD_1 = gs_excluded_word_1
else:
    GS_EXCLUDED_WORD_1 = ''

# word exclusion
gs_excluded_word_2 = GS_EXCLUDED_WORD_2
if gs_excluded_word_2:
    GS_EXCLUDED_WORD_2 = gs_excluded_word_2
else:
    GS_EXCLUDED_WORD_2 = ''

gs_space_perator = GS_OPERATOR_SPACE
if gs_space_perator:
    GS_OPERATOR_SPACE = gs_space_perator

else:
    GS_OPERATOR_SPACE = ''

###############################################################################


class GoogleNameSpider1(Spider):
    # timestamp = datetime.now().strftime('%Y-%b-%d')
    timestamp = datetime.now().strftime('%Y-%b-%d_%H%M')
    customs_settings = {}
    # name = 'google_spider'
    name = 'name'
    allowed_domains = ['google.com', 'linkedin.com']
    # Ignore the HTTP status code
    handle_httpstatus_list = [404, 302, 301, 429, 503]

    # NOTE: Please supply `CRAWLERA_USER API KEY`
    custom_settings = {
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_USER': '',
        'CRALERA_PRESERVE_DELAY': True,
        'DOWNLOAD_DELAY': 15,
        'FEED_URI': "export/{0}_{1}.csv".format(name, timestamp)
    }
    # NOTE
    #
    # 'https://www.google.com/search?q=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&oq=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&gs_l\'
    # =serp.3...5963.8711.0.9950.2.2.0.0.0.0.146.277.0j2.2.0....0...1.1.64.serp..0.0.0.bXd0pwkPwok
    # https://www.google.com/search?site=&source=hp&q=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&oq=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&gs_l=hp.3...970.970.0.1720.1.1.0.0.0.0.138.138.0j1.1.0....0...1.1.64.hp..0.0.0.rlmDAXb2pVo
    # https://www.google.com/search?num=50&safe=active&site=&source=hp&q=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&oq=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&gs_l=hp.3...2259.87379.0.88187.2.2.0.0.0.0.255.255.2-1.1.0....0...1.1.64.hp..1.0.0.Y2MYYNUsNro

    def start_requests(self):
        g_keyword_list = ['"Red blood cell" -jobs -topic site:linkedin.com']
        # query_string = {'linkedin_site': 'linkedin.com', 'minus_topic':'-topic', 'minus_jobs': '-jobs', }
        # g_keyword_list = ['"Red blood cell" -jobs -topic site:linkedin.com']

        # query_string = {'linkedin_site': 'linkedin.com', 'minus_topic':'-topic', 'minus_jobs': '-jobs', }

        """ : query_part1: %22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com
            : Google with 100 pages example: google_url = 'https://www.google.com/search?num=100&start=0&hl=en&q=site%3Alinkedin.com+"%40'

            : google_search_url_parts = {
                                        'part_1': 'https://www.google.com/search?site=&source=hp&q=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com',
                                        'part_2': '&gs_l=hp.3...970.970.0.1720.1.1.0.0.0.0.138.138.0j1.1.0....0...1.1.64.hp..0.0.0.rlmDAXb2pVo'
                                        }
            query_string = {
                        'q9_colon': '%3A' if False else '',
                        'q1_base_url' : 'https://www.google.com/search?num={0}&start={1}&hl=en&q='.format(GS_RESULTS_NUM, GS_RESULTS_START),
                        'q2_double_quote': GS_DOUBLE_QUOTE,
                        'q3_search_string': GS_QUERY_WORDS,
                        'q4_space': GS_OPERATOR_SPACE,
                        'q5_excluding_sign': GS_EXCLUDING_SIGN,
                        'q_at_the_rate': '%40' if False else '',
                        'q_ampersend': 'A%26' if False else '',
                        'q6_excluded_word_1': GS_EXCLUDED_WORD_1,
                        'q7_excluded_word_2': GS_EXCLUDED_WORD_2,
                        'q8_site_operator_1': GS_OPERATOR_SITE,
                        'q10_domain_name': GS_LINKEDIN_DOMAIN_NAME
                        }
        """

        query_string = {
            'q9_colon': '%3A',
                        'q1_base_url': 'https://www.google.com/search?num={0}&start={1}&hl=en&q='.format(GS_RESULTS_NUM, GS_RESULTS_START),
                        'q2_double_quote': GS_DOUBLE_QUOTE,
                        'q3_search_string': GS_QUERY_WORDS,
                        'q4_space': GS_OPERATOR_SPACE,
                        'q5_excluding_sign': GS_EXCLUDING_SIGN,
                        'q_at_the_rate': '%40' if False else '',
                        'q_ampersend': 'A%26' if False else '',
                        'q6_excluded_word_1': GS_EXCLUDED_WORD_1,
                        'q7_excluded_word_2': GS_EXCLUDED_WORD_2,
                        'q8_site_operator_1': GS_OPERATOR_SITE,
                        'q10_domain_name': GS_LINKEDIN_DOMAIN_NAME
        }

        start_urls_form = '{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}'.format(
            # query_string['q1_base_url'],
            query_string['q2_double_quote'],
            query_string['q3_search_string'],
            query_string['q2_double_quote'],
            query_string['q4_space'],
            query_string['q5_excluding_sign'],
            query_string['q6_excluded_word_1'],
            query_string['q4_space'],
            query_string['q5_excluding_sign'],
            query_string['q7_excluded_word_2'],
            query_string['q4_space'],
            query_string['q8_site_operator_1'],
            query_string['q9_colon'],
            query_string['q10_domain_name']
        )

        start_urls_form_sanitized = ' '.join(start_urls_form.split())
        # start_urls_list = []
        for gs_result_start in range(0, GS_RESULTS_PAGES_NUM):
            link = 'https://www.google.com/search?num={0}&start={1}&hl=en&q={2}'.format(
                GS_RESULTS_NUM, gs_result_start, start_urls_form_sanitized)
            if " " in link:
                link = link.replace(' ', '+')
                yield Request(
                    url=link,
                    callback=self.parse,
                    method="GET",
                    # meta={'item': item}
                )

    def parse(self, response):

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

            title_clean = google_title.replace(item['s1_address'], '')\
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
