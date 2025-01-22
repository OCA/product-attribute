odoo.define(
    "sale_product_matrix_secondary_unit.product_configurator",
    function (require) {
        "use strict";
        const ProductConfiguratorWidget = require("sale_product_configurator.product_configurator");

        ProductConfiguratorWidget.include({
            /*
             * @override
             * Whenever the secondary units differ for the same template, we'll force the
             * regular configurator.
             */
            _openConfigurator: function (result) {
                if (this.recordData.force_product_configurator) {
                    result.mode = "configurator";
                }
                return this._super.apply(this, arguments);
            },
            /*
             * @override
             * Whenever the secondary units differ for the same template, we'll force the
             * regular configurator.
             */
            _onEditProductConfiguration: function () {
                if (!this.recordData.force_product_configurator) {
                    this._super.apply(this, arguments);
                    return;
                }
                this._openProductConfigurator(
                    {
                        configuratorMode: "edit",
                        default_product_template_id:
                            this.recordData.product_template_id.data.id,
                        default_pricelist_id: this._getPricelistId(),
                        default_product_template_attribute_value_ids:
                            this._convertFromMany2Many(
                                this.recordData.product_template_attribute_value_ids
                            ),
                        default_product_no_variant_attribute_value_ids:
                            this._convertFromMany2Many(
                                this.recordData.product_no_variant_attribute_value_ids
                            ),
                        default_product_custom_attribute_value_ids:
                            this._convertFromOne2Many(
                                this.recordData.product_custom_attribute_value_ids
                            ),
                        default_quantity: this.recordData.product_uom_qty,
                    },
                    this.dataPointID
                );
            },
        });
    }
);
