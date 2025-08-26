from bs4 import BeautifulSoup
from bs4 import Tag

from SendMessage import SendMessage

import requests
import sqlite3

class FetchPCI:
    def __init__ (self, url, start, end, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        self.url = url
        self.start = start
        self.end = end
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, "lxml")

    def _getDivs (self) -> list[Tag]:
        start_div = self.soup.find(**self.start)
        end_div = self.soup.find(**self.end)
        divs_between = []
        current = start_div.next_sibling
        
        while current and current != end_div:
            if current.name:
                divs_between.append(current)
            current = current.next_sibling
    
        return divs_between
    
    def get_string (self, s: Tag):
        return s.decode_contents().strip().replace('<br/>', '\n').replace('<span>', '').replace('</span>','')
    
    def _getData (self):
        div_data = self._getDivs()
        result = []

        for element in div_data:
            k_result = dict()
            k_result["public_body"] = element.select_one(".ca > a").text
            k_result["pci_link"] = element.select_one(".ca > a").get("href")
            k_result["pb_icon"] = element.select_one(".cb > img").get("data-src")
            k_result["location"] = element.select_one(".cc").text
            k_result["additional_info"] = self.get_string(element.select_one(".cd"))
            k_result["enrolment_upto"] = element.select_one(".ce > span").text
            result.append(k_result)

        return result
    
    def fetch_data (self):
        client = SendMessage()
        messages = []
        
        data = self._getData()
        for d in data:
            self.cursor.execute(f"SELECT * FROM news WHERE pci_link=?", (d['pci_link'].replace("'", "''").strip(), ))
            row = self.cursor.fetchone()
            if (not row):
                self.cursor.execute("INSERT INTO news (public_body, pci_link, pb_icon, location, additional_info, enrolment_upto) VALUES (?, ?, ?, ?, ?, ?)", tuple(d.values()))
                messages.append(f"*{d['public_body']}*\n\n{d['additional_info']}\n\nInscrições até: {d['enrolment_upto']}\n\nMais informações em: {d['pci_link']}")
        
        if not messages: return "There's nothing."
        self.conn.commit()
        return client.send("\n\n".join(messages))