from ast import IsNot
import csv
import requests
import re
from bs4 import BeautifulSoup


cleaner = re.compile('<.*?>')
validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
domain = "https://revelrealestate.com"

def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email

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
                MLSIDMap = []
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
                        cleanLicense = re.sub(cleaner, '', str(licenseTag[0]))
                        license = re.sub(r"[\n\t\s]*", "", cleanLicense)
                        print(license)
                    else:
                        license = "none"
                        print("no license found")

                    fullNameTag = memberSoup.findAll(True, {'class':'agent-profile__title'})
                    if len(fullNameTag) > 0:
                        CleanfullName = re.sub(cleaner, '', str(fullNameTag[0]))
                        nospacefullName = re.sub(r"[\n\t\s]*", "", CleanfullName)
                        fullName = re.sub(r"(\w)([A-Z])", r"\1 \2", nospacefullName)
                        print(fullName)
                        MLSIDCheck(fullName)
                    else:
                        print("no name found")
                        fullName = "none"
                    
                    roleTag = memberSoup.findAll(True, {'class':'agent-profile__type'})
                    if len(roleTag) > 0:
                        role = re.sub(cleaner, '', str(roleTag[0]))
                        print(role)
                    else:
                        role = "none"
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
                    'License Number': str(license),
                    'Market & MLS IDs': str(MLSIDMap)
                })
                MLSIDMap = []
        except requests.exceptions.HTTPError as err:
                raise SystemExit(err)

print("congrats no errors happened!")
