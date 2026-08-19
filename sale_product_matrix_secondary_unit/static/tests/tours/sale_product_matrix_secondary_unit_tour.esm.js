/* Copyright 2025 Carlos Lopez - Tecnativa
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

import {registry} from "@web/core/registry";
import {stepUtils} from "@web_tour/tour_utils";
import tourUtils from "@sale/js/tours/tour_utils";

const commonSteps = () => [
    ...stepUtils.goToAppSteps("sale.sale_menu_root", "Go to the Sales App"),
    ...tourUtils.createNewSalesOrder(),
    ...tourUtils.selectCustomer("Deco Addict"),
    ...tourUtils.addProduct("SecondaryUnitMatrix"),
];

const fillMatrixWithOnes = {
    content: "Fill the whole matrix with 1",
    trigger: ".modal .o_matrix_input_table",
    run: function () {
        [...document.querySelectorAll(".o_matrix_input")].forEach((el) => {
            el.value = 1;
        });
    },
};

const waitForMatrixLines = {
    content: "Wait for the matrix to be applied on the order lines",
    trigger: "div[name='order_line'] .o_data_row:nth-child(4)",
};

const confirmMatrix = {
    content: "Apply the matrix",
    trigger: ".modal button:contains('Confirm')",
    run: "click",
};

registry.category("web_tour.tours").add("sale_matrix_with_secondary_unit", {
    url: "/odoo",
    steps: () => [
        ...commonSteps(),
        {
            content: "Select the secondary unit",
            trigger: ".modal select.o_matrix_secondary_unit",
            run: function () {
                const select = this.anchor;
                const option = [...select.options].find((el) =>
                    el.text.includes("Unit 1 12.0 Units")
                );
                select.value = option.value;
                select.dispatchEvent(new Event("change", {bubbles: true}));
            },
        },
        fillMatrixWithOnes,
        confirmMatrix,
        waitForMatrixLines,
        ...stepUtils.saveForm(),
    ],
});

registry.category("web_tour.tours").add("sale_matrix_without_secondary_unit", {
    url: "/odoo",
    steps: () => [
        ...commonSteps(),
        {
            content: "This product has no secondary units, so no selector is shown",
            trigger: ".modal .o_matrix_input_table",
            run: function () {
                if (document.querySelector("select.o_matrix_secondary_unit")) {
                    throw new Error("The secondary unit selector shouldn't be shown");
                }
            },
        },
        fillMatrixWithOnes,
        confirmMatrix,
        waitForMatrixLines,
        ...stepUtils.saveForm(),
    ],
});
