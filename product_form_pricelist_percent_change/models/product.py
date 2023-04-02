from lxml import etree

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    fixed_pricelist_item_ids = fields.One2many(copy=True)

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        """Check which mode render the item ids view:

        - editable tree-view for basic pricelist users that only
          will get access to fixed price feature

        -  for advanced pricelist user removing the 'editable'
        attribute will open the full form-view pricelist item"""

        res = super(ProductTemplate, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        pricelist_advanced = self.user_has_groups("product.group_sale_pricelist")
        if view_type != "form" or pricelist_advanced:
            return res

        # actually we add the editable, because this module removes it by default
        doc = etree.XML(
            res["fields"]["fixed_pricelist_item_ids"]["views"]["tree"]["arch"]
        )
        for node in doc.xpath("//tree"):
            node.set("editable", "bottom")
        res["fields"]["fixed_pricelist_item_ids"]["views"]["tree"][
            "arch"
        ] = etree.tostring(doc, encoding="unicode")
        return res
