/** @odoo-module **/

import {ProductMatrixDialog} from "@product_matrix/js/product_matrix_dialog";
import {SaleOrderLineProductField} from "@sale/js/sale_product_field";
import {patch} from "@web/core/utils/patch";

patch(SaleOrderLineProductField.prototype, {
    /*
     * @override
     * Whenever the secondary units differ for the same template, we'll force the
     * regular configurator.
     */
    async _openGridConfigurator(edit = false) {
        if (this.props.record.data.force_product_configurator) {
            this._openProductConfigurator();
            return;
        }
        return super._openGridConfigurator(edit);
    },
    /**
     * Triggers Matrix Dialog opening
     *
     * @param {String} jsonInfo matrix dialog content
     * @param {integer} productTemplateId product.template id
     * @param {Array} editedCellAttributes list of product.template.attribute.value ids
     *  used to focus on the matrix cell representing the edited line.
     *
     * @private
     * @override
     */
    _openMatrixConfigurator(jsonInfo, productTemplateId, editedCellAttributes) {
        const infos = JSON.parse(jsonInfo);
        if (!infos.secondary_units || !infos.secondary_units.length) {
            return super._openMatrixConfigurator(...arguments);
        }
        this.secondary_unit_id = infos.secondary_unit_id;
        this.dialog.add(ProductMatrixDialog, {
            header: infos.header,
            rows: infos.matrix,
            editedCellAttributes: editedCellAttributes.toString(),
            product_template_id: productTemplateId,
            record: this.props.record.model.root,
            // Provide additional properties to the dialog
            secondary_unit_id: infos.secondary_unit_id,
            secondary_units: infos.secondary_units,
            uom_name: infos.uom_name,
        });
    },
});
