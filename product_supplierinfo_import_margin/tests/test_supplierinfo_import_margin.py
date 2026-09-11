from odoo.tests.common import TransactionCase


class TestSupplierinfoImportMargin(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.wizard = cls.env["product.supplierinfo.import"].new(
            {
                "sale_margin": 15.0,
            }
        )

    def test_prepare_supplierinfo_values(self):
        """Test that sale_margin is added to the values."""
        row_data = {}
        values = self.wizard._prepare_supplierinfo_values(row_data)
        self.assertEqual(values.get("sale_margin"), 15.0)
