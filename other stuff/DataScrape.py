import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class DataScrape:
    def __init__(self, city, state, country):
        self.city = city
        self.state = state
        self.country = country
        self.driver = self.setup_webdriver()

    def setup_webdriver(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--start-maximized")
        return webdriver.Chrome(options=chrome_options)

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep duration if needed

    def scrape_page(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cy5jw6o")))

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        listings = soup.find_all("div", class_="cy5jw6o")
        for listing in listings:
            # Safely get name
            name_element = listing.find("div", {"data-testid": "listing-card-title"})
            name = name_element.text.strip() if name_element else "N/A"

            # Safely get description
            description_element = listing.find("span", class_="t6mzqp7")
            description = description_element.text if description_element else "N/A"

            # Safely get price
            price_element = listing.find("span", class_="_14y1gc")
            price = price_element.text.strip() if price_element else "N/A"

            # Safely get rating
            rating_element = listing.find("span", class_="r1dxllyb")
            rating = rating_element.text if rating_element else "N/A"

            print("Name:", name)
            print("Description:", description)
            print("Price:", price)
            print("Rating:", rating)
            print("-" * 30)

    def scrape_airbnb(self):
        airbnb_url = f"https://www.airbnb.com/s/{self.city}--{self.state}--{self.country}/homes"

        self.driver.get(airbnb_url)
        listings_urls = set()

        while True:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='/rooms/']")))
            listings = self.driver.find_elements(By.CSS_SELECTOR, "a[href^='/rooms/']")
            pages_urls = set([listing.get_attribute("href") for listing in listings])
            listings_urls.update(pages_urls)

            try:
                self.scroll_to_bottom()
                next_button = None
                time.sleep(1)
                try:
                    next_button = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Next")
                except:
                    potential_buttons = self.driver.find_elements(By.XPATH,
                                                                  "//a[contains(@aria-label, 'Next') or contains(@title, 'Next')]")
                    if potential_buttons:
                        next_button = potential_buttons[0]

                if next_button:
                    wait.until(EC.element_to_be_clickable((next_button)))
                    if not next_button.get_attribute("disabled"):
                        next_button.click()
                    else:
                        break
                else:
                    break
            except:
                break

        # Write the URLs to a file
        with open("airbnb_listing_urls.txt", "w") as file:
            for url in listings_urls:
                file.write(url + "\n")

        self.driver.quit()
        return listings_urls

# Function to initialize the WebDriver
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")  # Uncomment to run in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Function to navigate to the search result page
def navigate_to_search_page(driver, url):
    driver.get(url)

# Function to wait for the listings to load
def wait_for_listings(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='/rooms/']")))

# Function to scrape listing details
def scrape_listing_details(driver, wait, listing_url):
    # Navigate to the listing page
    driver.get(listing_url)

    # Extract data from the listing page using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extracting the title
    title = soup.find("h1", class_="_14i3z6h")

    # Extracting the rating
    rating = soup.select_one("span._1d6n3ph")

    # Extracting Superhost status
    superhost = soup.select_one("span._vbshq0")

    # Extracting the location
    location = soup.select_one("a._mkj4h13")

    # Extracting the response rate
    response_rate = soup.select_one("div._1hpgssa2 > span._fgq7ul")

    # Extracting the response time
    response_time = soup.select_one("div._1hpgssa2 > span._q1dfql")

    # Extracting the cancellation policy
    cancellation_policy = soup.select_one("div._qptau2")

    # Extracting check-in time
    checkin_time = soup.select_one("div._9fdqpn")

    # Extracting check-out time
    checkout_time = soup.select_one("div._36rlri")

    # Extracting guest maximum
    guest_maximum = soup.select_one("div._1fg5h3v")

    print("-" * 30)
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

    if response_rate:
        print("Response Rate:", response_rate.text.strip())
    else:
        print("Response Rate not found")

    if response_time:
        print("Response Time:", response_time.text.strip())
    else:
        print("Response Time not found")

    if cancellation_policy:
        print("Cancellation Policy:", cancellation_policy.text.strip())
    else:
        print("Cancellation Policy not found")

    if checkin_time:
        print("Check-in time:", checkin_time.text.strip())
    else:
        print("Check-in time not found")

    if checkout_time:
        print("Check-out time:", checkout_time.text.strip())
    else:
        print("Check-out time not found")

    if guest_maximum:
        print("Guest maximum:", guest_maximum.text.strip())
    else:
        print("Guest maximum not found")


# Function to read listing URLs from a file
def read_listing_urls_from_file(file_path):
    with open(file_path, "r") as file:
        listing_urls = [line.strip() for line in file.readlines()]
    return listing_urls

# Main function
def main():
    driver = initialize_driver()

    # Read listing URLs from the file
    file_path = "/Users/richiekumar/Documents/GitHub/StateWize/Backend/airbnb_listing_urls.txt"
    listing_urls = read_listing_urls_from_file(file_path)

    # Create a set to store visited URLs
    visited_urls = set()

    # Wait object for use in scrape_listing_details
    wait = WebDriverWait(driver, 10)

    # Iterate through each listing URL
    for listing_url in listing_urls:
        if listing_url not in visited_urls:
            visited_urls.add(listing_url)
            scrape_listing_details(driver, wait, listing_url)

    # Close the WebDriver when you're done
    driver.quit()

if __name__ == "__main__":
    main()
