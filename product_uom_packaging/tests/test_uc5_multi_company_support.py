"""
Test UC5: Multi-Company Support

As a multi-company user, I want to have different packaging configurations per company
so that each warehouse/company can define their own packaging standards.

Acceptance Criteria:
- Company field on packaging configuration
- Unique constraint includes company
- Records are filtered by current company in standard views
"""

from odoo.exceptions import ValidationError
from odoo.tests import Form
from odoo.tests.common import TransactionCase
from odoo.tools.misc import mute_logger


class TestUC5MultiCompanySupport(TransactionCase):
    """Test UC5: Multi-Company Support"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductUomPackaging = cls.env["product.uom.packaging"]

        # Products
        cls.product_a = cls.env["product.product"].create({"name": "Product A"})

        # UoMs
        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")

        # Companies
        cls.company_main = cls.env.company
        cls.company_other = cls.env["res.company"].create({"name": "Other Company"})

        # Package Types
        cls.package_small = cls.env["stock.package.type"].create(
            {
                "name": "Small Box",
                "packaging_length": 10,
                "width": 10,
                "height": 10,
                "base_weight": 0.5,
                "max_weight": 10,
            }
        )

    def test_default_company_assignment(self):
        """UC5: New records default to current user's company."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_small.id,
            }
        )
        self.assertEqual(packaging.company_id, self.env.company)

    def test_same_config_allowed_for_different_companies(self):
        """UC5: Same template/UoM/package_type can exist for different companies."""
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "company_id": self.company_main.id,
                "package_type_id": self.package_small.id,
            }
        )
        packaging_other = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "company_id": self.company_other.id,
                "package_type_id": self.package_small.id,
            }
        )
        self.assertEqual(packaging_other.company_id, self.company_other)

    def test_company_field_in_form(self):
        """UC5: company_id is accessible on the packaging form."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_small.id,
            }
        )
        with Form(packaging) as f:
            self.assertTrue(hasattr(f, "company_id"))

    @mute_logger("odoo.sql_db")
    def test_duplicate_within_same_company_rejected(self):
        """UC5: Cannot create duplicate template/UoM/package_type
        within same company."""
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "company_id": self.company_main.id,
                "package_type_id": self.package_small.id,
            }
        )
        with self._assertRaises(ValidationError):
            self.ProductUomPackaging.create(
                {
                    "product_tmpl_id": self.product_a.product_tmpl_id.id,
                    "uom_id": self.uom_dozen.id,
                    "company_id": self.company_main.id,
                    "package_type_id": self.package_small.id,
                }
            )
