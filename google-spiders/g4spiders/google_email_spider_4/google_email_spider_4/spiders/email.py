# @Author: Tariq
# @Date:   2018-07-25T05:30:05+06:00
# @Email:  pytariq@gmail.com
# @Filename: email.py
# @Last modified by:   Tariq
# @Last modified time: 2018-07-26T04:37:54+06:00



# -*- coding: utf-8 -*-

import scrapy

# from ..items import GoogleSpiderItem
# from ..items import GoogleDetailedSpiderItem
# from ..items import GoogleDomainItem
from ..items import GoogleCompanyDomainSpiderItem
from ..items import GoogleEmailSpiderItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from scrapy.shell import inspect_response
from scrapy.conf import settings
import logging
from scrapy.utils.log import configure_logging
import sys
import time
from datetime import datetime
# Regular Express
import re
from urlparse import urljoin
import csv
from pprint import pprint
from urlparse import urlparse


INPUT_FILE_DIR = 'import'
# INPUT_FILE_NAME = 'google_jobtitle_spider_2_27July2017.csv'
INPUT_FILE_NAME = 'find_company_domain_2017-Jul-30_020652.csv'
INPUT_FILE_PATH = '{0}/{1}'.format(INPUT_FILE_DIR, INPUT_FILE_NAME)

OUTPUT_FILE_DIR = 'export'
OUTPUT_FILE_NAME = ''
OUTPUT_FILE_PATH = '{0}/{1}'.format(OUTPUT_FILE_DIR, OUTPUT_FILE_NAME)


class GoogleEmailSpider(scrapy.Spider):

    # timestamp = datetime.now().strftime('%Y-%b-%d')
    timestamp = datetime.now().strftime('%Y-%b-%d_%H%M%S')
    customs_settings = {}

    # name = 'google_spider'
    name = 'email'

    # allowed_domains = ['google.com', 'linkedin.com']
    # Ignore the HTTP status code
    handle_httpstatus_list = [404, 302, 301, 429, 503]

    # settings parameters in settings.py overriden by using custom_settings
    # NOTE: Please as CRAWLERA_USER API KEY
    custom_settings = {
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_USER': '',
        'CRALERA_PRESERVE_DELAY': True,
        'HTTPCACHE_ENABLED': True,
        'DOWNLOAD_DELAY': 15,
        'FEED_URI': "{0}/{1}_{2}.csv".format(OUTPUT_FILE_DIR, name, timestamp)
    }

    """ This is a test section before reading "the company information" from CSV file
        It is easy to test before we execute the final spider, HTTP cache : enabled while testing
        HTTPCACHE makes the testing process easier as it stores all the source data.
        Proxy costs if we send the same request to the remote server, during test development
        test_list_of_company: the raw
    """
    test_list_of_company = """The fields data will be added"""
    # locompany_list = filter(None, test_list_of_company.split('\n'))
    # test_start_urls_list = []
    gurl = "https://www.google.com/search?q=Texas+A%26M+University&oq=Texas+A%26M+University"
    query_string = {"google_base_url": "https://www.google.com/search?q=",
                    "FullName": "", "JobTitle": "", "Company": "", "location": ""}
    # results = ""

    # for loc in locompany_list:
    #     location_plus = '+'.join(loc.split(' '))
    #     test_start_urls_list.append("{0}{1}{2}{3}&ie=utf-8&oe=utf-8".format(query_string['google_base_url'],
    #                                                     query_string['FullName'],
    #                                                     query_string['JobTitle'],
    #                                                     location_plus,
    #                                                     query_string['JobTitle']))
    # start_urls = test_start_urls_list
    # _____________________________________________________________END OF TEST___________________________________________

    def start_requests(self):
        start_urls_list = []
        with open(INPUT_FILE_PATH, 'rb') as input_file:
            csv_reader = csv.DictReader(input_file)
            for row in list(csv_reader):

                # url_test = {
                #             'https://www.google.com/search?num=100&start={counter}&hl=en&q="%40{word}"': 'usaid.gov'
                #             "word": "domain",
                #             "word" : "usaid.gov"
                #             "linkedin_example": "https://www.google.com/search?num=100&start=0&hl=en&q=site%3Alinkedin.com+%22%40steamteamutah.com"
                #             "site:linkedin.com \"@steamteamutah.com":
                #             }
                # init_search(self, url, word, limit, counterInit, counterStep, engineName):
                # app_emailharvester.init_search(url, domain, limit, 0, 100, 'Google')
                # domain = "wustl.edu"
                # limit = 100
                # counterInit =
                # counterStep = 100

                # queries = {"url": "url",
                #             "word": "domain",
                #             "limit": "limit",
                #             "0": "counterInit",
                #             "100": "counterStep",
                #             "engineName": "Google"}

                # all the fields will be passed to the new csv exported into export directory
                currentcompany = row['Current_Company']
                title = row['Title']
                firstname = row['FirstName']
                lastname = row['LastName']
                fullname = row['FullName']
                companydomain = row['CompanyDomain']
                suffix = row['Suffix']
                jobtitle = row['JobTitle']
                company = row['Company']
                current_company = row['Current_Company']
                previous_company = row['Previous_Company']
                education = row['Education']
                # companyemail1 = row['CompanyEmail1']
                # email2 = row['Email2']
                homephone = row['HomePhone']
                cellphone = row['CellPhone']
                workphone = row['WorkPhone']
                workext = row['WorkExt']
                address = row['Address']
                city = row['City']
                state = row['State']
                zip = row['Zip']
                country = row['Country']
                linkedinurl = row['LinkedInUrl']
                source = row['Source']
                notes = row['Notes']
                rawdata_address_jobtitle = row['RawData_Address_JobTitle']
                rawdata_fullname = row['RawData_FullName']
                rawdata_employment_history = row['RawData_Employment_History']

                # Mapping among fields and will be passed to the parse function
                meta_data_dict = {
                    'title': title,
                    'firstname': firstname,
                    'lastname': lastname,
                    'fullname': fullname,
                    'companydomain': companydomain,
                    'suffix': suffix,
                    'jobtitle': jobtitle,
                    'company': company,
                    'current_company': current_company,
                    'previous_company': previous_company,
                    'education': education,
                    # 'companyemail1': companyemail1,
                    # 'email2': email2,
                    'homephone': homephone,
                    'cellphone': cellphone,
                    'workphone': workphone,
                    'workext': workext,
                    'address': address,
                    'city': city,
                    'state': state,
                    'zip': zip,
                    'country': country,
                    'linkedinurl': linkedinurl,
                    'source': source,
                    'notes': notes,
                    'rawdata_address_jobtitle': rawdata_address_jobtitle,
                    'rawdata_fullname': rawdata_fullname,
                    'rawdata_employment_history': rawdata_employment_history
                }
                # final_query = "Anthony+Awojoodu"+"*+%40mckinsey.com"
                # https://www.google.com/search?client=ubuntu&channel=fs&q=%22Anthony+Awojoodu%22+%22*+%40mckinsey.com%22&oq=%22Anthony+Awojoodu%22+%22*+%40mckinsey.com%22&gs_l=psy-ab.3..33i160k1l2.5806.5806.0.6166.1.1.0.0.0.0.125.125.0j1.1.0....0...1.1.64.psy-ab..0.1.124.wOfKHqG-wHs
                link = '{0}%22{1}%22+%22*+%40{2}%22{3}&ie=utf-8&oe=utf-8'.format(self.query_string['google_base_url'],
                                                                                 row['FullName'].replace(
                                                                                     ' ', '+'),
                                                                                 row['CompanyDomain'],\
                                                                                 # self.query_string['JobTitle'],\
                                                                                 self.query_string['JobTitle']
                                                                                 )
                yield Request(
                    url=link,
                    callback=self.parse,
                    method="GET",
                    meta=meta_data_dict
                )

    def parse(self, response):

        item = GoogleEmailSpiderItem()
        results = response.body
        for e in '''<KW> </KW> </a> <b> </b> </div> <em> </em> <p> </span>
                    <strong> </strong> <title> <wbr> </wbr>'''.split():
            results = results.replace(e, '')
        for e in '%2f %3a %3A %3C %2B %3D & / : ; < = > \\'.split():
            results = results.replace(e, ' ')
        # item = GoogleSpiderItem()
        # item = GoogleDetailedSpiderItem()
        # item = GoogleDetailedSpiderItem()
        # item = GoogleCompanyDomainSpiderItem()

        # Below fields are imported from the "input_file"/obtained from spider2
        item['Title'] = response.meta['title']
        item['FirstName'] = response.meta['firstname']
        item['LastName'] = response.meta['lastname']
        item['FullName'] = response.meta['fullname']
        item['CompanyDomain'] = response.meta['companydomain']
        item['Suffix'] = response.meta['suffix']
        item['JobTitle'] = response.meta['jobtitle']
        item['Company'] = response.meta['company']
        item['Current_Company'] = response.meta['current_company']
        item['Previous_Company'] = response.meta['previous_company']
        item['Education'] = response.meta['education']
        # item['CompanyEmail1'] = response.meta['companyemail1']
        # item['Email2'] = response.meta['email2']
        item['HomePhone'] = response.meta['homephone']
        item['CellPhone'] = response.meta['cellphone']
        item['WorkPhone'] = response.meta['workphone']
        item['WorkExt'] = response.meta['workext']
        item['Address'] = response.meta['address']
        item['City'] = response.meta['city']
        item['State'] = response.meta['state']
        item['Zip'] = response.meta['zip']
        item['Country'] = response.meta['country']
        item['LinkedInUrl'] = response.meta['linkedinurl']
        item['Source'] = response.meta['source']
        item['Notes'] = response.meta['notes']
        item['RawData_Address_JobTitle'] = response.meta['rawdata_address_jobtitle']
        item['RawData_FullName'] = response.meta['rawdata_fullname']
        item['RawData_Employment_History'] = response.meta['rawdata_employment_history']

        # get the domain specific emails
        # reg_emails_domain_specific = re.compile('[a-zA-Z0-9.\-_+#~!$&\',;=:]+' +'@' +'[a-zA-Z0-9.-]*' +"mdanderson.org")
        reg_domain_specific = re.compile(
            '[a-zA-Z0-9.\-_+#~!$&\',;=:]+' + '@' + '[a-zA-Z0-9.-]*' + item['CompanyDomain'])
        emails_domain_specific = reg_domain_specific.findall(results)
        for eds in emails_domain_specific:
            if "+@" in eds:
                emails_domain_specific.remove(eds)
        emails_domain_specific = [i.strip().lower()
                                  for i in emails_domain_specific]
        # item['CompanyEmail1'] = '; '.join(list(set(emails_domain_specific)))
        emails_domain_specific = '; '.join(list(set(emails_domain_specific)))
        item['Email1_Raw'] = emails_domain_specific

        # get the  "general domains" based emails (like, gmail.com or yahoo.com or any other domains)
        reg_domain_general = re.compile(
            '[a-zA-Z0-9.\-_+#~!$&\',;=:]+' + '@' + '[a-zA-Z0-9.-]*')
        emails_domain_general = reg_domain_general.findall(results)
        for eds in emails_domain_general:
            if "+@" in eds:
                emails_domain_general.remove(eds)
        emails_domain_general = [i.strip().lower()
                                 for i in emails_domain_general]
        emails_domain_general = '; '.join(list(set(emails_domain_general)))
        item['Email2_Raw'] = emails_domain_general

        emails_domain_specific_plus_general = "{0}; {0}".format(
            emails_domain_specific, emails_domain_general)
        company_email_sanitized = self.find_name_in_email_match(
            item['FullName'], emails_domain_specific_plus_general)
        company_email_sanitized = filter(None, company_email_sanitized)
        company_email_sanitized = list(set(company_email_sanitized))
        # company_email_sanitized

        """
            NOTE:
            check the gathered emails list if it has more than one element or email address
            If gathered email has a single email address, it should be stored in CompanyEmail1
            or if it has 2 email addresses then "CompanyEmail1" and "Email2" will be storing the first and last one respectively
            if it has more than 2 emails then first email stored in "CompanyEmail1" otherwise from the 2nd one to the last one -
            will be stored in Email2
        """
        if len(company_email_sanitized) == 0:
            item['CompanyEmail1'] = ''.join(company_email_sanitized)
            item['Email2'] = ''.join(company_email_sanitized)
        elif len(i) == 1:
            item['CompanyEmail1'] = ''.join(company_email_sanitized)
            item['Email1'] = ''
        elif len(i) == 2:
            item['CompanyEmail1'] = company_email_sanitized[0]
            item['Email1'] = company_email_sanitized[1]
        elif len(i) > 2:
            item['CompanyEmail1'] = company_email_sanitized[0]
            item['Email2'] = ', '.join(company_email_sanitized[1:])

        else:
            item['CompanyEmail1'] = ''
            item['Email2'] = ''

        # item['Email2'] = item['CompanyEmail1']
        # emails
        # source url
        item['Source_Url_DomainSpider4'] = response.url
        yield item

    def find_name_in_email_match(self, fullname, all_emails):
        self.fullname1 = [i.strip().lower() for i in fullname.split(' ')]
        self.emails = [i.strip().lower() for i in all_emails.split(';')]
        self.emails_set = set(self.emails)
        self.emails = list(self.emails_set)
        # print(emails)
        self.emails_match_found = []
        for e in self.emails:
            for fname in self.fullname1:
                if fname in e:
                    self.emails_match_found.append(e)
        if emails_match_found:
            print("_____________________Match Found_____________{0}".format(
                self.emails_match_found))
        return self.emails_match_found

    # def find_name_in_email_match(self, fullname, all_emails):
    #     fullname1 = [i.strip().lower() for i in fullname.split(' ')]
    #     emails = [i.strip().lower() for i in all_emails.split(';')]
    #     emails_set = set(emails)
    #     emails = list(emails_set)
    #     # print(emails)
    #     emails_match_found = []
    #     for e in emails:
    #         for fname in fullname1:
    #             if fname in e:
    #                 emails_match_found.append(e)
    #     print("____________________________________Match Found_____________{0}".format(emails_match_found))
    #     return emails_match_found

    def unique(self):
        self.new = list(set(self.temp))
        return self.new

    # def genericClean(self, response):
    #     self.results = response.body
    #     for e in '''<KW> </KW> </a> <b> </b> </div> <em> </em> <p> </span>
    #                 <strong> </strong> <title> <wbr> </wbr>'''.split():
    #         self.results = self.results.replace(e, '')
    #     for e in '%2f %3a %3A %3C %3D & / : ; < = > \\'.split():
    #         self.results = self.results.replace(e, ' ')
