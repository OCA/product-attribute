# Copyright 2021 Camptocamp SA
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
from odoo.tests.common import SavepointCase
from odoo.tools.misc import mute_logger


class TestPackagingTypeRequired(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = product = cls.env.ref("product.product_product_6")
        cls.pkg_type_model = cls.env["product.packaging.type"]
        # create some required types
        cls.type_retail_box = cls.pkg_type_model.create(
            {"name": "Retail Box", "code": "PACK", "sequence": 3, "required": True}
        )
        cls.type_transport_box = cls.pkg_type_model.create(
            {"name": "Transport Box", "code": "CASE", "sequence": 4, "required": True}
        )
        cls.type_pallet = cls.pkg_type_model.create(
            {"name": "Pallet", "code": "PALLET", "sequence": 5, "required": True}
        )
        # Create packaging only for one of them
        cls.pkg_box = cls.env["product.packaging"].create(
            {
                "name": "Box",
                "product_id": product.id,
                "qty": 50,
                "packaging_type_id": cls.type_retail_box.id,
                "barcode": "BOX",
            }
        )

    @mute_logger(
        "odoo.addons.product_packaging_type_required.models.product_packaging_type"
    )
    def test_cron_create(self):
        products_count = self.env["product.product"].search_count(
            [("type", "in", ("product", "consu"))]
        )
        count_packaging = self.env["product.packaging"].search_count
        domain1 = [("packaging_type_id", "=", self.type_transport_box.id)]
        self.assertEqual(count_packaging(domain1), 0)
        domain2 = [("packaging_type_id", "=", self.type_pallet.id)]
        self.assertEqual(count_packaging(domain2), 0)
        domain3 = [("packaging_type_id", "=", self.type_retail_box.id)]
        self.assertEqual(count_packaging(domain3), 1)
        res = self.pkg_type_model.cron_check_create_required_packaging()
        # We get one required packaging per type per product
        self.assertEqual(count_packaging(domain1), products_count)
        self.assertEqual(count_packaging(domain2), products_count)
        self.assertEqual(count_packaging(domain3), products_count)
        # 1 was already created at the setup
        created_count = (products_count * 3) - 1
        self.assertEqual(res, f"CREATED {created_count} required packaging")
        # Let's add another one
        self.pkg_type_model.create(
            {"name": "Small box", "code": "S BOX", "sequence": 6, "required": True}
        )
        res = self.pkg_type_model.cron_check_create_required_packaging()
        self.assertEqual(res, f"CREATED {products_count} required packaging")
