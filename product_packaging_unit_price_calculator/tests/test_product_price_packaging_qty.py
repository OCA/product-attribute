from odoo.tests.common import SavepointCase


class TestProductPricePackagingQty(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product = cls.env["product.product"].create(
            {"name": "Test", "type": "service", "list_price": 222}
        )
        cls.wizard = cls.env["product.package.price.wizard"]
        cls.pkg_box = cls.env["product.packaging"].create(
            {"name": "Box", "product_id": cls.product.id}
        )
        # Qty is not added on create because it breaks on Travis with
        # packaging_uom installed
        cls.pkg_box.qty = 50
        cls.pkg_big_box = cls.env["product.packaging"].create(
            {"name": "Big Box", "product_id": cls.product.id}
        )
        cls.pkg_big_box.qty = 200
        cls.pkg_pallet = cls.env["product.packaging"].create(
            {"name": "Pallet", "product_id": cls.product.id}
        )
        cls.pkg_pallet.qty = 2000
        cls.wizard_1 = cls.wizard.with_context(
            product_tmpl_id=cls.product.product_tmpl_id.id
        ).create({})
        cls.supplier = cls.env.ref("base.res_partner_1")
        cls.supplier_info = cls.env["product.supplierinfo"].create(
            {
                "product_tmpl_id": cls.product.product_tmpl_id.id,
                "name": cls.supplier.id,
                "price": 333,
            }
        )

    def test_set_sale_package_price(self):
        self.wizard_1.packaging_price = 200
        self.wizard_1.selected_packaging_id = self.pkg_box
        self.assertEqual(self.wizard_1.current_unit_price, 222)
        self.assertEqual(self.wizard_1.unit_price, 4)
        self.wizard_1.action_set_price()
        self.assertEqual(self.product.list_price, 4)

    def test_set_purchase_pacakge_price(self):
        self.wizard_1.product_supplierinfo_id = self.supplier_info
        self.wizard_1.product_tmpl_id = self.product.product_tmpl_id
        self.assertEqual(self.wizard_1.current_unit_price, 333)
        self.wizard_1.packaging_price = 200
        self.wizard_1.selected_packaging_id = self.pkg_big_box
        self.assertEqual(self.wizard_1.unit_price, 1)
        self.wizard_1.action_set_price()
        self.assertEqual(self.supplier_info.price, 1)
