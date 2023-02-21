odoo.define("ooops_dimensions_core.ProductConfiguratorFormController", function (
    require
) {
    "use strict";
    var core = require("web.core");
    var _t = core._t;

    var OptionalProductsModal = require("sale_product_configurator.OptionalProductsModal");
    const ProductConfiguratorFormController = require("sale_product_configurator.ProductConfiguratorFormController");

    ProductConfiguratorFormController.include({
        get_digit_from_string: function (string_param) {
            var digit_param = 0;
            if (string_param.match(/^-?\d+$/)) {
                digit_param = parseInt(string_param, 10);
            } else if (string_param.match(/^\d+\.\d+$/)) {
                digit_param = parseFloat(string_param);
            }
            return digit_param;
        },

        _get_selected_attributes: function (attrs_list) {
            var self = this;
            var selected_attributes = {};
            for (const list_element_list of Object.entries(attrs_list)) {
                var list_element = list_element_list[1];
                if (list_element.children) {
                    for (const child_list of Object.entries(list_element.children)) {
                        var child = child_list[1];
                        var attribute_id = child.getAttribute("data-attribute_id");
                        var ptal = child.getAttribute("name");
                        if (child.nodeName === "SELECT") {
                            var selected_attr = child.options[child.selectedIndex];
                            if (selected_attr) {
                                selected_attributes[
                                    Number(selected_attr.getAttribute("data-value_id"))
                                ] = {
                                    ptav_id: Number(
                                        selected_attr.getAttribute("data-value_id")
                                    ),
                                    attribute_name: selected_attr.getAttribute(
                                        "data-attribute_name"
                                    ),
                                    ptav_name: selected_attr.getAttribute(
                                        "data-value_name"
                                    ),
                                    attribute_id: Number(attribute_id),
                                    ptal: Number(ptal.split("-")[1]),
                                };
                            }
                        }
                        if (child.nodeName === "INPUT") {
                            var custom_ptav_id = child.getAttribute(
                                "data-custom_product_template_attribute_value_id"
                            );
                            var ptav_value = self.get_digit_from_string(child.value);
                            let string_value = "";
                            if (ptav_value === 0) {
                                string_value = child.value;
                            }

                            selected_attributes[custom_ptav_id] = {
                                ptav_id: Number(custom_ptav_id),
                                is_custom_ptav: true,
                                attribute_name: list_element.getAttribute(
                                    "data-attribute_name"
                                ),
                                ptav_name: child.getAttribute(
                                    "data-attribute_value_name"
                                ),
                                value: ptav_value,
                                string_value: string_value,
                            };
                        }
                    }
                }
            }
            return selected_attributes;
        },

        /**
         * When the user adds a product that has optional products, we need to display
         * a window to allow the user to choose these extra options.
         *
         * This will also create the product if it's in "dynamic" mode
         * (see product_attribute.create_variant)
         *
         * If "self.renderer.state.context.configuratorMode" is 'edit', this will only send
         * the main product with its changes.
         *
         * As opposed to the 'add' mode that will add the main product AND all the configured optional products.
         *
         * A third mode, 'options', is available for products that don't have a configuration but have
         * optional products to select. This will bypass the configuration step and open the
         * options modal directly.
         *
         * @private
         */
        _handleAdd: function () {
            var self = this;
            var $modal = this.$el;
            var attrs_list = $modal.find(".js_add_cart_variants").find("li");
            var selected_attributes = self._get_selected_attributes(attrs_list);
            selected_attributes = {
                selected_attributes: selected_attributes,
            };
            const product_dimensions = {
                product_length:
                    parseFloat(
                        $modal.find("#custom_product_length").val() ||
                            $modal.find("#product_length").val()
                    ) || 0,
                product_width:
                    parseFloat(
                        $modal.find("#custom_product_width").val() ||
                            $modal.find("#product_width").val()
                    ) || 0,
                product_height:
                    parseFloat(
                        $modal.find("#custom_product_height").val() ||
                            $modal.find("#product_height").val()
                    ) || 0,
            };
            var productSelector = [
                'input[type="hidden"][name="product_id"]',
                'input[type="radio"][name="product_id"]:checked',
            ];
            var productId = parseInt(
                $modal.find(productSelector.join(", ")).first().val(),
                10
            );
            var productTemplateId = $modal.find(".product_template_id").val();
            this.renderer
                .selectOrCreateProduct($modal, productId, productTemplateId, false)
                .then(function (product_Id) {
                    $modal.find(productSelector.join(", ")).val(product_Id);

                    var variantValues = self.renderer.getSelectedVariantValues(
                        $modal.find(".js_product")
                    );

                    var productCustomVariantValues = self.renderer.getCustomVariantValues(
                        $modal.find(".js_product")
                    );

                    var noVariantAttributeValues = self.renderer.getNoVariantAttributeValues(
                        $modal.find(".js_product")
                    );

                    self.rootProduct = {
                        product_id: product_Id,
                        product_template_id: parseInt(productTemplateId, 10),
                        quantity: parseFloat(
                            $modal.find('input[name="add_qty"]').val() || 1
                        ),
                        variant_values: variantValues,
                        product_custom_attribute_values: productCustomVariantValues,
                        no_variant_attribute_values: noVariantAttributeValues,
                    };
                    self.rootProduct = _.extend(
                        selected_attributes,
                        product_dimensions,
                        self.rootProduct
                    );
                    if (self.renderer.state.context.configuratorMode === "edit") {
                        // Edit mode only takes care of main product
                        self._onAddRootProductOnly();
                        return;
                    }

                    self.optionalProductsModal = new OptionalProductsModal($("body"), {
                        rootProduct: self.rootProduct,
                        pricelistId: self.renderer.pricelistId,
                        okButtonText: _t("Confirm"),
                        cancelButtonText: _t("Back"),
                        title: _t("Configure"),
                        context: self.initialState.context,
                        previousModalHeight: self.$el
                            .closest(".modal-content")
                            .height(),
                    }).open();
                    self.optionalProductsModal.on(
                        "options_empty",
                        null,
                        // No optional products found for this product, only add the root product
                        self._onAddRootProductOnly.bind(self)
                    );

                    self.optionalProductsModal.on(
                        "update_quantity",
                        null,
                        self._onOptionsUpdateQuantity.bind(self)
                    );

                    self.optionalProductsModal.on(
                        "confirm",
                        null,
                        self._onModalConfirm.bind(self)
                    );

                    self.optionalProductsModal.on(
                        "closed",
                        null,
                        self._onModalClose.bind(self)
                    );
                });
        },
    });

    return ProductConfiguratorFormController;
});
