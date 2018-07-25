# Google Spiders #

The key goal of this project is to generate the leads by using Google X-Ray Search techniques for a particular group of professional.
Since directly scraping Email from LinkedIn is found to be hard, we have followed different approach in this case.




There are 4 spiders named as follows:
  1. google_name_spider_1
  2. google_jobtitle_spider_2
  3. google_company_domain_spider_3
  4. google_email_spider_4



## google_name_spider_1 ##

Using Google search keyword, first it forms the `start_urls` or list of urls to be scraped off.
Google name spider works in way that uses predefined Google search keyword supplied in `settings.py` before we run the spider.
Scraped data exported in CSV file located under `export` directory.

Before running the spider, change the below as required:



    # Google Keyword Example
    GS_KEYWORD = '"Red blood cell" -jobs -topic site:linkedin.com'

    # No of Google search results in a single page
    GS_RESULTS_NUM = 100

    # Google Number of Pages to be scraped
    GS_RESULTS_PAGES_NUM = 20

    # Example start_urls
    start_urls = 'https://www.google.com/search?num=100&start=1&hl=en&q=%22Red+blood+cell%22+-topic+-jobs+site%3Alinkedin.com'








## google_jobtitle_spider_2 ##

Exported data by `google_name_spider_1` fed into the `google_jobtitle_spider_2`.
For example, extracted [linkedin profile url](https://www.linkedin.com/in/stacy-martin-12329736) from name spider.
LinkedIn profile URL is parsed to obtain the *linkedin url with name only* such **linkedin.com/in/stacy-martin**
In order generate the `start_urls`, based on the study , it is found that the following Google operators with *linkedin url with name only* produces expected results regarding the job title.



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

    example_start_urls = 'https://www.google.com/search?q=site:linkedin.com/in/marisollimauro+%22Current%22+OR+%22Previous%22+OR+%22Education%22'



## google_company_domain_spider_3 ##

This spider scrapes the domain name by using "Company information obtained from google_spider2"


    query_string = {"google_base_url": "https://www.google.com/search?q=", "JobTitle":"", "Company": "", "location": ""}
    link = "{0}{1}{2}{3}&ie=utf-8&oe=utf-8".format(self.query_string['google_base_url'],
                                                            self.query_string['FullName'],
                                                            self.query_string['JobTitle'],
                                                            row['Current_Company'],
                                                            self.query_string['JobTitle'])



## google_email_spider_4 ##

  Data for `Fullname` and `Company Domain` scraped by `google_company_domain_spider_3` fed into the `google_email_spider_4`.
  The following URl formed in to get the Email address.
  

    link = '{0}%22{1}%22+%22*+%40{2}%22{3}&ie=utf-8&oe=utf-8'.format(self.query_string['google_base_url'],\
                                                                    row['FullName'].replace(' ', '+'),\
                                                                    row['CompanyDomain'],\
                                                                    # self.query_string['JobTitle'],\
                                                                    self.query_string['JobTitle']
                                                                    )







# How to Run the Spider from terminal #
Scrapy Spiders Development Environment was built based Python 2.7.6 on Ubuntu 14.04.
From terminal, it is run by going inside of spider project directory where Scrapy configuration file `scrapy.cfg` located.
once there, you can run the below command:


    # spider_1
    scrapy crawl name

    # spider_2
    scrapy crawl jobtitle

    # spider_3
    scrapy crawl companydomain

    # spider_4
    scrapy crawl email
