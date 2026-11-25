# Copyright 2021 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo_test_helper import FakeModelLoader

from odoo.fields import Command
from odoo.tests import Form, TransactionCase


class TestProductSecondaryUnitMixin(TransactionCase, FakeModelLoader):
    def setUp(self):
        super().setUp()
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()
        from .models import SecondaryUnitFake

        self.loader.update_registry((SecondaryUnitFake,))
        self.product_uom_unit = self.env.ref("uom.product_uom_unit")
        self.product_uom_dozen = self.env.ref("uom.product_uom_dozen")
        self.product_template = self.env["product.template"].create(
            {
                "name": "test",
                "uom_id": self.product_uom_unit.id,
                "uom_po_id": self.product_uom_unit.id,
                "secondary_uom_ids": [
                    Command.create(
                        {
                            "code": "C5",
                            "name": "box 5",
                            "uom_id": self.product_uom_unit.id,
                            "factor": 5,
                        }
                    ),
                    Command.create(
                        {
                            "code": "C10",
                            "name": "box 10",
                            "uom_id": self.product_uom_unit.id,
                            "factor": 10,
                        }
                    ),
                    Command.create(
                        {
                            "code": "C20",
                            "name": "box 20",
                            "dependency_type": "independent",
                            "uom_id": self.product_uom_unit.id,
                            "factor": 20,
                        }
                    ),
                    Command.create(
                        {
                            "code": "C3",
                            "name": "box 3",
                            "uom_id": self.product_uom_unit.id,
                            "factor": 3,
                        }
                    ),
                ],
            }
        )
        self.secondary_unit_box_5 = self.product_template.secondary_uom_ids[0]
        self.secondary_unit_box_10 = self.product_template.secondary_uom_ids[1]
        self.secondary_unit_box_20 = self.product_template.secondary_uom_ids[2]
        self.secondary_unit_box_3 = self.product_template.secondary_uom_ids[3]
        # Fake model which inherit from
        self.secondary_unit_fake = self.env["secondary.unit.fake"].create(
            {
                "name": "Secondary unit fake",
                "product_id": self.product_template.product_variant_ids.id,
                "product_uom_id": self.product_uom_unit.id,
            }
        )

    def tearDown(self):
        self.loader.restore_registry()
        return super().tearDown()

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

    def test_product_secondary_unit_independent_mixin(self):
        fake_model = self.secondary_unit_fake
        fake_model.write(
            {
                "product_uom_qty": 20,
                "secondary_uom_qty": 1,
                "secondary_uom_id": self.secondary_unit_box_20.id,
            }
        )
        self.assertEqual(fake_model.product_uom_qty, 20)
        fake_model.invalidate_recordset()
        fake_model.product_uom_id = self.product_uom_dozen
        fake_model._onchange_helper_product_uom_for_secondary()
        self.assertEqual(fake_model.secondary_uom_qty, 1)

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

    def test_set_secondary_uom_keeps_qty(self):
        """Setting the secondary unit after the quantity must not reset it to 0
        nor round it through a factor that does not divide it."""
        fake_model = self.secondary_unit_fake
        for dependency_type, secondary_qty in (
            ("dependent", 3.33),
            ("secondary_priority", 0.0),
        ):
            self.secondary_unit_box_3.dependency_type = dependency_type
            fake_model.write({"secondary_uom_id": False, "product_uom_qty": 10.0})
            fake_model.secondary_uom_id = self.secondary_unit_box_3
            self.assertEqual(fake_model.product_uom_qty, 10.0)
            self.assertEqual(fake_model.secondary_uom_qty, secondary_qty)

    def test_set_secondary_uom_keeps_qty_form(self):
        """Same in the form, with the quantity typed or already saved."""
        with Form(self.secondary_unit_fake) as form:
            form.product_uom_qty = 10.0
            form.secondary_uom_id = self.secondary_unit_box_3
            self.assertEqual(form.product_uom_qty, 10.0)
            self.assertEqual(form.secondary_uom_qty, 3.33)
            form.secondary_uom_qty = 0.0
            self.assertEqual(form.product_uom_qty, 0.0)
        for dependency_type, secondary_qty in (
            ("dependent", 3.33),
            ("secondary_priority", 0.0),
        ):
            self.secondary_unit_box_3.dependency_type = dependency_type
            self.secondary_unit_fake.write(
                {"secondary_uom_id": False, "product_uom_qty": 10.0}
            )
            with Form(self.secondary_unit_fake) as form:
                form.secondary_uom_id = self.secondary_unit_box_3
                self.assertEqual(form.product_uom_qty, 10.0)
                self.assertEqual(form.secondary_uom_qty, secondary_qty)
            self.assertEqual(self.secondary_unit_fake.product_uom_qty, 10.0)
            self.assertEqual(self.secondary_unit_fake.secondary_uom_qty, secondary_qty)

    def test_typed_secondary_qty_converts_rounded_qty(self):
        """A typed secondary qty sets the quantity even when it is what the
        quantity rounds to."""
        self.secondary_unit_box_5.uom_id.rounding = 1.0
        fake_model = self.secondary_unit_fake
        fake_model.write(
            {
                "secondary_uom_id": self.secondary_unit_box_5.id,
                "secondary_uom_qty": 3,
                "product_uom_qty": 12.0,
            }
        )
        fake_model.secondary_uom_qty = 2
        self.assertEqual(fake_model.product_uom_qty, 10.0)

    def test_write_secondary_uom_with_other_product(self):
        """A write that also changes the product does not mix units of measure."""
        uom_kg = self.env.ref("uom.product_uom_kgm")
        template_kg = self.env["product.template"].create(
            {
                "name": "test kg",
                "uom_id": uom_kg.id,
                "uom_po_id": uom_kg.id,
                "secondary_uom_ids": [
                    Command.create({"name": "bag 5", "uom_id": uom_kg.id, "factor": 5})
                ],
            }
        )
        fake_model = self.secondary_unit_fake
        fake_model.write({"secondary_uom_id": False, "product_uom_qty": 10.0})
        fake_model.write(
            {
                "product_id": template_kg.product_variant_ids.id,
                "product_uom_id": uom_kg.id,
                "secondary_uom_id": template_kg.secondary_uom_ids.id,
                "secondary_uom_qty": 3,
            }
        )
        self.assertEqual(fake_model.product_uom_qty, 15.0)
        self.assertEqual(fake_model.secondary_uom_qty, 3.0)

    def test_write_secondary_uom_with_secondary_qty(self):
        """Only a dependent unit's secondary qty matching the quantity keeps it."""
        fake_model = self.secondary_unit_fake
        for dependency_type, secondary_qty, qty in (
            ("dependent", 3.33, 10.0),
            ("dependent", 2.0, 6.0),
            ("secondary_priority", 3.33, 9.99),
        ):
            self.secondary_unit_box_3.dependency_type = dependency_type
            fake_model.write({"secondary_uom_id": False, "product_uom_qty": 10.0})
            fake_model.write(
                {
                    "secondary_uom_id": self.secondary_unit_box_3.id,
                    "secondary_uom_qty": secondary_qty,
                }
            )
            self.assertEqual(fake_model.product_uom_qty, qty)
            self.assertEqual(fake_model.secondary_uom_qty, secondary_qty)

    def test_set_secondary_uom_keeps_qty_batch(self):
        """Each record of a batch derives its own secondary qty."""
        fake_models = self.secondary_unit_fake + self.secondary_unit_fake.copy()
        fake_models.secondary_uom_id = False
        fake_models[0].product_uom_qty = 10.0
        fake_models[1].product_uom_qty = 11.0
        fake_models.secondary_uom_id = self.secondary_unit_box_3
        self.assertEqual(fake_models.mapped("product_uom_qty"), [10.0, 11.0])
        self.assertEqual(fake_models.mapped("secondary_uom_qty"), [3.33, 3.67])

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

    def test_secondary_priority_type(self):
        # "secondary_priority": primary IS computed from secondary (like
        # "dependent"), but secondary is NEVER recomputed from primary
        # (like "independent") - e.g. counting pieces of a product sold
        # by weight, where the piece count must stay exact.
        fake_model = self.secondary_unit_fake
        fake_model.secondary_uom_id = self.secondary_unit_box_5
        fake_model.secondary_uom_id.write({"dependency_type": "secondary_priority"})
        fake_model.write({"secondary_uom_qty": 2})
        self.assertEqual(fake_model.product_uom_qty, 10.0)
        self.assertEqual(fake_model.secondary_uom_qty, 2)

        fake_model.write({"product_uom_qty": 17})
        self.assertEqual(fake_model.product_uom_qty, 17)
        self.assertEqual(fake_model.secondary_uom_qty, 2)

        fake_model.write({"secondary_uom_qty": 4})
        self.assertEqual(fake_model.product_uom_qty, 20.0)
        self.assertEqual(fake_model.secondary_uom_qty, 4)

    def test_onchange_secondary_uom_id_for_qty(self):
        """The onchange wired to secondary_uom_id recomputes the target qty
        field, so any consuming model gets that behavior for free without
        having to declare it itself. Exercised through Form() so it goes
        through the same onchange() machinery a real client would use.
        """
        with Form(self.secondary_unit_fake) as form:
            form.secondary_uom_qty = 2
            form.secondary_uom_id = self.secondary_unit_box_5
        self.assertEqual(form.product_uom_qty, 10.0)

    def test_secondary_uom_qty_conversion_with_different_line_uom(self):
        product_uom_litre = self.env.ref("uom.product_uom_litre")
        volume_category = self.env.ref("uom.product_uom_categ_vol")
        product_uom_millilitre = self.env["uom.uom"].create(
            {
                "name": "mL",
                "category_id": volume_category.id,
                "uom_type": "smaller",
                "factor": 1000.0,
                "rounding": 0.01,
            }
        )
        product_template = self.env["product.template"].create(
            {
                "name": "Test",
                "uom_id": product_uom_millilitre.id,
                "uom_po_id": product_uom_millilitre.id,
                "secondary_uom_ids": [
                    Command.create(
                        {
                            "name": "Bottle",
                            "uom_id": product_uom_millilitre.id,
                            "factor": 1200.0,
                            "dependency_type": "dependent",
                        }
                    )
                ],
            }
        )
        bottle_secondary_uom = product_template.secondary_uom_ids
        fake_model = self.env["secondary.unit.fake"].create(
            {
                "name": "Secondary unit fake (volume)",
                "product_id": product_template.product_variant_ids.id,
                "product_uom_id": product_uom_litre.id,
                "product_uom_qty": 1.2,
                "secondary_uom_id": bottle_secondary_uom.id,
            }
        )
        self.assertEqual(fake_model.secondary_uom_qty, 1.0)
