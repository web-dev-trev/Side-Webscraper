import csv
from email import header
from urllib import request
import requests
import re
from bs4 import BeautifulSoup

domain = "https://www.allcityhomes.com"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
cleaner = re.compile('<.*?>')

def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email

with open('team_member_scrape.csv', 'w') as new_file:
        fieldnames = ['Team Member URL', 'Team Member Name', 'Title', 'Phone', 'Side Brand Email', 'License Number', ]
        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')
        csv_writer.writeheader()
        try:
            memberMap = []
            print("connecting to team member sitemap")
            page = requests.get(str(domain)+"/wp-sitemap-posts-member-1.xml", headers=headers)
            page.raise_for_status()
            soup = BeautifulSoup(page.content, features="xml")
            members = soup.findAll("loc")

            for member in members:
                memberClean = re.sub(cleaner, '', member.string)
                memberMap.append(memberClean)
                print("Found member: "+memberClean)
            
            for teamMember in memberMap:
                print("Requesting member page:"+ teamMember)
                memberURL = teamMember
                memberPage = requests.get(memberURL, headers=headers)
                memberSoup = BeautifulSoup(memberPage.content, features="html.parser")
                try:
                    licenseTag = memberSoup.findAll(True, {'class':'agent-profile__number'})
                    if len(licenseTag) > 0:
                        cleanLicense = re.sub(cleaner, '', str(licenseTag))
                        license = re.sub(r"[\n\t\s]*", "", cleanLicense)
                        print(license)
                    else:
                        print("no license found")

                    fullNameTag = memberSoup.findAll(True, {'class':'agent-profile__title'})
                    if len(fullNameTag) > 0:
                        CleanfullName = re.sub(cleaner, '', str(fullNameTag))
                        fullName = re.sub(r"[\n\t\s]*", "", CleanfullName)
                        print(fullName)
                    else:
                        print("no name found")
                    
                    roleTag = memberSoup.findAll(True, {'class':'agent-profile__type'})
                    if len(roleTag) > 0:
                        role = re.sub(cleaner, '', str(roleTag[0]))
                        print(role)
                    else:
                        print("no role found")

                    contactTag = memberSoup.findAll(True, {'class':'contact-info-item'})
                    print(str(len(contactTag))+" contact point(s) found")
                    if len(contactTag) == 1:
                        emailTag = contactTag[0]
                        if len(emailTag) > 0:
                            cfDecode = re.search('data-cfemail=(.*)>[email protected]', str(emailTag))
                            cfCode = re.findall('"([^"]*)"', str(cfDecode.group(1)))
                            print(cfCode)
                            email = cfDecodeEmail(str(cfCode[0]))
                            print(email)
                        else:
                            print("no email found")
                    elif len(contactTag) == 2:
                        emailTag = contactTag[0]
                        if len(emailTag) > 0:
                            cfDecode = re.search('data-cfemail=(.*)>[email protected]', str(emailTag))
                            cfCode = re.findall('"([^"]*)"', str(cfDecode.group(1)))
                            print(cfCode)
                            email = cfDecodeEmail(str(cfCode[0]))
                            print(email)
                        else:
                            print("no email found")
                        phoneTag = contactTag[1]
                        if len(phoneTag) > 0:
                            cleanPhone = re.sub(cleaner, '', str(phoneTag))
                            phone = re.sub(r"[\n\t\s]*", "", cleanPhone)
                            print(phone)
                        else:
                            print("no phone found")
                    else:
                        print("no contact info found")
                        phone = "None"
                        email = "None"
                except requests.exceptions.HTTPError as err:
                    raise SystemExit(err)
                print("Writing team member row for:"+str(memberURL))
                csv_writer.writerow({
                    'Team Member URL': str(memberURL),
                    'Team Member Name': str(fullName),
                    'Title': str(role),
                    'Phone': str(phone),
                    'Side Brand Email': str(email),
                    'License Number': str(license)
                })
        except requests.exceptions.HTTPError as err:
                raise SystemExit(err)




