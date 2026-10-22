# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.fields import Command
from odoo.tools.misc import mute_logger

from .common import ABCClassificationCase


class TestABCClassificationProfile(ABCClassificationCase):
    def test_00(self):
        """
        Data:
            A test profile
        Test case:
            Assign levels for a total of 100%
        Expected result:
            OK
        """
        self.classification_profile.write(
            {
                "level_ids": [
                    Command.create(
                        {
                            "percentage": 60,
                            "percentage_products": 40,
                            "name": "A",
                        }
                    ),
                    Command.create(
                        {
                            "percentage": 40,
                            "percentage_products": 60,
                            "name": "B",
                        }
                    ),
                ]
            }
        )
        self.assertEqual(len(self.classification_profile.level_ids), 2)

    def test_01(self):
        """
        Data:
            A test profile
        Test case:
            Assign levels for a total < 100%
        Expected result:
            ValidationError
        """
        with self.assertRaises(ValidationError):
            self.classification_profile.write(
                {
                    "level_ids": [
                        Command.create(
                            {
                                "percentage": 60,
                                "percentage_products": 40,
                                "name": "A",
                            }
                        ),
                        Command.create(
                            {
                                "percentage": 30,
                                "percentage_products": 60,
                                "name": "B",
                            }
                        ),
                    ]
                }
            )

    def test_02(self):
        """
        Data:
            A test profile
        Test case:
            Assign levels for a total > 100%
        Expected result:
            ValidationError
        """
        with self.assertRaises(ValidationError):
            self.classification_profile.write(
                {
                    "level_ids": [
                        Command.create(
                            {
                                "percentage": 60,
                                "percentage_products": 40,
                                "name": "A",
                            }
                        ),
                        Command.create(
                            {
                                "percentage": 50,
                                "percentage_products": 60,
                                "name": "B",
                            }
                        ),
                    ]
                }
            )

    def test_03(self):
        """
        Data:
            A test profile
        Test case:
            Assign levels for a total = 100% but with same percentage
        Expected result:
            ValidationError
        """
        with self.assertRaises(ValidationError):
            self.classification_profile.write(
                {
                    "level_ids": [
                        Command.create(
                            {
                                "percentage": 50,
                                "percentage_products": 40,
                                "name": "A",
                            }
                        ),
                        Command.create(
                            {
                                "percentage": 50,
                                "percentage_products": 60,
                                "name": "B",
                            }
                        ),
                    ]
                }
            )

    def test_04(self):
        """
        Data:
            A test profile
        Test case:
            Assign levels for a total = 100% but with one level with negative
            percentage and one level exceeding 100%
        Expected result:
            ValidationError
        """
        with self.assertRaises(ValidationError):
            self.classification_profile.write(
                {
                    "level_ids": [
                        Command.create(
                            {
                                "percentage": 150,
                                "percentage_products": 40,
                                "name": "A",
                            }
                        ),
                        Command.create(
                            {
                                "percentage": -50,
                                "percentage_products": 60,
                                "name": "B",
                            }
                        ),
                    ]
                }
            )

    @mute_logger("odoo.sql_db")
    def test_05(self):
        """
        Data:
            A test profile
        Test case:
            Assign levels for a total = 100% but with same name
        Expected result:
            IntegrityError (level name must be unique by profile)
        """
        with self.assertRaises(IntegrityError):
            self.classification_profile.write(
                {
                    "level_ids": [
                        Command.create(
                            {
                                "percentage": 60,
                                "percentage_products": 40,
                                "name": "A",
                            }
                        ),
                        Command.create(
                            {
                                "percentage": 40,
                                "percentage_products": 60,
                                "name": "A",
                            }
                        ),
                    ]
                }
            )

    def test_06(self):
        """
        Data:
            A test profile with 2 levels A and B
        Test case:
             Create a new profile with the same level name
        Expected result:
            Profile created without error since the level name is unique by
            profile
        """
        self.classification_profile.write(
            {
                "level_ids": [
                    Command.create(
                        {
                            "percentage": 60,
                            "percentage_products": 40,
                            "name": "A",
                        }
                    ),
                    Command.create(
                        {
                            "percentage": 40,
                            "percentage_products": 60,
                            "name": "B",
                        }
                    ),
                ]
            }
        )
        new_profile = self.ABCClassificationProfile.create(
            {
                "name": "New Profile test",
                "profile_type": "test_type",
                "level_ids": [
                    Command.create(
                        {
                            "percentage": 60,
                            "percentage_products": 40,
                            "name": "A",
                        }
                    ),
                    Command.create(
                        {
                            "percentage": 40,
                            "percentage_products": 60,
                            "name": "B",
                        }
                    ),
                ],
            }
        )
        self.assertTrue(new_profile)

    @mute_logger("odoo.sql_db")
    def test_07(self):
        """
        Data:
            A test profile
        Test case:
            Create a new profile with the same name
        Expected result:
            IntegrityError (profile name must be unique by profile)
        """
        with self.assertRaises(IntegrityError):
            self.ABCClassificationProfile.create(
                {
                    "name": self.classification_profile.name,
                    "profile_type": "test_type",
                }
            )

    def test_08(self):
        """
        Data:
            A test profile
        Test case:
            Create a level with a negative percentage
        Expected result:
            ValidationError (the percentage should be a positive number)
        """
        with self.assertRaises(ValidationError):
            self.env["abc.classification.level"].create(
                {
                    "name": "A",
                    "percentage": -50,
                    "percentage_products": 40,
                }
            )

    def test_09(self):
        """
        Data:
            A test profile
        Test case:
            Create a level with a products percentage above 100
        Expected result:
            ValidationError (the percentage of products cannot be greater
            than 100)
        """
        with self.assertRaises(ValidationError):
            self.env["abc.classification.level"].create(
                {
                    "name": "A",
                    "percentage": 50,
                    "percentage_products": 150,
                }
            )

    def test_10(self):
        """
        Data:
            A test profile
        Test case:
            Create a level with a negative products percentage
        Expected result:
            ValidationError (the percentage of products should be a positive
            number)
        """
        with self.assertRaises(ValidationError):
            self.env["abc.classification.level"].create(
                {
                    "name": "A",
                    "percentage": 50,
                    "percentage_products": -40,
                }
            )

    def test_11(self):
        """
        Data:
            A test profile
        Test case:
            Assign levels whose percentages total 100% but whose products
            percentages do not
        Expected result:
            ValidationError
        """
        with self.assertRaises(ValidationError):
            self.classification_profile.write(
                {
                    "level_ids": [
                        Command.create(
                            {
                                "percentage": 60,
                                "percentage_products": 40,
                                "name": "A",
                            }
                        ),
                        Command.create(
                            {
                                "percentage": 40,
                                "percentage_products": 50,
                                "name": "B",
                            }
                        ),
                    ]
                }
            )

    def test_12(self):
        """
        Data:
            A test profile
        Test case:
            Duplicate the profile, once letting the name be generated and once
            forcing it
        Expected result:
            Both copies are created, the generated one being suffixed since the
            profile name must be unique
        """
        copy = self.classification_profile.copy()
        self.assertEqual(copy.name, f"{self.classification_profile.name} (copy)")
        forced_copy = self.classification_profile.copy({"name": "Profile forced"})
        self.assertEqual(forced_copy.name, "Profile forced")
