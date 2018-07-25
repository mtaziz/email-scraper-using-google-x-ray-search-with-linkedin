# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogleSpiderItem(scrapy.Item):
    # define the fields for your item here like:

    s1_title_name_data = scrapy.Field()
    s1_linkedin_url = scrapy.Field()
    s1_linkedin_url_with_valid_name = scrapy.Field()
    s1_description = scrapy.Field()
    s1_name_in_linkedin_url = scrapy.Field()
    s1_name_in_title = scrapy.Field()
    s1_name_in_title_and_linkedin_url = scrapy.Field()
    s1_address = scrapy.Field()
    s1_workat = scrapy.Field()
    s1_phd_data = scrapy.Field()
    s1_education = scrapy.Field()
    s1_source_gurl = scrapy.Field()

# s1_name_in_title_and_linkedin_url


class GoogleDetailedSpiderItem(scrapy.Item):
    Title = scrapy.Field()
    FirstName = scrapy.Field()
    LastName = scrapy.Field()
    Suffix = scrapy.Field()
    JobTitle = scrapy.Field()
    CompanyEmail1 = scrapy.Field()
    Email2 = scrapy.Field()
    HomePhone = scrapy.Field()
    CellPhone = scrapy.Field()
    WorkPhone = scrapy.Field()
    WorkExt = scrapy.Field()
    Address = scrapy.Field()
    City = scrapy.Field()
    State = scrapy.Field()
    Zip = scrapy.Field()
    Country = scrapy.Field()
    LinkedInUrl = scrapy.Field()
    Source = scrapy.Field()
    Notes = scrapy.Field()
    pass
# Title   First Name  Last Name   Suffix  Job Title   Company Email1  Email2  Home phone  Cell phone  Work phone  Work ext    Address City    State   Zip Country LinkedIn URL    Source  Notes
