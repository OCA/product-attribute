# Copyright 2021 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo_test_helper import FakeModelLoader

from odoo.tests import TransactionCase


class TestProductSecondaryUnitMixin(TransactionCase, FakeModelLoader):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import SecondaryUnitFake

        cls.loader.update_registry((SecondaryUnitFake,))
        cls.product_uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.product_uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.product_uom_dozen = cls.env.ref("uom.product_uom_dozen")
        cls.product_template = cls.env["product.template"].create(
            {
                "name": "test",
                "uom_id": cls.product_uom_kg.id,
                "uom_po_id": cls.product_uom_kg.id,
                "secondary_uom_ids": [
                    (
                        0,
                        0,
                        {
                            "code": "C5",
                            "name": "box 5",
                            "uom_id": cls.product_uom_unit.id,
                            "factor": 5,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "code": "C10",
                            "name": "box 10",
                            "uom_id": cls.product_uom_unit.id,
                            "factor": 10,
                        },
                    ),
                ],
            }
        )
        cls.secondary_unit_box_5 = cls.product_template.secondary_uom_ids[0]
        cls.secondary_unit_box_10 = cls.product_template.secondary_uom_ids[1]
        # Fake model which inherit from
        cls.secondary_unit_fake = cls.env["secondary.unit.fake"].create(
            {
                "name": "Secondary unit fake",
                "product_id": cls.product_template.product_variant_ids.id,
                "product_uom_id": cls.product_uom_unit.id,
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        return super().tearDownClass()

    def test_product_secondary_unit_mixin(self):
        fake_model = self.secondary_unit_fake

        fake_model.write(
            {"secondary_uom_qty": 2, "secondary_uom_id": self.secondary_unit_box_5.id}
        )
        self.assertEqual(fake_model.product_uom_qty, 10.0)

        fake_model.write(
            {"secondary_uom_qty": 2, "secondary_uom_id": self.secondary_unit_box_10.id}
        )
        self.assertEqual(fake_model.product_uom_qty, 20.0)

        fake_model.write({"product_uom_qty": 40.0})
        self.assertEqual(fake_model.secondary_uom_qty, 4)

        # Test onchange helper method
        fake_model.write(
            {"secondary_uom_qty": 1, "secondary_uom_id": self.secondary_unit_box_10.id}
        )
        fake_model.invalidate_recordset()
        fake_model.product_uom_id = self.product_uom_dozen
        fake_model._onchange_helper_product_uom_for_secondary()
        self.assertEqual(fake_model.secondary_uom_qty, 12)

    def test_product_secondary_unit_mixin_no_uom(self):
        # If secondary_uom_id is not informed product_qty on target model is
        # not computed.
        fake_model = self.secondary_unit_fake
        fake_model.secondary_uom_qty = 23
        self.assertEqual(fake_model.product_uom_qty, 0)

    def test_product_secondary_unit_mixin_no_uom_onchange(self):
        # If secondary_uom_id is not informed secondary_uom_qty on source
        # model is not computed.
        fake_model = self.secondary_unit_fake
        # import pdb ; pdb.set_trace()
        fake_model._onchange_helper_product_uom_for_secondary()
        self.assertEqual(fake_model.secondary_uom_qty, 0)

    def test_chained_compute_field(self):
        """Secondary_uom_qty has not been computed when secondary_uom_id changes"""
        fake_model = self.secondary_unit_fake
        fake_model.secondary_uom_qty = 2.0
        fake_model.secondary_uom_id = self.secondary_unit_box_5
        self.assertEqual(fake_model.product_uom_qty, 10.0)
        self.assertEqual(fake_model.secondary_uom_qty, 2.0)
        fake_model.secondary_uom_id = self.secondary_unit_box_10
        self.assertEqual(fake_model.product_uom_qty, 20.0)
        self.assertEqual(fake_model.secondary_uom_qty, 2.0)

    def test_independent_type(self):
        # dependent type is already tested as dependency_type by default
        fake_model = self.secondary_unit_fake
        fake_model.secondary_uom_id = self.secondary_unit_box_5
        fake_model.secondary_uom_id.write({"dependency_type": "independent"})
        fake_model.write({"secondary_uom_qty": 2})
        self.assertEqual(fake_model.product_uom_qty, 0.0)
        self.assertEqual(fake_model.secondary_uom_qty, 2)

        fake_model.write({"product_uom_qty": 17})
        self.assertEqual(fake_model.product_uom_qty, 17)
        self.assertEqual(fake_model.secondary_uom_qty, 2)

        fake_model.write({"secondary_uom_qty": 4})
        self.assertEqual(fake_model.product_uom_qty, 17)
        self.assertEqual(fake_model.secondary_uom_qty, 4)
