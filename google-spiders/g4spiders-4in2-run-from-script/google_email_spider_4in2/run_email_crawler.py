import scrapy
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from google_email_spider_3in1.spiders.namespider1_parse import GoogleNameSpider1
from google_email_spider_3in1.spiders.emailspider3in1 import GoogleEmailSpider3In1
from scrapy.utils.project import get_project_settings
import os
import time

# Provide google search string as below

googleSearchKeywordsInput = 'erythrocyte red gene'
googleSearchKeywordsInput = "Red blood cell"

# Provide search keywords detail to search google along with Google operators
# operators
googleSearchKeywordsWithOperatorsDetail = 'site:linkedin.com erythrocyte red gene(phD OR PH.D D.Phil) viral lines -jobs'
googleSearchKeywordsWithOperatorsDetail = '"Red blood cell" -jobs -topic site:linkedin.com'

# Provide how many google search results would be returned,
# and how many pages would be crawled.
googleNoOfSearchResults = 20
googleSearchResultsNoOfPages = 10

# Check if file exist before we write
try:
    if os.path.exists("import/namespider1_{0}_items.csv".format(googleSearchKeywordsInput)):
        print "Name and LinkedInUrl File existed, removing....................."
        os.remove(
            "import/namespider1_{0}_items.csv".format(googleSearchKeywordsInput))
    elif os.path.exists("export/emailspider3in1_{0}_items.csv".format(googleSearchKeywordsInput)):
        print "Emails exported File existed, removing....................."
        os.remove(
            "export/emailspider3in1_{0}_items.csv".format(googleSearchKeywordsInput))
    else:
        pass
except:
    pass

settings = get_project_settings()
namespider1_settings = {
    'GOOGLE_SEARCH_KEWORDS': googleSearchKeywordsInput,
    'GOOGLE_SEARCH_KEWORDS_WITH_OPERATORS': googleSearchKeywordsWithOperatorsDetail,
    'GS_RESULTS_NUM': googleNoOfSearchResults,
    'GS_RESULTS_PAGES_NUM': googleSearchResultsNoOfPages,
    'DOWNLOADER_MIDDLEWARES': {
        'google_email_spider_3in1.middlewares.GoogleSpiderSpiderMiddleware': 543,
        'scrapy_crawlera.CrawleraMiddleware': 600
    },
    'CRAWLERA_ENABLED': True,
    'CRAWLERA_USER': '3e1257a319944e91b9f74c642c71e432',
    'CRALERA_PRESERVE_DELAY': True,
    'DOWNLOAD_DELAY': 15,
    'USER_AGENT': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0",
    'FEED_EXPORTERS': {'csv': 'google_email_spider_3in1.csv_exporters.ItemExporter'},
    'ITEM_PIPELINES': {
        'google_email_spider_3in1.pipelines.S1GoogleDupfilterPipeline': 550
        # 'google_email_spider_3in1.pipelines.S1GoogleDupfilterValidNamePipeline': 600
    },
    'FEED_FORMAT': 'csv',
    'FEED_URI': "import/namespider1_{0}_items.csv".format(googleSearchKeywordsInput),
    'FIELDS_TO_EXPORT': ['s1_title_name_data',
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
                         ],
    'HTTPCACHE_ENABLED': False,
    'HTTPCACHE_EXPIRATION_SECS': 8000000,
    'HTTPCACHE_DIR': 'httpcache'
}

emailspider_s3in1_settings = {
    'GOOGLE_SEARCH_KEWORDS': googleSearchKeywordsInput,
    'GOOGLE_SEARCH_KEWORDS_WITH_OPERATORS': googleSearchKeywordsWithOperatorsDetail,
    'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 600},
    'CRAWLERA_ENABLED': True,
    'CRAWLERA_USER': '3e1257a319944e91b9f74c642c71e432',
    'CRALERA_PRESERVE_DELAY': True,
    'DOWNLOAD_DELAY': 15,
    'USER_AGENT': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0",
    'FEED_EXPORTERS': {'csv': 'google_email_spider_3in1.csv_exporters.ItemExporter'},
    'ITEM_PIPELINES': {'google_email_spider_3in1.pipelines.S3In1GoogleDupfilterPipeline': 550},
    'FEED_FORMAT': 'csv',
    'FEED_URI': "export/emailspider3in1_{0}_items.csv".format(googleSearchKeywordsInput),
    'FIELDS_TO_EXPORT': [
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
        'Notes',
        'RawData_Address_JobTitle',
        'RawData_FullName',
        'RawData_Employment_History',
        's1_name_gurl',
        's2_jobtitle_gurl',
        's3_domain_gurl',
        's4_email_gurl'
    ],
    'INPUT_FILE_PATH': 'import/namespider1_{0}_items.csv'.format(googleSearchKeywordsInput),
    'HTTPCACHE_ENABLED': False,
    'HTTPCACHE_EXPIRATION_SECS': 8000000,
    'HTTPCACHE_DIR': 'httpcache'
}

configure_logging()
runner1 = CrawlerRunner(namespider1_settings)
runner2 = CrawlerRunner(emailspider_s3in1_settings)


@defer.inlineCallbacks
def crawl():
    yield runner1.crawl(GoogleNameSpider1)
    time.sleep(3)
    yield runner2.crawl(GoogleEmailSpider3In1)
    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished
