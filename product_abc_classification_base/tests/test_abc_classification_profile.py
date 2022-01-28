# -*- coding: utf-8 -*-
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from .common import ABCClassificationCase
from odoo.exceptions import ValidationError


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
                    (
                        0,
                        0,
                        {
                            "percentage": 60,
                            "percentage_products": 40,
                            "name": "A",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "percentage": 40,
                            "percentage_products": 60,
                            "name": "B",
                        },
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
                        (
                            0,
                            0,
                            {
                                "percentage": 60,
                                "percentage_products": 40,
                                "name": "A",
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "percentage": 30,
                                "percentage_products": 60,
                                "name": "B",
                            },
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
                        (
                            0,
                            0,
                            {
                                "percentage": 60,
                                "percentage_products": 40,
                                "name": "A",
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "percentage": 50,
                                "percentage_products": 60,
                                "name": "B",
                            },
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
                        (
                            0,
                            0,
                            {
                                "percentage": 50,
                                "percentage_products": 40,
                                "name": "A",
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "percentage": 50,
                                "percentage_products": 60,
                                "name": "B",
                            },
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
                        (
                            0,
                            0,
                            {
                                "percentage": 150,
                                "percentage_products": 40,
                                "name": "A",
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "percentage": -50,
                                "percentage_products": 60,
                                "name": "B",
                            },
                        ),
                    ]
                }
            )

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
                        (
                            0,
                            0,
                            {
                                "percentage": 60,
                                "percentage_products": 40,
                                "name": "A",
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "percentage": 40,
                                "percentage_products": 60,
                                "name": "A",
                            },
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
                    (
                        0,
                        0,
                        {
                            "percentage": 60,
                            "percentage_products": 40,
                            "name": "A",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "percentage": 40,
                            "percentage_products": 60,
                            "name": "B",
                        },
                    ),
                ]
            }
        )
        new_profile = self.ABCClassificationProfile.create(
            {
                "name": "New Profile test",
                "profile_type": "test_type",
                "level_ids": [
                    (
                        0,
                        0,
                        {
                            "percentage": 60,
                            "percentage_products": 40,
                            "name": "A",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "percentage": 40,
                            "percentage_products": 60,
                            "name": "B",
                        },
                    ),
                ],
            }
        )
        self.assertTrue(new_profile)

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

