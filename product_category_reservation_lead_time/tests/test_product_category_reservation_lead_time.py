from psycopg2 import IntegrityError

from odoo.tests import common
from odoo.tools import mute_logger


class TestProductCategoryReservationLeadTime(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Rule = cls.env["product.category.reservation.rule"]
        cls.Category = cls.env["product.category"]

        cls.company_a = cls.env.company
        cls.company_a.reservation_lead_days = 15
        cls.company_b = cls.env["res.company"].create({"name": "Reservation Test Co B"})
        cls.company_b.reservation_lead_days = 20

        # Category tree: root -> child -> grandchild
        cls.categ_root = cls.Category.create({"name": "Reservation Root"})
        cls.categ_child = cls.Category.create(
            {"name": "Reservation Child", "parent_id": cls.categ_root.id}
        )
        cls.categ_grandchild = cls.Category.create(
            {"name": "Reservation Grandchild", "parent_id": cls.categ_child.id}
        )

    def _resolve(self, category, company):
        return self.Rule._resolve_reservation_days(category, company)

    # V5 — no rule anywhere -> global default of the company
    def test_01_global_default(self):
        self.assertEqual(self._resolve(self.categ_grandchild, self.company_a), 15)

    # V1 — rule directly on the category -> its own value
    def test_02_rule_on_category(self):
        self.Rule.create(
            {
                "category_id": self.categ_grandchild.id,
                "company_id": self.company_a.id,
                "reservation_days": 7,
            }
        )
        self.assertEqual(self._resolve(self.categ_grandchild, self.company_a), 7)

    # V4 — inheritance: child without its own rule uses the ancestor's
    def test_03_inherit_from_ancestor(self):
        self.Rule.create(
            {
                "category_id": self.categ_root.id,
                "company_id": self.company_a.id,
                "reservation_days": 30,
            }
        )
        # grandchild has no rule -> resolves through child -> root
        self.assertEqual(self._resolve(self.categ_grandchild, self.company_a), 30)

    # V4 — override: the most specific rule wins over the ancestor's
    def test_04_child_overrides_ancestor(self):
        self.Rule.create(
            {
                "category_id": self.categ_root.id,
                "company_id": self.company_a.id,
                "reservation_days": 30,
            }
        )
        self.Rule.create(
            {
                "category_id": self.categ_grandchild.id,
                "company_id": self.company_a.id,
                "reservation_days": 5,
            }
        )
        self.assertEqual(self._resolve(self.categ_grandchild, self.company_a), 5)

    # V13 — a lead time of 0 is valid and not confused with "not configured"
    def test_05_zero_lead_time(self):
        self.Rule.create(
            {
                "category_id": self.categ_grandchild.id,
                "company_id": self.company_a.id,
                "reservation_days": 0,
            }
        )
        self.assertEqual(self._resolve(self.categ_grandchild, self.company_a), 0)

    # V12 — multi-company: same category, different rule per company
    def test_06_multicompany_rules(self):
        self.Rule.create(
            {
                "category_id": self.categ_child.id,
                "company_id": self.company_a.id,
                "reservation_days": 5,
            }
        )
        self.Rule.create(
            {
                "category_id": self.categ_child.id,
                "company_id": self.company_b.id,
                "reservation_days": 12,
            }
        )
        self.assertEqual(self._resolve(self.categ_child, self.company_a), 5)
        self.assertEqual(self._resolve(self.categ_child, self.company_b), 12)

    # V12 — no rule for this company -> that company's own global default
    def test_07_multicompany_falls_back_to_own_global(self):
        self.Rule.create(
            {
                "category_id": self.categ_child.id,
                "company_id": self.company_a.id,
                "reservation_days": 5,
            }
        )
        # company_b has no rule for this category -> its global (20)
        self.assertEqual(self._resolve(self.categ_child, self.company_b), 20)

    # V8 — editing the global default affects the next resolution
    def test_08_editable_global(self):
        self.company_a.reservation_lead_days = 3
        self.assertEqual(self._resolve(self.categ_grandchild, self.company_a), 3)

    # Inactive rules are ignored (search excludes them) -> falls back
    def test_09_inactive_rule_ignored(self):
        self.Rule.create(
            {
                "category_id": self.categ_grandchild.id,
                "company_id": self.company_a.id,
                "reservation_days": 2,
                "active": False,
            }
        )
        self.assertEqual(self._resolve(self.categ_grandchild, self.company_a), 15)

    # Constraint — one rule per (category, company)
    def test_10_unique_constraint(self):
        self.Rule.create(
            {
                "category_id": self.categ_child.id,
                "company_id": self.company_a.id,
                "reservation_days": 5,
            }
        )
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            with self.cr.savepoint():
                self.Rule.create(
                    {
                        "category_id": self.categ_child.id,
                        "company_id": self.company_a.id,
                        "reservation_days": 9,
                    }
                )

    # Constraint — no negative lead time
    def test_11_negative_days_constraint(self):
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            with self.cr.savepoint():
                self.Rule.create(
                    {
                        "category_id": self.categ_child.id,
                        "company_id": self.company_a.id,
                        "reservation_days": -1,
                    }
                )
