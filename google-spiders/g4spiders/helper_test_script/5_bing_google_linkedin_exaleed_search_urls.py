def search(domain, limit):
    all_emails = []
    app_emailharvester.show_message("[+] Searching in Linkedin")

    yahooUrl = "http://search.yahoo.com/search?p=site%3Alinkedin.com+%40{word}&n=100&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b={counter}"
    app_emailharvester.init_search(yahooUrl, domain, limit, 1, 100, 'Yahoo + Linkedin')
    app_emailharvester.process()
    all_emails += app_emailharvester.get_emails()

    bingUrl = "http://www.bing.com/search?q=site%3Alinkedin.com+%40{word}&count=50&first={counter}"
    app_emailharvester.init_search(bingUrl, domain, limit, 0, 50, 'Bing + Linkedin')
    app_emailharvester.process()
    all_emails += app_emailharvester.get_emails()

    googleUrl = 'https://www.google.com/search?num=100&start={counter}&hl=en&q=site%3Alinkedin.com+"%40{word}"'
    app_emailharvester.init_search(googleUrl, domain, limit, 0, 100, 'Google + Linkedin')
    app_emailharvester.process()
    all_emails += app_emailharvester.get_emails()

    url = 'http://www.baidu.com/search/s?wd=site%3Alinkedin.com+"%40{word}"&pn={counter}'
    app_emailharvester.init_search(url, domain, limit, 0, 10, 'Baidu + Linkedin')
    app_emailharvester.process()
    all_emails += app_emailharvester.get_emails()

    url = "http://www.exalead.com/search/web/results/?q=site%3Alinkedin.com+%40{word}&elements_per_page=10&start_index={counter}"
    app_emailharvester.init_search(url, domain, limit, 0, 50, 'Exalead + Linkedin')
    app_emailharvester.process()
    all_emails += app_emailharvester.get_emails()

    #dogpile seems to not support site:

    return all_emails
