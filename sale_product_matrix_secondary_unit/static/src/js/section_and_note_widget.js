odoo.define(
    "sale_product_matrix_secondary_unit.section_and_note_widget",
    function (require) {
        "use strict";
        const Dialog = require("web.Dialog");
        const core = require("web.core");
        const _t = core._t;
        const qweb = core.qweb;
        const {Markup} = require("web.utils");
        const fieldRegistry = require("web.field_registry");
        const {format} = require("web.field_utils");
        require("account.section_and_note_backend");
        const SectionAndNoteFieldOne2Many = fieldRegistry.get(
            "section_and_note_one2many"
        );

        SectionAndNoteFieldOne2Many.include({
            /**
             * @override
             *
             */
            _applyGrid: function (
                changes,
                productTemplateId,
                secondary_unit_changed,
                secondary_unit,
                changed
            ) {
                if (!secondary_unit_changed && !secondary_unit) {
                    return this._super.apply(this, arguments);
                }
                var grid = {
                    changes: changes,
                    product_template_id: productTemplateId,
                    changed: changed,
                };
                if (secondary_unit_changed || (secondary_unit && changes.length)) {
                    grid.secondary_unit = secondary_unit || false;
                }
                this.trigger_up("field_changed", {
                    dataPointID: this.dataPointID,
                    changes: {
                        grid: JSON.stringify(grid),
                        // To say that the changes to grid have to be applied to the SO.
                        grid_update: true,
                    },
                    viewType: "form",
                });
            },

            /**
             * @override
             *
             */
            _openMatrixConfigurator: function (
                jsonInfo,
                productTemplateId,
                editedCellAttributes
            ) {
                var self = this;
                var infos = JSON.parse(jsonInfo);
                if (!infos.secondary_units || !infos.secondary_units.length) {
                    return this._super.apply(this, arguments);
                }
                self.secondary_unit_id = infos.secondary_unit_id;
                var MatrixDialog = new Dialog(this, {
                    title: _t("Choose Product Variants"),
                    size: "extra-large",
                    $content: $(
                        qweb.render("sale_product_matrix_secondary_unit.matrix", {
                            header: infos.header,
                            rows: infos.matrix,
                            secondary_unit_id: infos.secondary_unit_id,
                            secondary_units: infos.secondary_units,
                            uom_name: infos.uom_name,
                            format({price, currency_id}) {
                                if (!price) {
                                    return "";
                                }
                                const sign = price < 0 ? "-" : "+";
                                const formatted = format.monetary(
                                    Math.abs(price),
                                    null,
                                    {currency_id}
                                );
                                return Markup`${sign}&nbsp;${formatted}`;
                            },
                        })
                    ),
                    buttons: [
                        {
                            text: _t("Confirm"),
                            classes: "btn-primary",
                            close: true,
                            click: function () {
                                var $inputs = this.$(".o_matrix_input");
                                var matrixChanges = [];
                                _.each($inputs, function (matrixInput) {
                                    if (
                                        (matrixInput.value &&
                                            matrixInput.value !==
                                                matrixInput.attributes.value
                                                    .nodeValue) ||
                                        matrixInput.attributes.value.nodeValue > 0
                                    ) {
                                        matrixChanges.push({
                                            qty: parseFloat(matrixInput.value),
                                            ptav_ids:
                                                matrixInput.attributes.ptav_ids.nodeValue
                                                    .split(",")
                                                    .map(function (id) {
                                                        return parseInt(id, 10);
                                                    }),
                                            changed:
                                                matrixInput.value &&
                                                matrixInput.value !==
                                                    matrixInput.attributes.value
                                                        .nodeValue,
                                        });
                                    }
                                });
                                var changed = matrixChanges.reduce(
                                    (is_changed, variant) =>
                                        is_changed || variant.changed,
                                    false
                                );
                                var $secondary_unit = this.$(
                                    ".o_matrix_secondary_unit"
                                );
                                var secondary_unit_changed = false;
                                var secondary_unit = parseInt(
                                    $secondary_unit.val() || 0,
                                    10
                                );
                                if (secondary_unit !== self.secondary_unit_id) {
                                    secondary_unit_changed = true;
                                }
                                if (
                                    matrixChanges.length > 0 ||
                                    secondary_unit_changed
                                ) {
                                    self._applyGrid(
                                        matrixChanges,
                                        productTemplateId,
                                        secondary_unit_changed,
                                        secondary_unit,
                                        changed
                                    );
                                }
                            },
                        },
                        {text: _t("Close"), close: true},
                    ],
                }).open();

                MatrixDialog.opened(function () {
                    MatrixDialog.$content
                        .closest(".o_dialog_container")
                        .removeClass("d-none");
                    if (editedCellAttributes.length > 0) {
                        var str = editedCellAttributes.toString();
                        MatrixDialog.$content
                            .find(".o_matrix_input")
                            .filter(
                                (k, v) => v.attributes.ptav_ids.nodeValue === str
                            )[0]
                            .focus();
                    } else {
                        MatrixDialog.$content.find(".o_matrix_input:first()").focus();
                    }
                });
            },
        });
        return SectionAndNoteFieldOne2Many;
    }
);
