/* Copyright 2024 Tecnativa - David Vidal
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html). */

import {ProductMatrixDialog} from "@product_matrix/js/product_matrix_dialog";
import {patch} from "@web/core/utils/patch";

patch(ProductMatrixDialog.prototype, {
    setup() {
        super.setup(...arguments);
        this.secondaryUnits = [];
        this.secondaryUnitId = false;
        this.uomName = "";
        const gridInfo = this.props.record.data.grid;
        if (gridInfo) {
            const infos = JSON.parse(gridInfo);
            this.secondaryUnits = infos.secondary_units || [];
            this.secondaryUnitId = infos.secondary_unit_id || false;
            this.uomName = infos.uom_name || "";
        }
    },

    /**
     * @override
     * Send the selected secondary unit along with the matrix changes.
     */
    _onConfirm() {
        if (!this.secondaryUnits.length) {
            return super._onConfirm(...arguments);
        }
        const select = document.querySelector("select.o_matrix_secondary_unit");
        const secondaryUnit = (select && parseInt(select.value, 10)) || false;
        const secondaryUnitChanged = secondaryUnit !== this.secondaryUnitId;
        const matrixChanges = [];
        for (const matrixInput of document.getElementsByClassName("o_matrix_input")) {
            const initialValue = matrixInput.attributes.value.nodeValue;
            const changed = matrixInput.value && matrixInput.value !== initialValue;
            // When the secondary unit changes, every filled cell has to be sent back
            // so that the quantities get recomputed with the new factor.
            if (
                changed ||
                (secondaryUnitChanged && parseFloat(initialValue || 0) > 0)
            ) {
                matrixChanges.push({
                    qty: parseFloat(matrixInput.value),
                    ptav_ids: matrixInput.attributes.ptav_ids.nodeValue
                        .split(",")
                        .map((id) => parseInt(id, 10)),
                });
            }
        }
        if (matrixChanges.length > 0 || secondaryUnitChanged) {
            // NB: server also removes current line opening the matrix
            this.props.record.update({
                grid: JSON.stringify({
                    changes: matrixChanges,
                    product_template_id: this.props.product_template_id,
                    secondary_unit: secondaryUnit,
                }),
                // To say that the changes to grid have to be applied to the SO.
                grid_update: true,
            });
        }
        this.props.close();
    },
});
