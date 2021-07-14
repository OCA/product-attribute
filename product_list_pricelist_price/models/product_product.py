# Copyright 2021 ForgeFlow, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import api, fields, models

from odoo.addons.base.models.ir_ui_view import (
    transfer_modifiers_to_node,
    transfer_node_to_modifiers,
)


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_product_pricelist_price(self):
        pricelists = self.env["product.pricelist"].search(
            [("display_pricelist_price", "=", True)]
        )
        result = pricelists.price_rule_get_multi(
            [(product, 1.0, False) for product in self]
        )
        for product in self:
            for pricelist in pricelists:
                field_name = "product_price_pricelist_%s" % (pricelist.id)
                product[field_name] = (
                    pricelist.currency_id.round(result[product.id][pricelist.id][0])
                    if result[product.id][pricelist.id]
                    and result[product.id][pricelist.id][0]
                    else 0.0
                )

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        result = super(ProductProduct, self).fields_view_get(
            view_id, view_type, toolbar=toolbar, submenu=submenu,
        )

        doc = etree.XML(result["arch"])
        name = result.get("name", False)
        if name == "product.product.pricelist.price":
            for placeholder in doc.xpath("//field[@name='type']"):
                for pricelist in self.env["product.pricelist"].search(
                    [("display_pricelist_price", "=", True)]
                ):
                    field_name = "product_price_pricelist_%s" % (pricelist.id)
                    tag_name = "Sales Price (%s)" % (pricelist.name)
                    elem = etree.Element(
                        "field",
                        {"name": field_name, "readonly": "True", "optional": "hide"},
                    )
                    modifiers = {}
                    transfer_node_to_modifiers(elem, modifiers)
                    transfer_modifiers_to_node(elem, modifiers)
                    placeholder.addnext(elem)
                    result["fields"].update(
                        {
                            field_name: {
                                "domain": [],
                                "context": {},
                                "string": tag_name,
                                "type": "float",
                            }
                        }
                    )

                result["arch"] = etree.tostring(doc)
        return result

    @api.model
    def _add_pricelist_price(self, field_name, tag_name):
        self._add_field(
            field_name,
            fields.Float(string=tag_name, compute="_compute_product_pricelist_price"),
        )
        return True

    def _register_hook(self):
        pricelists = self.env["product.pricelist"].search(
            [("display_pricelist_price", "=", True)]
        )
        for pricelist in pricelists:
            field_name = "product_price_pricelist_%s" % (pricelist.id)
            tag_name = "Sales Price (%s)" % (pricelist.name)
            if field_name in self._fields:
                continue
            self._add_pricelist_price(field_name, tag_name)
        self._setup_fields()
        self._setup_complete()
        return super(ProductProduct, self)._register_hook()
