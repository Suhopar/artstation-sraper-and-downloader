import time
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options
from concurrent.futures import as_completed


# Функція для завантаження списку проектів (посилання на окремі роботи)
def get_artwork_list(url):
    print("get_artwork_list - START")

    # Ініціалізація драйвера
    options = Options()
    options.add_argument("--window-size=0,0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.minimize_window()
    driver.get(url)

    # Скролінг для завантаження контенту
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Скролимо сторінку донизу
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Парсинг сторінки після скролінгу
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Знаходимо всі посилання на окремі роботи (наприклад, https://www.artstation.com/artwork/RKy3RE)
    for_links = soup.find_all("a", href=True)
    links = []

    for link in for_links:
        href = link.get('href')
        if '/artwork/' in href:
            full_link = href
            links.append(full_link)

    driver.quit()  # Закриваємо драйвер
    print("get_artwork_list - OK")

    # Виводимо знайдені посилання
    for l in links:
        print(l)

    return links


# Функція для отримання посилань на зображення з одного проекту
def process_single_artwork(link, name_of_artist, index, total_artworks):
    print(f'Processing artwork {index}/{total_artworks}: {link}')

    options = Options()
    options.add_argument("--window-size=0,0")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.minimize_window()
    driver.get(link)
    time.sleep(1)  # Мінімізуємо час очікування

    # Парсимо сторінку проекту
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()  # Закриваємо драйвер після отримання сторінки

    # Знаходимо всі теги <picture> із зображеннями
    for_img_links = soup.find_all("picture", {"class": "d-flex"})
    print(f'Found {len(for_img_links)} images in artwork {index}')

    # Збираємо посилання на зображення у список
    img_links_for_app = []
    for picture_tag in for_img_links:
        img_tag = picture_tag.find('img')
        if img_tag:
            img_url = img_tag.get('src')  # Беремо посилання з атрибуту src
            img_links_for_app.append(img_url)

    with open(f'{name_of_artist}_links_of_img.txt', 'a') as file:
        file.write(f"\n__LINKS FOR ARTWORK {index}:__\n")
        for i, picture_tag in enumerate(for_img_links, start=1):
            img_tag = picture_tag.find('img')
            if img_tag:
                img_url = img_tag.get('src')  # Беремо посилання з атрибуту src
                file.write(f'- {i}. {img_url}\n')
                print(img_url)
    file.close()

    return img_links_for_app  # Повертаємо список посилань на зображення


# Функція для отримання посилань на зображення з усіх проектів за допомогою багатопоточності
def get_artwork_img_links_to_file_from_artwork_list(artwork_list, name_of_artist):
    print("get_artwork_img_links_to_file_from_artwork_list - START")

    total_artworks = len(artwork_list)
    results_list = []  # Список для зберігання результатів

    # Використовуємо ThreadPoolExecutor для багатопоточної обробки
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        # Запускаємо обробку кожного проекту паралельно
        for index, link in enumerate(artwork_list, start=1):
            future = executor.submit(process_single_artwork, link, name_of_artist, index, total_artworks)
            futures.append(future)

        # Чекаємо завершення всіх завдань
        for future in as_completed(futures):
            results = future.result()
            if results:  # Якщо є результати, додаємо до загального списку
                results_list.extend(results)

    print("get_artwork_img_links_to_file_from_artwork_list - OK")
    return results_list  # Повертаємо список всіх зображень

# Основний блок програми
if __name__ == '__main__':
    name_of_artist = "test_name"
    # Отримуємо список посилань на роботи
    links = get_artwork_list('https://www.artstation.com/test_name')

    # Отримуємо посилання на зображення з кожної роботи з багатопоточною обробкою
    get_artwork_img_links_to_file_from_artwork_list(links, name_of_artist)
