import base64
import io

from PIL import Image

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class ProductStickerCommon(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        pa_model = cls.env["product.attribute"]
        pav_model = cls.env["product.attribute.value"]
        ps_model = cls.env["product.sticker"]
        pt_model = cls.env["product.template"]
        # No Variant Attribute
        cls.att_platform = pa_model.create(
            {"name": "Platform", "create_variant": "always"}
        )
        cls.att_platform_linux = pav_model.create(
            {"attribute_id": cls.att_platform.id, "name": "Linux"}
        )
        cls.att_platform_windows = pav_model.create(
            {"attribute_id": cls.att_platform.id, "name": "Windows"}
        )
        # Create Variant Attribute
        cls.att_license = pa_model.create(
            {"name": "License", "create_variant": "no_variant"}
        )
        cls.att_license_otp = pav_model.create(
            {"attribute_id": cls.att_license.id, "name": "One-time Payment"}
        )
        cls.att_license_subscription = pav_model.create(
            {"attribute_id": cls.att_license.id, "name": "Subscription"}
        )
        cls.att_license_freemium = pav_model.create(
            {"attribute_id": cls.att_license.id, "name": "Freemium"}
        )
        # Products
        cls.product_as400 = pt_model.create(
            {
                "name": "Amazing Software 400 - Diskette",
                "default_code": "AS400",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.att_platform.id,
                            "value_ids": [
                                (
                                    6,
                                    0,
                                    [
                                        cls.att_platform_linux.id,
                                        cls.att_platform_windows.id,
                                    ],
                                )
                            ],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.att_license.id,
                            "value_ids": [
                                (
                                    6,
                                    0,
                                    [
                                        cls.att_license_otp.id,
                                        cls.att_license_subscription.id,
                                    ],
                                )
                            ],
                        },
                    ),
                ],
            }
        )
        cls.product_as500 = pt_model.create(
            {
                "name": "Awful Software 500",
                "default_code": "AS500",
            }
        )
        # Product Stickers
        f_img = io.BytesIO()
        Image.new("RGB", (500, 500), "#FFFFFF").save(f_img, "PNG")
        f_img.seek(0)
        f_img_b64 = base64.b64encode(f_img.read())
        cls.ps_global = ps_model.create(
            {
                "name": "global_sticker",
                "image_1920": f_img_b64,
                "company_id": False,
                "image_size": "64",
            }
        )
        cls.ps_att_cc = ps_model.create(
            {
                "name": "attribute_platform_cross_company_sticker",
                "image_1920": f_img_b64,
                "company_id": False,
                "product_category_id": False,
                "product_attribute_id": cls.att_platform.id,
                "product_attribute_value_id": False,
                "show_sticker_note": False,
                "image_size": "64",
            }
        )
        cls.ps_attv_cc = ps_model.create(
            {
                "name": "attribute_license_freemium_value_cross_company_sticker",
                "image_1920": f_img_b64,
                "company_id": False,
                "product_category_id": False,
                "product_attribute_id": cls.att_license.id,
                "product_attribute_value_id": cls.att_license_freemium.id,
                "show_sticker_note": True,
                "image_size": "64",
            }
        )
