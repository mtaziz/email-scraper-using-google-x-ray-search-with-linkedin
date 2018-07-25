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
from google_email_spider_4in1.items import *
from scrapy.exporters import JsonLinesItemExporter
from scrapy.conf import settings
SETTINGS = get_project_settings
import csv
import re
from collections import OrderedDict
from pprint import pprint


class GoogleDupfilterPipeline(object):

    def __init__(self):
        self.ids_seen = set()
        self.LinkedInUrl_seen = set()

    def process_item(self, item, spider):

        if item['LinkedInUrl'] in self.LinkedInUrl_seen:
            raise DropItem(
                "_____Duplicates Removed: {0}_______".format(item['LinkedInUrl']))
        elif item['LinkedInUrl'] is None:
            return
        else:
            self.LinkedInUrl_seen.add(item['LinkedInUrl'])
            return item
