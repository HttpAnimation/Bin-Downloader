import os
import requests
import time

# Function to download a file from a URL and save it in the specified directory
def download_file(url, directory):
    filename = url.split("/")[-1]  # Extract the filename from the URL
    filepath = os.path.join(directory, filename)
    response = requests.get(url)
    with open(filepath, "wb") as file:
        file.write(response.content)

# List of input text files
text_files = ["audio.txt", "documents.txt", "photo.txt", "videos.txt", "devices.txt", "pdf.txt"]

# Read the last downloaded file from 'last_downloaded.txt' if it exists
if os.path.exists("last_downloaded.txt"):
    with open("last_downloaded.txt", "r") as file:
        last_downloaded = file.read().strip()
else:
    last_downloaded = ""

# Process each text file
for text_file in text_files:
    # Create a directory with the same name as the text file (without the extension)
    directory = os.path.splitext(text_file)[0]
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

    # Read the URLs from the text file
    with open(text_file, "r", encoding='utf-8') as file:
        urls = file.read().splitlines()

    # Find the index of the last downloaded file, if it exists in the current text file
    if last_downloaded and last_downloaded in urls:
        start_index = urls.index(last_downloaded) + 1
    else:
        start_index = 0

    # Download the files from the URLs and save them in the directory
    total_files = len(urls)
    for i in range(start_index, total_files):
        url = urls[i]
        print(f"Downloading file {i+1}/{total_files} from {text_file}: {url}")
        try:
            download_file(url, directory)
            print(f"Downloaded file {i+1}/{total_files} into {directory} directory.")
        except Exception as e:
            print(f"Error downloading file {i+1}/{total_files}: {e}")
            break

        # Save the last downloaded file to 'last_downloaded.txt'
        with open("last_downloaded.txt", "w") as file:
            file.write(url)

        if i < total_files - 1:
            print("Waiting 1 seconds before downloading the next file...")
            time.sleep(1)

    print(f"Downloaded {i+1} files from {text_file} into {directory} directory.")

# Remove 'last_downloaded.txt' after all files have been downloaded
if os.path.exists("last_downloaded.txt"):
    os.remove("last_downloaded.txt")

