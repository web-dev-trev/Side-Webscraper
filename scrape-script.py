import csv
import requests
import re
from bs4 import BeautifulSoup, Comment

standardPages = ['/communities', '/selling', '/buying', '/search-homes', '/properties', '/contact', '/home-valuation', '/testimonials', '/privacy-policy', '/about-us', '/blog', '/mortgage-calculator', '/working-with-the-team', '/off-market-listings']

with open('WPEngine_Sites_Cut.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    with open('WPEngine_Pocket_Listing_Stats.csv', 'a') as new_file:
        fieldnames = ['Site Category', 'Site Name', 'Site Domain', 'Pocket Listings']
        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')
        csv_writer.writeheader()

        for line in csv_reader:
            hasBlog = "False"
            print("\n crawling site: "+line['Site Domain'])
            URL = "https://"+line['Site Domain']+"/wp-sitemap.xml"
            print("URL Connecting...")
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            print("Sending headers.")
            print("Sending headers..")
            print("Sending headers...")
            page = requests.get(URL, headers=headers)
            print("Requesting Page...")

            print(page)

            soup = BeautifulSoup(page.content, features="xml")
            sitemaps = soup.findAll("loc")
            cleaner = re.compile('<.*?>')

            indexMap = []
            listingMap = []
            # standardPagesMap = []
            # blogpostsMap = []
            # testimonialpostsMap = []
            # membersMap = []
            # cappMap = []
            # communityMap = []
            # customPagesMap = []

            for maps in sitemaps:
                maps_clean = re.sub(cleaner, '', maps.string)
                indexMap.append(maps_clean)
                print("Found sitemap: "+maps_clean)
            print(len(indexMap))

            for submaps in indexMap:
                # if "posts-page" in submaps:
                #     print("opening... "+submaps)
                #     submapURL = submaps
                #     submapPage = requests.get(submapURL, headers=headers)
                #     submapPagesoup = BeautifulSoup(submapPage.content, features="xml")
                #     posts = submapPagesoup.findAll("loc")
                #     for post in posts:
                #         posts_clean = re.sub(cleaner, '', post.string)
                #         if any(standardPage in posts_clean for standardPage in standardPages) == False:
                #             customPagesMap.append(posts_clean)
                #     print(str(len(customPagesMap))+ " custom pages found")
                #     print("Custom Pages: "+str(customPagesMap))
                # standardPageCount = len(standardPagesMap)
                # customPagesCount = len(customPagesMap) - 1

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
                

                # if "posts-post" in submaps:
                #     print("opening... "+submaps)
                #     hasBlog = "True"
                #     submapURL = submaps
                #     submapPage = requests.get(submapURL, headers=headers)
                #     submapPagesoup = BeautifulSoup(submapPage.content, features="xml")
                #     posts = submapPagesoup.findAll("loc")
                #     for post in posts:
                #         posts_clean = re.sub(cleaner, '', post.string)
                #         blogpostsMap.append(posts_clean)
                #         print("Found blog post: "+posts_clean)
                #     print(len(blogpostsMap))
                # blogCount = len(blogpostsMap)
                
                # if "posts-member" in submaps:
                #     print("opening... "+submaps)
                #     submapURL = submaps
                #     submapPage = requests.get(submapURL, headers=headers)
                #     submapPagesoup = BeautifulSoup(submapPage.content, features="xml")
                #     posts = submapPagesoup.findAll("loc")
                #     for post in posts:
                #         memberType = "Standard"
                #         posts_clean = re.sub(cleaner, '', post.string)
                #         print("Found team member: "+posts_clean)
                #         memberURL = posts_clean
                #         memberPage = requests.get(memberURL, headers=headers)
                #         print("opening "+posts_clean)
                #         memberPagesoup = BeautifulSoup(memberPage.content, "html.parser")
                #         print("requesting page...")
                #         pageComments = memberPagesoup.find_all(string=lambda text: isinstance(text, Comment))
                #         for comment in pageComments:
                #             if "Team Member Block" in comment:
                #                 print("found EO tag")
                #                 memberType = "EO"
                #         print("Member page is a "+memberType+" page")
                #         if memberType == "Standard":
                #             membersMap.append(posts_clean)
                #         else:
                #             cappMap.append(posts_clean)
                #     print(str(len(membersMap))+" Standard Pages")
                #     print(str(len(cappMap))+" EO Pages")
                # memberCount = len(membersMap)
                # cappCount = len(cappMap)

                # if "posts-testimonial" in submaps:
                #     print("opening..."+submaps)
                #     submapURL = submaps
                #     submapPage = requests.get(submapURL, headers=headers)
                #     submapPagesoup = BeautifulSoup(submapPage.content, features="xml")
                #     posts = submapPagesoup.findAll("loc")
                #     for post in posts:
                #         posts_clean = re.sub(cleaner, '', post.string)
                #         testimonialpostsMap.append(posts_clean)
                #         print("Found testimonial post: "+posts_clean)
                #     print(len(testimonialpostsMap))
                # testimonialCount = len(testimonialpostsMap)

                # if "posts-community" in submaps:
                #     print("opening..."+submaps)
                #     submapURL = submaps
                #     submapPage = requests.get(submapURL, headers=headers)
                #     submapPagesoup = BeautifulSoup(submapPage.content, features="xml")
                #     posts = submapPagesoup.findAll("loc")
                #     for post in posts:
                #         posts_clean = re.sub(cleaner, '', post.string)
                #         communityMap.append(posts_clean)
                #         print("Found community post: "+posts_clean)
                #     print(len(communityMap))
                # communityCount = len(communityMap)
            print("Writing to row for "+(line['Site Domain']))
            csv_writer.writerow({'Site Category': line['Site Category'], 'Site Name': line['Site Name'], 'Site Domain': line['Site Domain'], 'Pocket Listings': str(listingCount)+" listings: "+str(listingMap)})
            indexMap = []
            standardPagesMap = []
            blogpostsMap = []
            testimonialpostsMap = []
            membersMap = []
            cappMap = []
            communityMap = []
            customPagesMap = []
            listingMap = []