from odoo.exceptions import UserError
from odoo.tests import Form, TransactionCase


class TestProductPricePackagingQty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        # Create a dummy product to avoid missing external ID error
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "list_price": 222,
            }
        )

        cls.wizard = cls.env["product.package.price.wizard"]

        # Find a reference UoM
        ref_uom = cls.env["uom.uom"].search([("relative_uom_id", "=", False)], limit=1)

        # Create UoMs instead of product.packaging
        cls.pkg_box = cls.env["uom.uom"].create(
            {
                "name": "Box",
                "relative_factor": 50.0,
                "relative_uom_id": ref_uom.id,
            }
        )
        cls.pkg_big_box = cls.env["uom.uom"].create(
            {
                "name": "Big Box",
                "relative_factor": 200.0,
                "relative_uom_id": ref_uom.id,
            }
        )
        cls.pkg_pallet = cls.env["uom.uom"].create(
            {
                "name": "Pallet",
                "relative_factor": 2000.0,
                "relative_uom_id": ref_uom.id,
            }
        )

        # Link UoMs to product
        cls.product.product_tmpl_id.uom_ids = [
            (6, 0, [cls.pkg_box.id, cls.pkg_big_box.id, cls.pkg_pallet.id])
        ]

        cls.wizard_1 = cls.wizard.with_context(
            product_tmpl_id=cls.product.product_tmpl_id.id
        ).create({})

        cls.supplier = cls.env["res.partner"].create(
            {
                "name": "Test Supplier",
            }
        )
        cls.supplier_info = cls.env["product.supplierinfo"].create(
            {
                "product_tmpl_id": cls.product.product_tmpl_id.id,
                "partner_id": cls.supplier.id,
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

        # BizzAppDev Customization: Start

    def test_no_selected_package(self):
        form = Form(self.wizard_1)
        form.packaging_price = 200
        form.save()
        with self.assertRaises(UserError):
            self.wizard_1.action_set_price()

    def test_reset_unit_price(self):
        form = Form(self.wizard_1)
        form.selected_packaging_id = self.pkg_box
        form.packaging_price = 100
        self.wizard_1.reset_unit_price()
        self.assertEqual(self.wizard_1.packaging_price, 0)
        self.assertFalse(self.wizard_1.selected_packaging_id)

    def test_no_packaging_price(self):
        form = Form(self.wizard_1)
        form.selected_packaging_id = self.pkg_box
        self.assertFalse(self.wizard_1.packaging_price)
        self.wizard_1.action_set_price()

    def test_open_package_product_template(self):
        open_package = self.product.product_tmpl_id.open_packaging_price()
        self.assertEqual(open_package.get("res_model"), "product.package.price.wizard")

    def test_open_package_product_product(self):
        open_package = self.product.open_packaging_price()
        self.assertEqual(open_package.get("res_model"), "product.package.price.wizard")

    def test_open_package_product_supplier_info(self):
        open_package = self.supplier_info.open_packaging_price()
        self.assertEqual(open_package.get("res_model"), "product.package.price.wizard")

    def test_open_package_product_pricelist_item(self):
        pricelist = self.env["product.pricelist"].create({"name": "Test Pricelist"})
        item = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": pricelist.id,
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "fixed_price": 100,
            }
        )
        open_package = item.open_packaging_price()
        self.assertEqual(open_package.get("res_model"), "product.package.price.wizard")

        # Test defaults and setting price on pricelist item
        wizard = self.wizard.with_context(
            active_model="product.pricelist.item",
            active_id=item.id,
            product_tmpl_id=self.product.product_tmpl_id.id,
        ).create({})
        self.assertEqual(wizard.product_pricelist_item_id, item)
        self.assertEqual(wizard.current_unit_price, 100)
        wizard.packaging_price = 100
        wizard.selected_packaging_id = self.pkg_box
        wizard.action_set_price()
        self.assertEqual(item.fixed_price, 2)

    def test_active_model_product_product(self):
        wizard = self.wizard.with_context(
            active_model="product.product",
            active_id=self.product.id,
            product_tmpl_id=self.product.product_tmpl_id.id,
        ).create({})
        self.assertEqual(wizard.product_id, self.product)
        self.assertEqual(wizard.current_unit_price, 222)
        wizard.packaging_price = 100
        wizard.selected_packaging_id = self.pkg_box
        wizard.action_set_price()
        self.assertEqual(self.product.lst_price, 2)

    def test_active_model_product_supplierinfo(self):
        wizard = self.wizard.with_context(
            active_model="product.supplierinfo",
            active_id=self.supplier_info.id,
            product_tmpl_id=self.product.product_tmpl_id.id,
        ).create({})
        self.assertEqual(wizard.product_supplierinfo_id, self.supplier_info)

    # BizzAppDev Customization: End
