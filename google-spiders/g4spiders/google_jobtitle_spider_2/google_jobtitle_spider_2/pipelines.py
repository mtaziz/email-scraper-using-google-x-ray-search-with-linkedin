# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pprint import pprint
import sys
import csv
import re
from collections import OrderedDict
from scrapy.exceptions import DropItem
import requests
from scrapy.utils.project import get_project_settings
from scrapy import signals
from ..items import *
from scrapy.exporters import JsonLinesItemExporter
from scrapy.conf import settings
SETTINGS = get_project_settings


class GoogleSpiderPipeline(object):

    def process_item(self, item, spider):

        # if item['G_Title']:
        google_title = item['G_Title']
        # name_list = []
        # phd_info_list = []
        company = re.search(r'(?<= at )(.*)', google_title)
        if company:
            item['G_WorkAt'] = company.group(0)
        else:
            item['G_WorkAt'] = ''
        address = re.search(r"\((.*?)\)", google_title)
        if address:
            item['G_Address'] = address.group(0)
        else:
            item['G_Address'] = ''

        # phd_data = 'Elena Kostova, PhD | Professioneel profiel - LinkedIn'
        phd_info = re.search(r'(\bPhD\b)|(Ph.D)', google_title)
        if phd_info:
            item['G_PhD'] = phd_info.group(0)
            # phd_info_list.append(phd)
        else:
            item['G_PhD'] = ''
            # phd_info_list.append(phd)

        title_clean = google_title\
            .replace(item['G_Address'], '')\
            .replace('at {0}'.format(company), '')\
            .replace('(', '').replace(')', '')\
            .replace('| Professional Profile - LinkedIn', '')\
            .replace(' | LinkedIn', '').replace(' on LinkedIn', '')\
            .replace('{}'.format(item['G_PhD']), '')
        title_clean = title_clean.split('|')[0]
        title_clean = title_clean.split(',')[0]
        item['G_Name_In_Title'] = title_clean
        # item['G_PhD'] = phd
        pprint("PhD or Ph.DTaken Off____________{0}".format(item['G_PhD']))
        # else:
        #     pass
        # if item['G_Title_Url']:
        #   item['G_LinkedIn_Url'] = item['G_Title_Url']
        # else:
        #   item['G_LinkedIn_Url'] = ''
        # G_Name_In_LinkedIn_Url
        # G_Name_In_Title
        # if item['G_LinkedIn_Url']:
        linkedin_url = item['G_LinkedIn_Url']
        if "/pulse/" in linkedin_url or "/learning/" in linkedin_url:
            item['G_LinkedIn_Url_For_Name'] = ''
        else:
            item['G_LinkedIn_Url_For_Name'] = linkedin_url
        name_in_linkedin_url_split = item['G_LinkedIn_Url_For_Name'].rsplit(
            '-', 1)[0]
        name_in_linkedin_url_split = (
            ' '.join((name_in_linkedin_url_split.split('/in/')[-1].split('-')))).title()
        item['G_Name_In_LinkedIn_Url'] = name_in_linkedin_url_split
        name_matched = re.search(
            item['G_Name_In_LinkedIn_Url'], item['G_Name_In_Title'], re.IGNORECASE)
        if name_matched:
            item['G_Matched_Name'] = name_matched.group(0)
            pprint("Name Found: \n {0} \n".format(name_matched))
        else:
            item['G_Matched_Name'] = ''
        if not item['G_Matched_Name']:
            name_string_in_title = item['G_Name_In_Title']
            name_string_in_title = name_string_in_title.split(' ')
            d = re.findall(r"(?=(" + '|'.join(name_string_in_title) + r"))",
                           item['G_Name_In_LinkedIn_Url'], re.IGNORECASE)
            item['G_Matched_Name'] = ' '.join(filter(None, d)).title()
        else:
            item['G_Matched_Name'] = item['G_Matched_Name'] = name_matched.group(
                0)

            # if not item['G_Matched_Name']:
            #     # name_in_single_word = re.search(item['G_Name_In_LinkedIn_Url'], item['G_Name_In_Title'], re.IGNORECASE)
            # else:

            # name_found.append(data)
            # pprint('name_found within loop: \n__________{0}__________\n'.format(name_found))
        return item
