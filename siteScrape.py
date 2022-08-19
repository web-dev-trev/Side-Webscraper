import csv
from email.mime import base
import requests
import re
from bs4 import BeautifulSoup, Comment

standardPages = ['/communities', '/selling', '/buying', '/search-homes', '/properties', '/contact', '/home-valuation', '/testimonials', '/privacy-policy', '/about-us', '/blog', '/mortgage-calculator', '/working-with-the-team', '/off-market-listings']

with open('WP_Engine_Sites.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    with open('DataMaster.csv', 'a') as new_file:
        fieldnames = ['Site Domain','Texas?', 'Past Sales', 'Blog', 'Testimonials', 'Communities', 'Custom Pages', 'Team Member Count', 'Standard Team Pages', 'EO Pages', 'Off-Market Listings','GA Tracking', 'Side GTM', 'Partner GTM', 'Fub Pixel', 'Adroll' ]
        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')
        csv_writer.writeheader()
        # change range to desired row to read from if an error occurs or you want to start script at a different index
        for i in range(200):
            csv_reader.__next__()

        for line in csv_reader:
            facebookPixelMap = []
            sideGtagMap = []
            customGtagMap = []
            fubPixelMap = []
            adrollIDMap = []
            GATrackingMap = []

            Gtag = "False"
            isTexas = "False"
            hasBlog = "False"
            print("\n crawling site: "+line['Site Domain'])
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            baseURL = "https://"+line['Site Domain']
            cleaner = re.compile('<.*?>')
            try:
                print("connecting to baseURL: "+ str(baseURL))
                page = requests.get(baseURL, headers=headers)
                page.raise_for_status()
                print("Success! Finding script tags and IABS...")
                soup = BeautifulSoup(page.content, features="html.parser")
                # Texas Check
                txTag = soup.findAll("a", "trec-iabs")
                if len(txTag) > 0:
                    isTexas = "True"
                    print("is a Texas site")
                else:
                    print("not a TX site")
                # Script tag checks
                scriptTag = soup.findAll("script")
                print(len(scriptTag))
                for script in scriptTag:
                    cleanScript = str(script)
                    if '<script async="" src="https://www.googletagmanager.com/gtag' in cleanScript:
                        print("Global Google Script Tag found")
                        sideGtagMap.append(cleanScript)
                        print("Global Google Script Tag Count = "+str(len(sideGtagMap)))

                    if  ((Gtag == "False") and (("j.src = 'https://www.googletagmanager.com/gtm.js?id='" in cleanScript) == True)):
                        print("Partner Google Script Tag found")
                        customGtagMap.append(cleanScript)
                        print("Partner Google Script Count = "+str(len(customGtagMap)))
                        Gtag = "True"

                    if "connect.facebook.net" in cleanScript:
                        print("Facebook Pixel Script Tag found")
                        facebookPixelMap.append(cleanScript)
                        print("Facebook Pixel Count = "+str(len(facebookPixelMap)))

                    if "adroll_pix" in cleanScript:
                        print("Adroll Pixel Script Tag found")
                        adrollIDMap.append(cleanScript)
                        print("Adroll Pixel Count = "+str(len(adrollIDMap)))

                    if "https://widgetbe.com/agent" in cleanScript:
                        print("Follow Up Boss Pixel Tag found")
                        fubPixelMap.append(cleanScript)
                        print("Fub Pixel Count = "+str(len(fubPixelMap)))

                    if "'ga_tracking_code'" in cleanScript:
                        print("GA Tracking Code found")
                        GATrackingMap.append(cleanScript)
                        print("GA Tracking Code Count = "+str(len(GATrackingMap)))

            except requests.exceptions.HTTPError as err:
                next(csv_reader)
                raise SystemExit(err)
            try:
                print("opening Past Sales@ "+ str(baseURL)+"/past-sales")
                page = requests.get((baseURL+"/past-sales"), headers=headers)
                page.raise_for_status()
                print("Success! Finding Past Sales")

                soup = BeautifulSoup(page.content, features="html.parser")
                psString = soup.find("span", {"class" : "num-of-results"})
                if not psString:
                    print("no past sales found")
                    pastSalesCount = 0
                else:
                    pastSalesClean = re.sub(cleaner, '', psString.string)
                    pastSalesCount = pastSalesClean.split("of ",1)[1]
                    print(str(pastSalesCount)+" past sales") 

            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)
            try:
                URL = "https://"+line['Site Domain']+"/wp-sitemap.xml"
                print("URL Connecting...")
                print("Sending headers.")
                print("Sending headers..")
                print("Sending headers...")
                page = requests.get(URL, headers=headers)
                print("Requesting Page...")

                print(page)

                soup = BeautifulSoup(page.content, features="xml")
                sitemaps = soup.findAll("loc")

                indexMap = []
                listingMap = []
                standardPagesMap = []
                blogpostsMap = []
                testimonialpostsMap = []
                membersMap = []
                cappMap = []
                communityMap = []
                customPagesMap = []

                for maps in sitemaps:
                    maps_clean = re.sub(cleaner, '', maps.string)
                    indexMap.append(maps_clean)
                    print("Found sitemap: "+maps_clean)
                print(len(indexMap))

                for submaps in indexMap:
                    if "posts-page" in submaps:
                        print("opening... "+submaps)
                        submapURL = submaps
                        submapPage = requests.get(submapURL, headers=headers)
                        submapPagesoup = BeautifulSoup(submapPage.content, features="xml")
                        posts = submapPagesoup.findAll("loc")
                        for post in posts:
                            posts_clean = re.sub(cleaner, '', post.string)
                            if any(standardPage in posts_clean for standardPage in standardPages) == False:
                                customPagesMap.append(posts_clean)
                        print(str(len(customPagesMap))+ " custom pages found")
                        print("Custom Pages: "+str(customPagesMap))
                    standardPageCount = len(standardPagesMap)
                    customPagesCount = len(customPagesMap) - 1

                    if "posts-listing" in submaps:
                        print("Found Pocket Listings :)")
                        print("opening... "+submaps)
                        submapURL = submaps
                        submapPage = requests.get(submapURL, headers=headers)
                        submapPagesoup = BeautifulSoup(submapPage.content, features="xml")
                        posts = submapPagesoup.findAll("loc")
                        for post in posts:
                            posts_clean = re.sub(cleaner, '', post.string)
                            listingMap.append(posts_clean)
                            print("Found pocket listing: "+posts_clean)
                        print(str(len(listingMap))+" pocket listings")
                    listingCount = len(listingMap)
                    

                    if "posts-post" in submaps:
                        print("opening... "+submaps)
                        hasBlog = "True"
                        submapURL = submaps
                        submapPage = requests.get(submapURL, headers=headers)
                        submapPagesoup = BeautifulSoup(submapPage.content, features="xml")
                        posts = submapPagesoup.findAll("loc")
                        for post in posts:
                            posts_clean = re.sub(cleaner, '', post.string)
                            blogpostsMap.append(posts_clean)
                            print("Found blog post: "+posts_clean)
                        print(len(blogpostsMap))
                    blogCount = len(blogpostsMap)
                    
                    if "posts-member" in submaps:
                        print("opening... "+submaps)
                        submapURL = submaps
                        submapPage = requests.get(submapURL, headers=headers)
                        submapPagesoup = BeautifulSoup(submapPage.content, features="xml")
                        posts = submapPagesoup.findAll("loc")
                        for post in posts:
                            memberType = "Standard"
                            posts_clean = re.sub(cleaner, '', post.string)
                            print("Found team member: "+posts_clean)
                            memberURL = posts_clean
                            memberPage = requests.get(memberURL, headers=headers)
                            print("opening "+posts_clean)
                            memberPagesoup = BeautifulSoup(memberPage.content, "html.parser")
                            print("requesting page...")
                            pageComments = memberPagesoup.find_all(string=lambda text: isinstance(text, Comment))
                            for comment in pageComments:
                                if "Team Member Block" in comment:
                                    print("found EO tag")
                                    memberType = "EO"
                            print("Member page is a "+memberType+" page")
                            if memberType == "Standard":
                                membersMap.append(posts_clean)
                            else:
                                cappMap.append(posts_clean)
                        print(str(len(membersMap))+" Standard Pages")
                        print(str(len(cappMap))+" EO Pages")
                    memberCount = len(membersMap)
                    cappCount = len(cappMap)

                    if "posts-testimonial" in submaps:
                        print("opening..."+submaps)
                        submapURL = submaps
                        submapPage = requests.get(submapURL, headers=headers)
                        submapPagesoup = BeautifulSoup(submapPage.content, features="xml")
                        posts = submapPagesoup.findAll("loc")
                        for post in posts:
                            posts_clean = re.sub(cleaner, '', post.string)
                            testimonialpostsMap.append(posts_clean)
                            print("Found testimonial post: "+posts_clean)
                        print(len(testimonialpostsMap))
                    testimonialCount = len(testimonialpostsMap)

                    if "posts-community" in submaps:
                        print("opening..."+submaps)
                        submapURL = submaps
                        submapPage = requests.get(submapURL, headers=headers)
                        submapPagesoup = BeautifulSoup(submapPage.content, features="xml")
                        posts = submapPagesoup.findAll("loc")
                        for post in posts:
                            posts_clean = re.sub(cleaner, '', post.string)
                            communityMap.append(posts_clean)
                            print("Found community post: "+posts_clean)
                        print(len(communityMap))
                    communityCount = len(communityMap)
                totalMemberCount = memberCount + cappCount
            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)
            print("Writing to row for "+(line['Site Domain']))
            csv_writer.writerow({'Site Domain': line['Site Domain'],'Texas?': str(isTexas),'Past Sales': str(pastSalesCount)+" past sales", 'Blog': str(hasBlog)+" posts: "+str(blogpostsMap), 'Testimonials': str(testimonialCount)+" testimonials: "+str(testimonialpostsMap), 'Communities': str(communityCount)+" communities: "+ str(communityMap), 'Custom Pages': str(customPagesCount)+" custom pages: "+str(customPagesMap), 'Team Member Count': str(totalMemberCount), 'Standard Team Pages': str(memberCount)+" member pages: "+str(membersMap), 'EO Pages': str(cappCount)+" EO Pages: "+str(cappMap), 'Off-Market Listings': str(listingCount)+" listings: "+str(listingMap), 'GA Tracking': str(GATrackingMap), 'Side GTM': str(sideGtagMap), 'Partner GTM': str(customGtagMap), 'Fub Pixel': str(fubPixelMap), 'Adroll': str(adrollIDMap)})
            indexMap = []
            standardPagesMap = []
            blogpostsMap = []
            testimonialpostsMap = []
            membersMap = []
            cappMap = []
            communityMap = []
            customPagesMap = []
            listingMap = []
            facebookPixelMap = []
            sideGtagMap = []
            customGtagMap = []
            fubPixelMap = []
            adrollIDMap = []
            GATrackingMap = []
