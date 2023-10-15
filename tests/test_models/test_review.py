#!/usr/bin/python3
"""Defines unittests for models/review.py."""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """Unittests that tests instantiation of the Review class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        rev = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(rev))
        self.assertNotIn("place_id", rev.__dict__)

    def test_user_id_is_public_class_attribute(self):
        rev = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(rev))
        self.assertNotIn("user_id", rev.__dict__)

    def test_text_is_public_class_attribute(self):
        rev = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(rev))
        self.assertNotIn("text", rev.__dict__)

    def test_two_reviews_unique_ids(self):
        rev1 = Review()
        rev2 = Review()
        self.assertNotEqual(rev1.id, rev2.id)

    def test_two_reviews_different_created_at(self):
        rev1 = Review()
        sleep(0.05)
        rev2 = Review()
        self.assertLess(rev1.created_at, rev2.created_at)

    def test_two_reviews_different_updated_at(self):
        rev1 = Review()
        sleep(0.05)
        rev2 = Review()
        self.assertLess(rev1.updated_at, rev2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        rev = Review()
        rev.id = "123456"
        rev.created_at = rev.updated_at = dt
        rev_str = rev.__str__()
        self.assertIn("[Review] (123456)", rev_str)
        self.assertIn("'id': '123456'", rev_str)
        self.assertIn("'created_at': " + dt_repr, rev_str)
        self.assertIn("'updated_at': " + dt_repr, rev_str)

    def test_args_unused(self):
        rev = Review(None)
        self.assertNotIn(None, rev.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        rev = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(rev.id, "345")
        self.assertEqual(rev.created_at, dt)
        self.assertEqual(rev.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests that tests the save method of the Review class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

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
        rev = Review()
        sleep(0.05)
        first_updated_at = rev.updated_at
        rev.save()
        self.assertLess(first_updated_at, rev.updated_at)

    def test_two_saves(self):
        rev = Review()
        sleep(0.05)
        first_updated_at = rev.updated_at
        rev.save()
        second_updated_at = rev.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        rev.save()
        self.assertLess(second_updated_at, rev.updated_at)

    def test_save_with_arg(self):
        rev = Review()
        with self.assertRaises(TypeError):
            rev.save(None)

    def test_save_updates_file(self):
        rev = Review()
        rev.save()
        rev_id = "Review." + rev.id
        with open("file.json", "r") as f:
            self.assertIn(rev_id, f.read())




if __name__ == "__main__":
    unittest.main()