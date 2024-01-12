import os
import requests
from bs4 import BeautifulSoup
import time
import re  

if not os.path.exists("images"):
    os.makedirs("images")

url = "https://www.gettyimages.in/photos/aamir-khan-actor"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")

image_elements = soup.find_all("img")

counter = 0

for image_element in image_elements:
    image_url = image_element.get("src")

    if image_url and image_url.startswith("https://media.gettyimages.com"):
        try:
            filename = re.sub(r'[^a-zA-Z0-9_.-]', '', image_url.split("/")[-1])

            response = requests.get(image_url, headers=headers)

            response.raise_for_status()

            with open(f"images/{filename}", "wb") as file:
                file.write(response.content)

            counter += 1

            print(f"Downloaded image {counter}: {image_url}")

            if counter == 60:
                break

            time.sleep(1)

        except Exception as e:
            print(f"Error downloading image {image_url}: {e}")

print(f"\nTotal number of downloaded images: {counter}")
print("Path to the downloaded images:", os.path.abspath("images"))
