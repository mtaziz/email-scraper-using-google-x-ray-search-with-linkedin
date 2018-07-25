# Google Spiders

The aim of the project is to scrape email leads for certain group of professionals.

##1 Objectives

a) The key goal of the project is to scrape Email addresses by using Google
b) The input data considered to be "Google searching operators and desired keywords"
c) The another key motivation was to scrape the emails from Google without taking the help from 3rd party service providers.



## List of projects

There are 3 projects as below.

### g4spiders ###
	`g` refers to `Google` whereas `4` refers to the number of spiders.
	In this project, at the very beginning of this project, these spiders were developed in order to obtain the email
	To get Email address, we have come up with an idea which is found to be worth trying.
	For example, Google X-Ray search techniques have been considered while developing these spiders.

	First off, using particular Google search keywords, from Google search results, we get the desired professional information.
	The spiders work flow split into 4 spiders.
	**name**>>**job title**>> **company domain** >> **email**


### g4spiders-4in2-run-from-script ###

		From `g4spiders` project, spiders were cloned and 4 spiders are merged into 2.
		name spider consideration to be the one and other 3 ( jobtitle, companydomain, email) spiders into another one.



( 4 Google spiders were )


#2 First Approach and development task list
2.1 spider1: get the name and corresponding linkedin urls
2.2 spider2: get the "job title" and "currently working company name" by feeding "the name" and "linked url" obtained from spider1
2.3 spider3: get the domain name by using "jobtitle" and "current company" information obtained from spider2
2.4 spider4: get the Email addresses using the domain name and individual's name obtained from spider3


#3 Google spiders
-- First off all, To extract email from primarily Google search results, mentioned tasks split into 4 parts.
-- At first, 4 seperate spiders developed to see how things work and at what level success could be attained from this.

** Four Spiders named as follows....

* Name_Spider_1
	-- ( i.e., Spider_1 scrapes the name and LinkedIn URLs.
	-- It dumps the data into CSV file that will be ultimately stored into the Database updated to the database)
* JobTitle_Spider_2
	-- ( i.e., From the DB/file, the LinkedIn URLs and name data will be read )
* Domain_Spider_3
* Email_Spider_4


#4 Second Approach
 	-- once the test for 4 above spiders worked as expected, and test passed from thereon, the effort was to merge those 4 spiders into the one so that it could be easier to maintain.
	-- In this case, 2 spiders built, out of which , one is called "spider4in1" and another one is "spider3in1"
	-- The "spider4in1" was built but it has some issues in terms of around 70% duplicates found in spider1
	-- Then "spider3in1" development ideas happens to be convincing.
	-- From the DB/file scraped by name_spider1, the LinkedIn URLs and name data will be fed into spider_3in1.
	-- spider_3in1 combines all 3 spiders (jobtitle_spider2, domain_spider3 and email_spider4) into the one.
	-- Spider3in1 found to be more effective an robust in terms of expected results.


#5 Why merging the spiders into the one required
	-- I attempted to merge all the spider into a single one but that did not work as expected.
    -- Spider1 may have lot of duplicates , for example , after testing '"Red blood cell" -jobs -topic site:linkedin.com'
    -- It dynamically scrapes around 5000 entries from google search results  but 600 found to be unique.
    -- Before, we feed the data from spider1 to the spider_3in1, this is very important that we remove the duplicates so that we don't have to send lot of unnecessary requests to the Google server.


#How does email spider works :

Well, the way it works, using "Google search"  spider1 extracts the "Name" and "LinkedIn URL"
The raw data from spider1 fed into the spider_3in1.
spider3in1 extracts "job title", "domain", and "emails".
