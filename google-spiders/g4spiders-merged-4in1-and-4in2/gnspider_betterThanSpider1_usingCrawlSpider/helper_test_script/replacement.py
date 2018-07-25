# -*- coding: utf-8 -*-
import scrapy

from ..items import GoogleSpiderItem
from ..items import GoogleDetailedSpiderItem
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
# Regular Express
import re
from urlparse import urljoin


class GoogleDetailedSpider(CrawlSpider):
    # timestamp = datetime.now().strftime('%Y-%b-%d')
    timestamp = datetime.now().strftime('%Y-%b-%d_%H%M')
    customs_settings = {}
    # name = 'google_spider'
    name = 'gs_detail'
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


    start_urls = ['https://www.google.com/search?site=&source=hp&q=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&oq=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&gs_l=hp.3...970.970.0.1720.1.1.0.0.0.0.138.138.0j1.1.0....0...1.1.64.hp..0.0.0.rlmDAXb2pVo']
    rules = (
        Rule(
            LinkExtractor(
                        # allow=(),
                        #
                        restrict_xpaths=('//table[@id="nav"]//a[contains(@class, "fl")]',),
                        # unique=True,
                        ),
            callback='parse_detail_product',
            follow=True,
            ),
        )

    def parse_detail_product(self, response):
        """
        # TODO
        In [20]: for div in divs:
                    print(div.xpath('.//div[@class="rc"]/h3/a/@href').extract())
        ....:
        [u'https://www.linkedin.com/pulse/your-health-red-blood-cells-kim-ulvberget']
        [u'https://www.linkedin.com/pulse/red-blood-cell-lysis-patrick-slama']
        [u'https://www.linkedin.com/pulse/searching-alternative-plasticizers-red-blood-cell-storage-chen']
        [u'https://www.linkedin.com/pulse/how-flexible-your-red-blood-cells-microfluidic-deborah-chen']
        [u'https://www.linkedin.com/pulse/role-red-blood-cell-distribution-width-assessment-severity-ricerca-1']
        [u'https://www.linkedin.com/pulse/red-blood-cell-transfusion-precision-vs-imprecision-medicine-janasik']
        [u'https://www.linkedin.com/pulse/red-cell-donation-packs-punch-barr-antilla']
        [u'https://www.linkedin.com/pulse/red-blood-cell-docosapentaenoic-acid-dpa-n-3-inversely-nutrients-mdpi']
        [u'https://www.linkedin.com/pulse/anemia-increase-hemoglobin-naturally-judith-cobb']
        [u'https://www.linkedin.com/pulse/fatty-acids-blood-immune-system-under-microscope-kim-ulvberget']
        # NOTE
        # Directly get the title url by using the following xpath
        # item['s1_title_name_data_Url'] = response.xpath('//div[contains(@class, "srg")]/div[@class="g"]/div/div/h3/a/@href').extract()

        #Date
        #
        In [31]: for div in divs:
                    print(div.xpath('.//span[@class="st"]/span[@class="f"]/text()').extract_first().replace(' - ', ''))
        ....:
            May 24, 2017
            Feb 2, 2016
            Oct 15, 2015
            Sep 14, 2015
            May 13, 2017
            Sep 11, 2015
            Jan 25, 2016
            Oct 14, 2015
            Mar 28, 2017
            Nov 17, 2016
        """
        # item = GoogleSpider()
        divs = response.xpath('//div[contains(@class, "srg")]/div[@class="g"]')
        for div in divs:
            item = GoogleSpiderItem()
            # print(div.xpath('.//div[@class="rc"]/h3/a/@href').extract())
            item['s1_title_name_data'] = div.xpath('.//div[@class="rc"]/h3/a/text()').extract_first()
            item['s1_linkedin_url'] = div.xpath('.//div[@class="rc"]/h3/a/@href').extract_first()
            item['s1_description'] = div.xpath('.//span[@class="st"]//text()').extract()
            yield item



class GoogleSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #
    #
    # s1_title_name_data = scrapy.Field()

    s1_title_name_data = scrapy.Field()
    s1_linkedin_url = scrapy.Field()
    s1_linkedin_url_with_valid_name = scrapy.Field()
    s1_description = scrapy.Field()
    s1_name_in_linkedin_url = scrapy.Field()
    s1_name_in_title = scrapy.Field()
    s1_name_in_title_and_linkedin_url = scrapy.Field()
    s1_address = scrapy.Field()
    s1_workat = scrapy.Field()
    s1_phd_data = scrapy.Field()
    s1_education = scrapy.Field()
    s1_name_gurl =scrapy.Field()


FIELDS_TO_EXPORT = ['s1_title_name_data',
                    's1_linkedin_url',
                    's1_linkedin_url_with_valid_name',
                    's1_name_in_title',
                    's1_name_in_linkedin_url',
                    # 's1_name_in_title',
                    's1_fullname',
                    's1_address',
                    's1_workat',
                    's1_phd_data',
                    's1_education',
                    's1_source_gurl']


class GoogleSpiderPipeline(object):

    def process_item(self, item, spider):

        # if item['s1_title_name_data']:
        google_title = item['s1_title_name_data']
        # name_list = []
        # phd_info_list = []
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
        # item['s1_phd_data'] = phd
        pprint("PhD or Ph.DTaken Off____________{0}".format(item['s1_phd_data']))
        # else:
        #     pass
        # if item['s1_title_name_data_Url']:
        #   item['s1_linkedin_url'] = item['s1_title_name_data_Url']
        # else:
        #   item['s1_linkedin_url'] = ''
        # s1_name_in_linkedin_url
        # s1_name_in_title
        # if item['s1_linkedin_url']:
        linkedin_url = item['s1_linkedin_url']
        if "/pulse/" in  linkedin_url or "/learning/" in linkedin_url:
            item['s1_linkedin_url_with_valid_name'] = ''
        else:
            item['s1_linkedin_url_with_valid_name'] = linkedin_url
        name_in_linkedin_url_split = item['s1_linkedin_url_with_valid_name'].rsplit('-', 1)[0]
        name_in_linkedin_url_split = (' '.join((name_in_linkedin_url_split.split('/in/')[-1].split('-')))).title()
        item['s1_name_in_linkedin_url'] = name_in_linkedin_url_split
        name_matched = re.search(item['s1_name_in_linkedin_url'], item['s1_name_in_title'], re.IGNORECASE)
        if name_matched:
            item['s1_name_in_title_and_linkedin_url'] = name_matched.group(0)
            pprint("Name Found: \n {0} \n".format(name_matched))
        else:
            item['s1_name_in_title_and_linkedin_url'] = ''
        if not item['s1_name_in_title_and_linkedin_url']:
            name_string_in_title = item['s1_name_in_title']
            name_string_in_title = name_string_in_title.split(' ')
            d = re.findall(r"(?=("+'|'.join(name_string_in_title)+r"))", item['s1_name_in_linkedin_url'], re.IGNORECASE)
            item['s1_name_in_title_and_linkedin_url'] = ' '.join(filter(None, d)).title()
        else:
            item['s1_name_in_title_and_linkedin_url'] = item['s1_name_in_title_and_linkedin_url'] = name_matched.group(0)
            # if not item['s1_name_in_title_and_linkedin_url']:
            #     # name_in_single_word = re.search(item['s1_name_in_linkedin_url'], item['s1_name_in_title'], re.IGNORECASE)
            # else:

                # name_found.append(data)
            # pprint('name_found within loop: \n__________{0}__________\n'.format(name_found))
        return item
