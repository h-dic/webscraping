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
    herbs = list()
    drugs = list()
    file_encoding = "utf8"

    json_name = "name"
    json_herbs = "herbs"
    json_drugs = "drugs"

    def __init__(self):
        pass

    @classmethod
    def load_herbs_from_file(cls):
        with open(Database.herbs_file, "r", encoding=Database.file_encoding) as f:
            data = f.read()
            Database.herbs = json.loads(data)

    @classmethod
    def load_drugs_from_file(cls):
        with open(Database.drugs_file, "r", encoding=Database.file_encoding) as f:
            data = f.read()
            Database.drugs = json.loads(data)

    @classmethod
    def save_herbs_to_file(cls):
        with open(Database.herbs_file, "w", encoding=Database.file_encoding) as f:
            json.dump(Database.herbs, f, ensure_ascii=False)

    @classmethod
    def save_drugs_to_file(cls):
        with open(Database.drugs_file, "w", encoding=Database.file_encoding) as f:
            json.dump(Database.drugs, f, ensure_ascii=False)

    @classmethod
    def load_herbs_from_site(cls):
        pass

    @classmethod
    def load_drugs_from_site(cls):
        pass

    def get_json_dict(self):
        pass


class Drug:

    json_name = "name"
    json_family = "family"
    json_url = "url"

    def __init__(self):
        self.name = None
        self.family = None
        self.url = None

    def load_name_from_site(self):
        pass

    def get_name(self):
        pass

    def get_url(self):
        pass

    def get_family(self):
        pass

    def get_json_dict(self):
        json = {
            Drug.json_name: self.get_name(),
            Drug.json_family: self.get_family(),
            Drug.json_url: self.get_url()
        }
        return json


class Herb:

    json_name = "name"
    json_url = "url"
    json_other_names = "other_names"

    def __init__(self):
        self.name = None
        self.url = None
        self.other_names = None

    def load_name_from_site(self):
        pass

    def load_other_names_from_site(self):
        pass

    def get_other_names(self):
        return self.other_names

    def get_page(self):
        pass

    def get_name(self):
        pass

    def get_url(self):
        pass

    def get_json_dict(self):
        json = {
            Herb.json_name: self.get_name(),
            Herb.json_other_names: self.get_other_names(),
            Herb.json_url: self.get_url()
        }
        return json
