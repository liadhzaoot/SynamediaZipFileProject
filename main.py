import pathlib

import requests
from bs4 import BeautifulSoup
import os

class Crawler:

    def __init__(self, site_url, dir_name):
        self.site_url = site_url
        self.dir_name = dir_name

    def get_html(self):
        request = requests.get(self.site_url)
        return request

    def crawl(self):
        source = self.get_html()
        soup = BeautifulSoup(source.text, "html.parser")
        self.check_directory(self.dir_name)  # create directory if does not exists
        for name in soup.findAll('a', href=True):  # iterate all href links
            zip_url = name['href']
            try:
                zip_link = requests.get(zip_url, stream=True)
                if zip_link.status_code == requests.codes.ok and zip_link.headers["Content-Type"] == "application/zip":  # check if the link is zip file
                    out_file_name = self.dir_name + "/" + zip_url.split('/')[-1]  # get the file name
                    f = open(out_file_name, "w")
                    f.write(zip_link.content)
                    f.close()
            except:
                pass

    def check_directory(self, dir_name):
        try:
            os.mkdir(dir_name)
        except:  # the file exists
            pass


if __name__ == "__main__":
    url_fake_zip = "https://www.nku.edu/~kenneyr/Buddhism/lib/bulk.html"
    url_with_zip = 'http://www.google.com/googlebooks/uspto-patents-grants.html'
    dir_name = "zip_directory"
    crawler = Crawler(url_with_zip, dir_name)
    crawler.crawl()


