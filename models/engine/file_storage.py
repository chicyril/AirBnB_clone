#!/usr/bin/python3
"""This module contains a class FileStorage used for serializing and
deserializing an instance to and from json representation respectively.
"""
import json


class FileStorage:
    """Contains attributes and methods necessary for serializing and
    deserializing an instance to and from json representation.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary which is the value of __objects."""
        return type(self).__objects

    def new(self, obj):
        """Set an Object obj in to the dictionary __objects with a key
        <obj class name>.id"""
        key = f'{obj.__class__.__name__}.{obj.id}'
        type(self).__objects[key] = obj

    def save(self):
        """Serialize __object to a file."""
        serializable = {}
        for key, obj in type(self).__objects.items():
            serializable[key] = obj.to_dict()
        with open(type(self).__file_path, "w", encoding='utf-8') as file:
            json.dump(serializable, file)

    def cls_ref(self):
        """Returns a dictionary referencing all valid classes."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        valid_classes = {'BaseModel': BaseModel,
                         'User': User,
                         'State': State,
                         'City': City,
                         'Amenity': Amenity,
                         'Place': Place,
                         'Review': Review
                         }
        return valid_classes

    def reload(self):
        """Deserialize a json file to __objects."""
        try:
            with open(self.__file_path, "r", encoding='utf-8') as file:
                from_json = json.load(file)
            for k, val in from_json.items():
                self.__objects[k] = self.cls_ref()[val['__class__']](**val)
        except FileNotFoundError:
            pass
