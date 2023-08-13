# import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import numpy as np
import requests


# implement crawler for crawling xml file
class crawling:
    def __init__(self, browser):
        self.browser = browser

    def navigate_to_dblp(self):
        sleep(np.random.randint(2, 6))
        dblp_url = "https://dblp.org/"
        self.browser.get(dblp_url)
        sleep(np.random.randint(2, 6))
        return self.browser

    def author_searching_function(self, authorname):
        searching_options_selector = "#search-mode-selector > div.head > img"
        searching_options = self.browser.find_element(
            By.CSS_SELECTOR,
            searching_options_selector,
        )
        searching_options.click()
        searching_author_selector = "#search-mode-author"
        searching_authors = self.browser.find_element(
            By.CSS_SELECTOR,
            searching_author_selector,
        )
        searching_authors.click()
        sleep(np.random.randint(2, 6))
        author_name_xpath = "/html/body/div[2]/div[2]/form/input"
        author_name_searching = self.browser.find_element(
            By.XPATH,
            author_name_xpath,
        )
        author_name_searching.send_keys(authorname)
        author_name_searching.send_keys(Keys.ENTER)
        sleep(np.random.randint(2, 6))
        author_chosen_selector = (
            "#completesearch-authors > div > ul:nth-child(2) > li > a"
        )
        author_chosen = self.browser.find_element(
            By.CSS_SELECTOR,
            author_chosen_selector,
        )
        author_chosen.click()
        return self.browser

    def access_author_link(self):
        sleep(np.random.randint(2, 6))
        xml_selector = "#headline > nav > ul > li.export.drop-down > div.body > ul:nth-child(2) > li:nth-child(6) > a"

        xml_option = self.browser.find_element(By.CSS_SELECTOR, xml_selector)
        xml_link = xml_option.get_attribute("href")
        return xml_link

    def download_xml(self, author_name, xml_link):
        author_name = author_name.replace(" ", "")
        filename = f"{author_name}.xml"
        response = requests.get(xml_link)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded {filename} successfully.")
        else:
            print(f"Failed to download {filename}. Status code: {response.status_code}")
        sleep(5)
        self.browser.close()
        return filename
