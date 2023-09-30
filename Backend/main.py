from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import concurrent.futures

# Function to scrape data from a single listing URL
def scrape_listing(listing_url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(listing_url)

    # Extract data from the listing page using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extracting the title (both cases)
    title = soup.find("h1", class_="_1xxgv6l")
    if not title:
        title = soup.find("h1", class_="hpipapi i1pmzyw7 dir dir-ltr")

    # Extracting the rating (both cases)
    rating = soup.select_one("span._1uaq0z1l")
    if not rating:
        rating = soup.select_one("span._1uaq0z1l")

    # Extracting Superhost status (both cases)
    superhost = soup.find("span", class_="_1x93jmy")
    if not superhost:
        superhost = soup.find("span", class_="_1x93jmy")

    # Extracting the location (both cases)
    location = soup.find("span", class_="_8x4fjw")
    if not location:
        location = soup.find("span", class_="_8x4fjw")

    if title:
        print("Listing Title:", title.text.strip())
    else:
        print("Title not found")

    if rating:
        print("Rating:", rating.text.strip())
    else:
        print("Rating not found")

    if superhost:
        print("Superhost Status:", superhost.text.strip())
    else:
        print("Superhost status not found")

    if location:
        print("Location:", location.text.strip())
    else:
        print("Location not found")

    print("-" * 30)

    driver.quit()

# Set up Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")  # Open in fullscreen

# Navigate to the Airbnb search result page for Atlanta, Georgia, United States
url = "https://www.airbnb.com/s/Atlanta--Georgia--United-States/homes"

# Create a set to store visited URLs
visited_urls = set()

# Get all the listing elements
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='/rooms/']")))
listings = driver.find_elements(By.CSS_SELECTOR, "a[href^='/rooms/']")
listing_urls = [listing.get_attribute("href") for listing in listings]

# Use concurrent.futures to parallelize the scraping
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Start scraping tasks for each listing URL in parallel
    futures = [executor.submit(scrape_listing, listing_url) for listing_url in listing_urls]

    # Wait for all tasks to complete
    concurrent.futures.wait(futures)

# Close the WebDriver when you're done
driver.quit()
