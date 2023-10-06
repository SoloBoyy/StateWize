from airbnb_scraper import AirbnbScraper

if __name__ == "__main__":
    scraper = AirbnbScraper()
    city = "Atlanta"
    state = "Georgia"
    country = "United-States"
    scraper.scrape_airbnb_listings(city, state, country)
    scraper.close_driver()
