from bs4 import BeautifulSoup
from connection import Connection
from database import Database


class MSKCC(Database):

    drugs = dict()
    herbs = dict()
    herbs_file = "mskcc_herbs.json"
    drugs_file = "mskcc_drugs.json"
    file_encoding = "utf8"
    param_herb = "data[htinteraction][herb_id]"
    param_drug = "data[dtinteraction][drug_id]"
    url_results = "https://www.mskcc.org/cancer-care/diagnosis-treatment/symptom-management/integrative-medicine/herbs/search"

    def __init__(self):
        super().__init__()


    @classmethod
    def get_nb_herbs(cls):
        page = requests.get(cls.url_results)
        soup = BeautifulSoup(page.content, 'html.parser')
        nb_herbs = soup.find_all('span', class_='msk-filtered-results__num')
        nb_herbs = list(nb_herbs)[0]
        return nb_herbs.get_text()

    @classmethod
    def get_herbs_names(cls, connection):
        herb_name = []
        nbherb = cls.get_nb_herbs()
        for i in range(nbherb // 10 + 1):
            page = requests.get(cls.baseUrl + "?page=" + str(i))
            soup = BeautifulSoup(page.content, 'html.parser')
            proteines_price_from = soup.find_all('a', class_='baseball-card__link')
            tmp_herbs = [val.text.strip() for val in proteines_price_from]
            herb_name.extend(tmp_herbs)
        return herb_name

    @classmethod
    def get_herbs_other_name(cls,herbCible):
        urlHerbsBase = "https://www.mskcc.org/cancer-care/integrative-medicine/herbs/"
        page = requests.get(urlHerbsBase + herbCible.replace(" ", "-"))
        soup = BeautifulSoup(page.content, 'html.parser')
        listapuce = soup.select('.list-bullets li')
        return [val.get_text() for val in listapuce]