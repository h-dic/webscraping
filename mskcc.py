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
    def get_other_names(herb):

        def get_page(herb):

            def herb_to_url(herb):

                def herb_name_to_url_name(herb_name):
                    return herb_name.replace(" ", "-")

                herbs_base_url = "https://www.mskcc.org/cancer-care/integrative-medicine/herbs"
                herb_url = f"{herbs_base_url}/{herb_name_to_url_name(herb)}"

            page = requests.get(herb_to_url(herb))
            return BeautifulSoup(page.content, 'html.parser')

        def treat_raw_name(raw_name):
            return raw_name.text.strip()

        herb_page = get_page(herb)
        raw_list_of_names = herb_page.select('.list-bullets li')
        return [treat_raw_name(herb) for herb in raw_list_of_names]


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
