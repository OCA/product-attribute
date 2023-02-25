import logging
import traceback

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_is_zero

_logger = logging.getLogger(__name__)


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    # Technical fields (non-stored):

    # Warning management for recursion and variants:
    # prefer class alert/warning/info divs at form-view level
    # over odoo.Exceptions because it's safer with @api.depends

    base_pricelist_id_recursion_prefetch = fields.Boolean(
        compute="_compute_base_pricelist_id_recursion_prefetch",
    )

    recursion_rule_warning = fields.Html(
        compute="_compute_base_pricelist_id_recursion_prefetch",
    )

    recursion_error_warning = fields.Html(
        compute="_compute_product_pricelist_selling_price",
    )

    product_has_variants = fields.Boolean(
        compute="_compute_product_pricelist_selling_price",
    )

    # UI Fields:

    product_pricelist_selling_price = fields.Float(
        string="Selling Price",
        compute="_compute_product_pricelist_selling_price",
    )

    selling_price_set_inverse = fields.Float(string="Set Discount %")

    @api.depends("pricelist_id", "base_pricelist_id")
    def _compute_base_pricelist_id_recursion_prefetch(self):
        """
        Some check for recursion between rules depending on pricelists.
        It would be a problem for this module because computed fields
        are not stored by default, so python recursion error is going
        to deny record access, and it has to be avoided. We prefer to
        show a warning at form level over odoo.Exceptions because it's
        safer to deal with @api.depends.

        If recursion is found:
        - we set 'base_pricelist_id_recursion_prefetch' to True, this
          will avoid _compute_price_rule() being recursively called

        - warning message will appear on both recursive rules form-views
          to notify that feature introduced by this module are disabled
          for those 'product pricelist rules' until recursion is removed

        - an html field is computed to show info about recursive records

        - dictionary {'rule_id': {rule info...}} will be shown in log
        """

        recursive_rule_data = {}

        for rule in self:

            rule.recursion_rule_warning = False
            rule.base_pricelist_id_recursion_prefetch = False

            if (
                rule.pricelist_id
                and rule.base_pricelist_id
                and rule.base == "pricelist"
            ):

                if rule.base_pricelist_id.id == rule.pricelist_id.id:
                    # skip if pricelist_id/base_pricelist_id is redundant, will be
                    # managed later by original @api.constrains _check_recursion()
                    rule.base_pricelist_id_recursion_prefetch = True
                    continue

                target_pricelist_id = rule.base_pricelist_id
                if not target_pricelist_id:
                    target_pricelist_id = rule.base_pricelist_id._origin

                # Prefetch product_id: we need to discard rule if not applied on same product
                active_rule_product_id = None
                if rule.applied_on == "1_product":
                    active_rule_product_id = rule.product_tmpl_id._origin.id
                elif rule.applied_on == "0_product_variant":
                    active_rule_product_id = rule.product_id._origin.id

                if not active_rule_product_id:
                    continue

                for item in target_pricelist_id.item_ids:
                    item_product_id = False
                    if item.applied_on == "1_product":
                        item_product_id = item.product_tmpl_id.id
                    elif item.applied_on == "0_product_variant":
                        item_product_id = item.product_id.id

                    if item_product_id != active_rule_product_id:
                        # avoid crossed warning between products with similar recursive rules
                        continue

                    if item.base_pricelist_id.id == rule.pricelist_id.id:

                        rule.base_pricelist_id_recursion_prefetch = True

                        recursive_rule_data[str(rule.id)] = {
                            "pricelist_id": rule.pricelist_id.name,
                            "base_pricelist_id": rule.base_pricelist_id.name,
                            "applied_on": rule.applied_on,
                            "product_id": active_rule_product_id,
                        }  # product recursive rules for syslog

                        pricelist_name = rule.base_pricelist_id.name
                        rule_name = item.name
                        rule_id = str(item.id)
                        item_product_id = str(item_product_id)

                        # UI info:
                        # Note: this does not work super well with pseudo-records: if both rules
                        # are pseudo-records 'item.base_pricelist_id' will not be reachable yet,
                        # so in that case warnings will show up after save of product record...
                        rule.recursion_rule_warning = (
                            "<br/><b>pricelist name:</b> "
                            + pricelist_name
                            + "<br/><b>rule name</b>: "
                            + rule_name
                            + "<br/><b>rule ID</b>: "
                            + rule_id
                            + "<br/><b>product ID</b>: "
                            + item_product_id
                        )

        if recursive_rule_data:
            _logger.info(
                "Found recursion on product pricelist items: %s" % recursive_rule_data
            )

    @api.depends(
        "pricelist_id",
        "product_tmpl_id",
        "product_id",
        "currency_id",
        "min_quantity",
        "compute_price",
        "fixed_price",
        "percent_price",
        "base",
        "price_discount",
        "price_surcharge",
        "price_round",
        "price_min_margin",
        "price_max_margin",
        "base_pricelist_id_recursion_prefetch",
        "recursion_rule_warning",
    )
    def _compute_product_pricelist_selling_price(self):

        """Show selling price on pricelist item. UI responsive."""

        for rule in self:

            rule.product_pricelist_selling_price = 0.00
            rule.product_has_variants = False
            rule.recursion_error_warning = False
            pricelist = rule.pricelist_id

            if (
                rule.applied_on not in ["1_product", "0_product_variant"]
                or not pricelist
            ):
                return

            product = None

            if rule.applied_on == "0_product_variant":
                product = rule.product_id
            elif rule.applied_on == "1_product":
                product = rule.product_tmpl_id
                if len(product.product_variant_ids) > 1:
                    rule.product_has_variants = True

            if not product:
                return

            product_price = 0.00

            if rule.base == "supplierinfo":
                # base for compatibility with 'product_pricelist_supplierinfo',
                # not actually implemented at the moment
                product_price = product._get_supplierinfo_pricelist_price(
                    rule, date=False, quantity=rule.min_quantity, product_id=product.id
                )
            elif rule.base in ["list_price", "standard_price"]:
                product_price = product.price_compute(rule.base)[product.id]
            elif rule.base == "pricelist":
                if not rule.base_pricelist_id:
                    # when 'based on other pricelist' is selected there is no
                    # there is no default 'base_pricelist_id' selected.
                    # return here avoid passing empty recordset (singleton error)
                    return

                product = product._origin  # avoid issues with newid

                if not rule.base_pricelist_id_recursion_prefetch:
                    try:
                        partner = date = uom_id = False
                        product_price = rule.base_pricelist_id._compute_price_rule(
                            products_qty_partner=[
                                (product, rule.min_quantity, partner)
                            ],
                            date=date,
                            uom_id=uom_id,
                        )[product.id][0]
                    except RecursionError:
                        # Important note: calling _compute_price_rule() can cause
                        # recursion error in several situations, some of them are
                        # prevented by _compute_base_pricelist_id_recursion_prefetch
                        # so we have not to wait for recursion error to show.
                        #
                        # There are other situation that are hard to catch or too
                        # expensive to check for performance, for example when a
                        # rule A depends on B, B has a rule that depends on C and
                        # C has a rule that depends on A. To avoid server error to
                        # show up in those situation we catch and manage exception.
                        # Still super-bad to wait for recursion error but at least
                        # user has record access and remove/correct recursive rules.
                        # (test with stored fields)
                        recursion_error_warning = (
                            "Catched Recursion Error on %s. It is based on %s "
                            "which has recursive pricelist rule. This can cause "
                            "performance issues. Module features will not be "
                            "available for this rule."
                            % (rule.pricelist_id.name, rule.base_pricelist_id.name)
                        )

                        # form-view warning + sys log if user reaches this point
                        rule.recursion_error_warning = recursion_error_warning
                        _logger.warning(recursion_error_warning)

            if product_price:
                # Setting computed field with get_product_price() would be possible, but
                # it would be much worse for responsiveness of the UI since it would not
                # recompute every time a dependency changes, but only on record Save.

                selling_price_rule = rule._compute_price(
                    price=product_price,
                    price_uom=False,
                    product=product,
                    quantity=rule.min_quantity,
                    partner=False,
                )

                rule.product_pricelist_selling_price = selling_price_rule

    def _get_percentage_change(self):

        """

        Getter method to compute the percent change between the computed
        selling price and user input.

        :returns dictionary 'discount' with two keys:

        - discount_field_name: the field on which percent change applies
        (can be 'price_discount' or 'percent_price')

        - discount: percentage change computed by formula:

         `(input value - selling price computed) / selling price computed x 100`

         where `input value` is selling_price_set_inverse field and `computed
         selling price` is product_pricelist_selling_price field

        """

        applied_on = self.applied_on

        product = None
        if applied_on == "1_product":
            product = self.product_tmpl_id
        elif applied_on == "0_product_variant":
            product = self.product_id

        self._get_percentage_change_consistency_check(product=product)

        discount = {}

        try:
            if self.compute_price == "percentage":  # % on sale price

                discount["discount_field_name"] = "percent_price"
                product_price = product.list_price
                discount["discount"] = (
                    (product_price - self.selling_price_set_inverse) / product_price
                ) * 100

            elif self.compute_price == "formula":

                discount["discount_field_name"] = "price_discount"

                if self.base == "list_price":  # % based on sale price

                    product_price = product.list_price
                    discount["discount"] = (
                        (product_price - self.selling_price_set_inverse) / product_price
                    ) * 100

                elif self.base == "standard_price":  # based on cost

                    product_price = product.standard_price
                    discount["discount"] = (
                        (product_price - self.selling_price_set_inverse) / product_price
                    ) * 100

                elif (
                    self.base == "pricelist"
                ):  # based on cost retrieved from other pricelist rule

                    if not self.base_pricelist_id:
                        raise UserError(
                            _("Select which pricelist this rule is based on.")
                        )

                    partner = date = uom_id = False

                    # prevent exception in some case to speed-up warning pop-up
                    self._onclick_check_pricelist_recursive()

                    try:
                        product_price = self.base_pricelist_id._compute_price_rule(
                            products_qty_partner=[
                                (product, self.min_quantity, partner)
                            ],
                            date=date,
                            uom_id=uom_id,
                        )[product.id][0]
                    except RecursionError:  # catch exc when it can't be prevented
                        warning = _(
                            "Recursion Error: selected pricelist has some recursive rules "
                            "with other pricelists. It will not possible to retrieve product "
                            "price and discount until recursion is removed. You can check "
                            "'%s' form-view to see info about recursive rules and solve issue. "
                            % self.base_pricelist_id.name
                        )
                        raise UserError(warning)

                    discount["discount"] = (
                        (product_price - self.selling_price_set_inverse) / product_price
                    ) * 100

        except ZeroDivisionError:

            based_on = "Product cost"
            if self.base == "list_price":
                based_on = "Product price"
            elif self.base == "pricelist":
                based_on = "Product price retrieved from selected pricelist"

            raise UserError(
                _(
                    "%s is equal to 0.00.\n"
                    "Cannot divide by zero, please correct parameters and try again.\n\n%s"
                    "Hint: if provided values are correct try to save unsaved records and "
                    "try again." % (based_on, traceback.format_exc())
                )
            )

        return discount if discount.get("discount") else {}

    def set_percentage_change(self):

        discount_dict = self._get_percentage_change()
        discount_field_name = discount_dict.get("discount_field_name")
        discount = discount_dict.get("discount")

        if discount_field_name and discount:
            self[discount_field_name] = discount

    def _onclick_check_pricelist_recursive(self):

        """Similar to @api.depends check but for button:

        Checks for recursive pricelist rules and tries to
        prevent RecursionError exception. This allows to
        speed up the odoo.Exception pop-up in some case.

        :returns: UserError if 'base_pricelist_id' has a rule
        based on 'self'

        See _compute_base_pricelist_id_recursion_prefetch()
        for more information.
        """

        if self.pricelist_id and self.base_pricelist_id and self.base == "pricelist":

            # discard from 'base_pricelist_id' rules recordset all rules that are
            # not related to the product linked on the active pricelist rule

            recursive_items = []
            active_rule_product_id = False

            if self.applied_on == "1_product":
                active_rule_product_id = self.product_tmpl_id.id
            elif self.applied_on == "0_product_variant":
                active_rule_product_id = self.product_id.id

            for item in self.base_pricelist_id.item_ids:
                item_product_id = False

                if item.applied_on == "1_product":
                    item_product_id = item.product_tmpl_id.id
                elif item.applied_on == "0_product_variant":
                    item_product_id = item.product_id.id

                if (
                    item_product_id == active_rule_product_id
                    and item.base_pricelist_id.id == self.pricelist_id.id
                ):
                    # recursive + same product id on both rules
                    recursive_items.append(item)
                else:
                    continue

            warning = _(
                "Recursive rule: selected pricelist %s has some rules that depends "
                "on this pricelist for same product and quantity, therefore is not "
                "possible to evaluate product price and discount until recursion "
                "will be removed. Recursive rules:\n" % self.base_pricelist_id.name
            )

            rules = ""
            if recursive_items:
                for rule in recursive_items:
                    rules += _(
                        "\n-Pricelist name: %s, rule name: %s, rule ID: %s"
                        % (rule.pricelist_id.name, rule.name, rule.id)
                    )

                raise UserError(warning + rules)

    def _get_percentage_change_consistency_check(self, product=None):

        """Check all is ready before computation. This method is
        mostly here for views that are possibly introduced by 3rd
        party modules. Standard views and views introduced by this
        module should avoid the access this computation by setting
        invisible/required properly at 'view level' with 'attrs'.

        Can be extended to add other checks.

        :param product: product record which rule applies on. Could
        be a template or variant

        :return: UserError if some field that is required for the
        computation has no value or its value is not allowed"""

        if self.applied_on not in ["1_product", "0_product_variant"]:
            raise UserError(
                _(
                    "This feature is only available for rules "
                    "applied on product template or variants."
                )
            )

        if not product:
            # already checked by '_check_product_consistency', remove?
            raise UserError(
                _(
                    "This feature is only available for products "
                    "and product variants. Please, select a product."
                )
            )

        if self.compute_price not in ["percentage", "formula"]:
            raise UserError(
                _(
                    "This feature is only available for rules with price "
                    "computation based on percentage or formula."
                )
            )

        # better hints for ZeroDivisionError
        if self.base == "list_price" and float_is_zero(
            value=product.list_price, precision_digits=4
        ):
            raise UserError(
                _(
                    "This pricelist-rule is based on 'Sales Price' which is set to 0.00.\n"
                    "Cannot set % discount on this rule (cannot divide by zero), "
                    "Please update product 'Sales Price' or pricelist rule parameters.\n\n"
                    "Hint: if you already provided correct value for 'Sales Price', "
                    "save record and try again."
                )
            )

        elif self.base == "standard_price" and float_is_zero(
            value=product.standard_price, precision_digits=4
        ):
            raise UserError(
                _(
                    "This pricelist-rule is based on 'Cost' which is set to 0.00.\n"
                    "Cannot set % discount on this rule (cannot divide by zero), "
                    "please update product 'cost' value or rule parameters.\n\n"
                    "Hint: if you already provided correct value for 'cost', "
                    "save record and try again."
                )
            )

    @api.model
    def default_get(self, default_fields):

        """Manage default fields if pricelist item form is opened by
        product view. Provides a basic management for variants."""

        default_fields.append("product_tmpl_id")

        values = super(ProductPricelistItem, self).default_get(default_fields)

        variant_easy_edit_view = self.env.context.get("variant_easy_edit_view")
        open_pricelist_item_by_product = self.env.context.get(
            "open_pricelist_item_by_product"
        )

        if open_pricelist_item_by_product and not variant_easy_edit_view:
            pid = self.env.context.get("pid")

            model_name = self.env.context.get("model_name")

            if model_name == "product_product":
                values["applied_on"] = "0_product_variant"
                values["product_id"] = pid
                values["pricelist_id"] = False

            elif not model_name or model_name == "product_template":
                values["applied_on"] = "1_product"
                values["product_tmpl_id"] = pid
                values["pricelist_id"] = False

        elif open_pricelist_item_by_product and variant_easy_edit_view:
            # see fields_view_get() for product_id management on this view
            values["applied_on"] = "0_product_variant"
            values["pricelist_id"] = False
        return values

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):

        """Better control for view-rendering.
        For more info on views read xml files."""

        if view_type == "form":

            open_pricelist_item_by_product = self.env.context.get(
                "open_pricelist_item_by_product"
            )

            module_prefix = "product_form_pricelist_percent_change."
            # flake8: names too long
            if open_pricelist_item_by_product:

                if self.env.context.get("variant_easy_edit_view"):

                    view_name = "product_pricelist_item_form_view_variant_smart_btn"
                    view_ref = module_prefix + view_name
                    view_id = self.env.ref(view_ref).id

                else:

                    view_name = "product_pricelist_item_form_view_by_product"
                    view_ref = module_prefix + view_name
                    view_id = self.env.ref(view_ref).id

            else:
                view_id = self.env.ref("product.product_pricelist_item_form_view").id

        res = super(ProductPricelistItem, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )

        doc = etree.XML(res["arch"])

        if self.env.context.get("variant_easy_edit_view"):
            # If variant view is opened by smart button the active_id
            # is not updating from product template to active variant.
            # This is a problem in this very specific case because when
            # default_get() is executed for pricelist item in product
            # it has no way to reach product, so we can't set default.
            # Best I can do for now is to restrict domain on active_id
            product_tmpl_id = self.env.context.get("pid")
            product_template = self.env["product.template"].browse(product_tmpl_id)
            variants_ids = product_template.mapped("product_variant_ids").ids

            if view_type == "form" and len(variants_ids) > 1:
                domain = "[('id', 'in', %s)]" % variants_ids
                for node in doc.xpath("//field[@name='product_id']"):
                    node.set("domain", domain)

        res["arch"] = etree.tostring(doc, encoding="unicode")
        return res

    def write(self, vals):

        """@override: once a 'base_pricelist_id' is set on a rule
        it is not possible to actually remove the relation from UI:
        if user select different value for 'Based On' field the m2o
        relation will stay set on record. It happend because the
        field is readonly on condition, so it will be protected on
        write. This can cause issues for recursive rules because if
        user adjust rule by changing 'Based On' value the relation
        m2o will stay set and in some case the rule can be considered
        recursive even if it's not actually based on another pricelist.
        This code is here to force-clear the 'base_pricelist_id' value
        if rule is not (anymore) based on another pricelist."""

        for rule in self:
            if ("base" in vals and vals["base"] != "pricelist") or (
                "base" not in vals and rule.base != "pricelist"
            ):
                vals["base_pricelist_id"] = False
        return super().write(vals)
