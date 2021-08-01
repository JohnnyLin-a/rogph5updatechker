from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

def fetchLatestVersionDetails():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome("./chromedriver/chromedriver.exe", chrome_options=options)

    driver.get("https://rog.asus.com/ca-en/phones/rog-phone-5-model/helpdesk_bios")
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "productSupportDriverBIOSBox")))
        versionEntries = driver.find_elements_by_class_name("productSupportDriverBIOSBox")
        versionDetails = versionEntries[0].text.split("\n")
        return [versionDetails[0].strip(), versionDetails[1].split(" ")[0].strip()]
        # version = versionDetails[1].split(" ")[0].strip()
    except TimeoutException:
        print("Waiting too long and aborted")
        exit(1)
    finally:
        driver.quit()


# Start of script execution
arr = fetchLatestVersionDetails()
print(arr)

