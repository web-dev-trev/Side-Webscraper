<<<<<<< HEAD
from ast import IsNot
import csv
import requests
import re
from bs4 import BeautifulSoup
from playsound import playsound


cleaner = re.compile('<.*?>')
validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
domain = "https://energy-realty.com"
=======
import csv
from email import header
from urllib import request
import requests
import re
from bs4 import BeautifulSoup

domain = "https://www.allcityhomes.com"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
cleaner = re.compile('<.*?>')
>>>>>>> 066cf7e52847369e5dd3ca4134fb19c30602dba2

def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email

<<<<<<< HEAD
def MLSIDCheck(fullName):
    print("requesting home junction API...")
    try:
        for market in markets:
            print("Searching for agent MLS ID in:"+str(market))
            url = "https://slipstream.homejunction.com/ws/markets/agents/search?name="+str(fullName)+"&market="+str(market)
            print(url)
            payload={}
            headers = {'HJI-Slipstream-Token': token}
            response = requests.request("GET", url, headers=headers, data=payload)
            jsonResponse = response.json()
            recordTotal = jsonResponse['result']['total']
            print(str(recordTotal)+" records found")
            if recordTotal == 1:
                MLSIDJson = jsonResponse['result']['agents'][0]['id']
                print(MLSIDJson)
                MLSIDMap.append(str(market)+": "+str(MLSIDJson))
            elif recordTotal > 1:
                for agent in jsonResponse['result']['agents']:
                    print(str(agent['name'])+": "+str(agent['id']))
                print("Too many agents with similar name. Please review the ID for: "+str(fullName))
                playsound('./sounds/hey.wav')
                MLSID = input()
                MLSIDMap.append(str(market)+": "+str(MLSID))
            else:
                print("No valid MLS ID found for "+str(fullName))
    except:
        print("An error has occurred")

markets = input("Enter MLS Markets separated by spaces: ").split()
print("Markets to search are: "+str(markets))

try:
    url = "https://slipstream.homejunction.com/ws/api/authenticate?license=49D4-0683-F220-6D1A"
    payload={}
    headers = {}
    print("authenticating token...")
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.status_code)
    jsonResponse = response.json()
    print("Token found: "+str(jsonResponse['result']['token']))
    token = str(jsonResponse['result']['token'])
except:
    print("Error connecting to HomeJunction API :(")

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

with open('team_member_scrape.csv', 'w') as new_file:
        fieldnames = ['Team Member URL', 'Team Member Name', 'Title', 'Phone', 'Side Brand Email', 'License Number', 'Market & MLS IDs']
=======
with open('team_member_scrape.csv', 'w') as new_file:
        fieldnames = ['Team Member URL', 'Team Member Name', 'Title', 'Phone', 'Side Brand Email', 'License Number', ]
>>>>>>> 066cf7e52847369e5dd3ca4134fb19c30602dba2
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
<<<<<<< HEAD
                MLSIDMap = []
=======
>>>>>>> 066cf7e52847369e5dd3ca4134fb19c30602dba2
                memberClean = re.sub(cleaner, '', member.string)
                memberMap.append(memberClean)
                print("Found member: "+memberClean)
            
            for teamMember in memberMap:
                print("Requesting member page:"+ teamMember)
                memberURL = teamMember
                memberPage = requests.get(memberURL, headers=headers)
                memberSoup = BeautifulSoup(memberPage.content, features="html.parser")
<<<<<<< HEAD

                try:
                    licenseTag = memberSoup.findAll(True, {'class':'agent-profile__number'})
                    if len(licenseTag) > 0:
                        cleanLicense = re.sub(cleaner, '', str(licenseTag[0]))
                        license = re.sub(r"[\n\t\s]*", "", cleanLicense)
                        print(license)
                    else:
                        license = "none"
=======
                try:
                    licenseTag = memberSoup.findAll(True, {'class':'agent-profile__number'})
                    if len(licenseTag) > 0:
                        cleanLicense = re.sub(cleaner, '', str(licenseTag))
                        license = re.sub(r"[\n\t\s]*", "", cleanLicense)
                        print(license)
                    else:
>>>>>>> 066cf7e52847369e5dd3ca4134fb19c30602dba2
                        print("no license found")

                    fullNameTag = memberSoup.findAll(True, {'class':'agent-profile__title'})
                    if len(fullNameTag) > 0:
<<<<<<< HEAD
                        CleanfullName = re.sub(cleaner, '', str(fullNameTag[0]))
                        nospacefullName = re.sub(r"[\n\t\s]*", "", CleanfullName)
                        fullName = re.sub(r"(\w)([A-Z])", r"\1 \2", nospacefullName)
                        print(fullName)
                        MLSIDCheck(fullName)
                    else:
                        print("no name found")
                        fullName = "none"
=======
                        CleanfullName = re.sub(cleaner, '', str(fullNameTag))
                        fullName = re.sub(r"[\n\t\s]*", "", CleanfullName)
                        print(fullName)
                    else:
                        print("no name found")
>>>>>>> 066cf7e52847369e5dd3ca4134fb19c30602dba2
                    
                    roleTag = memberSoup.findAll(True, {'class':'agent-profile__type'})
                    if len(roleTag) > 0:
                        role = re.sub(cleaner, '', str(roleTag[0]))
                        print(role)
                    else:
                        print("no role found")
<<<<<<< HEAD
                        role = "none"

                    contactTag = memberSoup.findAll(True, {'class':'contact-info-item'})
                    print(str(len(contactTag))+" contact point(s) found")

                    phone = "none"
                    email = "none"

                    for contact in contactTag:
                        contact_clean = re.sub(cleaner, '', str(contact))
                        phone_clean = re.findall(r'\+[-()\s\d]+?(?=\s*[+<])', str(contact_clean))
                        if "protected" in contact_clean:
                            print("email protected.. decoding email")
                            cfDecode = re.search('data-cfemail=(.*)>[email protected]', str(contact))
                            cfCode = re.findall('"([^"]*)"', str(cfDecode.group(1)))
                            email = cfDecodeEmail(str(cfCode[0]))
                            print(email)
                        elif "@" in contact_clean:
                            print("email found... cleaning")
                            clean_email = re.sub(cleaner, '', str(contact_clean))
                            email = re.sub(r"[\n\t\s]*", "", clean_email)
                            print(email)
                        if "Mobile" or "Work" or "Home" in contact_clean:
                            phone = re.sub(r"[\n\t\s]*", "", contact_clean)
                            print(phone)
                except requests.exceptions.HTTPError as err:
                    raise SystemExit(err)
                print("Writing team member row for:"+str(memberURL))

=======

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
>>>>>>> 066cf7e52847369e5dd3ca4134fb19c30602dba2
                csv_writer.writerow({
                    'Team Member URL': str(memberURL),
                    'Team Member Name': str(fullName),
                    'Title': str(role),
                    'Phone': str(phone),
                    'Side Brand Email': str(email),
<<<<<<< HEAD
                    'License Number': str(license),
                    'Market & MLS IDs': str(MLSIDMap)
                })
                MLSIDMap = []
        except requests.exceptions.HTTPError as err:
                raise SystemExit(err)

print("congrats no errors happened!")
playsound('./sounds/success.wav')
=======
                    'License Number': str(license)
                })
        except requests.exceptions.HTTPError as err:
                raise SystemExit(err)

>>>>>>> 066cf7e52847369e5dd3ca4134fb19c30602dba2



