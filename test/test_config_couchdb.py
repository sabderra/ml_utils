from src.ml_utils.config.config import Config
from config_couchdb import ConfigCouchDB
from cloudant.client import CouchDB
import pytest
import os


@pytest.fixture(scope="module")
def username():
    return os.environ['USERNAME']


@pytest.fixture(scope="module")
def password():
    return os.environ['PASSWORD']


@pytest.fixture(scope="module")
def url():
    return os.environ['URL']


@pytest.fixture(scope="session", autouse=True)
def db_cleanup(request):

    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    url = os.environ['URL']

    client = CouchDB(username, password, url=url, connect=True)

    def remove_doc():
        try:
            db = client['engine']
            test_conf = db['test_doc']
            test_conf.delete()
            print("Deleted")
        except KeyError:
            print("Nothing to deleted")

    def db_shutdown():
        client.disconnect()

    remove_doc()

    request.addfinalizer(remove_doc)

    return client


def test_save_config_file(username, password, url):
    conf_file = Config()
    c = conf_file.load('conf.json', validate_config=True)
    assert c.name == "test"
    assert c.description == "Some text"
    assert c.train['batch_size'] == 128

    conf = ConfigCouchDB("engine", username, password, url=url)
    conf.update(conf_file)
    conf.save("test_doc")


def test_load_config_file(username, password, url):
    conf = ConfigCouchDB("engine", username, password, url=url)
    c = conf.load("test_doc", validate_config=False)
    assert c.name == "test"
    assert c.description == "Some text"
    assert c.train['batch_size'] == 128

