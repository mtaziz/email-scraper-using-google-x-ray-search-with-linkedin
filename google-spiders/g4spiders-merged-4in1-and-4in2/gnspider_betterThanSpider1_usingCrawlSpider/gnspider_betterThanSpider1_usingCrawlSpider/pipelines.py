# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
from scrapy.exceptions import DropItem
import requests
from scrapy.utils.project import get_project_settings
from scrapy import signals
from gnspider_betterThanSpider1_usingCrawlSpider.items import *
from scrapy.exporters import JsonLinesItemExporter
from scrapy.conf import settings
SETTINGS = get_project_settings
import csv
import re
from collections import OrderedDict
from pprint import pprint


class GoogleDupfilterPipeline(object):

    def __init__(self):
        self.s1_linkedin_url_with_valid_name_seen = set()
        self.s1_linkedin_url_seen = set()

    def process_item(self, item, spider):

        if item['s1_linkedin_url'] in self.s1_linkedin_url_seen:
            raise DropItem("_____Duplicates Removed: {0}_______".format(
                item['s1_linkedin_url']))

        # elif item['s1_linkedin_url'] is None:
        #     return
        else:
            self.s1_linkedin_url_seen.add(item['s1_linkedin_url'])
            return item

        # if item['s1_linkedin_url_with_valid_name'] == "":
        #     raise DropItem("_____Duplicates Removed: {0}_______".format(item['s1_linkedin_url_with_valid_name']))

        # else:
        #     self.s1_linkedin_url_with_valid_name_seen.add(item['s1_linkedin_url_with_valid_name'])
        #     return item


class GoogleDupfilterValidNamePipeline(object):

    def __init__(self):
        self.s1_linkedin_url_with_valid_name_seen = set()
        # self.s1_linkedin_url_seen = set()

    def process_item(self, item, spider):

        if item['s1_linkedin_url_with_valid_name'] == "":
            raise DropItem("_____Duplicates Removed: {0}_______".format(
                item['s1_linkedin_url_with_valid_name']))

        else:
            self.s1_linkedin_url_with_valid_name_seen.add(
                item['s1_linkedin_url_with_valid_name'])
            return item


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
        pprint("PhD or Ph.DTaken Off____________{0}".format(
            item['s1_phd_data']))
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
        if "/pulse/" in linkedin_url or "/learning/" in linkedin_url:
            item['s1_linkedin_url_with_valid_name'] = ''
        else:
            item['s1_linkedin_url_with_valid_name'] = linkedin_url
        name_in_linkedin_url_split = item['s1_linkedin_url_with_valid_name'].rsplit(
            '-', 1)[0]
        name_in_linkedin_url_split = (
            ' '.join((name_in_linkedin_url_split.split('/in/')[-1].split('-')))).title()
        item['s1_name_in_linkedin_url'] = name_in_linkedin_url_split
        name_matched = re.search(
            item['s1_name_in_linkedin_url'], item['s1_name_in_title'], re.IGNORECASE)
        if name_matched:
            item['s1_name_in_title_and_linkedin_url'] = name_matched.group(0)
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
            item['s1_name_in_title_and_linkedin_url'] = item['s1_name_in_title_and_linkedin_url'] = name_matched.group(
                0)
        return item
