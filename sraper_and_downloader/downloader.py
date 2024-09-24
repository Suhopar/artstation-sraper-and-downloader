import os
import requests

import datetime


def downloader_img_of_links_from_file(name_of_artist):
    print("downloader_img_of_links_from_file - START")

    # Create a directory to store downloaded images for the artist
    os.mkdir("static/downloads/"+name_of_artist)

    # Read the lines from the file containing image links
    file_lines = open(name_of_artist + "_links_of_img.txt", "r").readlines()
    name_of_img = name_of_artist + " - "

    # Loop through each line in the file
    for lin in file_lines:
        print('downloader_img_of_links_from_file - ' + str(len(file_lines)) + "/" + str(file_lines.index(lin) + 1))
        # print(str(file_lines.index(lin)))
        # print(lin.split('__'))

        # Check if the line starts with an underscore (indicating a section header)
        if lin[0] == "_":
            # Set the image name to include the current timestamp
            name_of_img = name_of_artist + " - " + str(datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S"))+"__"

        # Check if the line starts with a hyphen (indicating an image link)
        elif lin[0] == '-':
            print(lin + " ---------------------- ")

            # Construct the image name based on the artist's name and the index of the link
            name_of_img = (name_of_artist.split('__')[0] + "__"
                           + str(file_lines.index(lin) + 1) + "_"
                           + (str(lin.split("/")[-1].split(".")[0])))
            # print(name_of_img)

            # Extract the image URL from the line
            url_of_img = str(lin.split(' ')[2])

            # Download the image data from the URL
            img_data = requests.get(url_of_img).content

            # Save the image data to a file in the artist's downloads directory
            with open(("static/downloads/"+ name_of_artist + "\\" + name_of_img + '.jpg'), 'wb') as handler:
                handler.write(img_data)
    print("downloader_img_of_links_from_file - OK")


if __name__ == '__main__':
    downloader_img_of_links_from_file("test_name")
