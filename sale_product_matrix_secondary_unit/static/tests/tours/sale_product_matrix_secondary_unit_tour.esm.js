/** @odoo-module */
/* Copyright 2025 Carlos Lopez - Tecnativa
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

import {registry} from "@web/core/registry";
import {stepUtils} from "@web_tour/tour_service/tour_utils";

const common_steps = [
    stepUtils.showAppsMenuItem(),
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
registry.category("web_tour.tours").add("sale_matrix_with_secondary_unit", {
    url: "/web",
    test: true,
    steps: () => [
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
            trigger: ".o_matrix_input_table",
            run: function () {
                // Fill the whole matrix with 1
                $(".o_matrix_input").val(1);
            },
        },
        {
            trigger: "button:contains('Confirm')",
        },
        ...stepUtils.saveForm(),
    ],
});
registry.category("web_tour.tours").add("sale_matrix_without_secondary_unit", {
    url: "/web",
    test: true,
    steps: () => [
        ...common_steps,
        {
            // This product does not have a secondary unit
            trigger: ":not(select#secondary_unit)",
        },
        {
            trigger: ".o_matrix_input_table",
            run: function () {
                // Fill the whole matrix with 1
                $(".o_matrix_input").val(1);
            },
        },
        {
            trigger: "button:contains('Confirm')",
        },
        ...stepUtils.saveForm(),
    ],
});
