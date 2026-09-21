from odoo import api, models
from odoo.tools import config


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _update_product_price_from_pricelist(self, pricelist_items=None):
        self.ensure_one()
        all_templates = self.env["product.template"]
        if not pricelist_items:
            pricelist_items = self.item_ids
        for item in pricelist_items:
            all_templates |= item._get_all_templates_from_pricelist_item()
        if all_templates:
            pricelist_data = self._compute_price_rule(all_templates, 1)
            for template in all_templates:
                new_price, suitable_rule = pricelist_data[template.id]
                if suitable_rule and new_price != template.list_price:
                    template.write({"list_price": new_price})
        return True

    def _get_domain_applicability_for_company(self):
        """Return the domain to check if the pricelist is applicable for the company."""
        self.ensure_one()
        main_company = self._get_main_company_to_compute_prices()
        domain = [
            ("base_pricelist_compute_price_id", "=", self.id),
            ("id", "=", main_company.id),
        ]
        return domain

    def _get_main_company_to_compute_prices(self):
        """:return: Recordset of res.company"""
        main_company_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("main_company_compute_price_id", "")
        )
        if main_company_id:
            return self.env["res.company"].browse(int(main_company_id))
        return self.company_id or self.env.company


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    @api.model_create_multi
    def create(self, vals_list):
        new_pricelist_items = super().create(vals_list)
        test_condition = not config["test_enable"] or (
            config["test_enable"]
            and self.env.context.get("test_compute_list_price_from_pricelist")
        )
        # recompute the product's sales price.
        if test_condition:
            for pricelist in new_pricelist_items.pricelist_id:
                pricelist._update_product_price_from_pricelist(new_pricelist_items)
        return new_pricelist_items

    def write(self, vals):
        res = super().write(vals)
        test_condition = not config["test_enable"] or (
            config["test_enable"]
            and self.env.context.get("test_compute_list_price_from_pricelist")
        )
        # If any field from the expected ones is changed,
        # recompute the product's sales price.
        if test_condition and set(vals.keys()).intersection(
            self._get_fields_to_recompute_product_list_price()
        ):
            for pricelist in self.pricelist_id:
                pricelist._update_product_price_from_pricelist(self)
        return res

    @api.model
    def _get_fields_to_recompute_product_list_price(self):
        """Return the list of fields that will trigger the
        recomputation of the products list price.
        :return: list(str)
        """
        fields_triggers = [
            "applied_on",
            "base",
            "base_pricelist_id",
            "categ_id",
            "compute_price",
            "date_start",
            "date_end",
            "fixed_price",
            "percent_price",
            "price_discount",
            "price_surcharge",
            "price_round",
            "product_tmpl_id",
            "product_id",
        ]
        return fields_triggers

    def _get_all_templates_from_pricelist_item(self):
        """Returns the products template
        affected by the pricelist item that require recomputation.
        :return: Recordset of product.template"""
        self.ensure_one()
        templates = self.env["product.template"]
        company = self.pricelist_id._get_main_company_to_compute_prices()
        is_pricelist_available = bool(
            self.env["res.company"].search_count(
                self.pricelist_id._get_domain_applicability_for_company()
            )
        )
        if not is_pricelist_available or (
            self.pricelist_id.company_id
            and self.pricelist_id.company_id.id != company.id
        ):
            return self.env["product.template"]  # empty recordset
        domain_company = [("company_id", "in", [False, company.id])]
        if self.applied_on == "3_global":
            templates = self.env["product.template"].search(domain_company)
        elif self.applied_on == "2_product_category" and self.categ_id:
            templates = self.env["product.template"].search(
                [("categ_id", "=", self.categ_id.id)] + domain_company
            )
        elif (
            self.applied_on == "1_product"
            and self.product_tmpl_id
            and (
                not self.product_tmpl_id.company_id
                or self.product_tmpl_id.company_id.id == company.id
            )
        ):
            templates = self.product_tmpl_id
        elif (
            self.applied_on == "0_product_variant"
            and self.product_id
            and (
                not self.product_id.company_id
                or self.product_id.company_id.id == company.id
            )
        ):
            templates = self.product_id.product_tmpl_id
        return templates
