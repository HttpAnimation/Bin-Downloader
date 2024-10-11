import os
import requests
import time

def download_file(url, directory):
    filename = url.split("/")[-1]
    filepath = os.path.join(directory, filename)
    response = requests.get(url)
    with open(filepath, "wb") as file:
        file.write(response.content)

text_files = ["photo.txt"]

if os.path.exists("last_downloaded.txt"):
    with open("last_downloaded.txt", "r", encoding='utf-8') as file:
        last_downloaded = file.read().strip()
else:
    last_downloaded = ""

for text_file in text_files:
    directory = os.path.splitext(text_file)[0]
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

    with open(text_file, "r", encoding='utf-8') as file:
        urls = file.read().splitlines()

    if last_downloaded and last_downloaded in urls:
        start_index = urls.index(last_downloaded) + 1
    else:
        start_index = 0

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

        with open("last_downloaded.txt", "w", encoding='utf-8) as file:
            file.write(url)

        if i < total_files - 1:
            print("Waiting 1 seconds before downloading the next file...")
            time.sleep(1)

    print(f"Downloaded {i+1} files from {text_file} into {directory} directory.")

if os.path.exists("last_downloaded.txt"):
    os.remove("last_downloaded.txt")
