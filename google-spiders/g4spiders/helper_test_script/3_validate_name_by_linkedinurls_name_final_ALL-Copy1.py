
# coding: utf-8

# In[34]:

test_linkedin_url = ['https://ca.linkedin.com/in/kerrynmatthews-6897b893', 'https://www.linkedin.com/in/xiaokui-zhang-868404a']
names_in_title_list = ['Kerryn Matthews | LinkedIn', 'Xiaokui Zhang | LinkedIn', 'Xiaokui Zhan | LinkedIn']
test_name_list = []
# pattern = re.compile(r"^/(?:\\.|[^/\\])*/")

# with open(input_file, 'rb') as file_read:
#     reader = csv.reader(file_read)
names_in_linkedin_url_list = []
for url in test_linkedin_url:
    test_name_list = []
    r_split = url.rsplit('-', 1)[0]
#     print(r_split)
#     test_name_list.append(r_split)
#     re_match = re.match(pattern, r_split)
    r_split_name = (' '.join((r_split.split('/in/')[-1].split('-')))).title()
    
    r_split_name = ''.join(r_split_name.lower())
    names_in_linkedin_url_list.append(r_split_name)

# print(names_in_linkedin_url_list)
a = 'https://ca.linkedin.com/in/kerrynmatthews-6897b893'
a = a.rsplit('-', 1)[0]
a = (' '.join((a.split('/in/')[-1].split('-')))).title()
print(a)
b = 'Kerryn Matthews | LinkedIn'
b = b.lower()
bb = b.split(' ')
string_lst = ['kerryn', 'matthews', '|', 'linkedin']
print(bb)
# ba = '|'.join(b)
# print(ba)
# c = re.findall(r'(\w)\1+', b, re.IGNORECASE)
# print(c)
d = re.findall(r"(?=("+'|'.join(string_list)+r"))",a, re.IGNORECASE)
d = ' '.join(filter(None, d)).title()

print(d)
# d = re.findall(r"(?=("++r"))",c)
# print(d)

#     print(r_split_name)
#     print(r_split_name)


# In[ ]:

import csv
import re
from collections import OrderedDict

input_file = '1_test_parse_raw_google_data_27rows_input.csv'
output_file = '1_test_after_parsing_27rows.csv'
test_linkedin_url = ['https://ca.linkedin.com/in/kerryn-matthews-6897b893', 'https://www.linkedin.com/in/xiaokui-zhang-868404a']
names_in_title_list = ['Kerryn Matthews | LinkedIn', 'Xiaokui Zhang | LinkedIn', 'Xiaokui Zhan | LinkedIn']
test_name_list = []
# pattern = re.compile(r"^/(?:\\.|[^/\\])*/")

with open(input_file, 'rb') as file_read:
    reader = csv.reader(file_read)
    names_in_linkedin_url_list = []
    for url in reader:
        r_split = url[1].rsplit('-', 1)[0]
        test_name_list.append(r_split)
        re_match = re.match(pattern, r_split)
        r_split_name = (' '.join((r_split.split('/in/')[-1].split('-')))).title()
        names_in_linkedin_url_list.append(r_split_name)
#     print(r_split_name)
#     print(r_split_name)

def match_name(names_in_linkedin_url_list, names_in_title_list):
    name_found = []
#     from collections import OrderedDict
    dict12 = OrderedDict(zip(names_in_linkedin_url_list, names_in_title_list))  
    for name_in_linkedin_url, name_in_title in dict12.iteritems():
#         print(k, v)
#         for name_in_title in names_in_title_list:
        data = re.search(name_in_linkedin_url, name_in_title, re.IGNORECASE)
        if data:
            data = data.group(0)
            name_found.append(data)
        else:
            data = 'not found'
            name_found.append(data)

    return name_found
match_name(names_in_linkedin_url_list, names_in_title_list)



# In[ ]:




# In[1]:

get_ipython().run_cell_magic(u'capture', u'', u'import csv\nimport re\nfrom collections import OrderedDict\nfrom pprint import pprint\n\n# input_file = \'1_test_parse_raw_google_data_27rows.csv\'\n# input_file = \'gs_2017-Jul-21.csv\'\n# input_file = \'gs_full.csv\'\n# output_file = \'1_test_after_parsing_27rows.csv\'\n# test_linkedin_url = [\'https://ca.linkedin.com/in/kerryn-matthews-6897b893\', \'https://www.linkedin.com/in/xiaokui-zhang-868404a\']\n# test_raw_name = [\'Kerryn Matthews | LinkedIn\', \'Xiaokui Zhang | LinkedIn\']\n# test_name_list = []\n# for url in test_linkedin_url:\n#     r_split = url.rsplit(\'-\', 1)[0]\n#     test_name_list.append(r_split)\n\ndef parse_title_to_get_the_name(input_file):\n    new_columns = ["Raw_Data", "WorkAt1", "WorkAt2", "Name_Sanitized"]\n    regexp_institute = re.compile("at(.*)$")\n    # phd_list = []\n    filtered_list = []\n    name_in_title_sanitized_list = []\n    with open(input_file, \'rb\') as f_read, open(\'sanitized_output.csv\', \'wb\') as f:\n        csv_reader = csv.reader(f_read, delimiter=\',\')\n        csv_writer = csv.writer(f, delimiter=\',\')\n        # headers = csv_reader.next()\n        # headers.append(new_columns)\n        # writer.write(headers)\n        # csv_writer_2.writerow(headers)\n        for title in csv_reader:\n            name_list = []\n            phd_info_list = []\n            # m_institute_1 = \'\'.join(re.findall(r\'(?<= at )(.*)\', title))\n            # m_institute_2 = \'\'.join(re.findall(r"\\((.*?)\\)", title))\n            m_institute_1 = re.search(r\'(?<= at )(.*)\', title[0])\n            if m_institute_1:\n                m_institute_1 = m_institute_1.group(0)\n            else:\n                m_institute_1 = \'\'\n            m_institute_2 = re.search(r"\\((.*?)\\)", title[0])\n            if m_institute_2:\n                m_institute_2 = m_institute_2.group(0)\n            else:\n                m_institute_2 = \'\'\n\n            test_phd_data = \'Elena Kostova, PhD | Professioneel profiel - LinkedIn\'\n            phd_info = re.search(r\'(\\bPhD\\b)|(Ph.D)\',title[0])\n            if phd_info:\n                phd = phd_info.group(0)\n                phd_info_list.append(phd)\n            else:\n                phd = \'\'\n                \n            # phd_info_list.append(phd)\n            # else:\n            #     phd_info_list.append(\'\')\n            # re.search(r\'\\bPhD\\b\',title).group(0)\n            # m_phd = \'\'.join(re.findall(r"", title))\n            # print(m_institute_1)\n            # print(\'\\n\\n\')\n            # print(m_institute_2)\n            # print(\'\\n\')\n            title_replaced = title[0].replace(m_institute_2, \'\')\\\n            .replace(\'at {0}\'.format(m_institute_1), \'\')\\\n            .replace(\'(\', \'\').replace(\')\', \'\')\\\n            .replace(\'| Professional Profile - LinkedIn\', \'\')\\\n            .replace(\' | LinkedIn\', \'\').replace(\' on LinkedIn\', \'\')\\\n            .replace(\'{}\'.format(phd), \'\')\n            title_clean = title_replaced.split(\'|\')[0]\n            title_clean = title_clean.split(\',\')[0]\n            name_in_title_sanitized_list.append(title_clean)\n#             print(title_replaced)\n            name_list.append(title[0])\n            name_list.append(m_institute_1)\n            name_list.append(m_institute_2)\n            name_list.append(phd)\n            name_list.append(title_clean)\n            csv_writer.writerow(name_list)\n            filtered_list.append(name_list)\n#             validate_name_by_lookup()\n#             name_list_returned = name_list\n#             csv_writer.writerow(name_list_returned)\n    return filtered_list\n\n\ndef get_the_name_from_title(input_file):\n    new_columns = ["Raw_Data", "WorkAt1", "WorkAt2", "Name_Sanitized"]\n    regexp_institute = re.compile("at(.*)$")\n    # phd_list = []\n    filtered_list = []\n    name_in_title_sanitized_list = []\n    with open(input_file, \'rb\') as f_read, open(\'sanitized_output.csv\', \'wb\') as f:\n        csv_reader = csv.reader(f_read, delimiter=\',\')\n        csv_writer = csv.writer(f, delimiter=\',\')\n        # headers = csv_reader.next()\n        # headers.append(new_columns)\n        # writer.write(headers)\n        # csv_writer_2.writerow(headers)\n        for title in csv_reader:\n            name_list = []\n            phd_info_list = []\n            # m_institute_1 = \'\'.join(re.findall(r\'(?<= at )(.*)\', title))\n            # m_institute_2 = \'\'.join(re.findall(r"\\((.*?)\\)", title))\n            m_institute_1 = re.search(r\'(?<= at )(.*)\', title[0])\n            if m_institute_1:\n                m_institute_1 = m_institute_1.group(0)\n            else:\n                m_institute_1 = \'\'\n            m_institute_2 = re.search(r"\\((.*?)\\)", title[0])\n            if m_institute_2:\n                m_institute_2 = m_institute_2.group(0)\n            else:\n                m_institute_2 = \'\'\n\n            test_phd_data = \'Elena Kostova, PhD | Professioneel profiel - LinkedIn\'\n            phd_info = re.search(r\'(\\bPhD\\b)|(Ph.D)\',title[0])\n            if phd_info:\n                phd = phd_info.group(0)\n                phd_info_list.append(phd)\n            else:\n                phd = \'\'\n                \n            # phd_info_list.append(phd)\n            # else:\n            #     phd_info_list.append(\'\')\n            # re.search(r\'\\bPhD\\b\',title).group(0)\n            # m_phd = \'\'.join(re.findall(r"", title))\n            # print(m_institute_1)\n            # print(\'\\n\\n\')\n            # print(m_institute_2)\n            # print(\'\\n\')\n            title_replaced = title[0].replace(m_institute_2, \'\')\\\n            .replace(\'at {0}\'.format(m_institute_1), \'\')\\\n            .replace(\'(\', \'\').replace(\')\', \'\')\\\n            .replace(\'| Professional Profile - LinkedIn\', \'\')\\\n            .replace(\' | LinkedIn\', \'\').replace(\' on LinkedIn\', \'\')\\\n            .replace(\'{}\'.format(phd), \'\')\n            title_clean = title_replaced.split(\'|\')[0]\n            title_clean = title_clean.split(\',\')[0]\n            name_in_title_sanitized_list.append(title_clean)\n#             print(title_replaced)\n            name_list.append(title[0])\n            name_list.append(m_institute_1)\n            name_list.append(m_institute_2)\n            name_list.append(phd)\n            name_list.append(title_clean)\n            csv_writer.writerow(name_list)\n            filtered_list.append(name_list)\n#             validate_name_by_lookup()\n#             name_list_returned = name_list\n#             csv_writer.writerow(name_list_returned)\n    return name_in_title_sanitized_list\n\ndef merge_two_csv_files(list_of_the_sanitized_in_title_list, match_found):\n    \n    \n    dict1 = {row[0]: row[1:] for row in match_found}\n    dict2 = OrderedDict((row[0], row[1:]) for row in list_of_the_sanitized_in_title_list)\n    pprint("____________dict1 sanitized___________________{0}".format(dict1))\n    pprint("_______________________________\\n")\n    pprint("____________dict2 match found___________________{0}".format(dict2))\n    # with open(input_file_2, \'rb\') as read_sanitized:\n    #     reader = csv.reader(read_sanitized)\n    #     # r = csv.reader(f)\n    #     dict1 = {row[0]: row[1:] for row in reader}\n\n    # with open(input_file, \'rb\') as incsv:\n    #     reader = csv.reader(incsv)\n    #     dict2 = OrderedDict((row[0], row[1:]) for row in reader)\n    #     # dict2 = {row[0]: row[1:] for row in parse_fields}\n    \n    result = OrderedDict()  \n    for d in (dict1, dict2):\n        for key, value in d.iteritems():\n            result.setdefault(key, []).extend(value)\n    \n    with open(\'combined_file_new.csv\', \'wb\') as outcsv:\n        writer = csv.writer(outcsv)\n        for key, value in result.iteritems():\n            writer.writerow([key] + value)\n\n\ndef get_the_name_from_linkedin_url(input_file):\n    with open(input_file, \'rb\') as file_read:\n        reader = csv.reader(file_read)\n        names_in_linkedin_url_list = []\n        for url in reader:\n            r_split = url[1].rsplit(\'-\', 1)[0]\n            # test_name_list.append(r_split)\n            r_split_name = (\' \'.join((r_split.split(\'/in/\')[-1].split(\'-\')))).title()\n            names_in_linkedin_url_list.append(r_split_name)\n    return names_in_linkedin_url_list\n\n    #     print(r_split_name)\n    #     print(r_split_name)\n\ndef find_a_match_bw_name_in_linkedinurl_and_title(names_in_linkedin_url_list, names_in_title_list, out_file):\n#     name_found = []\n#     from collections import OrderedDict\n#     print(names_in_linkedin_url_list)\n#     print(names_in_title_list)\n    dict1 = OrderedDict(zip(names_in_linkedin_url_list, names_in_title_list))\n#     matched_name_list = []\n    print("ordered_dict by names_in_linkedin_url: \\n{0}".format(dict1))\n    with open(out_file, \'wb\') as outfile:\n        matched_name_list = []\n        csv_writer = csv.writer(outfile)\n#         name_found = []\n        for name_in_linkedin_url, name_in_title in dict1.iteritems():\n            name_found = []\n#             print(type(name_in_linkedin_url))\n#             print(type(name_in_title))\n            data = re.search(name_in_linkedin_url, name_in_title, re.IGNORECASE)\n            if data:\n                data = data.group(0)\n                name_found.append(data)\n                pprint("Name Found: \\n {0} \\n".format(name_found))\n            else:\n                data = \'\'\n                name_found.append(data)\n            pprint(\'name_found within loop: \\n__________{0}__________\\n\'.format(name_found))\n            csv_writer.writerow(name_found)\n#             print(match_found)\n            matched_name_list.append(name_found)\n    pprint(\'matched_name_list: __{0}___\'.format(matched_name_list))\n    print("Matched Name list found______________________________________________________\\n")\n    return matched_name_list\n   \n\n# match_name(names_in_linkedin_url_list, names_in_title_list)\n            \nif __name__ == \'__main__\':\n#     input_file = \'1_test_parse_raw_google_data_27rows_input.csv\'\n    out_file = \'matched_name_new.csv\'\n    input_file = \'gs_full.csv\'\n    # input_file_2 = \'sanitized_output.csv\'\n    # input_file = \'1_test_parse_raw_google_data_27rows_input.csv\'\n    # output_file = \'1_test_after_parsing_27rows.csv\'\n    # test_linkedin_url = [\'https://ca.linkedin.com/in/kerryn-matthews-6897b893\', \'https://www.linkedin.com/in/xiaokui-zhang-868404a\']\n    # names_in_title_list = [\'Kerryn Matthews | LinkedIn\', \'Xiaokui Zhang | LinkedIn\', \'Xiaokui Zhan | LinkedIn\']\n    # test_name_list = []\n    # pattern = re.compile(r"^/(?:\\\\.|[^/\\\\])*/")\n    name_in_title = get_the_name_from_title(input_file)\n    name_in_linkedin_url = get_the_name_from_linkedin_url(input_file)\n    match_found = find_a_match_bw_name_in_linkedinurl_and_title(name_in_linkedin_url, name_in_title, out_file)\n    print("match found: {0}\\n".format(match_found))\n    list_of_the_sanitized_in_title_list = parse_title_to_get_the_name(input_file)\n    merge_two_csv_files(list_of_the_sanitized_in_title_list, match_found)\n    \n')


# In[ ]:




# In[ ]:



