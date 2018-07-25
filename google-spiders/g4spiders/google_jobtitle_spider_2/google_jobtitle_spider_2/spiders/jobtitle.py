# -*- coding: utf-8 -*-
import scrapy

# from ..items import GoogleSpiderItem
from ..items import GoogleDetailedSpiderItem
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


class GoogleDetailedSpider(scrapy.Spider):
    # timestamp = datetime.now().strftime('%Y-%b-%d')
    timestamp = datetime.now().strftime('%Y-%b-%d_%H%M%S')
    customs_settings = {}
    # name = 'google_spider'
    name = 'jobtitle'
    allowed_domains = ['google.com', 'linkedin.com']
    # Ignore the HTTP status code
    handle_httpstatus_list = [404, 302, 301, 429, 503]

    # NOTE: Please provide the Crawlera API Key
    custom_settings = {
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_USER': '',
        'CRALERA_PRESERVE_DELAY': True,
        'DOWNLOAD_DELAY': 15,
        'FEED_URI': "export/{0}_{1}.csv".format(name, timestamp)
    }

    g_keyword_list = ['"Red blood cell" -jobs -topic site:linkedin.com']
    # start_urls = ['https://www.google.com/search?site=&source=hp&q=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&oq=%22Red+blood+cell%22+-jobs+-topic+site%3Alinkedin.com&gs_l=hp.3...970.970.0.1720.1.1.0.0.0.0.138.138.0j1.1.0....0...1.1.64.hp..0.0.0.rlmDAXb2pVo']
    google_query_example_url = "https://www.google.com/#q=site:linkedin.com/in/floralicia+%22Current%22+OR+%22Previous%22+OR+%22Education%22"
    # 'https://www.google.com/search?q=site:linkedin.com/in/floralicia+%22Current%22+OR+%22Previous%22+OR+%22Education%22&cad=h'

    # NOTE: List of google operators to be using to form the "Google Query URLs"
    google_search_url_0 = 'https://www.google.com/search?q='
    gs_operator_in_site_1 = 'site'
    gs_operator_linkedin_url_2 = 'linkedin.com/in/floralicia'
    gs_operator_current_3 = 'Current'
    gs_operator_or_4 = 'OR'
    gs_operator_previous_5 = 'Previous'
    gs_operator_or_6 = 'OR'
    gs_operator_edu_7 = 'Education'
    linkedin_url = 'https://www.linkedin.com/in/stacy-martin-12329736'

    # Test linkedin urls before we run the final spider which will read the list of urls from a csv file stored in "import" project directory
    # test_linkedin_urls_list = [
    #                     'https://www.linkedin.com/in/david-kuhrt-0487a0a',
    #                     'https://uk.linkedin.com/in/alex-crick-9b2b14108',
    #                     'https://www.linkedin.com/in/kathleen-abadie-7896515a'
    #                     'https://www.linkedin.com/learning/maya-tips-tricks-techniques/simulate-red-blood-cells-in-an-artery',
    #                     'https://www.linkedin.com/in/ruipeng-mu-b03a6596',
    #                     'https://au.linkedin.com/in/peter-klinken-2b73577a',
    #                     'https://www.linkedin.com/in/tonychobot',
    #                     'https://ch.linkedin.com/in/olivier-rubin-a5949b43',
    #                     'https://nz.linkedin.com/in/stephenduffull'
    #                     ]

    # 1 Read LinkedInUrl from CSV file
    test_linkedin_urls_list = []
    file_import_directory = 'import/'
    # linkedin_urls_file_name = 'test_20urls.csv'
    # test_linkedin_urls_615.csv
    linkedin_urls_file_name = 'test_linkedin_urls_615.csv'
    input_file_path = "{0}{1}".format(
        file_import_directory, linkedin_urls_file_name)
    with open(input_file_path, 'rb') as file_input:
        csv_reader = csv.reader(file_input, delimiter=',')
        for url in csv_reader:
            test_linkedin_urls_list.append(url[1])
    # pprint(len(test_linkedin_urls))

    # Make sure all the  URLs are unique
    test_linkedin_urls_set = set(test_linkedin_urls_list)
    # pprint(len(test_linkedin_urls_set))

    # Converting set back to the list
    test_linkedin_urls_unique_list = list(test_linkedin_urls_set)
    # pprint(len(test_linkedin_urls_unique))
    # Remove any empty element from the list
    # test_linkedin_urls = filter(None, test_linkedin_urls)
    # Google queries acceptable example url[i.e., domain+name] refers to "uk.linkedin.com/in/alex-crick",
    # to comply with this we have to remove additonal "https://",  "https://www."" and "www.",

    linkedin_operator_based_urls_list = []
    query_qualified_urls_list = []
    for test_linkedin_url in test_linkedin_urls_unique_list:
        query_qualified_urls = test_linkedin_url.replace(
            'https://', '').replace('https://www.', '').replace('www.', '')
        query_qualified_urls_list.append(query_qualified_urls)

    # The url contains blog link which we will ignore, in order to keep only people's linkedin profile URLs
    # Make a list which will only have people's url.
    extracted_urls_with_only_name_list = []
    for query_qualified_url in query_qualified_urls_list:
        if "/in/" in query_qualified_url:
            extracted_urls_with_only_name_list.append(
                query_qualified_url.rsplit('-', 1)[0])

    # pprint(extracted_urls_with_only_name_list)
    pprint(len(linkedin_operator_based_urls_list))
    # example_extracted_linkedin_url = ['linkedin.com/in/david-kuhrt',
    #                          'uk.linkedin.com/in/alex-crick',
    #                          'linkedin.com/in/kathleen-abadie',
    #                          'linkedin.com/in/ruipeng-mu',
    #                          'au.linkedin.com/in/peter-klinken',
    #                          'linkedin.com/in/tonychobot',
    #                          'ch.linkedin.com/in/olivier-rubin',
    #                          'nz.linkedin.com/in/stephenduffull']

    # pprint(linkedin_operator_based_urls_list)
    # Get the list of Google queries urls using above filtered URL "Google Queries URLs formed"
    google_queries_urls_list = []
    for extracted_url_with_only_name in extracted_urls_with_only_name_list:
        google_search_query = "{0}{1}:{2}+%22{3}%22+{4}+%22{5}%22+{6}+%22{7}%22".format(google_search_url_0,
                                                                                        gs_operator_in_site_1,
                                                                                        extracted_url_with_only_name,
                                                                                        gs_operator_current_3,
                                                                                        gs_operator_or_4,
                                                                                        gs_operator_previous_5,
                                                                                        gs_operator_or_4,
                                                                                        gs_operator_edu_7)
        google_queries_urls_list.append(google_search_query)

    # Assign Google Queries to the Scrapy "start_urls" list.
    start_urls_list = google_queries_urls_list
    start_urls = start_urls_list
    # start_urls = ['https://www.google.com/search?q=site:linkedin.com/in/marisollimauro+%22Current%22+OR+%22Previous%22+OR+%22Education%22',\
    #             'https://www.google.com/search?q=site:linkedin.com/in/xavier-haskins+%22Current%22+OR+%22Previous%22+OR+%22Education%22',\
    #             'https://www.google.com/search?q=site:linkedin.com/in/xiaosonghuang+%22Current%22+OR+%22Previous%22+OR+%22Education%22',\
    #             'https://www.google.com/search?q=site:linkedin.com/in/mojtaba-taherisadr+%22Current%22+OR+%22Previous%22+OR+%22Education%22',\
    #             'https://www.google.com/search?q=site:linkedin.com/in/amanda-sivek+%22Current%22+OR+%22Previous%22+OR+%22Education%22']

    def parse(self, response):

        # item = GoogleSpiderItem()
        # item = GoogleDetailedSpiderItem()

        item = GoogleDetailedSpiderItem()
        address_and_job_title = response.xpath(
            'normalize-space(//div[@class="slp f"]/text())').extract_first()
        item['RawData_Address_JobTitle'] = address_and_job_title.encode(
            'ascii', 'ignore').strip()

        # print("{0}________".format(address_and_job_title))
        # pprint(address_and_job_title)
        # if address_and_job_title:
        # "Saint Louis, Missouri - MD/PhD candidate at Washington University School of Medicine in St. Louis"
        # "Phoenix, Arizona Area - Special Education Teacher at Scottsdale Unified School District - Wilson Language Training"
        address_and_job_title = address_and_job_title.strip().encode('ascii', 'ignore')
        if "-" in address_and_job_title:
            address_and_job_title_list = address_and_job_title.split('-')
            if len(address_and_job_title_list) == 2:
                item['Address'] = address_and_job_title_list[0].strip()
                item['JobTitle'] = address_and_job_title_list[1].strip()
                job_title = item['JobTitle']
                # company = item['Company']
                if " at " in job_title:
                    job_title_part1 = job_title.split(' at ')[0].strip()
                    item['JobTitle'] = job_title_part1
                    item['Company'] = job_title.split(' at ')[-1].strip()
                else:
                    item['JobTitle'] = job_title
                    item['Company'] = ''
            elif len(address_and_job_title_list) == 3:
                item['Address'] = address_and_job_title_list[0].strip()
                job_title = address_and_job_title_list[1].strip()
                item['JobTitle'] = job_title
                item['Company'] = address_and_job_title_list[2].strip()

                # job_title = item['JobTitle']
                company_name = item['Company']
                if " at " in job_title:
                    job_title_part1 = job_title.split(' at ')[0].strip()
                    item['JobTitle'] = job_title_part1
                    if not company_name:
                        item['Company'] = job_title.split(
                            ' at ')[-1].strip() + " " + company_name
                    else:
                        item['Company'] = company_name
                else:
                    item['JobTitle'] = job_title
                    item['Company'] = company_name

                # company_name = item['Company']
                # if not item['Company']:
                #     item['Company'] = job_title.split(' at ')[-1].strip()
                # else:
                #     item['Company'] = company_name
            # else:
                # item['Address'] = address_and_job_title
        # else:
        #     item['Address'] = address_and_job_title
        #     item['Company'] = ''

        # job_title = item['JobTitle']
        # company = item['Company']
        # if " at " in job_title:
        #     job_title_part1 = job_title.split(' at ')[0].strip()
        #     item['JobTitle'] = job_title_part1
        #     if not item['Company']:
        #         item['Company'] = job_title.split(' at ')[-1].strip()
        #     else:
        #         item['Company'] = company
        # else:
        #     item['JobTitle'] = job_title
        # if not item['Company']:
        # address_and_job_title = address_and_job_title.encode('utf-8')
        # address = address_and_job_title.split('-')[0]
        # item['Address'] = address

        ###
        # if item['Address']:
        #     inspect_response(response, self)
        # employment_history = map(unicode.strip, response.xpath('//span[@class="st"]/text()').extract())
        # Using Normalize (normalize-space)
        employment_history = response.xpath(
            '//span[@class="st"]/text()').extract()
        item['RawData_Employment_History'] = ' '.join([j.strip() for j in [i.encode(
            'ascii', 'ignore') for i in employment_history]]).replace('...', ' ')
        # if employment_history:
        # if len(employment_history)== 3:
        try:
            current_employment = (employment_history[0].encode(
                'ascii', 'ignore')).replace('.', '').replace(',', '').strip()
            item['Current_Company'] = current_employment
            # previous_employment = employment_history[1]
            item['Previous_Company'] = employment_history[1].replace(
                '.', '').replace(',', '').strip()
            # education = employment_history[2]
            education = employment_history[2].split('.')[0]
            item['Education'] = education.strip()
        except:
            pass
        # name_data = response.xpath('//h3[@class="r"]/a/text()').extract()
        # name_data = ''.join(name_data)
        #  = name_data.split('at')[0]
        # Name data
        # fullname_raw_data = map(unicode.strip, response.xpath('//h3[@class="r"]/a/text()').extract())
        fullname_raw_data = response.xpath(
            'normalize-space(//h3[@class="r"]/a/text())').extract()
        item['RawData_FullName'] = ' '.join([j.strip() for j in [i.encode(
            'ascii', 'ignore') for i in fullname_raw_data]]).replace('...', ' ')
        # for i in fullname_raw_data:
        #     i.encode('ascii', 'ignore')
        # ''.join(map(unicode.strip, response.xpath('//h3[@class="r"]/a/text()').extract())).split('|')[0].strip()
        # if fullname_raw_data:
        # try:
        # if len(fullname_raw_data) == 2:
        extracted_fullname = ''.join(fullname_raw_data).split('|')[
            0].strip().encode('ascii', 'ignore')
        # print("________________________{0}".format(item['Company']))
        # item['Company'] = item['Company'].strip()
        # if item['Company'] in extracted_fullname:
        #     item['FullName'] = extracted_fullname
        # else:
        #     item['FullName'] = extracted_fullname
        # company_name = item['Company']
        if " at " in extracted_fullname:
            item['FullName'] = extracted_fullname.split(" at ")[0]
            # if not item['Company']:
            # item['Company'] = extracted_fullname.split(" at ")[-1]
        else:
            item['FullName'] = extracted_fullname
            # item['Company'] = company_name

        extracted_fullname = item['FullName']
        extracted_fullname_list = extracted_fullname.split(' ')
        if len(extracted_fullname_list) == 2:
            item['FirstName'] = extracted_fullname_list[0]
            item['LastName'] = extracted_fullname_list[-1]
        elif len(extracted_fullname_list) == 3:
            item['FirstName'] = extracted_fullname_list[0]
            item['LastName'] = ' '.join(extracted_fullname_list[1:])
        else:
            item['FirstName'] = extracted_fullname
        firstname = item['FirstName']

        if "on LinkedIn" in firstname:
            item['FirstName'] = firstname.replace('on LinkedIn', '')
        else:
            item['FirstName'] = firstname
        item['LinkedInUrl'] = response.xpath(
            'normalize-space(//cite[@class="_Rm"]/text())').extract_first()
        item['Source'] = response.url
        # item['Address'] = response.xpath('//div[contains(@class, "slp f")]text()').extract()
        # item['JobTitle'] = response.xpath('//span[contains(@class, "st")]').extract()
        # item['']
        yield item
