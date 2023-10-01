# StateWize

```markdown
# Airbnb Web Scraper

This Python script allows you to scrape Airbnb listings for a specific city, state, and country using Selenium and BeautifulSoup. The scraped data includes information about each Airbnb listing, such as title, rating, superhost status, location, response rate, response time, cancellation policy, check-in/out times, and more.

## Getting Started

These instructions will help you set up and run the Airbnb web scraper on your local machine.

### Prerequisites

- Python 3.x
- Selenium (`pip install selenium`)
- BeautifulSoup (`pip install beautifulsoup4`)
- Chrome WebDriver (compatible with your Chrome browser version)

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/airbnb-web-scraper.git
   cd airbnb-web-scraper
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Download and place the Chrome WebDriver executable in the project directory or specify the path to it in the `airbnb_scraper.py` script.

### Usage

1. Open the `main.py` script and customize the `city`, `state`, and `country` variables to specify the location you want to scrape.

2. Run the script:

   ```bash
   python main.py
   ```

   This will start the scraping process, and the scraped data will be printed to the console. You can modify the `scrape_listing_details` method in `airbnb_scraper.py` to process or store the data as needed.

3. The script will automatically scroll through multiple pages of Airbnb listings and scrape the details of each listing.

### Closing the Scraper

When you are done, the script will automatically close the Chrome WebDriver. You can also manually terminate the script by pressing `Ctrl+C` in the terminal.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
