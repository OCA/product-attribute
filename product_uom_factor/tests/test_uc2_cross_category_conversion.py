"""
Test UC2: Cross-Category Quantity and Price Conversion

As a salesperson or purchaser, I want quantity and price conversions between
UoMs of different categories (e.g. mL to g) to use the product-specific
conversion factor so that when I sell or purchase in a cross-category UoM,
the resulting quantities and prices are correct.

The cross-category UoM may come from the product's packaging UoMs (uom_ids)
or from a vendor pricelist (product.supplierinfo.product_uom_id).

Conversion factors are stored in product.uom.factor records linked to the
product template (product_tmpl_id), with an optional product_ids M2M to
restrict to specific variants.

Acceptance Criteria:
- Converting mL to g uses the product's factor (e.g. 500 mL * 1.05 = 525 g)
- Converting g to mL uses the inverse (e.g. 525 g / 1.05 = 500 mL)
- Different products with different factors produce different results
- Same-category conversions (e.g. g to kg) are unaffected by the factor
- Conversions between non-base units work (e.g. L to kg)
- Price per g converted to price per mL accounts for density
  (e.g. $0.10/g * 1.05 g/mL = $0.105/mL)
- Price per mL converted to price per g is the inverse
- Same-category price conversions (e.g. g to kg) are unaffected
- Without a product in context, standard behavior is preserved
"""

from odoo.tests.common import TransactionCase


class TestUC2CrossCategoryConversion(TransactionCase):
    """Test UC2: Cross-Category Quantity and Price Conversion"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_gram = cls.env.ref("uom.product_uom_gram")
        cls.uom_ml = cls.env.ref("uom.product_uom_milliliter")

        cls.product_cyan = cls.env["product.product"].create(
            {
                "name": "Ink - Cyan",
                "uom_id": cls.uom_gram.id,
            }
        )
        # Specific gravity 1.05: 1 mL = 1.05 g
        cls.env["product.uom.factor"].create(
            {
                "product_tmpl_id": cls.product_cyan.product_tmpl_id.id,
                "uom_id": cls.uom_ml.id,
                "factor": 1.05,
            }
        )

    def test_ml_to_gram_conversion(self):
        """500 mL of cyan ink (SG 1.05) should convert to 525 g."""
        result = self.uom_ml.with_context(
            product_id=self.product_cyan.id
        )._compute_quantity(500, self.uom_gram, round=False)
        self.assertAlmostEqual(
            result,
            525.0,
            places=2,
            msg="500 mL of cyan ink (SG 1.05) should be 525 g",
        )

    def test_gram_to_ml_conversion(self):
        """525 g of cyan ink (SG 1.05) should convert to 500 mL."""
        result = self.uom_gram.with_context(
            product_id=self.product_cyan.id
        )._compute_quantity(525, self.uom_ml, round=False)
        self.assertAlmostEqual(
            result,
            500.0,
            places=2,
            msg="525 g of cyan ink (SG 1.05) should be 500 mL",
        )

    def test_different_products_different_factors(self):
        """Two products with different densities should produce different
        conversion results for the same quantity."""
        product_magenta = self.env["product.product"].create(
            {
                "name": "Ink - Magenta",
                "uom_id": self.uom_gram.id,
            }
        )
        # Magenta ink: SG 1.10 (denser than cyan's 1.05)
        self.env["product.uom.factor"].create(
            {
                "product_tmpl_id": product_magenta.product_tmpl_id.id,
                "uom_id": self.uom_ml.id,
                "factor": 1.10,
            }
        )
        cyan_result = self.uom_ml.with_context(
            product_id=self.product_cyan.id
        )._compute_quantity(500, self.uom_gram, round=False)
        magenta_result = self.uom_ml.with_context(
            product_id=product_magenta.id
        )._compute_quantity(500, self.uom_gram, round=False)
        self.assertAlmostEqual(cyan_result, 525.0, places=2)
        self.assertAlmostEqual(magenta_result, 550.0, places=2)
        self.assertNotAlmostEqual(
            cyan_result,
            magenta_result,
            places=2,
            msg="Different densities should produce different results",
        )

    def test_same_category_conversion_unaffected(self):
        """Same-category conversions (g to kg) should use standard UoM
        factors and not be affected by the cross-category factor."""
        uom_kg = self.env.ref("uom.product_uom_kgm")
        result = self.uom_gram.with_context(
            product_id=self.product_cyan.id
        )._compute_quantity(1000, uom_kg, round=False)
        self.assertAlmostEqual(
            result,
            1.0,
            places=5,
            msg="1000 g should be 1 kg regardless of cross-category factor",
        )

    def test_non_base_unit_conversion(self):
        """Conversions between non-base units (L to kg) should work by
        chaining the standard UoM factor with the cross-category factor.
        1 L = 1000 mL, factor 1.05 g/mL => 1 L = 1050 g = 1.05 kg."""
        uom_liter = self.env.ref("uom.product_uom_litre")
        uom_kg = self.env.ref("uom.product_uom_kgm")
        result = uom_liter.with_context(
            product_id=self.product_cyan.id
        )._compute_quantity(1, uom_kg, round=False)
        self.assertAlmostEqual(
            result,
            1.05,
            places=5,
            msg="1 L of cyan ink (SG 1.05) should be 1.05 kg",
        )

    def test_price_gram_to_ml(self):
        """Price per g converted to price per mL should account for density.
        $0.10/g * 1.05 g/mL = $0.105/mL."""
        result = self.uom_gram.with_context(
            product_id=self.product_cyan.id
        )._compute_price(0.10, self.uom_ml)
        self.assertAlmostEqual(
            result,
            0.105,
            places=5,
            msg="$0.10/g should be $0.105/mL for ink with SG 1.05",
        )

    def test_price_ml_to_gram(self):
        """Price per mL converted to price per g is the inverse.
        $0.105/mL / 1.05 g/mL = $0.10/g."""
        result = self.uom_ml.with_context(
            product_id=self.product_cyan.id
        )._compute_price(0.105, self.uom_gram)
        self.assertAlmostEqual(
            result,
            0.10,
            places=5,
            msg="$0.105/mL should be $0.10/g for ink with SG 1.05",
        )

    def test_same_category_price_unaffected(self):
        """Same-category price conversions (g to kg) should use standard
        UoM factors and not be affected by the cross-category factor."""
        uom_kg = self.env.ref("uom.product_uom_kgm")
        result = self.uom_gram.with_context(
            product_id=self.product_cyan.id
        )._compute_price(0.10, uom_kg)
        self.assertAlmostEqual(
            result,
            100.0,
            places=5,
            msg="$0.10/g should be $100/kg regardless of cross-category factor",
        )

    def test_no_product_in_context_standard_behavior(self):
        """Without a product_id in context, cross-category conversions
        should fall back to standard Odoo behavior (1:1 between base units)."""
        result_with = self.uom_ml.with_context(
            product_id=self.product_cyan.id
        )._compute_quantity(500, self.uom_gram, round=False)
        result_without = self.uom_ml._compute_quantity(500, self.uom_gram, round=False)
        self.assertAlmostEqual(result_with, 525.0, places=2)
        self.assertAlmostEqual(
            result_without,
            500.0,
            places=2,
            msg="Without product in context, standard 1:1 base-unit conversion",
        )

    def test_compute_quantity_with_rounding(self):
        """Cross-category conversion with round=True should round result."""
        result = self.uom_ml.with_context(
            product_id=self.product_cyan.id
        )._compute_quantity(500, self.uom_gram, round=True)
        self.assertAlmostEqual(result, 525.0, places=0)

    def test_compute_quantity_nonexistent_product(self):
        """A nonexistent product_id in context should fall back to super."""
        result = self.uom_ml.with_context(product_id=99999)._compute_quantity(
            500, self.uom_gram, round=False
        )
        self.assertAlmostEqual(result, 500.0, places=2)

    def test_find_product_uom_for_category_newid(self):
        """_find_product_uom_for_category returns None for non-int IDs."""
        from odoo.orm.identifiers import NewId

        result = self.uom_ml._find_product_uom_for_category(NewId(), self.uom_gram)
        self.assertIsNone(result)

    def test_find_product_uom_for_category_fallback(self):
        """When the exact UoM isn't on a factor line but a same-category
        UoM is, _find_product_uom_for_category should return it."""
        uom_litre = self.env.ref("uom.product_uom_litre")
        # Factor is defined for mL; searching for L should find it via
        # the category fallback path.
        result = self.uom_gram._find_product_uom_for_category(
            self.product_cyan.id, uom_litre
        )
        self.assertTrue(result)
        self.assertTrue(result.uom_id._has_common_reference(uom_litre))

    def test_compute_quantity_same_uom(self):
        """Converting a UoM to itself should return the original qty."""
        result = self.uom_ml.with_context(
            product_id=self.product_cyan.id
        )._compute_quantity(500, self.uom_ml, round=False)
        self.assertAlmostEqual(result, 500.0, places=2)

    def test_compute_price_same_uom(self):
        """Converting a price to the same UoM should return the original."""
        result = self.uom_ml.with_context(
            product_id=self.product_cyan.id
        )._compute_price(10.0, self.uom_ml)
        self.assertAlmostEqual(result, 10.0, places=2)

    def test_compute_price_nonexistent_product(self):
        """A nonexistent product_id in context should fall back to super."""
        result = self.uom_ml.with_context(product_id=99999)._compute_price(
            10.0, self.uom_gram
        )
        self.assertAlmostEqual(result, 10.0, places=2)
