odoo.define(
    "ooops_dimensions_core.01201_ooops_dimensions_core_tour_test_doc_1_2_1",
    function (require) {
        "use strict";
        const STANDART_TIMEOUT = require("ooops_dimensions_core.constants")
            .STANDART_TIMEOUT;
        var test_name = "TEST_DOC_1_2_1";
        var product = "test base area never no BM";
        var price = "10.00";
        var attribute = "net color";
        var attribute_value = "Blue (net color)";
        var height = "1000";
        var width = "1000";
        const test_array = [
            {
                trigger: "a:contains(Add a product)",
                extra_trigger: ".o_sale_order",
                timeout: STANDART_TIMEOUT,
            },
            {
                trigger: " .o_field_many2one[name='product_template_id']",
                extra_trigger: ".o_sale_order",
                run: function (actions) {
                    actions.text(product, this.$anchor.find("input"));
                },
                timeout: STANDART_TIMEOUT,
            },
            {
                trigger: " .ui-state-active",
                timeout: STANDART_TIMEOUT,
            },
            {
                trigger: "#custom_product_height",
                timeout: STANDART_TIMEOUT,
                run: function (actions) {
                    actions.text(height);
                },
            },
            {
                trigger: "#custom_product_width",
                timeout: STANDART_TIMEOUT,
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
                },
            },
            {
                trigger: `.oe_currency_value:contains('${price}')`,
                timeout: STANDART_TIMEOUT,
                run: function () {
                    const current_price = this.$anchor.text();
                    console.log(current_price);
                },
            },
            {
                trigger: ".o_sale_product_configurator_add",
                timeout: STANDART_TIMEOUT,
                run: function (actions) {
                    actions.click();
                },
            },
            {
                trigger: `td:contains('${price}')`,
                timeout: STANDART_TIMEOUT,
            },
            {
                trigger: ".o_list_record_remove",
                timeout: STANDART_TIMEOUT,
            },
        ];
        return {
            test_array: test_array,
            test_name: test_name,
            product: product,
            price: price,
            attribute: attribute,
            attribute_value: attribute_value,
            height: height,
            width: width,
        };
    }
);
