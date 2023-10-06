import os
import requests
from bs4 import BeautifulSoup

# Define the URL of the page containing the links to city data.
base_url = "http://insideairbnb.com/get-the-data/"

# Send an HTTP request to the URL.
response = requests.get(base_url)

# Check if the request was successful.
if response.status_code == 200:
    # Parse the HTML content of the page.
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all cities listed on the page.
    cities = soup.find_all('h3')

    # Loop through the cities and download files for United States cities.
    for city in cities:
        city_name = city.text.strip()
        if "United States" in city_name:
            # Find the table associated with the city.
            city_table = city.find_next('table')

            # Find all rows in the table.
            rows = city_table.find_all('tr')

            # Loop through the rows and download files.
            for row in rows[1:]:  # Skip the header row
                columns = row.find_all('td')
                file_name = columns[1].find('a').text
                file_url = columns[1].find('a')['href']
                
                # Construct the absolute URL.
                file_url = base_url + file_url

                # Download the file and save it to a local directory.
                with open(os.path.join("downloaded_data", file_name), 'wb') as file:
                    file_response = requests.get(file_url)
                    file.write(file_response.content)
                    print(f"Downloaded: {file_name} for {city_name}")

else:
    print("Failed to fetch the page.")
