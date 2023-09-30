from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")  # Open in fullscreen
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the Airbnb search result page for Atlanta, Georgia, United States
url = "https://www.airbnb.com/s/Atlanta--Georgia--United-States/homes"
driver.get(url)

# Wait for the listings to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='/rooms/']")))

# Create a set to store visited URLs
visited_urls = set()

# Get all the listing elements
listings = driver.find_elements(By.CSS_SELECTOR, "a[href^='/rooms/']")

# Extract the URLs of the listings
listing_urls = [listing.get_attribute("href") for listing in listings]

# Iterate through each listing URL
for listing_url in listing_urls:
    if listing_url not in visited_urls:
        visited_urls.add(listing_url)

        # Navigate to the listing page
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

        # Navigate back to the search results page
        driver.back()
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='/rooms/']")))

# Close the WebDriver when you're done
driver.quit()