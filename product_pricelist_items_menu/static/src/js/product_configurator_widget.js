odoo.define("ooops_dimensions_core.sale_product_configurator_widget", function (
    require
) {
    "use strict";
    var SaleProductConfiguratorWidget = require("sale_product_configurator.product_configurator");

    /**
     * Extension of the ProductConfiguratorWidget to support product configuration.
     * It opens when a configurable product_template is set.
     * (multiple variants, or custom attributes)
     *
     * The product customization information includes :
     * - is_configurable_product
     * - product_template_attribute_value_ids
     *
     */

    SaleProductConfiguratorWidget.include({
        _getMainProductChanges: function (mainProduct) {
            var result = {
                product_id: {id: mainProduct.product_id},
                product_template_id: {id: mainProduct.product_template_id},
                product_uom_qty: mainProduct.quantity,
                product_length: mainProduct.product_length,
                product_width: mainProduct.product_width,
                product_height: mainProduct.product_height,
                configurator_data: JSON.stringify({
                    product_length: mainProduct.product_length,
                    product_width: mainProduct.product_width,
                    product_height: mainProduct.product_height,
                    selected_attributes: mainProduct.selected_attributes,
                }),
            };
            var customAttributeValues = mainProduct.product_custom_attribute_values;
            var customValuesCommands = [{operation: "DELETE_ALL"}];
            if (customAttributeValues && customAttributeValues.length !== 0) {
                _.each(customAttributeValues, function (customValue) {
                    // FIXME awa: This could be optimized by adding a "disableDefaultGet" to avoid
                    // having multiple default_get calls that are useless since we already
                    // have all the default values locally.
                    // However, this would mean a lot of changes in basic_model.js to handle
                    // those "default_" values and set them on the various fields (text,o2m,m2m,...).
                    // -> This is not considered as worth it right now.
                    customValuesCommands.push({
                        operation: "CREATE",
                        context: [
                            {
                                default_custom_product_template_attribute_value_id:
                                    customValue.custom_product_template_attribute_value_id,
                                default_custom_value: customValue.custom_value,
                            },
                        ],
                    });
                });
            }

            result.product_custom_attribute_value_ids = {
                operation: "MULTI",
                commands: customValuesCommands,
            };

            var noVariantAttributeValues = mainProduct.no_variant_attribute_values;
            var noVariantCommands = [{operation: "DELETE_ALL"}];
            if (noVariantAttributeValues && noVariantAttributeValues.length !== 0) {
                var resIds = _.map(noVariantAttributeValues, function (noVariantValue) {
                    return {id: parseInt(noVariantValue.value, 10)};
                });

                noVariantCommands.push({
                    operation: "ADD_M2M",
                    ids: resIds,
                });
            }

            result.product_no_variant_attribute_value_ids = {
                operation: "MULTI",
                commands: noVariantCommands,
            };

            return result;
        },
    });

    return SaleProductConfiguratorWidget;
});
