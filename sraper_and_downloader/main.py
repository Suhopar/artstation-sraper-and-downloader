import downloader
import scraper
if __name__ == '__main__':
    name_of_artist = "angrysnail"
    url = 'https://www.artstation.com/angrysnail'

    # --- scraper
    print("---scraper---")
    links = scraper.get_artwork_list(url)
    scraper.get_artwork_img_links_to_file_from_artwork_list(links, name_of_artist)

    # --- downloader
    # print("---downloader---")
    # downloader.downloader_img_of_links_from_file(name_of_artist)
