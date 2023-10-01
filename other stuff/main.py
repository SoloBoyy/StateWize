import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Function to initialize the WebDriver
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")  # Open in fullscreen
    # chrome_options.add_argument("--headless")  # Run in headless mode
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
def scrape_listing_details(driver, wait, listing_url, csv_writer):
    # Navigate to the listing page
    driver.get(listing_url)

    # Wait for the Cancellation Policy element to become visible
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".h4lj7td h3")))

    # Extract data from the listing page using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extracting the title
    title = soup.find("h1", class_="hpipapi")

    # Extracting the rating
    rating = soup.select_one("span.a8jt5op")

    # Extracting Superhost status
    superhost = soup.select_one("div.r1lutz1s")

    # Extracting the location
    location = soup.select_one("h1.hpipapi")

    # Extracting the Response rate
    response_rate = soup.select_one(".fhhmddr .f19phm7j:nth-child(1) .ll4r2nl")

    # Extracting the Response time
    response_time = soup.select_one(".fhhmddr .f19phm7j:nth-child(2) .ll4r2nl")

    # Extracting the Cancellation Policy
    cancellation_policy = soup.select_one(".h4lj7td h3")

    # Extracting Check-in time
    checkin_time = soup.select_one(".is50c2g:nth-child(2) span")

    # Extracting Check-out time
    checkout_time = soup.select_one(".is50c2g:nth-child(3) span")

    # Extracting Guest maximum
    guest_maximum = soup.select_one(".is50c2g:nth-child(4) span")

    data = {
        "Title": title.text.strip() if title else "N/A",
        "Rating": rating.text.strip() if rating else "N/A",
        "Superhost": superhost.text.strip() if superhost else "N/A",
        "Location": location.text.strip() if location else "N/A",
        "Response Rate": response_rate.text.strip() if response_rate else "N/A",
        "Response Time": response_time.text.strip() if response_time else "N/A",
        "Cancellation Policy": cancellation_policy.text.strip() if cancellation_policy else "N/A",
        "Check-in Time": checkin_time.text.strip() if checkin_time else "N/A",
        "Check-out Time": checkout_time.text.strip() if checkout_time else "N/A",
        "Guest Maximum": guest_maximum.text.strip() if guest_maximum else "N/A",
    }

    # Write data to CSV
    csv_writer.writerow(data)

    print("-" * 30)
    for key, value in data.items():
        print(f"{key}: {value}")

# Main function
def main():
    driver = initialize_driver()

    # Navigate to the Airbnb search result page for Atlanta, Georgia, United States
    url = "https://www.airbnb.com/s/Atlanta--Georgia--United-States/homes"
    navigate_to_search_page(driver, url)

    while True:
        # Wait for the listings to load
        wait_for_listings(driver)

        # Create a set to store visited URLs
        visited_urls = set()

        # Get all the listing elements
        listings = driver.find_elements(By.CSS_SELECTOR, "a[href^='/rooms/']")

        # Extract the URLs of the listings
        listing_urls = [listing.get_attribute("href") for listing in listings]

        # Wait object for use in scrape_listing_details
        wait = WebDriverWait(driver, 10)

        # Create and open a CSV file for writing
        with open("airbnb_listing_data.csv", "a", newline="", encoding="utf-8") as csv_file:
            fieldnames = ["Title", "Rating", "Superhost", "Location", "Response Rate", "Response Time",
                          "Cancellation Policy", "Check-in Time", "Check-out Time", "Guest Maximum"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Iterate through each listing URL
            for listing_url in listing_urls:
                if listing_url not in visited_urls:
                    visited_urls.add(listing_url)
                    scrape_listing_details(driver, wait, listing_url, csv_writer)

        # Try to find and click the "Next" button to navigate to the next page
        try:
            next_button = driver.find_element(By.PARTIAL_LINK_TEXT, "Next")
            if next_button.is_enabled():
                next_button.click()
            else:
                break  # If the "Next" button is disabled, there are no more pages
        except:
            break  # Handle any exceptions when the button is not found or not clickable

    # Close the WebDriver when you're done
    driver.quit()

if __name__ == "__main__":
    main()
