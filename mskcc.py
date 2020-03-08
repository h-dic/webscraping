from bs4 import BeautifulSoup
from database import Database, Herb
import requests


class MSKCC(Database):
    herbs_file = "mskcc_herbs.json"
    drugs_file = None
    param_page = "page"
    file_encoding = "utf8"
    herbs_search_url = "https://www.mskcc.org/cancer-care/diagnosis-treatment/symptom-management/integrative-medicine/herbs/search"

    name = "MSKCC"

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_nb_herbs():
        page = requests.get(MSKCC.herbs_search_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        nb_herbs = soup.select(".msk-filtered-results__num")
        nb_herbs = nb_herbs[0]
        return 9
        # return nb_herbs / 10 + 1

    # @classmethod
    # def load_herbs(cls):
    #     with open(Hedrine.herbs_file, "r", encoding=Hedrine.file_encoding) as f:
    #         data = f.read()
    #         Hedrine.herbs = json.loads(data)
    #
    # @classmethod
    # def save_herbs(cls):
    #     with open(Hedrine.herbs_file, "w", encoding=Hedrine.file_encoding) as f:
    #         json.dump(Hedrine.herbs, f, ensure_ascii=False)

    @classmethod
    def load_herbs_from_site(cls):
        MSKCC.herbs = list()
        nb_herbs = MSKCC.get_nb_herbs()
        for i in range(nb_herbs // 10 + 1):
            parameters = {
                MSKCC.param_page: i
            }
            page = requests.get(MSKCC.herbs_search_url, params=parameters)
            soup = BeautifulSoup(page.content, 'html.parser')
            raw_herbs = soup.select(".baseball-card__link")
            MSKCC.herbs.extend([HerbMskcc(f"{HerbMskcc.urlBase}{herb_url['href']}") for herb_url in raw_herbs])

    # def get_json_dict(self):
    #     json = {
    #         MSKCC.json_name: MSKCC.name,
    #         MSKCC.json_herbs: MSKCC.get_json_herbs
    #     }
    #     return json















class HerbMskcc(Herb):

    urlBase = 'https://www.mskcc.org'

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.load_name_from_site()

    def get_url(self):
        return self.url

    def load_name_from_site(self):

        def treat_raw_name(raw_name):
            return raw_name.text.strip()

        page = self.get_page()
        raw_name = page.select(
            ".msk-left-rail__content .field.field--name-title.field--type-string.field--label-hidden")[0]
        self.name = treat_raw_name(raw_name)

    def get_name(self):
        if self.name is None:
            self.load_name_from_site()
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"""
    nom : {self.get_name()}
    url : {self.get_url()}
    other_names : {str(self.get_other_names())}
"""

    def load_other_names_from_site(self):

        def treat_raw_name(raw_name):
            return raw_name.text.strip()

        herb_page = self.get_page()
        raw_list_of_names = herb_page.select('.list-bullets li')
        self.other_names = [treat_raw_name(raw_name) for raw_name in raw_list_of_names]

    def get_other_names(self):
        if self.other_names is None:
            self.load_other_names_from_site()
        return self.other_names

    def get_page(self):
        page = requests.get(self.url)
        return BeautifulSoup(page.content, 'html.parser')











def test():
    MSKCC.load_herbs_from_site()
    for herb in MSKCC.herbs:
        print(repr(herb))
    for herb in MSKCC.herbs:
        print(repr(herb))


if __name__ == '__main__':
    test()
