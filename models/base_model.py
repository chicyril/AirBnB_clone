#!/usr/bin/python3
"""This module contains the class BaseModel which is the Base class from which
other classes are derived for this project.
"""
from uuid import uuid4
from datetime import datetime
from models import storage


class BaseModel:
    """This is a base class that defines all common attributes/methods
    for other classes.
    """
    def __init__(self, *args, **kwargs):
        """Initialize public instance attributes for instances."""
        if kwargs:
            dateTime_format = '%Y-%m-%dT%H:%M:%S.%f'
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key == 'created_at':
                    self.created_at = datetime.strptime(kwargs['created_at'],
                                                        dateTime_format)
                elif key == 'updated_at':
                    self.updated_at = datetime.strptime(kwargs['updated_at'],
                                                        dateTime_format)
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Return the string representation of the object."""
        return (f'[{type(self).__name__}] ({self.id}) {self.__dict__}')

    def save(self):
        """Update the attributes udated_at with the current datetime."""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Return the dictionary representation of an instance."""
        dico = self.__dict__.copy()
        dico['__class__'] = self.__class__.__name__
        dico['created_at'] = self.created_at.isoformat()
        dico['updated_at'] = self.updated_at.isoformat()
        return dico
