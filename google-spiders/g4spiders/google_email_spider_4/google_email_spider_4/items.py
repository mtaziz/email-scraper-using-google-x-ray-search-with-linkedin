# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogleSpiderItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
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
    domain_name = scrapy.Field()


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


class GoogleCompanyDomainSpiderItem(scrapy.Item):

    # network_location = scrapy.Field()
    CompanyName2 = scrapy.Field()
    CompanyWebsite = scrapy.Field()
    CompanyDomain = scrapy.Field()
    Source_Url_DomainSpider3 = scrapy.Field()

    # From spider2( GoogleDetailedSpiderItem )
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
    pass


class GoogleEmailSpiderItem(scrapy.Item):
    # network_location = scrapy.Field()
    CompanyName2 = scrapy.Field()
    CompanyWebsite = scrapy.Field()
    CompanyDomain = scrapy.Field()
    Source_Url_DomainSpider4 = scrapy.Field()

    # From spider2( GoogleDetailedSpiderItem )
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
    Email1_Raw = scrapy.Field()
    Email2_Raw = scrapy.Field()
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
    pass
