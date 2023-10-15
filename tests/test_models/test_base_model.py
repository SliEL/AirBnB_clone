import unittest
from models.base_model import BaseModel
from datetime import datetime
from unittest.mock import patch, MagicMock


class TestBaseModel(unittest.TestCase):
    def setUp(self):
        self.base_model = BaseModel()
        self.base_model.save = MagicMock()  # Mock the save method

    def tearDown(self):
        pass  # No need to delete in this context

    def test_id_generation(self):
        self.assertTrue(hasattr(self.base_model, 'id'))
        self.assertIsInstance(self.base_model.id, str)

    def test_created_at(self):
        self.assertTrue(hasattr(self.base_model, 'created_at'))
        self.assertIsInstance(self.base_model.created_at, datetime)

    def test_updated_at(self):
        self.assertTrue(hasattr(self.base_model, 'updated_at'))
        self.assertIsInstance(self.base_model.updated_at, datetime)

    def test_to_dict(self):
        obj_dict = self.base_model.to_dict()
        self.assertEqual(obj_dict['__class__'], 'BaseModel')
        self.assertEqual(type(obj_dict['created_at']), str)
        self.assertEqual(type(obj_dict['updated_at']), str)

    def test_str(self):
        expected_str = "[BaseModel] ({}) {}".format(
            self.base_model.id, self.base_model.__dict__)
        self.assertEqual(str(self.base_model), expected_str)

        def test_kwargs_initialization(self):
            data = {
                "id": "test_id",
                "created_at": "2023-10-14T10:00:00",
                "updated_at": "2023-10-14T11:00:00",
                "custom_attr": "test_value"
            }
            custom_base_model = BaseModel(**data)

            self.assertEqual(custom_base_model.id, "test_id")
            self.assertEqual(custom_base_model.created_at,
                             datetime.fromisoformat("2023-10-14T10:00:00"))
            self.assertEqual(custom_base_model.updated_at,
                             datetime.fromisoformat("2023-10-14T11:00:00"))
            self.assertEqual(custom_base_model.custom_attr, "test_value")


if __name__ == "__main__":
    unittest.main()
