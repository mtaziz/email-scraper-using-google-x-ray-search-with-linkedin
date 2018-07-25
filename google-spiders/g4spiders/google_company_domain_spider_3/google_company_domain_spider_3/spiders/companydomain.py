# -*- coding: utf-8 -*-
import scrapy

# from ..items import GoogleSpiderItem
# from ..items import GoogleDetailedSpiderItem
# from ..items import GoogleDomainItem
from ..items import GoogleCompanyDomainSpiderItem
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
INPUT_FILE_NAME = 'google_jobtitle_spider_2_27July2017.csv'
INPUT_FILE_PATH = '{0}/{1}'.format(INPUT_FILE_DIR, INPUT_FILE_NAME)

OUTPUT_FILE_DIR = 'export'
OUTPUT_FILE_NAME = ''
OUTPUT_FILE_PATH = '{0}/{1}'.format(OUTPUT_FILE_DIR, OUTPUT_FILE_NAME)


class GoogleCompanyDomainSpider(scrapy.Spider):

    # timestamp = datetime.now().strftime('%Y-%b-%d')
    timestamp = datetime.now().strftime('%Y-%b-%d_%H%M%S')
    customs_settings = {}

    # name = 'google_spider'
    name = 'companydomain'

    # allowed_domains = ['google.com', 'linkedin.com']
    # Ignore the HTTP status code
    handle_httpstatus_list = [404, 302, 301, 429, 503]

    # settings parameters in settings.py overriden by using custom_settings
    custom_settings = {
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_USER': '3e1257a319944e91b9f74c642c71e432',
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

    test_list_of_company = """
                            MD Anderson Cancer Center
                            Brown University
                            Sinai Hospital of Baltimore
                            Texas A&M University
                            Biology mayo de 2010 This publication was selected as Cover Picture for the Journal Autores: Ada Repiso Villanueva; Amy L Brittle; Jose Casal
                            (Owner) Hazardous
                            Alkermes; Outdoor Discovery Adventure Company; Dunnes Stores  Animal Welfare;
                            University of Pittsburgh: Sluis-Cremer Lab
                            Weizmann Institute of Science; Davidson institute of science
                            Blue Cross NC
                            University of Kentucky
                            Moderna Therapeutics; Merck; Pfizer
                            EIP
                            The disclosed invention holds distinct advantages over the
                            Wilko
                            Northeastern University; Arizona State University; University of Pennsylvania
                            Swiss-American Contract Development and Manufacturing
                            United States Army Institute of Surgical Research Recommendations
                            """
    # locompany_list = filter(None, test_list_of_company.split('\n'))
    # test_start_urls_list = []
    gurl = "https://www.google.com/search?q=Texas+A%26M+University&oq=Texas+A%26M+University"
    query_string = {"google_base_url": "https://www.google.com/search?q=",
                    "JobTitle": "", "Company": "", "location": ""}

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
            for row in csv_reader:
                # firstname = row['FirstName']
                # lastname = row['LastName']
                # fullname = row['FullName']

                # all the fields will be passed to the new csv exported into export directory
                currentcompany = row['Current_Company']
                title = row['Title']
                firstname = row['FirstName']
                lastname = row['LastName']
                fullname = row['FullName']
                suffix = row['Suffix']
                jobtitle = row['JobTitle']
                company = row['Company']
                current_company = row['Current_Company']
                previous_company = row['Previous_Company']
                education = row['Education']
                companyemail1 = row['CompanyEmail1']
                email2 = row['Email2']
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

                meta_data_dict = {
                    'title': title,
                    'firstname': firstname,
                    'lastname': lastname,
                    'fullname': fullname,
                    'suffix': suffix,
                    'jobtitle': jobtitle,
                    'company': company,
                    'current_company': current_company,
                    'previous_company': previous_company,
                    'education': education,
                    'companyemail1': companyemail1,
                    'email2': email2,
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

                # location_plus = '+'.join(loc.split(' '))
                link = "{0}{1}{2}{3}&ie=utf-8&oe=utf-8".format(self.query_string['google_base_url'],
                                                               self.query_string['FullName'],
                                                               self.query_string['JobTitle'],
                                                               row['Current_Company'],
                                                               self.query_string['JobTitle'])
                yield Request(
                    url=link,
                    callback=self.parse,
                    method="GET",
                    meta=meta_data_dict
                )
        # start_urls = start_urls_list
        # start_urls = start_urls_list[:10]

    def parse(self, response):
        """
            This spider scrapes the domain name by using "comany information obtained from google_spider2"
        """

        # item = GoogleSpiderItem()
        # item = GoogleDetailedSpiderItem()
        # item = GoogleDetailedSpiderItem()
        item = GoogleCompanyDomainSpiderItem()

        # Below fields are imported from the "input_file"/obtained from spider2
        item['Title'] = response.meta['title']
        item['FirstName'] = response.meta['firstname']
        item['LastName'] = response.meta['lastname']
        item['FullName'] = response.meta['fullname']
        item['Suffix'] = response.meta['suffix']
        item['JobTitle'] = response.meta['jobtitle']
        item['Company'] = response.meta['company']
        item['Current_Company'] = response.meta['current_company']
        item['Previous_Company'] = response.meta['previous_company']
        item['Education'] = response.meta['education']
        item['CompanyEmail1'] = response.meta['companyemail1']
        item['Email2'] = response.meta['email2']
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

        company_name_data = response.xpath(
            '//div[@class="rc"]/h3/a/text()').extract_first()
        item['CompanyName2'] = company_name_data

        # Company Website Address
        company_website_data = response.xpath(
            '//div[@class="rc"]/h3/a/@href').extract_first()
        item['CompanyWebsite'] = company_website_data

        # Company Domain
        if company_website_data:
            try:
                network_location_part = urlparse(company_website_data).netloc
                item['CompanyDomain'] = network_location_part.replace(
                    'www.', '')
            except:
                pass
        else:
            return

        # source url
        item['Source_Url_DomainSpider3'] = response.url
        yield item
