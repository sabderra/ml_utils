from cloudant.client import CouchDB
import sys


class CouchDBHelper:

    def __init__(self, database, username, password, url='http://127.0.0.1:5984'):
        self.database = database
        self.username = username
        self.password = password
        self.url = url
        self.client = None
        self.db = None

    def create_database(self):
        self.client = CouchDB(self.username, self.password, url=self.url, connect=True)
        self.client.create_database(self.database)

    def connect(self):
        if self.client is None:
            self.client = CouchDB(self.username, self.password, url=self.url, connect=True)
        self.db = self.client[self.database]

    def disconnect(self):
        self.client.disconnect()

    def load(self, doc_name):
        try:
            doc_json = self.db[doc_name]
        except KeyError:
            print("Unexpected error:", sys.exc_info()[0])
            raise FileNotFoundError

        return doc_json['payload']

    def save(self, doc_name, payload, overwrite=False):

        try:
            doc = self.db[doc_name]

            if not overwrite and doc.exists():
                raise FileExistsError(doc_name)

            doc['payload'] = payload
            doc.save()
            return

        except KeyError:
            pass

        # doc does not exist create
        doc = {'_id': doc_name, 'payload': payload}
        return self.db.create_document(doc)
