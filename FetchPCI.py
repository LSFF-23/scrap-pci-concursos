import requests
from bs4 import BeautifulSoup
from bs4 import Tag

class FetchPCI:
    def __init__ (self, url, start, end):
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
    
    def _getData (self):
        div_data = self._getDivs()
        result = []

        for element in div_data:
            k_result = dict()
            k_result["public_body"] = element.select_one(".ca > a").text
            k_result["pci_link"] = element.select_one(".ca > a").get("href")
            k_result["pb_icon"] = element.select_one(".cb > img").get("data-src")
            k_result["location"] = element.select_one(".cc").text
            k_result["additional_info"] = element.select_one(".cd").decode_contents().strip()
            k_result["enrolment_upto"] = element.select_one(".ce > span").text
            result.append(k_result)

        return result

if __name__ == "__main__":
    sb = FetchPCI("https://www.pciconcursos.com.br/concursos/nordeste/", {"id": "MA"}, {"id": "PB"})
    print(sb._getData())