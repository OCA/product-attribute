# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# Copyright 2018 ForgeFlow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import SavepointCase


class TestProductSupplierinfoForCustomer(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductSupplierinfoForCustomer, cls).setUpClass()
        cls.supplierinfo_model = cls.env["product.supplierinfo"]
        cls.customerinfo_model = cls.env["product.customerinfo"]
        cls.pricelist_item_model = cls.env["product.pricelist.item"]
        cls.pricelist_model = cls.env["product.pricelist"]
        cls.customer = cls._create_customer("customer1")
        cls.unknown = cls._create_customer("customer2")
        cls.product = cls.env.ref("product.product_product_4")
        cls.customerinfo = cls._create_partnerinfo(
            "customer", cls.customer, cls.product
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {"name": "Test Pricelist", "currency_id": cls.env.ref("base.USD").id}
        )
        cls.company = cls.env.ref("base.main_company")
        cls.pricelist_item = cls.env["product.pricelist.item"].create(
            {
                "applied_on": "1_product",
                "base": "list_price",
                "name": "Test Pricelist Item",
                "pricelist_id": cls.pricelist.id,
                "compute_price": "fixed",
                "fixed_price": 100.0,
                "product_tmpl_id": cls.product.product_tmpl_id.id,
            }
        )

    @classmethod
    def _create_customer(cls, name):
        """Create a Partner."""
        return cls.env["res.partner"].create(
            {"name": name, "email": "example@yourcompany.com", "phone": 123456}
        )

    @classmethod
    def _create_partnerinfo(cls, supplierinfo_type, partner, product):
        return cls.env["product." + supplierinfo_type + "info"].create(
            {
                "name": partner.id,
                "product_id": product.id,
                "product_code": "00001",
                "price": 100.0,
            }
        )

    def test_default_get(self):
        """ checking values returned by default_get() """
        fields = ["name"]
        values = self.customer.with_context(select_type=True).default_get(fields)
        self.assertEqual(values["customer"], False, "Incorrect default")

    def test_product_supplierinfo_for_customer(self):
        cond = [("name", "=", self.customer.id)]
        supplierinfos = self.supplierinfo_model.search(cond)
        self.assertEqual(len(supplierinfos), 0, "Error: Supplier found in Supplierinfo")
        cond = [("name", "=", self.customer.id)]
        customerinfos = self.customerinfo_model.search(cond)
        self.assertNotEqual(
            len(customerinfos), 0, "Error: Customer not found in Supplierinfo"
        )
        price, rule_id = self.pricelist.get_product_price_rule(
            self.product, 1, partner=self.customer
        )
        self.assertEqual(
            rule_id, self.pricelist_item.id, "Error: Price unit not found for customer"
        )
        self.assertEqual(
            price, 100.0, "Error: Price not found for product and customer"
        )

    def test_product_supplierinfo_price(self):
        price = self.product._get_price_from_customerinfo(partner_id=self.customer.id)
        self.assertEqual(
            price, 100.0, "Error: Price not found for product and customer"
        )
        self.product.company_id = self.company
        res = self.product.with_context(partner_id=self.customer.id).price_compute(
            "partner", self.product.uom_id, self.company.currency_id, self.company
        )
        self.assertEqual(
            res[self.product.id], 100.0, "Error: Wrong price for product and customer"
        )
        res = self.product.with_context(partner_id=self.unknown.id).price_compute(
            "partner", self.product.uom_id, self.company.currency_id, self.company
        )
        self.assertEqual(
            res[self.product.id], 750.0, "Error: price does not match list price"
        )

    def test_variant_supplierinfo_price(self):
        """
        This test check the price for a customer with a product with variants.
        Create a pricelist based on partner price.
        Assign specific price for a variant (100.0) and for template (all
        other variants --> 30.0).
        """
        self.piece_template = self.env["product.template"].create(
            {"name": "Piece for test", "price": 10.0, "company_id": self.company.id}
        )
        self.large_attribute = self.env["product.attribute"].create(
            {"name": "Large test", "sequence": 1}
        )
        self.large_125 = self.env["product.attribute.value"].create(
            {
                "name": "Large 125",
                "attribute_id": self.large_attribute.id,
                "sequence": 1,
            }
        )
        self.large_250 = self.env["product.attribute.value"].create(
            {
                "name": "Large 250",
                "attribute_id": self.large_attribute.id,
                "sequence": 2,
            }
        )
        self.piece_large_attribute_lines = self.env[
            "product.template.attribute.line"
        ].create(
            {
                "product_tmpl_id": self.piece_template.id,
                "attribute_id": self.large_attribute.id,
                "value_ids": [(6, 0, [self.large_125.id, self.large_250.id])],
            }
        )

        template = self.piece_template
        product = template.product_variant_ids[0]
        product_1 = template.product_variant_ids[1]

        pricelist = self.env["product.pricelist"].create(
            {
                "name": "Test Pricelist Customer",
                "currency_id": self.env.ref("base.USD").id,
            }
        )
        self.env["product.pricelist.item"].create(
            {
                "applied_on": "3_global",
                "base": "partner",
                "name": "Test Pricelist Item",
                "pricelist_id": pricelist.id,
                "compute_price": "formula",
            }
        )
        self._create_partnerinfo("customer", self.customer, product)
        price_by_template = self.customerinfo_model.create(
            {"name": self.customer.id, "product_tmpl_id": template.id, "price": 30.0}
        )
        res = product.with_context(partner_id=self.customer.id).price_compute(
            "partner", product.uom_id, self.company.currency_id, self.company
        )
        self.assertEqual(res[product.id], 100.0)
        res = product_1.with_context(partner_id=self.customer.id).price_compute(
            "partner", product_1.uom_id, self.company.currency_id, self.company
        )
        self.assertEqual(res[product_1.id], 30.0)
        # Remove template specific price, the price must be the template
        # list_price
        price_by_template.unlink()
        res = product_1.with_context(partner_id=self.customer.id).price_compute(
            "partner", product_1.uom_id, self.company.currency_id, self.company
        )
        self.assertEqual(res[product_1.id], 10.0)
