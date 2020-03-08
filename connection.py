import requests


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
