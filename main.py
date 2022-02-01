import pathlib

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin


class Crawler:

    def __init__(self, site_url, dir_name, number_of_inner_pages_to_check):
        self.number_of_visited_websites = 0
        self.site_url = site_url
        self.dir_name = dir_name
        self.number_of_inner_pages_to_check = number_of_inner_pages_to_check
        self.dept_url_set = set()

    def get_html(self, url):
        request = requests.get(url)
        return request

    def get_soup(self, url):
        source = self.get_html(url)
        soup = BeautifulSoup(source.text, "html.parser")
        return soup

    # def crawl(self):
    #     source = self.get_html(self.site_url)
    #     soup = BeautifulSoup(source.text, "html.parser")
    #     self.check_directory(self.dir_name)  # create directory if does not exists
    #     for name in soup.findAll('a', href=True):  # iterate all href links
    #         zip_url = name['href']
    #         try:
    #             zip_link = requests.get(zip_url, stream=True)
    #             if zip_link.status_code == requests.codes.ok and\
    #                     zip_link.headers["Content-Type"] == "application/zip":  # check if the link is zip file
    #                 out_file_name = self.dir_name + "/" + zip_url.split('/')[-1]  # get the file name
    #                 f = open(out_file_name, "w")
    #                 f.write(zip_link.content)
    #                 f.close()
    #         except:
    #             pass

    def crawl(self):
        self.check_directory(self.dir_name)  # create directory if does not exists
        self.depth_crawl(self.site_url)

    def depth_crawl(self, url):
        if self.number_of_visited_websites <= self.number_of_inner_pages_to_check:
            soup = self.get_soup(url)
            for name in soup.findAll('a', href=True):  # iterate all href links
                href_link = name['href']
                try:
                    absolute_url = urljoin(url, href_link)
                    link = requests.get(absolute_url, stream=True)
                    if link.status_code == requests.codes.ok:
                        if link.headers["Content-Type"] == "application/zip":  # check if the link is zip file
                            out_file_name = self.dir_name + "/" + href_link.split('/')[-1]  # get the file name
                            f = open(out_file_name, "w")
                            f.write(link.content)
                            f.close()
                        elif "text/html" in link.headers["Content-Type"] and \
                                absolute_url not in self.dept_url_set:
                            # check if the file is html link, and check if we did not visit the same link twice
                            # (using set)
                            self.number_of_visited_websites += 1  # count the number of link clicked
                            self.dept_url_set.add(absolute_url)  # add to url_set
                            self.depth_crawl(absolute_url)  # recursive :)
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
    number_of_inner_pages_to_check = 6
    crawler = Crawler(url_with_zip, dir_name, number_of_inner_pages_to_check)
    crawler.crawl()
