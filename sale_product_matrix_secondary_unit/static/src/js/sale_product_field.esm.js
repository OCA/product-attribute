/* Copyright 2024 Tecnativa - David Vidal
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html). */

import {
    SaleOrderLineProductField,
    saleOrderLineProductField,
} from "@sale/js/sale_product_field";
import {patch} from "@web/core/utils/patch";

patch(SaleOrderLineProductField.prototype, {
    /**
     * @override
     * Whenever the secondary units differ for the same template, the matrix can't
     * represent them, so we'll force the regular configurator.
     */
    async _openGridConfigurator(edit = false) {
        if (this.props.record.data.force_product_configurator) {
            // `edit` isn't forwarded on purpose: `sale_product_matrix` redirects the
            // product configurator back to the matrix when editing a matrix line.
            return this._openProductConfigurator(false);
        }
        return super._openGridConfigurator(edit);
    },
});

Object.assign(saleOrderLineProductField, {
    fieldDependencies: [
        ...saleOrderLineProductField.fieldDependencies,
        {name: "force_product_configurator", type: "boolean"},
    ],
});
