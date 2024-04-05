# Copyright 2021 ForgeFlow, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import api, fields, models

from odoo.addons.base.models.ir_ui_view import (
    transfer_modifiers_to_node,
    transfer_node_to_modifiers,
)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _compute_product_template_pricelist_price(self):
        pricelists = self.env["product.pricelist"].search(
            [("display_pricelist_price", "=", True)]
        )

        result = pricelists._compute_price_rule_multi(
            self, 1.0, False
        )
        for product in self:
            for pricelist in pricelists:
                field_name = "product_tmpl_price_pricelist_%s" % (pricelist.id)
                product[field_name] = (
                    pricelist.currency_id.round(result[product.id][pricelist.id][0])
                    if result[product.id][pricelist.id]
                    and result[product.id][pricelist.id][0]
                    else 0.0
                )

    @api.model
    def get_view(
        self, view_id=None, view_type="form", **options
    ):
        result = super(ProductTemplate, self).get_view(
            view_id,
            view_type,
            **options,
        )

        doc = etree.XML(result["arch"])
        for placeholder in doc.xpath("//field[@name='type']"):
            for pricelist in self.env["product.pricelist"].search(
                [("display_pricelist_price", "=", True)]
            ):
                field_name = "product_tmpl_price_pricelist_%s" % (pricelist.id)
                elem = etree.Element(
                    "field",
                    {"name": field_name, "readonly": "True", "optional": "hide"},
                )
                modifiers = {}
                transfer_node_to_modifiers(elem, modifiers)
                transfer_modifiers_to_node(elem, modifiers)
                placeholder.addnext(elem)

            result["arch"] = etree.tostring(doc)
        return result

    @api.model
    def _add_pricelist_price(self, field_name, tag_name):
        self._add_field(
            field_name,
            fields.Float(
                string=tag_name, compute="_compute_product_template_pricelist_price"
            ),
        )
        return True

    def _register_hook(self):
        pricelists = self.env["product.pricelist"].search(
            [("display_pricelist_price", "=", True)]
        )
        for pricelist in pricelists:
            field_name = "product_tmpl_price_pricelist_%s" % (pricelist.id)
            tag_name = "Sales Price (%s)" % (pricelist.name)
            if field_name in self._fields:
                continue
            self._add_pricelist_price(field_name, tag_name)
        self._setup_fields()
        self._setup_complete()
        return super(ProductTemplate, self)._register_hook()
