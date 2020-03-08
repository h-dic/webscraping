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
    url_results = "https://hedrine.univ-grenoble-alpes.fr/htinteractions/hdi"

    def __init__(self):
        super().__init__()

    @classmethod
    def get_drugs_names(cls, connection):
        base_url = "https://hedrine.univ-grenoble-alpes.fr/drugs/view"
        nb_max = 659
        for index in range(1, nb_max+1):
            url = f"{base_url}/{index}"
            request = connection.session.get(url)
            html = BeautifulSoup(request.content, "html.parser")
            try:
                name = html.select(".drugs.view dl dd")[0]
                # Hedrine.drugs[index] = name.text.strip()
            except IndexError:
                pass

    @classmethod
    def get_herbs_names(cls, connection):
        base_url = "https://hedrine.univ-grenoble-alpes.fr/herbs/view"
        nb_max = 201
        for index in range(1, nb_max+1):
            url = f"{base_url}/{index}"
            request = connection.session.get(url)
            html = BeautifulSoup(request.content, "html.parser")
            try:
                name = html.select(".herbs.view dl dd")[0]
                # Hedrine.herbs[index] = name.text.strip()
            except IndexError:
                pass


class ConnectionMSKCC(Connection):

    def __init__(self):
        super().__init__(MSKCC(), "", "")