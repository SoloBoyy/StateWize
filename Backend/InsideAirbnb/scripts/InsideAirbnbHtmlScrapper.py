from bs4 import BeautifulSoup
import re
import json

# Specify the path to your HTML file
html_file_path = '../html/insideairbnb.html'

# Read the contents of the HTML file
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all links with href attributes
all_links = soup.find_all('a', href=True)

# Define a regular expression pattern to extract city names from links
city_pattern = re.compile(r'/([^/]+)/\d{4}-\d{2}-\d{2}')

# Initialize a list to store city data
city_data_list = []

# Initialize variables to track the current city and its associated URLs
current_city = None
city_urls = {}

# Iterate through all links and extract city names and links
for link in all_links:
    href = link['href']
    match = city_pattern.search(href)
    
    if match:
        city_name = match.group(1)
        if "united-states" in href:  # Filter for US cities
            if current_city is None or current_city != city_name:
                if current_city is not None:
                    city_data_list.append({
                        "location": current_city,
                        "data": city_urls
                    })
                current_city = city_name
                city_urls = {}
            file_name = href.split("/")[-1]
            if file_name not in city_urls:
                city_urls[file_name] = []
            city_urls[file_name].append(href)

# Append the last city's data
if current_city is not None:
    city_data_list.append({
        "location": current_city,
        "data": city_urls
    })

# Specify the path for the JSON output file
output_json_file_path = '../json/city_data.json'

# Write the city_data_list to the JSON file
with open(output_json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(city_data_list, json_file, indent=2)

print(f'Data has been saved to {output_json_file_path}')

# Read the original JSON file
with open('../json/city_data.json', 'r') as file:
    original_data = json.load(file)

# Create a new dictionary to store the restructured data
restructured_data = {}

# Iterate through each location in the original data
for location_data in original_data:
    location = location_data['location']
    data = location_data['data']

    # Iterate through each data type in the location's data
    for data_type, urls in data.items():
        # If the data_type is not already a key in restructured_data, initialize it as an empty list
        if data_type not in restructured_data:
            restructured_data[data_type] = []

        # Append the URLs from the current location to the restructured_data dictionary
        restructured_data[data_type].extend(urls)
        
        # If the data_type is "reviews.csv.gz", break out of the loop to stop further processing
        if data_type == "reviews.csv.gz":
            break

# Convert the adjusted data back to a JSON string
modified_json = json.dumps(restructured_data, indent=2)

# Define the path to save the restructured JSON file
output_restructured_json_path = '../json/restructured_data.json'

# Write the modified JSON string to the specified path
with open(output_restructured_json_path, 'w') as file:
    file.write(modified_json)

print(f"Data has been restructured and saved to '{output_restructured_json_path}'.")