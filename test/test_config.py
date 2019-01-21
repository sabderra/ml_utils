from src.ml_utils.config.config import Config
from jsonschema import validate
import json
import pytest
import os


def test_schema():

    with open('conf_schema.json') as schema_file:
        schema = json.load(schema_file)

    with open('conf.json') as conf_file:
        conf = json.load(conf_file)

    validate(conf, schema)


def test_conf_object_build():

    with open('conf.json') as conf_file:
        conf = json.load(conf_file)

    conf = Config(conf)
    c = conf.build()
    assert c.name == "test"
    assert c.description == "Some text"
    assert c.train['batch_size'] == 128


def test_conf_object_build_validate():

    with open('conf.json') as conf_file:
        conf = json.load(conf_file)

    conf = Config(conf)
    c = conf.build(validate_config=True)
    assert c.name == "test"
    assert c.description == "Some text"
    assert c.train['batch_size'] == 128


def test_conf_build_validate():

    with open('conf.json') as conf_file:
        conf = json.load(conf_file)

    conf = Config(conf)
    assert conf['name'] == "test"
    assert conf['train']['batch_size'] == 128


def test_load_config_file():
    conf = Config()
    c = conf.load('conf.json', validate_config=True)
    assert c.name == "test"
    assert c.description == "Some text"
    assert c.train['batch_size'] == 128


def test_expand():
    conf = Config()
    c = conf.load('conf.json', validate_config=True)
    print(*c)


def test_save_no_overwrite():
    with pytest.raises(FileExistsError) as e_info:
        conf = Config()
        c = conf.load('conf.json', validate_config=True)
        conf.save('conf.json')


def test_save_write():
    test_file = 'conf2.json'
    conf = Config()
    c = conf.load('conf.json', validate_config=True)
    conf.save(test_file, overwrite=True)
    c = conf.load(test_file, validate_config=True)
    conf.save(test_file, overwrite=True)
    os.remove(test_file)
