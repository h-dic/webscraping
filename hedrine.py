import json
import sys

import bs4
import requests
from bs4 import BeautifulSoup
from connection import Connection


class Drug:

    def __init__(self):
        self.name = ""


class DrugHedrine(Drug):
    def __init__(self):
        super().__init__()


class Herb:

    def __init__(self):
        self.name = ""


class HerbHedrine(Herb):

    def __init__(self):
        super().__init__()





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

    color_to_intensity = {
        "rouge": "forte",
        "orange": "moyenne",
        "jaune": "faible",
        "blanc": "aucune",
        "mauve": "inconnue"
    }

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_intensity(raw_intensity):
        color = raw_intensity["class"][0]
        return Hedrine.color_to_intensity[color]

    @staticmethod
    def get_effect(raw_effect):
        return raw_effect.text.strip()

    @staticmethod
    def get_consequence(raw_consequence):
        return raw_consequence.text.strip()

    @classmethod
    def get_drugs_names(cls, connection):
        base_url = "https://hedrine.univ-grenoble-alpes.fr/drugs/view"
        nb_max = 659
        for index in range(1, nb_max + 1):
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
        for index in range(1, nb_max + 1):
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
        interactions = {
            "studies": Hedrine.treat_raw_studies(raw_studies),
            "possibilities": Hedrine.treat_raw_possibilities(raw_possibilities)
        }
        return interactions

    @staticmethod
    def treat_raw_studies(raw_studies):
        studies = raw_studies.select("tr:nth-child(3n+2)")
        studies_results = [Hedrine.treat_raw_study(raw_study) for raw_study in studies]
        return studies_results

    @staticmethod
    def treat_raw_study(raw_study):
        raw_effect = raw_study.select("td")[1]
        raw_intensity = raw_study.select("td")[2]
        study = {
            "effect": Hedrine.get_effect(raw_effect),
            "intensity": Hedrine.get_intensity(raw_intensity)
        }
        return study

    @staticmethod
    def treat_raw_possibilities(raw_possibilities):
        raw_possible_interactions = raw_possibilities.select("tr:nth-child(3n+3)")
        possibilities_results = [Hedrine.treat_raw_possible_interaction(interaction)
                                 for interaction in raw_possible_interactions]
        return possibilities_results

    @staticmethod
    def treat_raw_possible_interaction(raw_possible_interaction):
        raw_herb_effect = raw_possible_interaction.select("td")[0]
        raw_herb_intensity = raw_possible_interaction.select("td")[1]
        raw_consequence = raw_possible_interaction.select("td")[2]
        raw_drug_effect = raw_possible_interaction.select("td")[3]
        raw_drug_intensity = raw_possible_interaction.select("td")[4]
        interaction = {
            "herb_effect": Hedrine.treat_raw_herb_effect(raw_herb_effect),
            "herb_intensity": Hedrine.treat_raw_herb_intensity(raw_herb_intensity),
            "consequence": Hedrine.treat_raw_consequence(raw_consequence),
            "drug_effect": Hedrine.treat_raw_drug_effect(raw_drug_effect),
            "drug_intensity": Hedrine.treat_raw_drug_intensity(raw_drug_intensity)
        }
        return interaction

    @staticmethod
    def treat_raw_herb_effect(raw_herb_effect):
        return Hedrine.get_effect(raw_herb_effect)

    @staticmethod
    def treat_raw_herb_intensity(raw_herb_intensity):
        return Hedrine.get_intensity(raw_herb_intensity)

    @staticmethod
    def treat_raw_consequence(raw_consequence):
        return Hedrine.get_consequence(raw_consequence)

    @staticmethod
    def treat_raw_drug_effect(raw_drug_effect):
        return Hedrine.get_effect(raw_drug_effect)

    @staticmethod
    def treat_raw_drug_intensity(raw_drug_intensity):
        return Hedrine.get_intensity(raw_drug_intensity)

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


class ConnectionHedrine(Connection):

    def __init__(self, username, password):
        super().__init__(Hedrine(), username, password)




def test():
    username = sys.argv[1]
    password = sys.argv[2]
    connection_hedrine = ConnectionHedrine(username, password)
    herb_id = 26
    drug_id = 87
    raw_interactions = Hedrine.send_intersection(connection_hedrine, drug_id, herb_id)
    interactions = Hedrine.treat_raw_interactions(raw_interactions)
    print(json.dumps(interactions, ensure_ascii=False))
    connection_hedrine.close()


if __name__ == '__main__':
    test()
