/** @odoo-module **/

import {ProductMatrixDialog} from "@product_matrix/js/product_matrix_dialog";
import {patch} from "@web/core/utils/patch";

patch(ProductMatrixDialog.prototype, {
    _onConfirm() {
        let secondary_unit = document.getElementsByClassName("o_matrix_secondary_unit");
        if (!secondary_unit || !secondary_unit.length) {
            return super._onConfirm(...arguments);
        }
        let secondary_unit_changed = false;
        secondary_unit = parseInt(secondary_unit[0].value || 0, 10);
        // TODO: enviar datos al server cuando solo cambie la UdM secundaria y no las cantidades
        if (secondary_unit !== self.secondary_unit_id) {
            secondary_unit_changed = true;
        }
        // Override the original _onConfirm method to include secondary unit changes
        const inputs = document.getElementsByClassName("o_matrix_input");
        const matrixChanges = [];
        for (const matrixInput of inputs) {
            if (
                (matrixInput.value &&
                    matrixInput.value !== matrixInput.attributes.value.nodeValue) ||
                matrixInput.attributes.value.nodeValue > 0
            ) {
                matrixChanges.push({
                    qty: parseFloat(matrixInput.value),
                    ptav_ids: matrixInput.attributes.ptav_ids.nodeValue
                        .split(",")
                        .map((id) => parseInt(id, 10)),
                });
            }
        }
        if (matrixChanges.length > 0 || secondary_unit_changed) {
            // NB: server also removes current line opening the matrix
            this.props.record.update({
                grid: JSON.stringify({
                    changes: matrixChanges,
                    product_template_id: this.props.product_template_id,
                    secondary_unit: secondary_unit || false,
                }),
                grid_update: true, // To say that the changes to grid have to be applied to the SO.
            });
        }
        this.props.close();
    },
});
ProductMatrixDialog.props = {
    ...ProductMatrixDialog.props,
    secondary_unit_id: {optional: true},
    secondary_units: {type: Array, optional: true},
    uom_name: {type: String, optional: true},
};
