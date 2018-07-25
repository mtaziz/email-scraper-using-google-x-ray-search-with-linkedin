# -*- coding:utf-8 -*-
from scrapy.dupefilters import RFPDupeFilter


class CustomURLFilter(RFPDupeFilter):
    def request_fingerprint(self, request):
        if "timestamp" in request.meta:
            return request.url + "--" + request.meta["timestamp"]
        else:
            return request.url
