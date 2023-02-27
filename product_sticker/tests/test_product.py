from .common import ProductStickerCommon


class TestStickersOnProducts(ProductStickerCommon):
    def test_global_stickers(self):
        stickers = self.product_as500.get_product_stickers()
        self.assertEqual(len(stickers), 1, "Global sticker must be present")

    def test_product_template_stickers(self):
        stickers = self.product_as400.get_product_stickers()
        self.assertEqual(
            len(stickers), 1, "Attribute that create variants has been generated"
        )
        # Add a new attribute value to the template
        self.product_as400.attribute_line_ids.filtered(
            lambda al: al.attribute_id == self.att_license
        ).write(
            {
                "value_ids": [(4, self.att_license_freemium.id)],
            }
        )
        new_stickers = self.product_as400.get_product_stickers()
        self.assertEqual(
            len(new_stickers), 2, "Attribute Value sticker must be present"
        )

    def test_product_product_stickers(self):
        stickers = self.product_as400.product_variant_ids[0].get_product_stickers()
        self.assertEqual(
            len(stickers), 2, "Attribute that create variants has been generated"
        )
        # Add a new attribute value to the template
        self.product_as400.attribute_line_ids.filtered(
            lambda al: al.attribute_id == self.att_license
        ).write(
            {
                "value_ids": [(4, self.att_license_freemium.id)],
            }
        )
        new_stickers = self.product_as400.product_variant_ids[0].get_product_stickers()
        self.assertEqual(
            len(new_stickers),
            3,
            "Sticker for Attribute with no create variants not present",
        )
