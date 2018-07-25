# -*- coding: utf-8 -*-


import scrapy
from ..items import GoogleNameSpider1Item
from ..items import GoogleJobTitleSpider2Item
from ..items import GoogleCompanyDomainSpider3Item
from ..items import GoogleEmailSpider4Item

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


#Google search results information#############################################
# 1.1 No of google results in a single page
GS_RESULTS_NUM = 100

# 1.2 at which page it should start off
GS_RESULTS_START = 0

# 1.3
# :param - how many results should be returned by a search
GS_RESULTS_STEP = 100

# 1.4
GS_RESULTS_PAGES_NUM = 10

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
CRAWLERA_USER_API_KEY = ''


class GoogleEmailSpider(Spider):
    # timestamp = datetime.now().strftime('%Y-%b-%d')
    timestamp = datetime.now().strftime('%Y-%b-%d_%H%M')
    customs_settings = {}
    # name = 'google_spider'
    name = 'emailspider4in1'
    allowed_domains = ['google.com', 'linkedin.com']
    # Ignore the HTTP status code
    handle_httpstatus_list = [404, 302, 301, 429, 503]
    custom_settings = {
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_USER': CRAWLERA_USER_API_KEY,
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
        """
            Goolge Name Spider1 (s1)
        """
        item = GoogleNameSpider1Item()
        divs = response.xpath('//div[contains(@class, "srg")]/div[@class="g"]')
        # s1_linkedin_urls = []
        for div in divs:

            s1_title = div.xpath(
                './/div[@class="rc"]/h3/a/text()').extract_first()
            s1_linkedin_url = div.xpath(
                './/div[@class="rc"]/h3/a/@href').extract_first()
            s1_description = div.xpath(
                './/span[@class="st"]//text()').extract()
            item['s1_title'] = s1_title
            item['s1_linkedin_url'] = s1_linkedin_url
            # s2_linkedin_operator_urls = []
            # for s1_linkedin_url in s1_linkedin_urls:
            if "/in/" in s1_linkedin_url:
                s1_linkedin_url.replace(
                    'https://', '').replace('https://www.', '').replace('www.', '')

            item['s1_linkedin_url'] = s1_linkedin_url

            item['s1_description'] = s1_description
            # s1_title = item['s1_title']
            # s1_linkedin_url = item['s1_linkedin_url']
            # s1_description = item['s1_description']
            # s1_linkedin_urls.append(s1_linkedin_url)
            # yield item

            # s1_linkedin_urls = list(set(s1_linkedin_urls))
            # print "__________________________________we are in parse function"
            # pprint(s1_linkedin_urls)

            #Spider2: Scrape Job Title#############################################################
            s2_gs_url = 'https://www.google.com/search?q='
            s2_gs_operator_in_site_1 = 'site'
            # s2_gs_operator_linkedin_url_2 = 'linkedin.com/in/floralicia'
            s2_gs_operator_current_3 = 'Current'
            s2_gs_operator_or_4 = 'OR'
            s2_gs_operator_previous_5 = 'Previous'
            # s2_gs_operator_or_6 = 'OR'
            s2_gs_operator_edu_7 = 'Education'
            # s2_gs_linkedin_url = 'https://www.linkedin.com/in/stacy-martin-12329736'
            item['s1_name_gurl'] = response.url
            # google_queries_urls= []
            # for url_name in s2_linkedin_operator_urls:
            gs_query_url = "{0}{1}:{2}+%22{3}%22+{4}+%22{5}%22+{6}+%22{7}%22".format(s2_gs_url,
                                                                                     s2_gs_operator_in_site_1,
                                                                                     item['s1_linkedin_url'],
                                                                                     s2_gs_operator_current_3,
                                                                                     s2_gs_operator_or_4,
                                                                                     s2_gs_operator_previous_5,
                                                                                     s2_gs_operator_or_4,
                                                                                     s2_gs_operator_edu_7)
            # google_queries_urls.append(google_search_query)
            # pprint(google_queries_urls)
            # for q_url in google_queries_urls:
            yield Request(url=gs_query_url, callback=self.parse_jobtitle_s2, meta={'item': item})

    def parse_jobtitle_s2(self, response):
        """ s2:
            Extract Job title information the raw data collected or scraped form google search results
        """

        item = response.meta['item']
        s2_address_jobtitle = response.xpath(
            'normalize-space(//div[@class="slp f"]/text())').extract_first()
        item['RawData_Address_JobTitle'] = s2_address_jobtitle.encode(
            'ascii', 'ignore').strip()

        # s2.1: spider2 address and job title extracted from the raw data found in  item['RawData_Address_JobTitle']
        s2_address_jobtitle = s2_address_jobtitle.strip().encode('ascii', 'ignore')
        if "-" in s2_address_jobtitle:
            s2_address_jobtitle_list = s2_address_jobtitle.split('-')
            if len(s2_address_jobtitle_list) == 2:
                item['Address'] = s2_address_jobtitle_list[0].strip()
                item['JobTitle'] = s2_address_jobtitle_list[1].strip()
                jobtitle = item['JobTitle']
                if " at " in jobtitle:
                    jobtitle_part1 = jobtitle.split(' at ')[0].strip()
                    item['JobTitle'] = jobtitle_part1
                    item['Company'] = jobtitle.split(' at ')[-1].strip()
                else:
                    item['JobTitle'] = jobtitle
                    item['Company'] = ''

            elif len(s2_address_jobtitle_list) == 3:
                item['Address'] = s2_address_jobtitle_list[0].strip()
                jobtitle = s2_address_jobtitle_list[1].strip()
                item['JobTitle'] = jobtitle
                item['Company'] = s2_address_jobtitle_list[2].strip()

                # jobtitle = item['JobTitle']
                company_name = item['Company']
                if " at " in jobtitle:
                    jobtitle_part1 = jobtitle.split(' at ')[0].strip()
                    item['JobTitle'] = jobtitle_part1
                    if not company_name:
                        item['Company'] = jobtitle.split(
                            ' at ')[-1].strip() + " " + company_name
                    else:
                        item['Company'] = company_name
                else:
                    item['JobTitle'] = jobtitle
                    item['Company'] = company_name

                company_name = item['Company']
                if not item['Company']:
                    item['Company'] = jobtitle.split(' at ')[-1].strip()
                else:
                    item['Company'] = company_name
            else:
                item['Address'] = s2_address_jobtitle
        else:
            item['Address'] = s2_address_jobtitle
            item['Company'] = ''

        # s2.2 Employment history, from employment history current company , previous company and education information extracted
        employment_history = response.xpath(
            '//span[@class="st"]/text()').extract()
        item['RawData_Employment_History'] = ' '.join([j.strip() for j in [i.encode(
            'ascii', 'ignore') for i in employment_history]]).replace('...', ' ')

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

        # s2.3
        s2_fulln_raw_data = response.xpath(
            'normalize-space(//h3[@class="r"]/a/text())').extract()
        item['RawData_FullName'] = ' '.join([j.strip() for j in [i.encode(
            'ascii', 'ignore') for i in s2_fulln_raw_data]]).replace('...', ' ')

        # s2.4: FullName data extracted from extracted fullname data
        s2_extracted_fulln = ''.join(s2_fulln_raw_data).split('|')[
            0].strip().encode('ascii', 'ignore')
        if " at " in s2_extracted_fulln:
            item['FullName'] = s2_extracted_fulln.split(" at ")[0]
        else:
            item['FullName'] = s2_extracted_fulln

        # s2.5: FirstName and LastName extracted from s2_extracted_fulln
        s2_extracted_fulln = item['FullName']
        s2_extracted_fulln_list = s2_extracted_fulln.split(' ')

        if len(s2_extracted_fulln_list) == 2:
            item['FirstName'] = s2_extracted_fulln_list[0]
            item['LastName'] = s2_extracted_fulln_list[-1]

        elif len(s2_extracted_fulln_list) == 3:
            item['FirstName'] = s2_extracted_fulln_list[0]
            item['LastName'] = ' '.join(s2_extracted_fulln_list[1:])
        else:
            item['FirstName'] = s2_extracted_fulln

        # s2.6: first name sanitized
        firstname = item['FirstName']
        if "on LinkedIn" in firstname:
            item['FirstName'] = firstname.replace('on LinkedIn', '')
        else:
            item['FirstName'] = firstname

        item['LinkedInUrl'] = response.xpath(
            'normalize-space(//cite[@class="_Rm"]/text())').extract_first()
        item['s3_jobtitle_url'] = response.url
        # s3_gurl = "https://www.google.com/search?q=Texas+A%26M+University&oq=Texas+A%26M+University"
        s3_query_string = {"google_base_url": "https://www.google.com/search?q=",
                           "JobTitle": "", "Company": "", "location": ""}
        s3_link = "{0}{1}&ie=utf-8&oe=utf-8".format(
            s3_query_string['google_base_url'], item['Current_Company'])

        # Google job title search URL
        item['s2_jobtitle_gurl'] = response.url

        yield Request(
            url=s3_link,
            callback=self.parse_company_domain_s3,
            method="GET",
            # meta={'item': item, 'fulln': fulln}
            meta={'item': item}
        )

    def parse_company_domain_s3(self, response):

        item = response.meta['item']
        s3_company_name_data = response.xpath(
            '//div[@class="rc"]/h3/a/text()').extract_first()
        item['CompanyName2'] = s3_company_name_data

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
        # s3_company_domain = item['CompanyDomain']
        # item['Source_Url_DomainSpider3'] = response.url
        s4_no_of_pages = 100
        s4_start_page = 0
        s4_google_100pages_base_url = 'https://www.google.com/search?num={0}&start={1}&hl=en&q='.format(
            s4_no_of_pages, s4_start_page)
        print "\n_______Crawling Company Domain__________________________________________________\n"
        pprint(item)

        # Google Source URL
        item['s3_domain_gurl'] = response.url

        if item['FullName'] and item['CompanyDomain']:
            s4_link = '{0}%22{1}%22+%22%40{2}%22&ie=utf-8&oe=utf-8'.format(s4_google_100pages_base_url,
                                                                           item['FullName'].replace(
                                                                               ' ', '+'),
                                                                           item['CompanyDomain'])
            yield Request(
                url=s4_link,
                callback=self.parse_email_s4,
                method="GET",
                # meta={'item': item, 's3_fullname': s3_fullname, 's3_company_domain': s3_company_domain}
                meta={'item': item}
            )

    def parse_email_s4(self, response):
        item = response.meta['item']
        # item = GoogleEmailSpider4Item()
        results = response.body
        for e in '''<KW> </KW> </a> <b> </b> </div> <em> </em> <p> </span>
                    <strong> </strong> <title> <wbr> </wbr>'''.split():
            results = results.replace(e, '')
        for e in '%2f %3a %3A %3C +@ 22@ 2522@ %2B %3D & / : ; < = > \\'.split():
            results = results.replace(e, ' ')
        fullname_plus_removed = item['FullName'].replace('+', ' ')
        item['FullName'] = fullname_plus_removed

        # get the domain specific emails
        # reg_emails_domain_specific = re.compile('[a-zA-Z0-9.\-_+#~!$&\',;=:]+' +'@' +'[a-zA-Z0-9.-]*' +"mdanderson.org")
        emails_domain_specific_plus_general = []
        reg_domain_specific = re.compile(
            '[a-zA-Z0-9.\-_+#~!$&\',;=:]+' + '@' + '[a-zA-Z0-9.-]*' + item['CompanyDomain'])
        emails_domain_specific = reg_domain_specific.findall(results)
        emails_domain_specific = [i.strip().lower()
                                  for i in emails_domain_specific]
        emails_domain_specific = list(set(emails_domain_specific))

        # for eds in emails_domain_specific:
        #     if "+@" or "22@" or "2522@" in eds:
        #         emails_domain_specific.remove(eds)
        emails_domain_specific_plus_general.extend(emails_domain_specific)

        # emails_domain_specific = ', '.join(list(set(emails_domain_specific)))
        # for emails_domain_sp in emails_domain_specific:
        item['Email1_Raw'] = ', '.join(emails_domain_specific)

        # get the  "general domains" based emails (like, gmail.com or yahoo.com or any other domains)
        reg_domain_general = re.compile(
            '[a-zA-Z0-9.\-_+#~!$&\',;=:]+' + '@' + '[a-zA-Z0-9.-]*')
        emails_domain_general = reg_domain_general.findall(results)
        emails_domain_general = [i.strip().lower()
                                 for i in emails_domain_general]
        emails_domain_general = list(set(emails_domain_general))
        # for eds in emails_domain_general:
        #     if "+@" or "22@" or "2522@" or "linkedin" in eds:
        #         edg_rm = emails_domain_general.remove(eds)
        emails_domain_specific_plus_general.extend(emails_domain_general)
        item['Email2_Raw'] = ', '.join(list(set(emails_domain_general)))

        emails_domain_specific_plus_general = list(
            set(emails_domain_specific_plus_general))
        # emails_domain_specific_plus_general = "{0}; {0}".format(emails_domain_specific, emails_domain_general)
        company_email_sanitized = self.find_name_in_email_match(
            item['FullName'], emails_domain_specific_plus_general)
        company_email_sanitized = filter(None, company_email_sanitized)
        company_email_sanitized = list(set(company_email_sanitized))

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
        elif len(company_email_sanitized) == 1:
            item['CompanyEmail1'] = ''.join(company_email_sanitized)
            item['Email1'] = ''
        elif len(company_email_sanitized) == 2:
            item['CompanyEmail1'] = company_email_sanitized[0]
            item['Email1'] = company_email_sanitized[1]
        elif len(company_email_sanitized) > 2:
            item['CompanyEmail1'] = company_email_sanitized[0]
            item['Email2'] = ', '.join(company_email_sanitized[1:])

        else:
            item['CompanyEmail1'] = ''
            item['Email2'] = ''

        item['s4_email_gurl'] = response.url
        return item

    def find_name_in_email_match(self, fullname, all_emails):
        self.fullname1 = [i.strip().lower() for i in fullname.split(' ')]
        self.emails = all_emails
        # self.emails_set = set(self.emails)
        # self.emails = list(self.emails_set)
        # print(emails)
        self.emails_match_found = []
        for e in self.emails:
            for fname in self.fullname1:
                if fname in e:
                    self.emails_match_found.append(e)
        if self.emails_match_found:
            print("_____________________Match Found_____________{0}".format(
                self.emails_match_found))
        return self.emails_match_found
