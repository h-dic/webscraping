import json
import sys

import requests
from bs4 import BeautifulSoup


class Database:

    param_username = ""
    param_password = ""
    url_connection = ""
    param_herb = ""
    param_drug = ""
    url_results = ""

    def __init__(self):
        pass


class Hedrine(Database):

    drugs = dict()
    herbs = dict()
    herbs_file = "hedrine_herbs.json"
    drugs_file = "hedrine_drugs.json"
    file_encoding = "utf8"
    param_herb = "data[htinteraction][herb_id]"
    param_drug = "data[dtinteraction][drug_id]"
    param_username = "data[User][username]"
    param_password = "data[User][password]"
    url_connection = "https://hedrine.univ-grenoble-alpes.fr/users/login"
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
                Hedrine.drugs[index] = name.text.strip()
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
                Hedrine.herbs[index] = name.text.strip()
            except IndexError:
                pass

    @classmethod
    def send_intersection(cls, connection, drug_id, herb_id):
        parameters = {
            cls.param_drug: drug_id,
            cls.param_herb: herb_id
        }
        request = connection.session.post(cls.url_results, parameters)
        html = BeautifulSoup(request.content, "html.parser")
        raw_interactions = html.select(".hdi.index")
        return raw_interactions

    @staticmethod
    def treat_raw_interactions(raw_interactions):
        raw_studies = raw_interactions[0]
        raw_possibilities = raw_interactions[1]
        studies_results = Hedrine.treat_raw_studies(raw_studies)
        possibilities_results = Hedrine.treat_raw_studies(raw_possibilities)

    @staticmethod
    def treat_raw_studies(raw_studies):
        try:
            effect = raw_studies.select("td")[1]
            print(f"effect : {effect}")
            intensity = raw_studies.select("td")[2]
            print(f"intensity : {intensity}")
        except IndexError:
            pass
        studies_results = None
        return studies_results

    @staticmethod
    def treat_raw_possibilities(raw_studies):
        raw_possible_interactions = raw_studies.select("tr:nth-child(3n+3)")
        possibilities_results = [Hedrine.treat_raw_possible_interaction(interaction) for interaction in raw_possible_interactions]
        return possibilities_results

    @staticmethod
    def treat_raw_possible_interaction(raw_possible_interaction):

        possibilities_results = None
        return possibilities_results

    @classmethod
    def load_herbs(cls):
        with open(Hedrine.herbs_file, "r", encoding=Hedrine.file_encoding) as f:
            data = f.read()
            Hedrine.herbs = json.loads(data)

    @classmethod
    def load_drugs(cls):
        with open(Hedrine.drugs_file, "r", encoding=Hedrine.file_encoding) as f:
            data = f.read()
            Hedrine.drugs = json.loads(data)

    @classmethod
    def save_herbs(cls):
        with open(Hedrine.herbs_file, "w", encoding=Hedrine.file_encoding) as f:
            json.dump(Hedrine.herbs, f, ensure_ascii=False)

    @classmethod
    def save_drugs(cls):
        with open(Hedrine.drugs_file, "w", encoding=Hedrine.file_encoding) as f:
            json.dump(Hedrine.drugs, f, ensure_ascii=False)


class MSKCC(Database):

    def __init__(self):
        super().__init__()


class Connection:

    def __init__(self, database, username, password):
        self.username = username
        self.password = password
        self.database = database
        self.session = requests.Session()
        self.connection()

    def connection(self):
        parameters = {
            self.database.param_username: self.username,
            self.database.param_password: self.password
        }
        self.session.post(self.database.url_connection, data=parameters)

    def close(self):
        self.session.close()


class ConnectionHedrine(Connection):

    def __init__(self, username, password):
        super().__init__(Hedrine(), username, password)


class ConnectionMSKCC(Connection):

    def __init__(self):
        super().__init__(MSKCC(), "", "")


def test():
    username = sys.argv[1]
    password = sys.argv[2]
    connection_hedrine = ConnectionHedrine(username, password)
    interactions = Hedrine.send_intersection(connection_hedrine, 1, 1)
    Hedrine.treat_raw_interactions(interactions)
    connection_hedrine.close()


if __name__ == '__main__':
    test()
