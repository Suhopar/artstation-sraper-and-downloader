from flask import Flask, render_template, request, send_from_directory
import downloader
import scraper
import os

app = Flask(__name__)

# Шлях для збереження завантажених зображень
DOWNLOAD_FOLDER = 'static/downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html', links=[], images=[])


@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    name_of_artist = request.form['artist_name']

    # Отримання списку посилань на роботи
    links = scraper.get_artwork_list(url)

    # Отримання посилань на зображення з кожної роботи
    img_links = scraper.get_artwork_img_links_to_file_from_artwork_list(links, name_of_artist)

    # Відображення посилань на сторінці
    return render_template('index.html', links=img_links, images=img_links)


@app.route('/download', methods=['POST'])
def download_image():
    name_of_artist = request.form['artist_name']
    print(name_of_artist)
    # Запускаємо завантажувач
    downloader.downloader_img_of_links_from_file(name_of_artist)

    # Шлях до папки зображень конкретного артиста
    artist_folder = os.path.join(DOWNLOAD_FOLDER, name_of_artist)

    # Перевірка, чи папка існує
    if not os.path.exists(artist_folder):
        return render_template('index.html', links=[], images=[], download_complete=False)

    # Отримання списку завантажених зображень
    images = [f"/static/downloads/{name_of_artist}/{file}" for file in os.listdir(artist_folder) if
              file.endswith(('.png', '.jpg', '.jpeg'))]
    return render_template('index.html', links=[], images=images, download_complete=True)



if __name__ == '__main__':
    app.run(debug=True)
