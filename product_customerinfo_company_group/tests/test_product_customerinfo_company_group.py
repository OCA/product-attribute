# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestProductCustomerinfoCompanyGroup(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.CustomerInfo = cls.env["product.customerinfo"]
        cls.product = cls.env["product.product"].create(
            {"name": "Test product", "type": "consu"}
        )
        cls.company_group = cls.env["res.partner"].create(
            {"name": "Test Group HQ", "is_company": True}
        )
        cls.parent_company = cls.env["res.partner"].create(
            {
                "name": "Test Parent Co",
                "is_company": True,
                "company_group_id": cls.company_group.id,
            }
        )
        # ``company_group_id`` is a commercial field: it is synced down from
        # ``parent_company`` onto ``client`` as soon as ``parent_id`` is set.
        cls.client = cls.env["res.partner"].create(
            {
                "name": "Test Client Contact",
                "parent_id": cls.parent_company.id,
            }
        )

    def _create_customerinfo(self, partner, **values):
        return self.CustomerInfo.create(
            {
                "partner_id": partner.id,
                "product_id": self.product.id,
                **values,
            }
        )

    def test_client_level_takes_precedence(self):
        """A client-level match wins even when the parent company and the
        company group also have one with a "better" sequence/price."""
        self._create_customerinfo(
            self.company_group, product_code="GROUP", sequence=1, price=1.0
        )
        self._create_customerinfo(
            self.parent_company, product_code="PARENT", sequence=1, price=1.0
        )
        client_info = self._create_customerinfo(
            self.client, product_code="CLIENT", sequence=10, price=10.0
        )

        result = self.product._select_customerinfo(partner=self.client)

        self.assertEqual(result, client_info)

    def test_falls_back_to_parent_company(self):
        self._create_customerinfo(self.company_group, product_code="GROUP")
        parent_info = self._create_customerinfo(
            self.parent_company, product_code="PARENT"
        )

        result = self.product._select_customerinfo(partner=self.client)

        self.assertEqual(result, parent_info)

    def test_falls_back_to_company_group(self):
        """``company_group_id`` is an explicit tag independent of the
        ``parent_id``/``commercial_partner_id`` chain, so it cannot be
        reached without looking it up on its own."""
        group_info = self._create_customerinfo(self.company_group, product_code="GROUP")

        result = self.product._select_customerinfo(partner=self.client)

        self.assertEqual(result, group_info)

    def test_no_customerinfo_returns_empty(self):
        result = self.product._select_customerinfo(partner=self.client)

        self.assertFalse(result)
