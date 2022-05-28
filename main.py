import os
import json
from dotenv import load_dotenv
import requests

def fetchLatestVersionDetails():
    retValue = None

    reqURL = "https://rog.asus.com/support/webapi/product/GetPDBIOS?website=ca-en&model=ROG-Phone-5&pdid=15527&cpu=&LevelTagId=120421&systemCode=rog"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'}
    getReq = requests.get(reqURL, headers=headers)
    if not (getReq.status_code >= 200 and getReq.status_code < 300):
        print("HTTP status code not successful", getReq.status_code)
        return None

    response = getReq.json()

    for versionObj in response['Result']['Obj'][0]['Files']:
        if not versionObj['Version'].startswith('WW'):
            continue
        return [ 'Version ' + versionObj['Version'], versionObj['ReleaseDate']]

    return retValue

def notifyDiscord(versionDetails):
    success = False
    user_id = os.getenv("DISCORD_USERID")
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if user_id == None or webhook_url == None:
        print(".env not configured")
        return success
    postReq = requests.post(webhook_url, {'content': "<@" + user_id + "> New update available: " + versionDetails[0] + " " + versionDetails[1]})
    if postReq.status_code >= 200 and postReq.status_code < 300:
        success = True
        print("Successfully notified on discord with status code: " + str(postReq.status_code))
    else:
        print("Failed to notify discord with status code: " +  str(postReq.status_code))
    return success


# Start of script execution
# Load .env
load_dotenv()

# Fetch Latest Version and Date
versionDetails = fetchLatestVersionDetails()

if versionDetails == None:
    exit(1)
print("Checked", versionDetails)

# Check if version.json exists and dump it if it doesn't, then exit
if os.path.isfile("./version/version.json") == False:
    with open('./version/version.json', 'w') as f:
        print("Dump 1st json file")
        json.dump(versionDetails, f, ensure_ascii=False, indent=4)
        exit(0)

# Read json and compare
storedVersion = None
with open('./version/version.json') as f:
    storedVersion = json.load(f)

print("Cached:", storedVersion)

if storedVersion == None:
    print("Stored json file error")
    exit(1)
different = False
if storedVersion[0] != versionDetails[0] and storedVersion[1] != versionDetails[1] and versionDetails[0].lower().startswith("version ww"):
    print("New version detected")
    different = True
else:
    print("Did not find new version")

print("Different:", different)

# Check compare results, then notify if needed
if different:
    print("Notifying discord...")
    success = notifyDiscord(versionDetails)
    if success:
        print("Writing new version to file.")
        os.remove("./version/version.json")
        with open('./version/version.json', 'w') as f:
            print("Dumping...")
            json.dump(versionDetails, f, ensure_ascii=False, indent=4)

print("End of script")