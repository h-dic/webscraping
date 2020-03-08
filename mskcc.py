from bs4 import BeautifulSoup
from database import Database
import requests


class MSKCC(Database):
    drugs = dict()
    herbs = dict()
    herbs_file = "mskcc_herbs.json"
    drugs_file = "mskcc_drugs.json"
    param_page = "page"
    file_encoding = "utf8"
    herbs_search_url = "https://www.mskcc.org/cancer-care/diagnosis-treatment/symptom-management/integrative-medicine/herbs/search"

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_nb_herbs():
        page = requests.get(MSKCC.herbs_search_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        nb_herbs = soup.select(".msk-filtered-results__num")
        nb_herbs = nb_herbs[0]
        return int(nb_herbs.text)

    @staticmethod
    def get_herbs_names():
        herbs_names = []
        nb_herbs = MSKCC.get_nb_herbs()
        for i in range(nb_herbs // 10 + 1):
            parameters = {
                MSKCC.param_page: i
            }
            page = requests.get(MSKCC.herbs_search_url, params=parameters)
            soup = BeautifulSoup(page.content, 'html.parser')
            raw_herbs_names = soup.select(".baseball-card__link")
            herbs_names.extend([herb.text.strip() for herb in raw_herbs_names])
        return herbs_names

    @staticmethod
    def get_herbs_other_name(herb):

        def herb_name_to_url_name(herb_name):
            return herb.replace(" ", "-")

        url_herbs_base = "https://www.mskcc.org/cancer-care/integrative-medicine/herbs/"
        page = requests.get(url_herbs_base + herb_name_to_url_name(herb))
        soup = BeautifulSoup(page.content, 'html.parser')
        list_a_puce = soup.select('.list-bullets li')
        return [val.get_text() for val in list_a_puce]


    # @classmethod
    # def load_herbs(cls):
    #     with open(Hedrine.herbs_file, "r", encoding=Hedrine.file_encoding) as f:
    #         data = f.read()
    #         Hedrine.herbs = json.loads(data)
    #
    # @classmethod
    # def load_drugs(cls):
    #     with open(Hedrine.drugs_file, "r", encoding=Hedrine.file_encoding) as f:
    #         data = f.read()
    #         Hedrine.drugs = json.loads(data)
    #
    # @classmethod
    # def save_herbs(cls):
    #     with open(Hedrine.herbs_file, "w", encoding=Hedrine.file_encoding) as f:
    #         json.dump(Hedrine.herbs, f, ensure_ascii=False)
    #
    # @classmethod
    # def save_drugs(cls):
    #     with open(Hedrine.drugs_file, "w", encoding=Hedrine.file_encoding) as f:
    #         json.dump(Hedrine.drugs, f, ensure_ascii=False)


def test():
    herbs_names = MSKCC.get_herbs_names()
    print(herbs_names)


if __name__ == '__main__':
    test()
