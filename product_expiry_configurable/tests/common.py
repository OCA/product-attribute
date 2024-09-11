# Copyright 2022 Creu Blanca
# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


class ProductExpiryCategoryCommon:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.ProductProduct = cls.env["product.product"]
        cls.ProductCategory = cls.env["product.category"]
        cls.StockProductionLot = cls.env["stock.lot"]
        cls.ProductCategory._parent_store_compute()
        cls.categ_lvl = cls.env.ref("product.product_category_all")
        cls.categ_lvl_1 = cls.ProductCategory.create(
            {"name": "level_1", "parent_id": cls.categ_lvl.id}
        )
        cls.categ_lvl_1_1 = cls.ProductCategory.create(
            {"name": "level_1_1", "parent_id": cls.categ_lvl_1.id}
        )

        cls.categ_lvl_1_1_1 = cls.ProductCategory.create(
            {"name": "level_1_1_1", "parent_id": cls.categ_lvl_1_1.id}
        )
        cls.product = cls.ProductProduct.create(
            {
                "name": "test product",
                "categ_id": cls.categ_lvl_1_1_1.id,
                "type": "product",
            }
        )

    @classmethod
    def _get_times(cls):
        return ["alert_time", "use_time", "removal_time"]
