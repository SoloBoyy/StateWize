# StateWize

## Airbnb Data Processor

### Overview

This repository offers a suite of tools for web scraping, processing, and analyzing Airbnb datasets. Leveraging Python scripts, it aids in efficiently downloading data, restructuring it, and deriving insights through sentiment analysis.

### Contents

1. **insideairbnb.html**:
   - An HTML document containing links to Airbnb datasets. This includes listings, reviews, and calendar data spanning various cities and dates.
   
2. **InsideAirbnbHtmlScrapper.py**:
   - **Purpose**: This script is designed to scrape data from the `insideairbnb.html` page.
   - **Features**:
     - Uses `BeautifulSoup` to parse HTML.
     - Efficiently extracts links related to different Airbnb datasets.
   - **Usage**: Modify the `html_file_path` variable to point to your local copy of the `insideairbnb.html` file and then run the script.

3. **batch_csv_processor.py**:
   - **Purpose**: Automate the process of downloading and handling CSV files from the Airbnb dataset.
   - **Features**:
     - Can download and extract compressed `.gz` files.
     - Utilizes `pandas` for data manipulations.
   - **Usage**: Call the `download_and_extract` function with appropriate parameters (URL and save folder).

4. **reviews_sa.py**:
   - **Purpose**: Conduct sentiment analysis on Airbnb reviews.
   - **Features**:
     - Computes sentiment scores using `TextBlob`.
     - Aggregates sentiment scores by 'listing_id'.
     - Merges sentiment scores with original listings.
   - **Usage**: Ensure you have the `reviews_test.csv` and `listings_test.csv` files in the appropriate directory. Run the script to get a merged dataframe with sentiment scores.

5. **JSON Files**: `restructured_data.json`, `test.json`, `city_data.json`:
   - These files contain structured links to Airbnb datasets.
   - Organized either by data type (e.g., listings, reviews) or by city for easy referencing.

### Installation and Setup

1. **Dependencies**:
   - Install the necessary Python libraries using pip:
     ```bash
     pip install beautifulsoup4 pandas textblob
     ```
2. **Setup**:
   - Clone this repository to your local machine.
   - Ensure you have the required data files in the appropriate directories.
   - Modify file paths in the scripts if necessary.

### Contributing

Interested in making this tool even better? We welcome contributions! 
1. Fork the repository.
2. Make your changes or enhancements.
3. Create a pull request for review.

### License

(You can specify the license details here.)

---

This README offers a more detailed breakdown of each component and its usage. Adjustments can be made as needed, especially if you have specific paths or additional steps to mention.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
