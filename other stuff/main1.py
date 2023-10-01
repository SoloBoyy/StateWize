import DataScrape

atlanta_scrape = DataScrape.DataScrape(city="Atlanta", state="Georgia", country="United States")
atlanta_listings = atlanta_scrape.scrape_airbnb()
atlanta_scrape.scrape_page