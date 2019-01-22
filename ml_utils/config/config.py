import json
from collections import namedtuple
from jsonschema import validate
from pathlib import Path

default_schema = {
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "description": {"type": "string"},
    "train": {
      "type": "object",
      "properties": {
          "batch_size": {"type": "number"},
          "seq_length": {"type": "number"},
          "steps_per_epoch": {"type": "number"},
          "validation_steps": {"type": "number"},
          "num_epochs": {"type": "number"},
          "epochs_before_decay": {"type": "number"},
          "lrate": {"type": "number"},
          "patience": {"type": "number"}
      }
    }
  },
  "required": ["name", "description"]
}


def load_conf(conf_filename, validate_config=True):
    conf_file = Config()
    conf_file.load(conf_filename, validate_config=validate_config)
    return conf_file


class Config(dict):

    def __init__(self, *args, schema_file=None, **kwargs):
        self.update(*args, **kwargs)
        self.data = None
        self.schema_file = schema_file

    def load(self, conf_filename, validate_config=False):
        with open(conf_filename) as conf_file:
            data = json.load(conf_file)
            self.update(data)

        return self.build(validate_config)

    def save(self, conf_filename, overwrite=False):
        conf_file = Path(conf_filename)
        if not overwrite and conf_file.is_file():
            raise FileExistsError(conf_filename)

        with open(conf_filename, "w") as conf_file:
            json.dump(self, conf_file)

    def build(self, validate_config=False):

        if validate_config:
            if self.schema_file is not None:
                with open('conf_schema.json') as schema_file:
                    schema = json.load(schema_file)
            else:
                schema = default_schema

            validate(self, schema)

        self.data = namedtuple("Conf", self.keys())(*self.values())
        return self.data

    def display(self):
        """Display Configuration values."""
        print("\nConfigurations:")
        for a in dir(self):
            if not a.startswith("__") and not callable(getattr(self, a)):
                print("{:30} {}".format(a, getattr(self, a)))
        print("\n")

