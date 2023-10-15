import unittest
from models.city import City


class TestCity(unittest.TestCase):
    def setUp(self):
        self.city = City()

    def test_attributes(self):
        self.assertTrue(hasattr(self.city, 'id'))
        self.assertTrue(hasattr(self.city, 'created_at'))
        self.assertTrue(hasattr(self.city, 'updated_at'))
        self.assertTrue(hasattr(self.city, 'state_id'))
        self.assertTrue(hasattr(self.city, 'name'))

    def test_defaults(self):
        self.assertEqual(self.city.state_id, "")
        self.assertEqual(self.city.name, "")

    def test_str(self):
        expected_str = "[City] ({}) {}".format(
            self.city.id, self.city.__dict__)
        self.assertEqual(str(self.city), expected_str)


if __name__ == "__main__":
    unittest.main()
