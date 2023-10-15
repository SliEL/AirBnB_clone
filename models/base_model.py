#!/usr/bin/python3
"""Module that defines the BaseModel Class."""

import models
from datetime import datetime
from uuid import uuid4

class BaseModel:
    """Cls that represents the BaseModel for airbnb project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance.

        Args:
            *args: Unused.
            **kwargs (dict): key/val pairs of attrbs.
        """
        self.id = str(uuid4())
        tform = "%Y-%m-%dT%H:%M:%S.%f"
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        
        if (len(kwargs) != 0):
            for key, val in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(val, tform)
                else:
                    self.__dict__[key] = val
        else:
            models.storage.new(self)
    
    
    def __str__(self):
        """Returns the str representation of the BaseModel instance."""
        cls_name = self.__class__.__name__
        return f"[{cls_name}] ({self.id} {self.__dict__})"

    def save(self):
        """Update update_at with the current time."""
        self.updated_at = datetime.today()
        models.storage.save()

    
    def to_dict(self):
        """Returns a dictionary containing all 

        keys/values of __dict__ of the instance.
        """
        ret_dict = self.__dict__.copy()
        ret_dict["created_at"] = self.created_at.isoformat()
        ret_dict["updated_at"] = self.updated_at.isoformat()
        ret_dict["__class__"] = self.__class__.__name__
        return ret_dict
