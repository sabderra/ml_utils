from src.ml_utils.config.config import Config, load_conf
from src.ml_utils.db.couchdb_helper import CouchDBHelper
from cloudant.client import CouchDB
import pytest
import os


DB_NAME = "test_db"


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
            db = client[DB_NAME]
            test_conf = db['test_doc']
            test_conf.delete()

            client.delete_database(DB_NAME)
            print("Deleted")
        except KeyError:
            print("Nothing to deleted")

    def db_shutdown():
        client.disconnect()

    remove_doc()

    request.addfinalizer(remove_doc)

    return client


def test_create_database(username, password, url):
    db_helper = CouchDBHelper(DB_NAME, username, password, url=url)
    db_helper.create_database()
    db_helper.connect()
    db_helper.disconnect()


def test_save_config_file(username, password, url):
    conf_file = load_conf('conf.json', validate_config=True)
    c = conf_file.data
    assert c.name == "test"
    assert c.description == "Some text"
    assert c.train['batch_size'] == 128

    db_helper = CouchDBHelper(DB_NAME, username, password, url=url)
    db_helper.connect()
    db_helper.save("test_doc", conf_file)
    db_helper.disconnect()


def test_overwrite_config_file(username, password, url):
    conf_file = load_conf('conf.json', validate_config=True)
    c = conf_file.data
    assert c.name == "test"
    assert c.description == "Some text"
    assert c.train['batch_size'] == 128

    db_helper = CouchDBHelper(DB_NAME, username, password, url=url)
    db_helper.connect()
    db_helper.save("test_doc", conf_file, overwrite=True)
    db_helper.disconnect()

    db_helper = CouchDBHelper(DB_NAME, username, password, url=url)
    db_helper.connect()

    try:
        db_helper.save("test_doc", conf_file)
        assert True, 'expected FileExistsError'
    except FileExistsError:
        pass

    db_helper.disconnect()


def test_load_config_file(username, password, url):
    db_helper = CouchDBHelper(DB_NAME, username, password, url=url)
    db_helper.connect()

    data = db_helper.load("test_doc")
    conf = Config(data)
    c = conf.build()
    assert c.name == "test"
    assert c.description == "Some text"
    assert c.train['batch_size'] == 128

    db_helper.disconnect()


def test_update_config_file(username, password, url):
    db_helper = CouchDBHelper(DB_NAME, username, password, url=url)
    db_helper.connect()

    data = db_helper.load("test_doc")
    conf = Config(data)
    c = conf.build()
    assert c.name == "test"
    assert c.description == "Some text"
    assert c.train['batch_size'] == 128

    conf['train']['batch_size'] = 999
    db_helper.save("test_doc", conf, overwrite=True)

    payload = db_helper.load("test_doc")
    assert payload['train']['batch_size'] == 999

