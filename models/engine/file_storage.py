#!/bin/usr/python3
"""Module that defines the FileStorage class."""

import json
from models.base_model import BaseModel


class FileStorage:
    """The FileStorage class which represents abstract storage engine.

    Attributes:
        __file_path (str): path to the file where we save the objects.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the entire __objects dict"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects obj with key <obj_class_name>.id"""
        objname = obj.__class__.__name__
        FileStorage.__objects[f"{objname}.{obj.id}"] = obj

    def save(self):
        """Serializes __objects to the JSON file __file_path."""
        obj_dict = FileStorage.__objects
        serialized_obj = {key: obj.to_dict() for key, obj in obj_dict.items()}
        with open(FileStorage.__file_path, 'w') as file:
            json.dump(serialized_obj, file)

    def reload(self):
        """Deserialize and load the objects from the JSON file."""
        try:
            with open(FileStorage.__file_path, 'r') as file:
                data = json.load(file)
                for val in data.values():
                    cls_name = val["__class__"]
                    del val["__class__"]
                    self.new(eval(cls_name)(**val))
        except FileNotFoundError:
            pass
