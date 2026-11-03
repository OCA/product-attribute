# Copyright 2026 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo_test_helper import FakeModelLoader

from odoo.exceptions import AccessError, UserError
from odoo.fields import Command
from odoo.tests import Form, TransactionCase, new_test_user


class TestProductAttributeValueMerge(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import ProductAttributeValueFakeRecord

        cls.loader.update_registry((ProductAttributeValueFakeRecord,))
        cls.env["res.lang"]._activate_lang("es_ES")
        cls.env["res.lang"]._activate_lang("fr_FR")
        # Internal users work in Spanish; French is only a customer language
        cls.manager = new_test_user(
            cls.env,
            login="pav_merge_manager",
            groups="base.group_user,product.group_product_manager",
            lang="es_ES",
        )
        cls.user = new_test_user(
            cls.env, login="pav_merge_user", groups="base.group_user"
        )
        cls.env = cls.env(user=cls.manager)
        cls.attribute = cls.env["product.attribute"].create(
            {"name": "Weight", "create_variant": "always"}
        )
        cls.v34, cls.v34b, cls.v45, cls.v23 = cls.env["product.attribute.value"].create(
            [
                {"name": "3-4kg", "attribute_id": cls.attribute.id},
                {"name": "3/4kg", "attribute_id": cls.attribute.id},
                {"name": "4-5kg", "attribute_id": cls.attribute.id},
                {"name": "2-3kg", "attribute_id": cls.attribute.id},
            ]
        )
        # Created by a Spanish user who typed the name the way it is shown
        cls.v34b.update_field_translations("name", {"es_ES": "3-4kg"})
        cls.product_a = cls._create_template("Hake", cls.v34 | cls.v45)
        cls.product_b = cls._create_template("Cod", cls.v34b | cls.v45)
        records = cls.env["product.attribute.value.fake.record"].sudo()
        cls.lot = records.create(
            {
                "name": "Lot",
                "value_id": cls.v34b.id,
                "value_ids": [Command.set(cls.v34b.ids)],
            }
        )
        cls.both = records.create(
            {"name": "Both", "value_ids": [Command.set((cls.v34 | cls.v34b).ids)]}
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super().tearDownClass()

    @classmethod
    def _create_template(cls, name, values):
        return cls.env["product.template"].create(
            {
                "name": name,
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": cls.attribute.id,
                            "value_ids": [Command.set(values.ids)],
                        }
                    )
                ],
            }
        )

    def _snapshot(self):
        """Rows a merge touches, to compare before and after an undo."""
        self.env.flush_all()
        cr = self.env.cr
        result = {}
        for key, query in {
            "ptav": "SELECT id, product_attribute_value_id, attribute_line_id,"
            " ptav_active FROM product_template_attribute_value ORDER BY id",
            "lines": "SELECT * FROM"
            " product_attribute_value_product_template_attribute_line_rel"
            " ORDER BY 1, 2",
            "variants": "SELECT id, combination_indices, active FROM product_product"
            " ORDER BY id",
            "records": "SELECT id, value_id FROM product_attribute_value_fake_record"
            " ORDER BY id",
            "record_values": "SELECT * FROM product_attribute_value_fake_record_rel"
            " ORDER BY 1, 2",
            "values": "SELECT id, name, active, merged_into_id, html_color"
            " FROM product_attribute_value ORDER BY id",
        }.items():
            cr.execute(query)
            result[key] = cr.fetchall()
        return result

    def _merge(self, values, keeper=None, names=None):
        """Merge through the wizard as from the merge button of a value."""
        action = values[:1].action_merge()
        wizard_form = Form(
            self.env[action["res_model"]].with_context(**action["context"])
        )
        for value in values - wizard_form.value_ids[:]:
            wizard_form.value_ids.add(value)
        if keeper:
            wizard_form.keeper_id = keeper
        for code, name in (names or {}).items():
            for index in range(len(wizard_form.name_ids)):
                with wizard_form.name_ids.edit(index) as line:
                    if line.lang == code:
                        line.name = name
        wizard = wizard_form.save()
        action = wizard.action_merge()
        return self.env[action["res_model"]].browse(action["res_id"])

    def test_find_duplicates(self):
        loose = self.env["product.attribute.value"].create(
            {"name": "2 / 3 kg", "attribute_id": self.attribute.id}
        )
        action = self.attribute.action_find_duplicate_values()
        finder = self.env[action["res_model"]].browse(action["res_id"])
        # Only Spanish users see 3/4kg as 3-4kg, that is enough
        self.assertEqual(finder.group_ids.value_ids, self.v34 | self.v34b)
        finder.loose = True
        finder.action_search()
        self.assertEqual(len(finder.group_ids), 2)
        self.assertIn(self.v23 | loose, [group.value_ids for group in finder.group_ids])

    def test_find_duplicates_in_chosen_languages(self):
        # A wrong customer translation gives two different values the same name
        self.v23.update_field_translations("name", {"fr_FR": "4-5 kg"})
        action = self.attribute.action_find_duplicate_values()
        finder = self.env[action["res_model"]].browse(action["res_id"])
        self.assertNotIn("fr_FR", finder.lang_ids.mapped("code"))
        self.assertNotIn(
            self.v23 | self.v45, [group.value_ids for group in finder.group_ids]
        )
        finder.lang_ids |= self.env["res.lang"]._lang_get("fr_FR")
        finder.action_search()
        group = finder.group_ids.filtered(lambda g: self.v23 in g.value_ids)
        self.assertEqual(group.value_ids, self.v23 | self.v45)
        self.assertIn("fr_FR", group.matches)

    def test_warn_unknown_reference(self):
        # A table left by an uninstalled module still points to the values
        self.env.cr.execute(
            "CREATE TABLE pav_merge_leftover (value_id integer"
            " REFERENCES product_attribute_value(id) ON DELETE CASCADE)"
        )
        self.env.cr.execute(
            "INSERT INTO pav_merge_leftover VALUES (%s)", (self.v34b.id,)
        )
        # A company dependent field is not moved either
        self.lot.company_value_id = self.v34b
        action = self.v34b.action_merge()
        wizard_form = Form(
            self.env[action["res_model"]].with_context(**action["context"])
        )
        wizard_form.keeper_id = self.v34
        self.assertIn("pav_merge_leftover", wizard_form.warning)
        self.assertIn("Company Value", wizard_form.warning)
        wizard_form.save().action_merge()
        # The merged value is archived, not deleted: the leftover rows survive
        self.env.cr.execute("SELECT value_id FROM pav_merge_leftover")
        self.assertEqual(self.env.cr.fetchall(), [(self.v34b.id,)])

    def test_merge_wizard_proposal(self):
        action = self.v34b.action_merge()
        wizard_form = Form(
            self.env[action["res_model"]].with_context(**action["context"])
        )
        self.assertEqual(wizard_form.value_ids[:], self.v34 | self.v34b)
        wizard_form.keeper_id = self.v34
        wizard = wizard_form.save()
        roles = {line.value_id: line.role for line in wizard.line_ids}
        self.assertEqual(roles, {self.v34: "keep", self.v34b: "merge"})
        # The kept value is chosen in its field: the list follows
        wizard.keeper_id = self.v34b
        roles = {line.value_id: line.role for line in wizard.line_ids}
        self.assertEqual(roles, {self.v34: "merge", self.v34b: "keep"})
        wizard.keeper_id = self.v34
        names = {line.lang: line for line in wizard.name_ids}
        self.assertEqual(names["en_US"].name, "3-4kg")
        self.assertEqual(names["en_US"].alternatives, "3/4kg")
        self.assertTrue(names["en_US"].conflict)
        # The kept value has no Spanish name: the merged one gives it
        self.assertEqual(names["es_ES"].name, "3-4kg")
        self.assertFalse(names["es_ES"].conflict)

    def test_merge_keeps_variants(self):
        variants = (self.product_a | self.product_b).product_variant_ids
        indices = variants.mapped("combination_indices")
        ptav_b = self.product_b.attribute_line_ids.product_template_value_ids.filtered(
            lambda ptav: ptav.product_attribute_value_id == self.v34b
        )
        merge = self._merge(self.v34 | self.v34b, keeper=self.v34)
        self.assertEqual(
            (self.product_a | self.product_b).product_variant_ids, variants
        )
        self.assertEqual(variants.mapped("combination_indices"), indices)
        self.assertEqual(ptav_b.product_attribute_value_id, self.v34)
        self.assertEqual(
            self.product_b.attribute_line_ids.value_ids, self.v34 | self.v45
        )
        self.assertEqual(self.lot.value_id, self.v34)
        self.assertEqual(self.lot.value_ids, self.v34)
        self.assertEqual(self.both.value_ids, self.v34)
        self.assertFalse(self.v34b.active)
        self.assertEqual(self.v34b.merged_into_id, self.v34)
        self.assertEqual(self.v34.with_context(lang="es_ES").name, "3-4kg")
        self.assertEqual(merge.state, "done")
        self.assertEqual(self.attribute.value_merge_count, 1)
        # Creating a variant with the kept value still works
        self.product_b.attribute_line_ids.value_ids = [Command.link(self.v23.id)]
        self.assertEqual(len(self.product_b.product_variant_ids), 3)

    def test_undo_restores_everything(self):
        self.v34b.html_color = "#ff0000"
        before = self._snapshot()
        merge = self._merge(
            self.v34 | self.v34b, keeper=self.v34, names={"en_US": "3-4 kg"}
        )
        self.assertEqual(self.v34.with_context(lang="en_US").name, "3-4 kg")
        # French had no name of its own: it keeps following en_US
        self.assertEqual(self.v34.with_context(lang="fr_FR").name, "3-4 kg")
        self.assertEqual(self.v34.html_color, "#ff0000")
        merge.action_undo()
        self.assertEqual(merge.state, "undone")
        self.assertFalse(merge.undo_report)
        self.assertEqual(self._snapshot(), before)

    def test_undo_keeps_later_changes(self):
        merge = self._merge(
            self.v34 | self.v34b, keeper=self.v34, names={"en_US": "3-4 kg"}
        )
        # After the merge, users go on working with the kept value
        self.v34.with_context(lang="en_US").name = "3-4 KG"
        self.lot.value_id = self.v45
        product_c = self._create_template("Monkfish", self.v34)
        self.product_b.attribute_line_ids.value_ids = [Command.unlink(self.v34.id)]
        merge.action_undo()
        self.assertTrue(merge.undo_report)
        self.assertEqual(self.lot.value_id, self.v45)
        self.assertEqual(self.lot.value_ids, self.v34b)
        self.assertEqual(product_c.attribute_line_ids.value_ids, self.v34)
        self.assertEqual(self.product_b.attribute_line_ids.value_ids, self.v45)
        self.assertEqual(
            self.product_a.attribute_line_ids.value_ids, self.v34 | self.v45
        )
        self.assertTrue(self.v34b.active)
        self.assertFalse(self.v34b.merged_into_id)
        self.assertEqual(self.v34.with_context(lang="en_US").name, "3-4 KG")
        self.assertIn("en_US", merge.undo_report)

    def test_shared_line(self):
        product_both = self._create_template("Squid", self.v34 | self.v34b)
        variants = product_both.product_variant_ids
        before = self._snapshot()
        action = self.v34b.action_merge()
        wizard_form = Form(
            self.env[action["res_model"]].with_context(**action["context"])
        )
        wizard_form.keeper_id = self.v34
        self.assertEqual(wizard_form.shared_product_tmpl_ids[:], product_both)
        self.assertTrue(wizard_form.warning)
        merge = self.env["product.attribute.value.merge"].browse(
            wizard_form.save().action_merge()["res_id"]
        )
        self.assertEqual(product_both.product_variant_ids, variants)
        self.assertEqual(
            product_both.attribute_line_ids.value_ids, self.v34 | self.v34b
        )
        self.assertEqual(
            self.product_b.attribute_line_ids.value_ids, self.v34 | self.v45
        )
        self.assertTrue(self.v34b.active)
        self.assertEqual(merge.kept_value_ids, self.v34b)
        # Merging the same values again moves nothing
        with self.assertRaises(UserError):
            self._merge(self.v34 | self.v34b, keeper=self.v34)
        merge.action_undo()
        self.assertEqual(self._snapshot(), before)

    def test_value_left_on_archived_variants(self):
        product_c = self._create_template("Monkfish", self.v34b | self.v45)
        variant = product_c.product_variant_ids.filtered(
            lambda p: self.v34b
            in p.product_template_attribute_value_ids.mapped(
                "product_attribute_value_id"
            )
        )
        self.lot.product_id = variant
        # The user replaced 3/4kg with 3-4kg by hand: the used variant is archived
        line = product_c.attribute_line_ids
        line.value_ids = [Command.set((self.v34 | self.v45).ids)]
        archived_ptav = line.with_context(
            active_test=False
        ).product_template_value_ids.filtered(lambda ptav: not ptav.ptav_active)
        self.assertEqual(archived_ptav.product_attribute_value_id, self.v34b)
        before = self._snapshot()
        merge = self._merge(self.v34 | self.v34b, keeper=self.v34)
        self.assertFalse(merge.kept_value_ids)
        self.assertFalse(self.v34b.active)
        self.assertEqual(archived_ptav.product_attribute_value_id, self.v34b)
        self.assertEqual(line.value_ids, self.v34 | self.v45)
        self.assertEqual(
            self.product_b.attribute_line_ids.value_ids, self.v34 | self.v45
        )
        merge.action_undo()
        self.assertEqual(self._snapshot(), before)

    def test_merge_archived_value(self):
        old = self.env["product.attribute.value"].create(
            {"name": "3 - 4 kg", "attribute_id": self.attribute.id}
        )
        old.action_archive()
        before = self._snapshot()
        merge = self._merge(self.v34 | old, keeper=self.v34)
        self.assertEqual(old.merged_into_id, self.v34)
        merge.action_undo()
        self.assertFalse(old.active)
        self.assertEqual(self._snapshot(), before)

    def test_undo_order(self):
        first = self._merge(self.v34 | self.v34b, keeper=self.v34)
        second = self._merge(self.v23 | self.v34, keeper=self.v23)
        with self.assertRaises(UserError):
            first.action_undo()
        second.action_undo()
        first.action_undo()
        self.assertTrue(all((self.v34 | self.v34b).mapped("active")))

    def test_merge_needs_product_manager(self):
        with self.assertRaises(AccessError):
            self.env["product.attribute.value.merge.wizard"].with_user(
                self.user
            ).create({"value_ids": [Command.set((self.v34 | self.v34b).ids)]})
        merge = self._merge(self.v34 | self.v34b, keeper=self.v34)
        with self.assertRaises(AccessError):
            merge.with_user(self.user).read(["state"])
        # Other users still read the attributes
        self.attribute.with_user(self.user).read()

    def test_merge_log_is_read_only(self):
        merge = self._merge(self.v34 | self.v34b, keeper=self.v34)
        # The undo moves what the log says: managers cannot write it
        with self.assertRaises(AccessError):
            merge.write({"keeper_id": self.v23.id})
        with self.assertRaises(AccessError):
            merge.change_ids[:1].write({"model": "res.users"})
        with self.assertRaises(AccessError):
            self.env["product.attribute.value.merge"].create({"keeper_id": self.v34.id})
        # A field that is not an attribute value reference is never moved back
        groups_before = self.manager.groups_id
        merge.change_ids.sudo().create(
            {
                "merge_id": merge.id,
                "kind": "many2many",
                "model": "res.users",
                "field_name": "groups_id",
                "value_id": self.v34b.id,
                "res_ids": [self.manager.id],
            }
        )
        merge.action_undo()
        self.assertTrue(merge.undo_report)
        self.assertEqual(self.manager.groups_id, groups_before)
