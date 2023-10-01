import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AirbnbScraper:
    def __init__(self):
        self.setup_webdriver()

    def setup_webdriver(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=chrome_options)

    def scroll_to_bottom(self):
        self.visit_each_listing()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    def visit_each_listing(self):
        main_window = self.driver.current_window_handle
        listings = self.driver.find_elements(By.CLASS_NAME, "cy5jw6o")

        for listing in listings:
            listing.click()
            time.sleep(2)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            self.scrape_listing_details()

            # Placeholder for scraping logic
            self.driver.close()
            self.driver.switch_to.window(main_window)
            time.sleep(2)

    def scrape_listing_details(self):
        # We already navigated to the page, so just get the page source directly
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # Extract the required details
        title = soup.find("h1", class_="hpipapi")
        rating = soup.select_one("span.a8jt5op")
        superhost = soup.select_one("div.r1lutz1s")
        location = soup.select_one("h1.hpipapi")
        response_rate = soup.select_one(".fhhmddr .f19phm7j:nth-child(1) .ll4r2nl")
        response_time = soup.select_one(".fhhmddr .f19phm7j:nth-child(2) .ll4r2nl")
        cancellation_policy = soup.select_one(".h4lj7td h3")
        checkin_time = soup.select_one(".is50c2g:nth-child(2) span")
        checkout_time = soup.select_one(".is50c2g:nth-child(3) span")
        guest_maximum = soup.select_one(".is50c2g:nth-child(4) span")

        # Additional details
        title_under_images = soup.select_one("h2")
        bedrooms = soup.select_one(".lgx66tx li:nth-child(2) span")
        beds = soup.select_one(".lgx66tx li:nth-child(3) span")
        baths = soup.select_one(".lgx66tx li:last-child span")

        # Extract the text content of the elements
        bedrooms_text = bedrooms.text.strip() if bedrooms else "N/A"
        beds_text = beds.text.strip() if beds else "N/A"
        baths_text = baths.text.strip() if baths else "N/A"

        # You can now process or store the extracted details as required.
        # For now, let's just print them out:
        print("Title:", title.text if title else "N/A")
        print("Rating:", rating.text if rating else "N/A")
        print("Superhost:", superhost.text if superhost else "N/A")
        print("Location:", location.text if location else "N/A")
        print("Response Rate:", response_rate.text if response_rate else "N/A")
        print("Response Time:", response_time.text if response_time else "N/A")
        print("Cancellation Policy:", cancellation_policy.text if cancellation_policy else "N/A")
        print("Check-in Time:", checkin_time.text if checkin_time else "N/A")
        print("Check-out Time:", checkout_time.text if checkout_time else "N/A")
        print("Guest Maximum:", guest_maximum.text if guest_maximum else "N/A")
        print("Title under Images:", title_under_images.text if title_under_images else "N/A")
        print("# of Bedrooms:", bedrooms_text)
        print("# of Beds:", beds_text)
        print("# of Baths:", baths_text)
        print("-" * 30)  # Separator for clarity between listings

    def scrape_airbnb_listings(self, city, state, country):
        airbnbURL = f"https://www.airbnb.com/s/{city}--{state}--{country}/homes"
        print(airbnbURL)
        self.driver.get(airbnbURL)
        time.sleep(5)

        while True:
            # Then, scroll to the bottom
            self.scroll_to_bottom()

            # Now, try to find and click the "Next" button to navigate to the next page
            wait = WebDriverWait(self.driver, 10)

            try:
                # Scroll to the bottom of the page to load more listings
                self.scroll_to_bottom()

                # Attempt to find the "Next" button element using various methods
                next_button = None
                time.sleep(1)
                try:
                    # First, try to locate by partial link text
                    next_button = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Next")
                except:
                    # If not found, try to locate by other attributes (e.g., title, aria-label)
                    potential_buttons = self.driver.find_elements(By.XPATH, "//a[contains(@aria-label, 'Next') or contains(@title, 'Next')]")
                    if potential_buttons:
                        next_button = potential_buttons[0]

                # If we found the "Next" button, proceed
                if next_button:
                    # Explicitly wait for the button to become clickable
                    wait.until(EC.element_to_be_clickable((next_button)))

                    # Check if the "Next" button is disabled
                    if not next_button.get_attribute("disabled"):
                        # Click the "Next" button to go to the next page
                        next_button.click()
                    else:
                        # If the "Next" button is disabled, there are no more pages
                        break
                else:
                    break
            except:
                # Handle any exceptions when the button is not found or not clickable
                break

    def close_driver(self):
        self.driver.quit()
