# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from openerp import _, api, fields, models
from openerp.exceptions import ValidationError
from openerp.tools.float_utils import float_round


class ProductTemplate(models.Model):
    _inherit = "product.template"

    bundle_ok = fields.Boolean(
        string="Is bundle",
        help="Is a Product Bundle?"
    )
    bundle_lines_lst_price = fields.Monetary(
        string="Bundled products public price",
        compute="_compute_bundle_lines_lst_price",
        currency_field="currency_id",
        help="Sum of all bundled products' public price. This is a good hint "
             "to know what public price to set for this bundle.",
    )
    bundle_line_ids = fields.One2many(
        related="product_variant_ids.bundle_line_ids",
    )
    inverse_bundle_line_ids = fields.One2many(
        related="product_variant_ids.inverse_bundle_line_ids",
    )

    @api.one
    @api.depends("bundle_ok", "bundle_line_ids.total_lst_price")
    def _compute_bundle_lines_lst_price(self):
        self.bundle_lines_lst_price = sum(
            self.mapped("bundle_line_ids.total_lst_price"))

    @api.one
    @api.constrains("bundle_ok", "attribute_line_ids")
    def _check_no_variants_in_bundle(self):
        """Ensure bundles have no product variants."""
        if self.bundle_ok and self.attribute_line_ids:
            raise ValidationError(_("Bundles cannot have variants."))

    @api.one
    @api.constrains("bundle_ok", "type")
    def _check_consumable_bundles(self):
        """Ensure bundles are consumable."""
        if self.bundle_ok and self.type != "consu":
            raise ValidationError(
                _("Bundles are always consumable, no matter the type of their "
                  "included products."))

    @api.multi
    @api.onchange("bundle_ok")
    def _onchange_bundle_delete_variants(self):
        """Bundles have no variants and are consumable always."""
        if self.bundle_ok:
            self.type = "consu"
            self.attribute_line_ids = False

    @api.multi
    def write(self, vals):
        """Bundle lines get written in the variant."""
        lines = vals.pop("bundle_line_ids", None)
        if lines:
            self.mapped("product_variant_ids").write({
                "bundle_line_ids": lines,
            })
        return super(ProductTemplate, self).write(vals)


class ProductProduct(models.Model):
    _inherit = "product.product"

    bundle_line_ids = fields.One2many(
        comodel_name="product.bundle.line",
        inverse_name="bundle_id",
        string="Bundled products",
    )
    inverse_bundle_line_ids = fields.One2many(
        comodel_name="product.bundle.line",
        inverse_name="product_id",
        string="Included In Bundles",
        help="Bundles that include this product.",
    )

    # HACK https://github.com/odoo/odoo/issues/10799#issuecomment-241704243
    qty_available = fields.Float(compute="_compute_quantities")
    incoming_qty = fields.Float(compute="_compute_quantities")
    outgoing_qty = fields.Float(compute="_compute_quantities")
    virtual_available = fields.Float(compute="_compute_quantities")

    # HACK https://github.com/odoo/odoo/issues/10799#issuecomment-241704243
    # TODO Inspired from v10, refactor this when migrating
    @api.multi
    @api.depends("reception_count", "delivery_count")
    def _compute_quantities(self):
        res = self._product_available()
        for product in self:
            product.qty_available = res[product.id]["qty_available"]
            product.incoming_qty = res[product.id]["incoming_qty"]
            product.outgoing_qty = res[product.id]["outgoing_qty"]
            product.virtual_available = res[product.id]["virtual_available"]

    @api.multi
    def _product_available(self, field_names=None, arg=False):
        """Stock is calculated depending on included products'."""
        # Do nothing with non-bundles
        bundles = self.filtered("bundle_ok")
        result = super(ProductProduct, (self - bundles))._product_available(
            field_names, arg)

        # Bundles stock is their included products'
        for bundle in bundles:
            bundle_qtys = dict()
            for line in bundle.bundle_line_ids:
                # Only stockable products are taken into account
                if line.product_id.type != "product":
                    continue
                # Get availabilities for included product in this line
                subprod_qtys = line.product_id._product_available(
                    field_names, arg)[line.product_id.id]
                for key in subprod_qtys:
                    # Quantity depends on how many are bundled
                    subqty = float_round(
                        subprod_qtys[key] // line.qty,
                        precision_rounding=line.product_id.uom_id.rounding)
                    try:
                        # The lesser quantity is used
                        bundle_qtys[key] = min(bundle_qtys[key], subqty)
                    except KeyError:
                        bundle_qtys[key] = subqty
            bundle_qtys.setdefault("qty_available", 0)
            bundle_qtys.setdefault("virtual_available", 0)
            bundle_qtys.setdefault("incoming_qty", 0)
            bundle_qtys.setdefault("outgoing_qty", 0)
            result[bundle.id] = bundle_qtys
        return result

    @api.one
    @api.constrains("company_id", "bundle_line_ids")
    def _check_bundle_products_company(self):
        """Check that bundles are related to bundles of same company."""
        for line in self.bundle_line_ids:
            if line.product_id.company_id != self.company_id:
                raise ValidationError(_(
                    "Bundle company must be the same as the included "
                    "products'."))

    @api.one
    @api.constrains("company_id", "inverse_bundle_line_ids")
    def _check_inverse_bundle_products_company(self):
        """Check that bundles are related to bundles of same company."""
        for line in self.inverse_bundle_line_ids:
            if line.bundle_id.company_id != self.company_id:
                raise ValidationError(_(
                    "Bundle company must be the same as the included "
                    "products'."))
