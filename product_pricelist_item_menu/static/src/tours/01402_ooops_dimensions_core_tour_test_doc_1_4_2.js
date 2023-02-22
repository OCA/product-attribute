odoo.define(
    "ooops_dimensions_core.01402_ooops_dimensions_core_tour_test_doc_1_4_2",
    function (require) {
        "use strict";
        const constants = require("ooops_dimensions_core.constants");
        var test_name = "TEST_DOC_1_4_2";
        var product = "test base area exclusion";
        var price = "0.00";
        var attribute = "net color";
        var attribute_value = "Blue (net color)";
        var attribute_value_2 = "Yellow (net color)";
        var height = "2000";
        var width = "2000";
        const test_array = [
            {
                trigger: "a:contains(Add a product)",
                extra_trigger: ".o_sale_order",
                timeout: constants.STANDART_TIMEOUT,
            },
            {
                setWaitingTimeout: constants.WAITING_ELEMENT_TIMEOUT,
            },
            {
                trigger: " .o_field_many2one[name='product_template_id']",
                extra_trigger: ".o_sale_order",
                run: function (actions) {
                    actions.text(product, this.$anchor.find("input"));
                },
                timeout: constants.STANDART_TIMEOUT,
            },
            {
                trigger: " .ui-state-active",
                timeout: constants.STANDART_TIMEOUT,
            },
            {
                trigger: "#custom_product_height",
                timeout: constants.STANDART_TIMEOUT,
                run: function (actions) {
                    actions.text(height);
                },
            },
            {
                trigger: "#custom_product_width",
                timeout: constants.STANDART_TIMEOUT,
                run: function (actions) {
                    actions.text(width);
                },
            },
            {
                trigger: `[data-attribute_name='${attribute}']`,
                run: function () {
                    this.$anchor
                        .find(`select option:contains("${attribute_value}")`)
                        .prop("selected", true);
                    this.$anchor.change();
                },
            },
            {
                trigger: `.css_not_available_msg`,
            },
            {
                setWaitingTimeout: constants.WAITING_ELEMENT_TIMEOUT,
                selector: `[data-attribute_name='${attribute}']`,
            },
            {
                trigger: `[data-attribute_name='${attribute}']`,
                run: function () {
                    this.$anchor
                        .find(`select option:contains("${attribute_value_2}")`)
                        .prop("selected", true);
                    this.$anchor.change();
                },
            },
            {
                trigger: `.oe_currency_value:contains('${price}')`,
                timeout: constants.STANDART_TIMEOUT,
                run: function () {
                    const current_price = this.$anchor.text();
                    console.log(current_price);
                },
            },
            {
                trigger: ".o_sale_product_configurator_add",
                timeout: constants.STANDART_TIMEOUT,
                run: function (actions) {
                    actions.click();
                },
            },
            {
                trigger: `td:contains('${price}')`,
                timeout: constants.STANDART_TIMEOUT,
            },
            {
                trigger: ".o_list_record_remove",
                timeout: constants.STANDART_TIMEOUT,
            },
        ];
        return {
            test_array: test_array,
            test_name: test_name,
            product: product,
            price: price,
            attribute: attribute,
            attribute_value: attribute_value,
            attribute_value_2: attribute_value_2,
            height: height,
            width: width,
        };
    }
);
