odoo.define("product_pricelist_items_menu.mixin", function (require) {
    "use strict";

    const ajax = require("web.ajax");
    return {
        _getCombinationInfo: function (ev) {
            var self = this;
            var $component = false;
            if ($(ev.currentTarget).closest("form").length > 0) {
                $component = $(ev.currentTarget).closest("form");
            } else if (
                $(ev.currentTarget).closest(".oe_optional_products_modal").length > 0
            ) {
                $component = $(ev.currentTarget).closest(".oe_optional_products_modal");
            } else if (
                $(ev.currentTarget).closest(".o_product_configurator").length > 0
            ) {
                $component = $(ev.currentTarget).closest(".o_product_configurator");
            } else {
                $component = $(ev.currentTarget);
            }
            var qty = $component.find('input[name="add_qty"]').val();

            var $parent = $(ev.target).closest(".js_product");

            var combination = this.getSelectedVariantValues($parent);
            var parentCombination = $parent
                .find("ul[data-attribute_exclusions]")
                .data("attribute_exclusions").parent_combination;

            var productTemplateId = parseInt(
                $parent.find(".product_template_id").val(),
                10
            );

            // Cetmix
            const context = {
                product_length:
                    parseFloat(
                        $parent.find("#custom_product_length").val() ||
                            $parent.find("#product_length").val()
                    ) || 0,
                product_width:
                    parseFloat(
                        $parent.find("#custom_product_width").val() ||
                            $parent.find("#product_width").val()
                    ) || 0,
                product_height:
                    parseFloat(
                        $parent.find("#custom_product_height").val() ||
                            $parent.find("#product_height").val()
                    ) || 0,
                pricelist: this.pricelistId || false,
            };
            self._checkExclusions($parent, combination);
            return ajax
                .jsonRpc(this._getUri("/sale/get_combination_info"), "call", {
                    product_template_id: productTemplateId,
                    product_id: this._getProductId($parent),
                    combination: combination,
                    add_qty: parseInt(qty, 10),
                    pricelist_id: this.pricelistId || false,
                    parent_combination: parentCombination,
                    context: context,
                })
                .then(function (combinationData) {
                    self._onChangeCombination(ev, $parent, combinationData);
                });
        },
        /**
         * Will add the "custom value" input for this attribute value if
         * the attribute value is configured as "custom" (see product_attribute_value.is_custom)
         *
         * @private
         * @param {MouseEvent} $target
         */
        handleCustomValues: function ($target) {
            var $variantContainer = false;
            var $customInput = false;
            if ($target.is("input[type=radio]") && $target.is(":checked")) {
                $variantContainer = $target.closest("ul").closest("li");
                $customInput = $target;
            } else if ($target.is("select")) {
                $variantContainer = $target.closest("li");
                $customInput = $target.find('option[value="' + $target.val() + '"]');
            }

            if ($variantContainer) {
                if ($customInput && $customInput.data("is_custom") === "True") {
                    var attributeValueId = $customInput.data("value_id");
                    var attributeValueName = $customInput.data("value_name");

                    if (
                        $variantContainer.find(".variant_custom_value").length === 0 ||
                        $variantContainer
                            .find(".variant_custom_value")
                            .data("custom_product_template_attribute_value_id") !==
                            parseInt(attributeValueId, 10)
                    ) {
                        $variantContainer.find(".variant_custom_value").remove();
                        // Cetmix
                        var $input = false;
                        var attributeDimension = $customInput.data("dimension");
                        if (
                            attributeDimension &&
                            typeof attributeDimension !== typeof undefined
                        ) {
                            $input = $("<input>", {
                                type: "text",
                                "data-custom_product_template_attribute_value_id": attributeValueId,
                                "data-attribute_value_name": attributeValueName,
                                class: "variant_custom_value form-control is-dimension",
                                id: "custom_" + attributeDimension,
                            });
                        } else {
                            $input = $("<input>", {
                                type: "text",
                                "data-custom_product_template_attribute_value_id": attributeValueId,
                                "data-attribute_value_name": attributeValueName,
                                class: "variant_custom_value form-control",
                            });
                        }

                        var isRadioInput =
                            $target.is("input[type=radio]") &&
                            $target.closest("label.css_attribute_color").length === 0;

                        if (
                            isRadioInput &&
                            $customInput.data("is_single_and_custom") !== "True"
                        ) {
                            $input.addClass("custom_value_radio");
                            $target.closest("div").after($input);
                        } else {
                            $input.attr("placeholder", attributeValueName);
                            $input.addClass("custom_value_own_line");
                            $variantContainer.append($input);
                        }
                    }
                } else {
                    $variantContainer.find(".variant_custom_value").remove();
                }
            }
        },
    };
});
