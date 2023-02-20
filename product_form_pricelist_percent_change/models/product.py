from lxml import etree

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    fixed_pricelist_item_ids = fields.One2many(copy=True)

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        """Adjust editable attribute depending on current pricelist setting:

        In product views:

        - Always set editable=bottom for basic pricelist

        - Always remove editable attribute for advanced pricelists, this will
        lead to the pricelist item form-view when clicking on One2many field
        `fixed_pricelist_item_ids`

        Todo: should remove 'editable' attr in xml after last refactor?
        """

        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )

        if view_type != "form":
            return res

        doc = etree.XML(
            res["fields"]["fixed_pricelist_item_ids"]["views"]["tree"]["arch"]
        )

        pricelist_advanced = self.user_has_groups("product.group_sale_pricelist")

        if pricelist_advanced:
            for node in doc.xpath("//tree"):
                node.attrib.pop("editable", None)
        else:
            for node in doc.xpath("//tree"):
                node.attrib["editable"] = "bottom"
        res["fields"]["fixed_pricelist_item_ids"]["views"]["tree"][
            "arch"
        ] = etree.tostring(doc, encoding="unicode")
        return res


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        # This has to be replicated otherwise logic will not be applied
        # to product.product views. This is a verbatim copy of template
        # implementation, but we don't delegate to product template class
        # in order to manage view processing individually for both models.

        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )

        if view_type != "form":
            return res

        doc = etree.XML(
            res["fields"]["fixed_pricelist_item_ids"]["views"]["tree"]["arch"]
        )

        pricelist_advanced = self.user_has_groups("product.group_sale_pricelist")

        if pricelist_advanced:
            for node in doc.xpath("//tree"):
                node.attrib.pop("editable", None)
        else:
            for node in doc.xpath("//tree"):
                node.attrib["editable"] = "bottom"
        res["fields"]["fixed_pricelist_item_ids"]["views"]["tree"][
            "arch"
        ] = etree.tostring(doc, encoding="unicode")
        return res
