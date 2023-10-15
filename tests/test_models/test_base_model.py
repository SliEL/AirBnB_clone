#!/usr/bin/python3
"""Defines unittests for models/base_model.py."""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests that tests instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        basemodel1 = BaseModel()
        basemodel2 = BaseModel()
        self.assertNotEqual(basemodel1.id, basemodel2.id)

    def test_two_models_different_created_at(self):
        basemodel1 = BaseModel()
        sleep(0.05)
        basemodel2 = BaseModel()
        self.assertLess(basemodel1.created_at, basemodel2.created_at)

    def test_two_models_different_updated_at(self):
        basemodel1 = BaseModel()
        sleep(0.05)
        basemodel2 = BaseModel()
        self.assertLess(basemodel1.updated_at, basemodel2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        basemodel = BaseModel()
        basemodel.id = "123456"
        basemodel.created_at = basemodel.updated_at = dt
        basemodel_str = basemodel.__str__()
        self.assertIn("[BaseModel] (123456)", basemodel_str)
        self.assertIn("'id': '123456'", basemodel_str)
        self.assertIn("'created_at': " + dt_repr, basemodel_str)
        self.assertIn("'updated_at': " + dt_repr, basemodel_str)

    def test_args_unused(self):
        basemodel = BaseModel(None)
        self.assertNotIn(None, basemodel.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        basemodel = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(basemodel.id, "345")
        self.assertEqual(basemodel.created_at, dt)
        self.assertEqual(basemodel.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        basemodel = BaseModel(
            "12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(basemodel.id, "345")
        self.assertEqual(basemodel.created_at, dt)
        self.assertEqual(basemodel.updated_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """Unittests that tests the save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        basemodel = BaseModel()
        sleep(0.05)
        first_updated_at = basemodel.updated_at
        basemodel.save()
        self.assertLess(first_updated_at, basemodel.updated_at)

    def test_two_saves(self):
        basemodel = BaseModel()
        sleep(0.05)
        first_updated_at = basemodel.updated_at
        basemodel.save()
        second_updated_at = basemodel.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        basemodel.save()
        self.assertLess(second_updated_at, basemodel.updated_at)

    def test_save_with_arg(self):
        basemodel = BaseModel()
        with self.assertRaises(TypeError):
            basemodel.save(None)

    def test_save_updates_file(self):
        basemodel = BaseModel()
        basemodel.save()
        basemodel_id = "BaseModel." + basemodel.id
        with open("file.json", "r") as f:
            self.assertIn(basemodel_id, f.read())


if __name__ == "__main__":
    unittest.main()
