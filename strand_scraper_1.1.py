#####################################
#   SCRAPE PRICE INFO FROM STRAND   #
#####################################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import ChromiumOptions
import sys

# define driver options
options = ChromiumOptions()
options.add_experimental_option("excludeSwitches", ['enable-logging'])
options.set_capability("browserVersion", "117")
options.add_argument("--log-level=3")
options.add_argument("--headless=new")

def init():
    # Logic checks for valid ISBN before calling scrapePrice()
    if (len(sys.argv) > 1) and (len(sys.argv[1]) == (10) or len(sys.argv[1]) == (13)):
        scrapePrice()
    else:
        sys.stdout.write("ERROR: Invalid ISBN.")

def scrapePrice():
    # Takes ISBN argument from console and tries to find strand product URL.
    # Waits for 'item-price-RxI' or 'searchPage-noResult-LaX' element to load,
    # scrapes price if item-price-RxI exists, otherwise prints NULL to console.
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.strandbooks.com/catalogsearch/result/?q=" + sys.argv[1])
    elementNames = ['price', 'message.notice']
    bValid = 1

    try:                        # Wait until item page loads
        WebDriverWait(driver, 15).until(EC.any_of(
            EC.presence_of_element_located((By.CLASS_NAME, 'price')),
            EC.presence_of_element_located((By.CLASS_NAME, 'message.notice'))))
    except TimeoutException:    # If exception is thrown, set valid bool to false
        bValid = 0

    if bValid == 1:             # If expected element found
        handlePage(driver, elementNames)
    else:                       # If no expected element found
        sys.stdout.write("ERROR: No valid elements found.")

    driver.close()

def handlePage(driver, elementNames):
    # Take list of element names being searched for, and choose behavior
    # depending on which element was located. Assumes an element from
    # the list has already been found.
    for elem in elementNames:
        try:                # look for each element in search list
            element = driver.find_element(By.CLASS_NAME, elem)
        except NoSuchElementException:
            continue

    if element.get_attribute("class") == "price":             # If item price exists
        element_text = element.text.replace("$", "")          # Format price text
        sys.stdout.write(element_text)
    elif element.get_attribute("class") == "message notice":  # If item does not exist
        sys.stdout.write("No listings found for ISBN.")

init()
sys.exit()
