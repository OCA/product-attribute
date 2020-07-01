from odoo.tests.common import Form, SavepointCase


class TestProductPricePackagingQty(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product = cls.env.ref("product.product_product_1")
        cls.product.list_price = 222
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
        form = Form(self.wizard_1)
        form.packaging_price = 200
        form.selected_packaging_id = self.pkg_box
        self.assertEqual(self.wizard_1.current_unit_price, 222)
        self.assertEqual(form.unit_price, 4)
        form.save()
        self.wizard_1.action_set_price()
        self.assertEqual(self.product.list_price, 4)

    def test_set_purchase_pacakge_price(self):
        self.wizard_1.product_supplierinfo_id = self.supplier_info
        form = Form(self.wizard_1)
        self.assertEqual(self.wizard_1.current_unit_price, 333)
        form.packaging_price = 200
        form.selected_packaging_id = self.pkg_big_box
        self.assertEqual(form.unit_price, 1)
        form.save()
        self.wizard_1.action_set_price()
        self.assertEqual(self.supplier_info.price, 1)
