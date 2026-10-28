import importlib.util

from odoo.tools import SQL, file_path

from odoo.addons.base.tests.common import BaseCommon


def _load_script():
    path = file_path("product_customerinfo/migrations/20.0.1.0.0/pre-migration.py")
    spec = importlib.util.spec_from_file_location("customerinfo_pre_migration", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPreMigration(BaseCommon):
    _test_user_groups = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.script = _load_script()
        cls.unit, cls.other_unit = cls.env["uom.uom"].search([], limit=2)
        product = cls.env["product.product"].create({"name": "Test product"})
        cls.customerinfo = cls.env["product.customerinfo"].create(
            {
                "partner_id": cls.partner.id,
                "product_tmpl_id": product.product_tmpl_id.id,
                "uom_id": cls.other_unit.id,
            }
        )
        cls.env.flush_all()

    def _columns(self):
        self.env.cr.execute(
            """
            SELECT column_name FROM information_schema.columns
             WHERE table_name = 'product_customerinfo'
               AND column_name IN ('uom_id', 'product_uom_id')
            """
        )
        return {row[0] for row in self.env.cr.fetchall()}

    def _uom(self, column):
        self.env.cr.execute(
            SQL(
                "SELECT %s FROM product_customerinfo WHERE id = %s",
                SQL.identifier(column),
                self.customerinfo.id,
            )
        )
        return self.env.cr.fetchone()[0]

    def test_renames_the_old_column(self):
        self.env.cr.execute(
            "ALTER TABLE product_customerinfo RENAME COLUMN uom_id TO product_uom_id"
        )
        self.script.migrate(self.env.cr, "19.0.1.0.1")
        self.assertEqual(self._columns(), {"uom_id"})
        self.assertEqual(self._uom("uom_id"), self.other_unit.id)

    def test_copies_the_old_column_when_both_exist(self):
        self.env.cr.execute(
            "ALTER TABLE product_customerinfo ADD COLUMN product_uom_id integer"
        )
        self.env.cr.execute(
            "UPDATE product_customerinfo SET uom_id = %s, product_uom_id = %s",
            (self.unit.id, self.other_unit.id),
        )
        self.script.migrate(self.env.cr, "19.0.1.0.1")
        self.assertEqual(self._uom("uom_id"), self.other_unit.id)

    def test_does_nothing_without_the_old_column(self):
        self.script.migrate(self.env.cr, "19.0.1.0.1")
        self.assertEqual(self._columns(), {"uom_id"})
        self.assertEqual(self._uom("uom_id"), self.other_unit.id)

    def test_renames_the_field_record_and_its_xmlid(self):
        cr = self.env.cr
        old = "field_product_customerinfo__product_uom_id"
        new = "field_product_customerinfo__uom_id"
        cr.execute(
            "ALTER TABLE product_customerinfo RENAME COLUMN uom_id TO product_uom_id"
        )
        cr.execute(
            """
            UPDATE ir_model_fields SET name = 'product_uom_id'
             WHERE model = 'product.customerinfo' AND name = 'uom_id'
            """
        )
        cr.execute(
            "UPDATE ir_model_data SET name = %s "
            "WHERE module = 'product_customerinfo' AND name = %s",
            (old, new),
        )
        cr.execute(
            """
            SELECT id FROM ir_model_fields
             WHERE model = 'product.customerinfo' AND name = 'product_uom_id'
            """
        )
        field_id = cr.fetchone()[0]
        self.script.migrate(cr, "19.0.1.0.1")
        cr.execute("SELECT name FROM ir_model_fields WHERE id = %s", (field_id,))
        self.assertEqual(cr.fetchone()[0], "uom_id")
        cr.execute(
            "SELECT res_id FROM ir_model_data "
            "WHERE module = 'product_customerinfo' AND name = %s",
            (new,),
        )
        self.assertEqual(cr.fetchone()[0], field_id)
