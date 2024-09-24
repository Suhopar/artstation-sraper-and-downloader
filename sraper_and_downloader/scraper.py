import time
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options
from concurrent.futures import as_completed


# Function to download the list of projects (links to individual works)
def get_artwork_list(url):
    print("get_artwork_list - START")

    # Initialize the driver
    options = Options()
    options.add_argument("--window-size=0,0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.minimize_window()
    driver.get(url)

    # Scrolling to load content
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Parsing the page after scrolling
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Finding all links to individual works (e.g., https://www.artstation.com/artwork/LAkmk)
    for_links = soup.find_all("a", href=True)
    links = []

    for link in for_links:
        href = link.get('href')
        if '/artwork/' in href:
            full_link = href
            links.append(full_link)

    driver.quit()  # Close the driver
    print("get_artwork_list - OK")

    # Output the found links
    for l in links:
        print(l)

    return links


# Function to get image links from a single project
def process_single_artwork(link, name_of_artist, index, total_artworks):
    print(f'Processing artwork {index}/{total_artworks}: {link}')

    options = Options()
    options.add_argument("--window-size=0,0")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.minimize_window()
    driver.get(link)
    time.sleep(1)  # Minimize wait time

    # Parsing the project page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()  # Close the driver after fetching the page

    # Finding all <picture> tags with images
    for_img_links = soup.find_all("picture", {"class": "d-flex"})
    print(f'Found {len(for_img_links)} images in artwork {index}')

    # Collecting image links into a list
    img_links_for_app = []
    for picture_tag in for_img_links:
        img_tag = picture_tag.find('img')
        if img_tag:
            img_url = img_tag.get('src')  # Get the link from the src attribute
            img_links_for_app.append(img_url)

    with open(f'{name_of_artist}_links_of_img.txt', 'a') as file:
        file.write(f"\n__LINKS FOR ARTWORK {index}:__\n")
        for i, picture_tag in enumerate(for_img_links, start=1):
            img_tag = picture_tag.find('img')
            if img_tag:
                img_url = img_tag.get('src')  # Get the link from the src attribute
                file.write(f'- {i}. {img_url}\n')
                print(img_url)
    file.close()

    return img_links_for_app  # Return the list of image links


# Function to get image links from all projects using multithreading
def get_artwork_img_links_to_file_from_artwork_list(artwork_list, name_of_artist):
    print("get_artwork_img_links_to_file_from_artwork_list - START")

    total_artworks = len(artwork_list)
    results_list = []  # List to store results

    # Use ThreadPoolExecutor for multithreaded processing
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        # Start processing each project in parallel
        for index, link in enumerate(artwork_list, start=1):
            future = executor.submit(process_single_artwork, link, name_of_artist, index, total_artworks)
            futures.append(future)

        # Wait for all tasks to complete
        for future in as_completed(futures):
            results = future.result()
            if results:   # If there are results, add to the overall list
                results_list.extend(results)

    print("get_artwork_img_links_to_file_from_artwork_list - OK")
    return results_list  # Return the list of all images

# For test
if __name__ == '__main__':
    name_of_artist = "test_name"
    # Get the list of links to works
    links = get_artwork_list('https://www.artstation.com/test_name')

    # Get image links from each work with multithreading
    get_artwork_img_links_to_file_from_artwork_list(links, name_of_artist)
