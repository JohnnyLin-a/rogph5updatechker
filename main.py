from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import os
import json
from dotenv import load_dotenv
import requests

def fetchLatestVersionDetails():
    retValue = None
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path="/usr/bin/geckodriver")

    driver.get("https://rog.asus.com/ca-en/phones/rog-phone-5-model/helpdesk_bios")
    
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "productSupportDriverBIOSBox")))
        versionEntries = driver.find_elements_by_class_name("productSupportDriverBIOSBox")
        versionDetails = versionEntries[0].text.split("\n")
        retValue = [versionDetails[0].strip(), versionDetails[1].split(" ")[0].strip()]
    except TimeoutException:
        print("Waiting too long and aborted")
    finally:
        driver.quit()
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
print(versionDetails)

# Check if version.json exists and dump it if it doesn't, then exit
if os.path.isfile("./version.json") == False:
    with open('version.json', 'w') as f:
        print("Dump 1st json file")
        json.dump(versionDetails, f, ensure_ascii=False, indent=4)
        exit(0)

# Read json and compare
storedVersion = None
with open('./version.json') as f:
    storedVersion = json.load(f)

print(storedVersion)

if storedVersion == None:
    print("Stored json file error")
    exit(1)
different = False
if storedVersion[0] != versionDetails[0] and storedVersion[1] != versionDetails[1] and versionDetails[0].lower().startswith("version ww"):
    print("New version detected")
    different = True
else:
    print("Did not find new version")

# Check compare results, then notify if needed
if different:
    print("Notifying discord...")
    success = notifyDiscord(versionDetails)
    if success:
        print("Writing new version to file.")
        os.remove("./version.json")
        with open('version.json', 'w') as f:
            print("Dumping...")
            json.dump(versionDetails, f, ensure_ascii=False, indent=4)

print("End of script")