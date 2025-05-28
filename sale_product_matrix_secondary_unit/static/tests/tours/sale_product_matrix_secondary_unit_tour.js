odoo.define(
    "sale_product_matrix_secondary_unit.sale_matrix_secondary_unit",
    function (require) {
        "use strict";
        var tour = require("web_tour.tour");

        const common_steps = [
            tour.stepUtils.showAppsMenuItem(),
            {
                trigger: ".o_app[data-menu-xmlid='sale.sale_menu_root']",
            },
            {
                trigger: ".o_list_button_add",
                extra_trigger: ".o_sale_order",
            },
            {
                trigger: "div[name=partner_id] input",
                run: "text Deco Addict",
            },
            {
                trigger: ".ui-menu-item > a:contains('Deco Addict')",
                auto: true,
            },
            {
                trigger: "a:contains('Add a product')",
            },
            {
                trigger: "div[name='product_template_id'] input",
                run: "text SecondaryUnitMatrix",
            },
            {
                trigger: "ul.ui-autocomplete a:contains('SecondaryUnitMatrix')",
            },
        ];

        tour.register(
            "sale_matrix_with_secondary_unit",
            {
                url: "/web",
                test: true,
            },
            [
                ...common_steps,
                {
                    trigger: "#secondary_unit",
                    content: "Select the secondary unit",
                    run: function () {
                        const select = $("select.o_matrix_secondary_unit");
                        const option = select.find("option").filter(function () {
                            return $(this).text().includes("Unit 1 12.0 Units");
                        });
                        select.val(option.val()).change();
                    },
                },
                {
                    trigger: ".o_product_variant_matrix",
                    run: function () {
                        // Fill the whole matrix with 1
                        $(".o_matrix_input").val(1);
                    },
                },
                {
                    trigger: "span:contains('Confirm')",
                },
                {
                    trigger: '.o_form_button_save:contains("Save")',
                },
                {
                    // Ensure the form is saved before closing the browser
                    trigger: '.o_form_button_edit:contains("Edit")',
                },
            ]
        );
        tour.register(
            "sale_matrix_without_secondary_unit",
            {
                url: "/web",
                test: true,
            },
            [
                ...common_steps,
                {
                    // This product does not have a secondary unit
                    trigger: ":not(select#secondary_unit)",
                },
                {
                    trigger: ".o_product_variant_matrix",
                    run: function () {
                        // Fill the whole matrix with 1
                        $(".o_matrix_input").val(1);
                    },
                },
                {
                    trigger: "span:contains('Confirm')",
                },
                {
                    trigger: '.o_form_button_save:contains("Save")',
                },
                {
                    // Ensure the form is saved before closing the browser
                    trigger: '.o_form_button_edit:contains("Edit")',
                },
            ]
        );
    }
);
