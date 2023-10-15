import unittest
from models.state import State


class TestState(unittest.TestCase):
    def setUp(self):
        self.state = State()

    def test_attributes(self):
        self.assertTrue(hasattr(self.state, 'id'))
        self.assertTrue(hasattr(self.state, 'created_at'))
        self.assertTrue(hasattr(self.state, 'updated_at'))
        self.assertTrue(hasattr(self.state, 'name'))

    def test_defaults(self):
        self.assertEqual(self.state.name, "")

    def test_str(self):
        expected_str = "[State] ({}) {}".format(
            self.state.id, self.state.__dict__)
        self.assertEqual(str(self.state), expected_str)


if __name__ == "__main__":
    unittest.main()
