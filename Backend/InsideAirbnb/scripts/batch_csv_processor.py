import json
import os
import requests
import pandas as pd
import gzip
import shutil
from urllib.parse import urlparse

# Function to download and extract files
def download_and_extract(url, save_folder):
    response = requests.get(url)
    if response.status_code == 200:
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        save_path = os.path.join(save_folder, filename)

        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {url} to {save_path}")

        # Check if the file is a .gz file
        if filename.endswith('.gz'):
            extracted_file_path = os.path.join(save_folder, filename[:-3])  # Remove .gz extension
            with gzip.open(save_path, 'rb') as f_in:
                with open(extracted_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(save_path)  # Remove the original .gz file
            return extracted_file_path
        else:
            return save_path
    else:
        print(f"Failed to download {url}")
        return None

# Function to combine CSV files
def combine_csv(input_files, output_file):
    dfs = []
    for input_file in input_files:
        df = pd.read_csv(input_file)
        dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv(output_file, index=False)
    print(f"Combined {len(input_files)} CSV files into {output_file}")
    print("-------------------------------------------------------------------")

# Read the JSON file with download links
json_file = '../json/restructured_data.json'

try:
    with open(json_file, 'r') as file:
        download_links = json.load(file)

    # Create a folder for combined CSVs
    combined_folder = '../Combined CSVs'
    os.makedirs(combined_folder, exist_ok=True)

    # Process each key in the JSON
    for key, links in download_links.items():
        extracted_csvs = []

        # Download and extract files for the current key
        for index, link in enumerate(links, start=1):
            downloaded_file = download_and_extract(link, combined_folder)
            if downloaded_file and downloaded_file.endswith('.csv'):
                print(f"Stored extracted CSV file: {downloaded_file}")
                extracted_csvs.append(downloaded_file)

        # Combine the downloaded CSV files into one CSV file for the current key
        if extracted_csvs:
            output_csv = os.path.join(combined_folder, f'{key.split(".")[0]}.csv')
            combine_csv(extracted_csvs, output_csv)

except FileNotFoundError:
    print(f"JSON file '{json_file}' not found.")

except Exception as e:
    print(f"An error occurred: {str(e)}")
