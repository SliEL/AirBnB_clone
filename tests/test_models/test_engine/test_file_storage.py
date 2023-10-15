import unittest
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage()
        self.base_model = BaseModel()
        self.user = User()
        self.place = Place()
        self.state = State()
        self.city = City()
        self.amenity = Amenity()
        self.review = Review()

    def tearDown(self):
        if os.path.exists(self.storage._FileStorage__file_path):
            os.remove(self.storage._FileStorage__file_path)

    def test_all(self):
        objects = self.storage.all()
        self.assertIsInstance(objects, dict)
        self.assertIn("BaseModel.{}".format(self.base_model.id), objects)
        self.assertIn("User.{}".format(self.user.id), objects)
        self.assertIn("Place.{}".format(self.place.id), objects)
        self.assertIn("State.{}".format(self.state.id), objects)
        self.assertIn("City.{}".format(self.city.id), objects)
        self.assertIn("Amenity.{}".format(self.amenity.id), objects)
        self.assertIn("Review.{}".format(self.review.id), objects)

    def test_new(self):
        self.storage.new(self.base_model)
        objects = self.storage.all()
        self.assertIn("BaseModel.{}".format(self.base_model.id), objects)

    def test_save_and_reload(self):
        self.storage.new(self.base_model)
        self.storage.new(self.user)
        self.storage.new(self.place)
        self.storage.save()

        # Create a new storage instance and reload data
        new_storage = FileStorage()
        new_storage.reload()

        # Check if objects were loaded correctly
        objects = new_storage.all()
        self.assertIn("BaseModel.{}".format(self.base_model.id), objects)
        self.assertIn("User.{}".format(self.user.id), objects)
        self.assertIn("Place.{}".format(self.place.id), objects)


if __name__ == "__main__":
    unittest.main()
