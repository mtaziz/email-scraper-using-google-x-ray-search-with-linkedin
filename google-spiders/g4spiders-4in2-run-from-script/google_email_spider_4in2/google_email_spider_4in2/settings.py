# -*- coding: utf-8 -*-

# Scrapy settings for google_email_spider_4in2 project

# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
from datetime import datetime
import time
import scrapy
BOT_NAME = 'google_email_spider_4in2'
# google_email_spider_4in2

SPIDER_MODULES = ['google_email_spider_4in2.spiders']
# NEWSPIDER_MODULE = 'google_email_spider_4in2.spiders'
#
CRAWLERA_ENABLED = True
CRAWLERA_USER = ''
# USER_AGENT = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0"
DOWNLOAD_DELAY = 15
DOWNLOADER_MIDDLEWARES = {
                           'google_email_spider_4in2.middlewares.GoogleSpiderSpiderMiddleware': 543,
                           'scrapy_crawlera.CrawleraMiddleware': 600
                        }
# spider_name = "g_spider"
# Custom exporter to enforce field order
FEED_EXPORTERS = {
                    'csv': 'google_email_spider_4in2.csv_exporters.ItemExporter'
                }

ITEM_PIPELINES = { 'google_email_spider_4in2.pipelines.S1GoogleDupfilterPipeline': 300 }

timestmp = datetime.now().strftime('%Y-%b-%d_%H-%M-%S')
FEED_FORMAT = 'csv'
# exports to csv
# dateTimeString = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
FEED_URI = "import/namespider1_{0}.csv".format(timestmp)
FIELDS_TO_EXPORT = [
                    'Title',
                    'FirstName',
                    'LastName',
                    'FullName',
                    'CompanyDomain',
                    'CompanyEmail1',
                    'Email2',
                    'Email1_Raw',
                    'Email2_Raw',
                    'Suffix',
                    'JobTitle',
                    'Company',
                    'Current_Company',
                    'CompanyName2',
                    'Previous_Company',
                    'Education',
                    # 'CompanyEmail1',
                    # 'Email2',
                    'CompanyWebsite',
                    'HomePhone',
                    'CellPhone',
                    'WorkPhone',
                    'WorkExt',
                    'Address',
                    'City',
                    'State',
                    'Zip',
                    'Country',
                    'LinkedInUrl',
                    # 'Source',
                    'Notes',
                    'RawData_Address_JobTitle',
                    'RawData_FullName',
                    'RawData_Employment_History',
                    's1_name_gurl',
                    's2_jobtitle_gurl',
                    's3_domain_gurl',
                    's4_email_gurl',
                    's1_title_name_data',
                    's1_linkedin_url',
                    's1_linkedin_url_with_valid_name',
                    's1_name_in_title',
                    's1_name_in_linkedin_url',
                    's1_name_in_title_and_linkedin_url',
                    's1_address',
                    's1_workat',
                    's1_phd_data',
                    's1_education',
                    's1_source_gurl'

                    # 'Source_Url_DomainSpider3',
                    # 's1_source_url'
                    ]

# s1_name_gurl = scrapy.Field()
# s2_jobtitle_gurl = scrapy.Field()
# s3_domain_gurl = scrapy.Field()
# s4_email_gurl = scrapy.Field()
#
"""FIELDS_TO_EXPORT_FINAL = ['Title',
                    'FirstName',
                    'LastName',
                    'Suffix',
                    'JobTitle',
                    'CompanyEmail1',
                    'Email2',
                    'HomePhone',
                    'CellPhone',
                    'WorkPhone',
                    'WorkExt',
                    'Address',
                    'City',
                    'State',
                    'Zip',
                    'Country',
                    'LinkedInUrl',
                    'Source',
                    'Notes']
"""

# -- extracted name and linkedin urls from namespider1 fed into the emailspider3in1
INPUT_FILE_DIR = 'import'
INPUT_FILE_NAME = 'namespider1_items.csv'
INPUT_FILE_PATH = 'import/namespider1_items.csv'
OUTPUT_FILE_DIR = 'export'
OUTPUT_FILE_NAME = ''
OUTPUT_FILE_PATH = '{0}/{1}'.format(OUTPUT_FILE_DIR, OUTPUT_FILE_NAME)

GS_RESULTS_NUM = 10
GS_RESULTS_PAGES_NUM = 1
GOOGLE_SEARCH_KEWORDS = 'red blood cell'
GOOGLE_SEARCH_KEWORDS_WITH_OPERATORS = '"Red blood cell" -jobs -topic site:linkedin.com'
# -- extracted name and linkedin urls from namespider1 fed into the emailspider3in1

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'google_email_spider_4in2.pipelines.GoogleSpiderPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 8000000
HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    #Chrome
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.38 Safari/537.36",
    #IE
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    "Mozilla/5.0 (IE 11.0; Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C; rv:11.0) like Gecko",
    "Mozilla/5.0 (IE 11.0; Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
    #Safari
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_6; it-it) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-HK) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; sv-SE) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/6.1.3 Safari/537.75.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/600.3.10 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.10",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    ]
