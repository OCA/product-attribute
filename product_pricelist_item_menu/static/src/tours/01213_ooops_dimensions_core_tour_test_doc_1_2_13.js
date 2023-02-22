odoo.define(
    "ooops_dimensions_core.01213_ooops_dimensions_core_tour_test_doc_1_2_13",
    function (require) {
        "use strict";
        const constants = require("ooops_dimensions_core.constants");
        var test_name = "TEST_DOC_1_2_13";
        var product = "test base fixed price";
        var price = "30.00";
        var attribute = "net color";
        var attribute_value = "Blue (net color)";
        var attribute_2 = "net color 2";
        var attribute_value_2 = "green (net color 2)";
        var height = "1000";
        var width = "1000";

        const test_array = [
            {
                trigger: "a:contains(Add a product)",
                extra_trigger: ".o_sale_order",
                timeout: constants.STANDART_TIMEOUT,
            },
            {
                trigger: "body",
                run: function () {
                    setTimeout(function () {
                        $("body").append(`<p>${constants.KEY}</p>`);
                    }, constants.WAITING_ELEMENT_TIMEOUT);
                },
                timeout: constants.STANDART_TIMEOUT,
            },
            {
                trigger: `p:contains(${constants.KEY})`,
                run: function () {
                    this.$anchor.remove();
                },
                timeout: constants.STANDART_TIMEOUT,
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
                },
            },
            {
                trigger: `[data-attribute_name='${attribute_2}']`,
                run: function () {
                    this.$anchor
                        .find(`select option:contains("${attribute_value_2}")`)
                        .prop("selected", true);
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
            attribute_2: attribute_2,
            attribute_value_2: attribute_value_2,
            height: height,
            width: width,
        };
    }
);
