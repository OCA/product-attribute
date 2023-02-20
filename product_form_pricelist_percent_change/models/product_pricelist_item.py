import logging
import traceback

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_is_zero

_logger = logging.getLogger(__name__)


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    # UI Fields:

    product_pricelist_selling_price = fields.Float(
        string="Selling Price", compute="_compute_product_pricelist_selling_price"
    )

    percent_change_user_input = fields.Float(string="Set Discount %")

    # Technical fields:

    # Warning management for recursion or variants info:
    # prefer class alert/warning/info divs at form-view level
    # over odoo.Exceptions because it's safer with @api.depends

    recursion_error_warning = fields.Html(
        compute="_compute_product_pricelist_selling_price"
    )

    product_has_variants = fields.Boolean(
        compute="_compute_product_pricelist_selling_price"
    )

    base_pricelist_id_recursion_prefetch = fields.Boolean(
        compute="_compute_base_pricelist_id_recursion_prefetch",
    )

    recursion_rule_warning = fields.Html(
        compute="_compute_base_pricelist_id_recursion_prefetch",
    )

    show_percent_change_button = fields.Boolean(
        default=False,
        help="Technical field to compute button visibility. Rule buttons "
        "must become visible/clickable after rule creation.",
    )

    def _get_product_price_rule_base(self, product):
        """
        Inheritable method to compute and return selling
        price, depending on 'based on' parameter.
        Depending on 'base' we might want to use another
        method, change context, use different args...

        :param product: product linked to pricelist-rule
        :returns:
        - product price (computed by rule parameters)
        - False if it's not possible to compute price rule
        for selected product
        """
        self.ensure_one()

        product_price = 0.0

        qty_uom_id = product.uom_id
        currency_id = self.currency_id or self.pricelist_id.currency_id
        company_id = self.env.company

        if self.compute_price in ["fixed", "percentage"]:

            product_price = product.price_compute(
                "list_price", uom=qty_uom_id, currency=currency_id, company=company_id
            )[product.id]

        elif self.compute_price == "formula":

            if self.base in ["list_price", "standard_price"]:
                product_price = product.price_compute(
                    self.base, uom=qty_uom_id, currency=currency_id, company=company_id
                )[product.id]

            elif self.base == "pricelist":

                if not self.base_pricelist_id:
                    # when 'based on other pricelist' is selected there is no
                    # there is no default 'base_pricelist_id' selected.
                    # return here avoid passing empty recordset (singleton error)
                    return

                product = product._origin  # avoid issues with newid

                if not self.base_pricelist_id_recursion_prefetch:
                    try:
                        partner = date = uom_id = False
                        product_price = self.base_pricelist_id._compute_price_rule(
                            products_qty_partner=[
                                (product, self.min_quantity, partner)
                            ],
                            date=date,
                            uom_id=uom_id,
                        )[product.id][0]

                        # Support for multi-currency: we can't call price_compute()
                        # in this flow so if pricelist or product has different
                        # currency than company, we must deal with it

                        current_currency = (
                            self.currency_id or self.pricelist_id.currency_id
                        )

                        if current_currency != product.currency_id:
                            current_currency = product.currency_id

                        converted_price = self.base_pricelist_id.currency_id._convert(
                            from_amount=product_price,
                            to_currency=current_currency,
                            company=company_id,
                            date=fields.Date.today(),
                        )

                        product_price = converted_price

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
                            % (self.pricelist_id.name, self.base_pricelist_id.name)
                        )

                        # form-view warning + sys log if user reaches this point
                        self.recursion_error_warning = recursion_error_warning
                        _logger.warning(recursion_error_warning)

        return product_price

    def _set_product_pricelist_selling_price(self, product_price, product):

        """Setter hook to help with UI responsiveness:
        _compute_price_rule() and get_product_price() are executed on
        'product.pricelist', if we don't recall _compute_price(), the
        UI will not update until we save (product) record.

        TODO/fixme: if you create two rules on product that belongs to
         different pricelists, and second rule is based on pricelist_id
         of the first rule, the selling price on second rule will not
         update until first rule is saved"""

        selling_price_rule = self._compute_price(
            price=product_price,
            price_uom=False,
            product=product,
            quantity=self.min_quantity,
            partner=False,
        )

        self.product_pricelist_selling_price = selling_price_rule

    # base_pricelist_id.item_ids dependencies are added to make
    # possible the recomputation of rule based on pricelist, when
    # computed fields are stored. Note that if pricelist C >
    # depending on B > depending on A > the C pricelist selling
    # price will not be automatically recomputed with store=True.
    # Can be probably fixed with cache invalidate or method
    # add_to_recompute() and some checks, but if that's your
    # need at that point you probably just want to use store=False
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
        "base_pricelist_id",
        "base_pricelist_id.item_ids.product_tmpl_id",
        "base_pricelist_id.item_ids.product_id",
        "base_pricelist_id.item_ids.currency_id",
        "base_pricelist_id.item_ids.min_quantity",
        "base_pricelist_id.item_ids.compute_price",
        "base_pricelist_id.item_ids.fixed_price",
        "base_pricelist_id.item_ids.percent_price",
        "base_pricelist_id.item_ids.base",
        "base_pricelist_id.item_ids.price_discount",
        "base_pricelist_id.item_ids.price_surcharge",
        "base_pricelist_id.item_ids.price_round",
        "base_pricelist_id.item_ids.price_min_margin",
        "base_pricelist_id.item_ids.price_max_margin",
        "base_pricelist_id.item_ids.base_pricelist_id_recursion_prefetch",
        "base_pricelist_id.item_ids.recursion_rule_warning",
    )
    def _compute_product_pricelist_selling_price(self):

        """Compute selling price to display on pricelist item"""

        for rule in self:

            # as first operaton, assign possible non-stored
            # field 'dummy' values to avoid ValueError
            rule.product_pricelist_selling_price = 0.00
            rule.product_has_variants = False
            rule.recursion_error_warning = False
            pricelist = rule.pricelist_id

            allowed_base_rule = self._get_allowed_base_rule()

            if rule.base not in allowed_base_rule:
                # main reason of this check is to avoid key errors when we
                # call price_compute() function to retrieve product prices.
                # Modules can inherit and add proper key to this check.
                return

            # Only compute price for specific products selected on the rule
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

            product_price = rule._get_product_price_rule_base(product=product)

            if product_price:
                rule._set_product_pricelist_selling_price(
                    product_price=product_price, product=product
                )  # for UI responsiveness

    def _get_percent_change_rule_base(self, product):

        """Inheritable method: compute discount depending on 'base' field

         :returns dictionary 'discount' with two keys:

        * 'discount_field_name': the field on which percent change applies
        (can be 'price_discount' or 'percent_price')

        * 'discount': percentage change computed by formula:

         ``(input - computed selling price) / computed selling price x 100``

         where:
         *`input` is provided user input (percent_change_user_input field),
           representing the desired selling price

         *`computed selling price`, which is 'product_pricelist_selling_price'
         field, represents the initial selling price, recomputed on btn click
         using provided rule/product parameters

         ToDo: add better support for product variants
        """

        discount = {}
        product_price = 0.00

        qty_uom_id = product.uom_id
        currency_id = self.currency_id or self.pricelist_id.currency_id
        company_id = self.env.company

        # raising UserError probably better than put feature invisible
        # on 'attrs' and reset values when rule changes...
        if self.compute_price == "fixed":
            raise UserError(
                _(
                    "This feature cannot be used on fixed price pricelist-rule.\n"
                    "You can use pricelist percentage change feature only on "
                    "rule based on fixed percentage or formula."
                )
            )

        if self.compute_price == "percentage":  # % on sale price
            discount["discount_field_name"] = "percent_price"
            # fixed % discount or surcharge where 'price start' is product
            # sale price or purchase price. price_compute() will return
            # proper price for set rule with proper uom/currency context
            product_price = product.price_compute(
                "list_price", uom=qty_uom_id, currency=currency_id, company=company_id
            )[product.id]

        elif self.compute_price == "formula":
            discount["discount_field_name"] = "price_discount"
            if self.base != "pricelist":
                # more complex formula including fixed and percentage
                # discount/surcharge and margins. Start price can be
                # product purchase price, sale price or even an outcome
                # from another pricelist.
                product_price = product.price_compute(
                    self.base, uom=qty_uom_id, currency=currency_id, company=company_id
                )[product.id]

            elif self.base == "pricelist":
                # price based on the outcome of other pricelist rule. To
                # return the outcome here we must call _compute_price_rule()
                if not self.base_pricelist_id:
                    raise UserError(_("Select which pricelist this rule is based on."))
                partner = date = uom_id = False

                # prevent exception in some case to speed-up warning pop-up
                self._onclick_check_pricelist_recursive()

                try:
                    product_price = self.base_pricelist_id._compute_price_rule(
                        products_qty_partner=[(product, self.min_quantity, partner)],
                        date=date,
                        uom_id=uom_id,
                    )[product.id][0]

                    # Support for multi-currency: we can't call price_compute()
                    # in this flow so if pricelist or product has different
                    # currency than company, we must deal with it

                    current_currency = self.currency_id or self.pricelist_id.currency_id

                    if current_currency != product.currency_id:
                        current_currency = product.currency_id

                    converted_price = self.base_pricelist_id.currency_id._convert(
                        from_amount=product_price,
                        to_currency=current_currency,
                        company=company_id,
                        date=fields.Date.today(),
                    )

                    product_price = converted_price

                except RecursionError:  # catch exc when it can't be prevented
                    warning = _(
                        "Recursion Error: selected pricelist has some recursive rules "
                        "with other pricelists. It will not possible to retrieve product "
                        "price and discount until recursion is removed. You can check "
                        "'%s' form-view to see info about recursive rules and solve issue. "
                        % self.base_pricelist_id.name
                    )
                    raise UserError(warning)

        discount["product_price"] = product_price
        return discount

    def _get_percentage_change(self):

        """Getter method to compute the percent change between
        the computed selling price and user input.

        :return: dictionary with discount percentage and field on
        which apply the value. See _get_percent_change_rule_base()
        method to get more info."""

        applied_on = self.applied_on

        product = None
        if applied_on == "1_product":
            product = self.product_tmpl_id
        elif applied_on == "0_product_variant":
            product = self.product_id

        self._get_percentage_change_consistency_check(product=product)
        discount = self._get_percent_change_rule_base(product)
        return discount

    def set_percentage_change(self):

        """Inheritable method: make checks before the assignement
        of % discount or change fetch for the price based on rule setup"""

        allowed_base_rule = self._get_allowed_base_rule()

        if self.base not in allowed_base_rule:
            # main reason of this check is to avoid key errors when we
            # call price_compute() function to retrieve product prices.
            # Modules can inherit and add proper key to this check.
            return

        discount_dict = self._get_percentage_change()

        # user input errors management
        self._manage_percent_change_user_input_errors(discount_dict)

        # no user input error on input field, try to set the % field
        price = discount_dict.get("product_price")

        try:
            discount = ((price - self.percent_change_user_input) / price) * 100
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

        discount_field_name = discount_dict.get("discount_field_name")
        if discount_field_name and discount:
            self[discount_field_name] = discount

        # reset input value
        self._reset_percent_change_user_input()

    def _manage_percent_change_user_input_errors(self, discount_dict):
        """manage possible error on user input extendable"""

        if self.percent_change_user_input == 0.00:
            # a possible missclick can lead to a 100% discount
            # setup, we want to avoid that
            raise UserError(
                _(
                    "Be careful, set price discount with user input "
                    "at 0.00 will setup a  100% discount on product "
                    "for the chosen rule. If you want to apply this "
                    "you should do it manually."
                )
            )

        product_price = discount_dict.get("product_price")
        if product_price == self.percent_change_user_input:
            # very likely a user input mistake, you wouldn't
            # configure rule with 0% discount
            raise UserError(
                _(
                    "Please chose a different value from the "
                    "selling computed price. The applied "
                    "discount would be 0.00% in this case."
                )
            )

    def _reset_percent_change_user_input(self):
        """manage user input value at the end of execution"""
        self.percent_change_user_input = 0.00

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
    def _get_allowed_base_rule(self):

        """This method is here to avoid possible key errors on
        price_compute() calls, when 3rd party modules are installed.
        The recomputations of selling price will trigger only when
        the selected key for field 'base' is one of the key returned
        by this list.

        If you want to enable recomputation for extensive modules,
        not only you have to implement custom computation method,
        but you also must extend this list."""

        return ["list_price", "standard_price", "pricelist"]

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

        for rule in self:

            # make possible to remove 'base_pricelist_id' relation
            # when switching from a rule that is based on pricelist
            # to a different 'based on' value. Once relation is set
            # this is not possible to do manually because the field
            # 'base_pricelist_id is protected on write when 'base'
            # is not set on 'pricelist' (because field is invisible).
            # Cleaning the value if pricelist is not based on another
            # pricelists will make possible to correct a recursive
            # rule by chaning it's 'base' parameter, without having
            # to delete and remake the rule.

            if ("base" in vals and vals["base"] != "pricelist") or (
                "base" not in vals and rule.base != "pricelist"
            ):
                vals["base_pricelist_id"] = False

        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):

        # When buttons are clicked on PricelistItem pseudo-record
        # :meth:`create()` will be executed and new record will be
        # flushed in DB. This is a very dangerous behaviour because
        # rule is flushed unintentionally.
        #
        # To bypass this issue:
        #
        # we use a technical field `show_percent_change_buttonthat` that
        # we set True on create(), and show button only if field is True.
        #
        # This still pretty dangerous in case of:
        # * call from external API
        # * attrs in removed from XML header definition for some reason
        #
        # In fact, it would be MUCH better to check field value python side
        # and raise UserError when technical field is false after create,
        # instead of manipulating button visibility in XML side. On the other
        # hand the situation is a little bit more complex to manage by using
        # :exc:`~odoo.exceptions.UserError` since :meth:`set_percentage_change()`
        # will be called after :meth:`create()` and python context is not shared
        # between two methods, this basically makes technical field unreliable
        # at python-side.

        for values in vals_list:
            values.update(dict(show_percent_change_button=True))
        res = super().create(vals_list)
        return res

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
