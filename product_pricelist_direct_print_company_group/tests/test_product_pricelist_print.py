from odoo.tests import common


class TestProductPricelistPrint(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_group = cls.env["res.partner"].create({"name": "Test Group"})

        cls.partner_1 = cls.env["res.partner"].create(
            {
                "name": "Partner 1",
                "company_group_id": cls.company_group.id,
            }
        )
        cls.partner_2 = cls.env["res.partner"].create(
            {
                "name": "Partner 2",
                "company_group_id": cls.company_group.id,
            }
        )
        cls.partner_3 = cls.env["res.partner"].create(
            {
                "name": "Partner 3",
            }
        )

    def test_get_sale_order_domain_with_company_group(self):
        """Test domain generation for partner acting as a company group."""
        wizard = self.env["product.pricelist.print"]
        domain = wizard._get_sale_order_domain(self.company_group)

        group_domain = (
            "partner_id",
            "in",
            self.company_group.company_group_member_ids.ids,
        )
        self.assertIn(group_domain, domain)

        origin_domain = ("partner_id", "child_of", self.company_group.id)
        self.assertNotIn(origin_domain, domain)

    def test_get_sale_order_domain_without_company_group(self):
        """Test domain generation for partner without a company group."""
        wizard = self.env["product.pricelist.print"]
        domain = wizard._get_sale_order_domain(self.partner_3)
        self.assertTrue(isinstance(domain, list))
