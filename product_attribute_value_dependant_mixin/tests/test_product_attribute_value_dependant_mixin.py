# Copyright 2023 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_test_helper import FakeModelLoader

from odoo.tests import SavepointCase


class TestProductAttributeValueDependantMixin(SavepointCase, FakeModelLoader):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import ProductSupplierinfoFake

        cls.loader.update_registry((ProductSupplierinfoFake,))

        # Fake model which inherit from
        cls.product_supplierinfo_fake = cls.env["product.supplierinfo.fake"].create(
            {
                "name": cls.env.ref("base.res_partner_1").id,
                "product_tmpl_id": cls.env.ref(
                    "product.product_product_4_product_template"
                ).id,
                "price": 100.00,
                "currency_id": cls.env.ref("base.USD").id,
                "min_qty": 1.0,
                "delay": 1.0,
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super(TestProductAttributeValueDependantMixin, cls).tearDownClass()

    def test_product_attribute_value_dependant_mixin(self):
        fake_model = self.product_supplierinfo_fake
        self.assertTrue(fake_model.available_attribute_value_domain)
