# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>)
# Copyright (C) 2020 ForgeFlow S.L. (<http://www.forgeflow.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import logging
import time

import requests

from odoo import api, models

_logger = logging.getLogger(__name__)


class ProductCatalogReport(models.AbstractModel):
    _name = "report.product_catalog_report.report_product_catalog"
    _description = "Product Catalog Report"

    def _get_imagepath(self, product_id):
        datas = self.env["ir.attachment"].search_read(
            [("res_model", "=", "product.product"), ("res_id", "=", product_id)],
            limit=1,
        )
        if len(datas):
            # if there are several, pick first
            try:
                if datas[0]["link"]:
                    try:
                        img_data = base64.encodestring(
                            requests.get(datas[0]["link"]).content
                        )
                        return img_data
                    except Exception as innerEx:
                        _logger.exception(innerEx)
                elif datas[0]["datas"]:
                    return datas[0]["datas"]
            except Exception as e:
                _logger.exception(e)
        return None

    def setCat(self, cat_ids):
        categories = self.env["product.category"].browse(cat_ids)
        return (categories + categories.child_id).ids

    def _getCategories(self, cat_ids):
        cat_ids = self.setCat(cat_ids)
        tmpCat_ids = []
        for cat_id in cat_ids:
            prod_ids = self.env["product.template"].search([("categ_id", "=", cat_id)])
            if len(prod_ids):
                tmpCat_ids.append(cat_id)
        return self.env["product.category"].browse(tmpCat_ids).read()

    def _getProducts(self, category, lang):
        prod_tmpIDs = (
            self.env["product.template"].search([("categ_id", "=", category)]).ids
        )
        return (
            self.env["product.product"]
            .with_context(lang=lang)
            .search_read([("product_tmpl_id", "in", prod_tmpIDs)])
        )

    def _get_currency(self):
        return self.env.company.currency_id.name

    def _get_packaging_title(self, product_id, index):
        packs = self.env["product.packaging"].search_read(
            [("product_id", "=", product_id)], ["name"], limit=4
        )
        if len(packs) > index:
            s = str(packs[index]["name"])
            if len(s) > 9:
                p = str(s[0:9]) + "..."
                return p
            elif not s == "False":
                return s
        return " "

    def _get_packaging_value(self, product_id, index):
        packs = self.env["product.packaging"].search_read(
            [("product_id", "=", product_id)], ["qty"], limit=4
        )
        if len(packs) > index:
            return str(packs[index]["qty"])
        return False

    def _get_price(self, product_id, pricelist_id):
        pricelist = self.env["product.pricelist"].browse([pricelist_id])
        price = pricelist.with_context(uom=False).price_get(product_id, 1.0, None)[
            pricelist_id
        ]
        if not price:
            price = 0.0
        return price

    def _get_desc(self, template_id):
        if template_id:
            prodtmpl = self.env["product.template"].browse(template_id).read()[0]

            if prodtmpl["description_sale"]:
                return prodtmpl["description_sale"]
            else:
                return "no Description Specified"
        else:
            return "This is Test Description"

    @api.model
    def _get_report_values(self, docids, data=None):
        docids = docids or self._context.get("active_ids", [])
        return {
            "doc_ids": docids,
            "doc_model": "res.partner",
            "docs": self.env["res.partner"].browse(docids),
            "time": time,
            "image_url": self._get_imagepath,
            "currency_code": self._get_currency,
            "categories": self._getCategories,
            "products": self._getProducts,
            "description": self._get_desc,
            "packaging_title": self._get_packaging_title,
            "packaging_value": self._get_packaging_value,
            "Price": self._get_price,
            "data": data,
        }
