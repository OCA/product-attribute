# Copyright 2025 ForgeFlow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo.addons.base.tests.common import BaseCommon


class TestProductCategoryNameTranslatable(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        categ_obj = cls.env["product.category"]
        cls.parent_categ = categ_obj.create({"name": "Test Category"})
        lang_es = cls.env.ref("base.lang_es")
        if not lang_es.active:
            lang_es.toggle_active()

    def test_product_category_name_translatable(self):
        # Update translated name
        self.parent_categ.with_context(lang="es_ES").write(
            {"name": "Categoria de Prueba"}
        )
        self.assertEqual(
            self.parent_categ.with_context(lang="es_ES").name, "Categoria de Prueba"
        )
        self.assertEqual(self.parent_categ.name, "Test Category")
