# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogleSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #
    #
    Title = scrapy.Field()
    Title_Url = scrapy.Field()
    Description_Data = scrapy.Field()
    URL = scrapy.Field()
    LinkedIn_Profile_Url = scrapy.Field()
    Name = scrapy.Field()
    Company = scrapy.Field()
    G_Title = scrapy.Field()
    G_LinkedIn_Url = scrapy.Field()
    G_LinkedIn_Url_For_Name = scrapy.Field()
    G_Description = scrapy.Field()
    G_Name_In_LinkedIn_Url = scrapy.Field()
    G_Name_In_Title = scrapy.Field()
    G_Matched_Name = scrapy.Field()
    G_Address = scrapy.Field()
    G_WorkAt = scrapy.Field()
    G_PhD = scrapy.Field()
    G_Education = scrapy.Field()
    pass


class GoogleDetailedSpiderItem(scrapy.Item):
    Title = scrapy.Field()
    FirstName = scrapy.Field()
    LastName = scrapy.Field()
    FullName = scrapy.Field()
    Suffix = scrapy.Field()
    Company = scrapy.Field()
    JobTitle = scrapy.Field()
    Current_Company = scrapy.Field()
    Previous_Company = scrapy.Field()
    Education = scrapy.Field()
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
    # Raw Data Fields just for testing
    RawData_Address_JobTitle = scrapy.Field()
    RawData_FullName = scrapy.Field()
    RawData_Employment_History = scrapy.Field()

    # Current_Company = scrapy.Field()
    # Previous_Company = scrapy.Field()
    # Education = scrapy.Field()
    pass
# Title   First Name  Last Name   Suffix  Job Title   Company Email1  Email2  Home phone  Cell phone  Work phone  Work ext    Address City    State   Zip Country LinkedIn URL    Source  Notes
# item = GoogleDetailedSpiderItem()
#         address_and_job_title = response.xpath('//div[@class="slp f"]/text()').extract_first().strip()
#         address = address_and_job_title.split('-')[0].strip()
#         item['Address'] = address
#         job_title = ' '.join(address_and_job_title.split('-')[1:])
#         item['JobTitle'] = job_title
#         employment_history = response.xpath('//span[@class="st"]/text()').extract()
#         current_employment = employment_history[0]
#         item['Current_Company'] = current_employment
#         previous_employment = employment_history[1]
#         item['Previous_Company'] = previous_employment
#         education = employment_history[2]
#         education = education.split('.')[1].strip()
#         item['Eduction'] = education
#         name_data = response.xpath('//h3[@class="r"]/a/text()').extract()
#         name_data = ''.join(name_data)
#         fullname = name_data.split('at')[0].strip()
#         item['FullName'] = fullname
#         item['FirstName'] = fullname.split(' ')[0]
#         item['LastName'] = full.split(' ')[-1]
#         item['LinkedInUrl'] = response.url#
