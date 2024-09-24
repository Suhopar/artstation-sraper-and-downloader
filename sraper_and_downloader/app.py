from flask import Flask, render_template, request, send_from_directory
import downloader
import scraper
import os

app = Flask(__name__)

# Path for saving downloaded images
DOWNLOAD_FOLDER = 'static/downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html', links=[], images=[])


@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    name_of_artist = request.form['artist_name']

    # Fetch the list of artwork links
    links = scraper.get_artwork_list(url)

    # Get image links from each artwork
    img_links = scraper.get_artwork_img_links_to_file_from_artwork_list(links, name_of_artist)

    # Display the links on the page
    return render_template('index.html', links=img_links, images=img_links)


@app.route('/download', methods=['POST'])
def download_image():
    name_of_artist = request.form['artist_name']
    print(name_of_artist)
    # Start the downloader
    downloader.downloader_img_of_links_from_file(name_of_artist)

    # Path to the artist's image folder
    artist_folder = os.path.join(DOWNLOAD_FOLDER, name_of_artist)

    # Check if the folder exists
    if not os.path.exists(artist_folder):
        return render_template('index.html', links=[], images=[], download_complete=False)

    # Get the list of downloaded images
    images = [f"/static/downloads/{name_of_artist}/{file}" for file in os.listdir(artist_folder) if
              file.endswith(('.png', '.jpg', '.jpeg'))]
    return render_template('index.html', links=[], images=images, download_complete=True)



if __name__ == '__main__':
    app.run(debug=True)
