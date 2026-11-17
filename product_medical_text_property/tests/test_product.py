# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from markupsafe import Markup

from odoo.addons.base.tests.common import BaseCommon


class TestProduct(BaseCommon):
    def test_product(self):
        self.product = self.env["product.product"].create(
            {
                "name": "Medic 1",
                "medical_usage": "Usage",
                "medical_composition": "Composition",
                "medical_contra_indication": "Contra Indication",
                "medical_full_description": "Full Description",
                "medical_indication": "Indication",
                "medical_legal_text": "Legal Text",
                "medical_nutritional_value": "Nutritional Value",
                "medical_properties": "Properties",
            }
        )

        self.assertRecordValues(
            self.product.product_tmpl_id,
            [
                {
                    "medical_usage": Markup("<p>Usage</p>"),
                    "medical_composition": Markup("<p>Composition</p>"),
                    "medical_contra_indication": Markup("<p>Contra Indication</p>"),
                    "medical_full_description": Markup("<p>Full Description</p>"),
                    "medical_indication": Markup("<p>Indication</p>"),
                    "medical_legal_text": Markup("<p>Legal Text</p>"),
                    "medical_nutritional_value": Markup("<p>Nutritional Value</p>"),
                    "medical_properties": Markup("<p>Properties</p>"),
                }
            ],
        )

        self.product.product_tmpl_id.update(
            {
                "medical_usage": "Usage 1",
                "medical_composition": "Composition 1",
                "medical_contra_indication": "Contra Indication 1",
                "medical_full_description": "Full Description 1",
                "medical_indication": "Indication 1",
                "medical_legal_text": "Legal Text 1",
                "medical_nutritional_value": "Nutritional Value 1",
                "medical_properties": "Properties 1",
            }
        )

        self.assertRecordValues(
            self.product,
            [
                {
                    "medical_usage": Markup("<p>Usage 1</p>"),
                    "medical_composition": Markup("<p>Composition 1</p>"),
                    "medical_contra_indication": Markup("<p>Contra Indication 1</p>"),
                    "medical_full_description": Markup("<p>Full Description 1</p>"),
                    "medical_indication": Markup("<p>Indication 1</p>"),
                    "medical_legal_text": Markup("<p>Legal Text 1</p>"),
                    "medical_nutritional_value": Markup("<p>Nutritional Value 1</p>"),
                    "medical_properties": Markup("<p>Properties 1</p>"),
                }
            ],
        )
