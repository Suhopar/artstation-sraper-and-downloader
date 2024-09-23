import os
import requests

import datetime


def downloader_img_of_links_from_file(name_of_artist):
    print("downloader_img_of_links_from_file - START")
    os.mkdir("static/downloads/"+name_of_artist)
    file_lines = open(name_of_artist + "_links_of_img.txt", "r").readlines()
    name_of_img = name_of_artist + " - "
    for lin in file_lines:
        print('downloader_img_of_links_from_file - ' + str(len(file_lines)) + "/" + str(file_lines.index(lin) + 1))
        # print(str(file_lines.index(lin)))
        # print(lin.split('__'))
        if lin[0] == "_":
            name_of_img = name_of_artist + " - " + str(datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S"))+"__"

        elif lin[0] == '-':
            print(lin + " ---------------------- ")
            name_of_img = (name_of_artist.split('__')[0] + "__"
                           + str(file_lines.index(lin) + 1) + "_"
                           + (str(lin.split("/")[-1].split(".")[0])))
            # print(name_of_img)

            url_of_img = str(lin.split(' ')[2])
            img_data = requests.get(url_of_img).content
            with open(("static/downloads/"+ name_of_artist + "\\" + name_of_img + '.jpg'), 'wb') as handler:
                handler.write(img_data)
    print("downloader_img_of_links_from_file - OK")


if __name__ == '__main__':
    downloader_img_of_links_from_file("test_name")
