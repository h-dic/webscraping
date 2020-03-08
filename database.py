import json


class Database:
    param_username = ""
    param_password = ""
    url_connection = ""
    param_herb = ""
    param_drug = ""
    url_results = ""
    herbs_file = ""
    drugs_file = ""

    def __init__(self):
        pass

    @classmethod
    def load_herbs(cls):
        with open(Database.herbs_file, "r", encoding=Database.file_encoding) as f:
            data = f.read()
            Database.herbs = json.loads(data)

    @classmethod
    def load_drugs(cls):
        with open(Database.drugs_file, "r", encoding=Database.file_encoding) as f:
            data = f.read()
            Database.drugs = json.loads(data)

    @classmethod
    def save_herbs(cls):
        with open(Database.herbs_file, "w", encoding=Database.file_encoding) as f:
            json.dump(Database.herbs, f, ensure_ascii=False)

    @classmethod
    def save_drugs(cls):
        with open(Database.drugs_file, "w", encoding=Database.file_encoding) as f:
            json.dump(Database.drugs, f, ensure_ascii=False)


class Drug:

    def __init__(self):
        self.name = ""
        self.family = ""
        self.url = ""


class Herb:

    def __init__(self):
        self.scientific_name = ""
        self.url = ""

    def other_names(self):
        pass
