from pprint import pprint

google_query_example_url = "https://www.google.com/#q=site:linkedin.com/in/floralicia+%22Current%22+OR+%22Previous%22+OR+%22Education%22"

google_search_url_0 = 'https://www.google.com/#q='
gs_operator_in_site_1 = 'site'
gs_operator_linkedin_url_2 = 'linkedin.com/in/floralicia'
gs_operator_current_3 = 'Current'
gs_operator_or_4 = 'OR'
gs_operator_previous_5 = 'Previous'
gs_operator_or_6 = 'OR'
gs_operator_edu_7 = 'Education'

linkedin_url = 'https://www.linkedin.com/in/stacy-martin-12329736'
ll = """
        https://www.linkedin.com/in/david-kuhrt-0487a0a
        https://uk.linkedin.com/in/alex-crick-9b2b14108
        https://www.linkedin.com/in/kathleen-abadie-7896515a
        https://www.linkedin.com/learning/maya-tips-tricks-techniques/simulate-red-blood-cells-in-an-artery
        https://www.linkedin.com/in/ruipeng-mu-b03a6596
        https://au.linkedin.com/in/peter-klinken-2b73577a
        https://www.linkedin.com/in/tonychobot
        https://ch.linkedin.com/in/olivier-rubin-a5949b43
        https://nz.linkedin.com/in/stephenduffull
    """
ll = ll.split('\n')[1:]
pprint(ll)
for i in ll:
    pprint("'"+i+"',")

test_linkedin_urls = [
                    'https://www.linkedin.com/in/david-kuhrt-0487a0a',
                    'https://uk.linkedin.com/in/alex-crick-9b2b14108',
                    'https://www.linkedin.com/in/kathleen-abadie-7896515a',
                    'https://www.linkedin.com/learning/maya-tips-tricks-techniques/simulate-red-blood-cells-in-an-artery',
                    'https://www.linkedin.com/in/ruipeng-mu-b03a6596',
                    'https://au.linkedin.com/in/peter-klinken-2b73577a',
                    'https://www.linkedin.com/in/tonychobot',
                    'https://ch.linkedin.com/in/olivier-rubin-a5949b43',
                    'https://nz.linkedin.com/in/stephenduffull'
                    ]

test_linkedin_urls = filter(None, test_linkedin_urls)
linkedin_operator_based_urls_list = []
for test_linkedin_url in test_linkedin_urls:
    if "/in/" in test_linkedin_url:
        if "//www." in test_linkedin_url:
            test_linkedin_url_split = test_linkedin_url.split('www.')[-1]
            test_linkedin_url_split = test_linkedin_url_split.rsplit('-', 1)[0]
            linkedin_operator_based_urls_list.append(test_linkedin_url_split)
        else:
            test_linkedin_url_split = test_linkedin_url.replace('https://', '')
            test_linkedin_url_split = test_linkedin_url_split.rsplit('-', 1)[0]
            linkedin_operator_based_urls_list.append(test_linkedin_url_split)

        #     gs_operator_linkedin_url_2 = linkedin_url

l_operator_urls_list = """['linkedin.com/in/david-kuhrt',
                             'https://uk.linkedin.com/in/alex-crick',
                             'linkedin.com/in/kathleen-abadie',
                             'linkedin.com/in/ruipeng-mu',
                             'https://au.linkedin.com/in/peter-klinken',
                             'linkedin.com/in/tonychobot',
                             'https://ch.linkedin.com/in/olivier-rubin',
                             'https://nz.linkedin.com/in/stephenduffull']
                             """

pprint(linkedin_operator_based_urls_list)

google_queries_urls_list = []
for linked_operator_url in linkedin_operator_based_urls_list:
    google_search_query = "{0}{1}:{2}+%22{3}%22+{4}+%22{5}%22+{6}+%22{7}%22".format(google_search_url_0,\
                                                                                     gs_operator_in_site_1,\
                                                                                     linked_operator_url,\
                                                                                     gs_operator_current_3,\
                                                                                     gs_operator_or_4,\
                                                                                     gs_operator_previous_5,\
                                                                                     gs_operator_or_4,\
                                                                                     gs_operator_edu_7)
    google_queries_urls_list.append(google_search_query)
start_urls_list = google_queries_urls_list
pprint(start_urls_list)
# print(google_search_query)